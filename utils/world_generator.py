#!/usr/bin/env python3

from lxml.etree import Element, SubElement, ElementTree, XMLParser, parse
from random import randint, uniform
from math import pi

DIFF_PLANTS = 3
HEIGHT_MIN = -0.16
HEIGHT_MAX = -0.15
DISTANCE_TOLERANCE = 0.01
PLANT_RADIUS = 0.1

class FieldParameters:
    def __init__(self, width, depth, lineNum, headland, ridge, furrow, cropHeight):
        self.width = width
        self.depth = depth
        self.lineNum = lineNum
        self.headland = headland
        self.ridge = ridge
        self.furrow = furrow
        self.cropHeight = cropHeight

    def getRidgeFurrow(self):
        return self.ridge + self.furrow
    
    def getSideland(self):
        crops = self.lineNum * self.ridge + (self.lineNum - 1) * self.furrow
        return (self.width - crops) / 2.0

class Color:
    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def brighter(self):
        r = self.r
        g = self.g 
        b = self.b
        a = self.a

        if r == 0 and g == 0 and b == 0:
            return Color(3, 3, 3, a)
        if r > 0 and r < 3:
            r = i
        if g > 0 and g < 3:
            g = i
        if b > 0 and b < 3:
            b = i
        return Color(min(int(r/0.7), 255), min(int(g/0.7), 255), min(int(b/0.7), 255), a)

    def getText(self):
        r = self.r
        g = self.g 
        b = self.b
        a = self.a

        return "%.2f %.2f %.2f %.2f" % (r/255.0, g/255.0, b/255.0, a/255.0)

class Material:
    def __init__(self, ambient, diffuse=None):
        self.ambient = ambient
        if diffuse is None:
            self.diffuse = ambient.brighter()
        else:
            self.diffuse = diffuse

    def createElement(self):
        material = Element('material')
        
        ambient = SubElement(material, 'ambient')
        ambient.text = self.ambient.getText()

        diffuse = SubElement(material, 'diffuse')
        diffuse.text = self.diffuse.getText()

        specular = SubElement(material, 'specular')
        specular.text = "0.01 0.01 0.01 1"

        emissive = SubElement(material, 'emissive')
        emissive.text = "0 0 0 1"

        return material

GROUND = Material(Color(102, 74, 53), Color(102, 74, 53))
GREEN = Material(Color(33, 153, 84))
BLACK = Material(Color(25, 25, 25))
BLUE = Material(Color(10, 51, 102))
RED = Material(Color(158, 21, 21))

class Pose:
    def __init__(self, x, y, z, roll, pitch, yaw):
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def createElement(self):
        pose = Element('pose', frame='')
        pose.text = "%.2f %.2f %.2f %.2f %.2f %.2f" % (self.x, self.y, self.z, self.roll, self.pitch, self.yaw)
        return pose

def addModel(world, model, pose):
    world.append(model)
    modelState = SubElement(world.find('state'), 'model', name=model.get('name'))
    modelState.append(pose.createElement())

def createBoxGeometry(x, y, z):
    geometry = Element('geometry')
    box = SubElement(geometry, 'box')
    size = SubElement(box, 'size')
    size.text = "%.2f %.2f %.2f" % (x, y, z)
    return geometry

def createBox(x, y, z, material, name):
    model = Element('model', name=name)
    link = SubElement(model, 'link', name=name)
    link.append(Pose(0, 0, 0, 0, 0, 0).createElement())

    visual = SubElement(link, 'visual', name='visual')
    visual.append(Pose(0, 0, 0, 0, 0, 0).createElement())
    visual.append(createBoxGeometry(x, y, z))
    SubElement(visual, 'cast_shadows').text = '1'
    visual.append(material.createElement())

    collision = SubElement(link, 'collision', name='collision')
    SubElement(collision, 'max_contacts').text = '10'
    collision.append(Pose(0, 0, 0, 0, 0, 0).createElement())
    collision.append(createBoxGeometry(x, y, z))
    surface = SubElement(collision, 'surface')
    contact = SubElement(surface, 'contact')
    SubElement(contact, 'collide_without_contact').text = 'true'

    SubElement(model, 'static').text = '1'
    return model

def getPlant():
    return randint(1, DIFF_PLANTS)
    
def getHeight():
    return uniform(HEIGHT_MIN, HEIGHT_MAX)
    
def getDistance():
    return uniform(-DISTANCE_TOLERANCE, DISTANCE_TOLERANCE)
    
def getYaw():
    return uniform(0.0, pi * 2.0);

def createVisualPlants(y, material):
    visualElements = []
    yFrom = -y / 2.0;
    yTo = y / 2.0;
    dist = yFrom + PLANT_RADIUS;
    i = 1;
    while dist < yTo + PLANT_RADIUS:
        visual = Element('visual', name='visual' + str(i))
        visual.append(Pose(0, dist + getDistance(), getHeight(), 0, 0, getYaw()).createElement())
        geometry = SubElement(visual, 'geometry')
        mesh = SubElement(geometry, 'mesh')
        SubElement(mesh, 'uri').text = 'file://very_low/plant_' + str(getPlant()) + '.stl'
        SubElement(visual, 'cast_shadows').text = '1'
        visual.append(material.createElement())
        visualElements.append(visual)
        dist += 2 * PLANT_RADIUS
        i += 1
    return visualElements

def createPlants(x, y, z, material, name, meshes):
    model = Element('model', name=name)
    link = SubElement(model, 'link', name=name)
    link.append(Pose(0, 0, 0, 0, 0, 0).createElement())

    if meshes:
        for plant in createVisualPlants(y, material):
            link.append(plant)
    else:
        visual = SubElement(link, 'visual', name='visual')
        visual.append(Pose(0, 0, 0, 0, 0, 0).createElement())
        visual.append(createBoxGeometry(x, y, z))
        SubElement(visual, 'cast_shadows').text = '1'
        visual.append(material.createElement())

    collision = SubElement(link, 'collision', name='collision')
    SubElement(collision, 'max_contacts').text = '10'
    collision.append(Pose(0, 0, 0, 0, 0, 0).createElement())
    collision.append(createBoxGeometry(x, y, z))
    surface = SubElement(collision, 'surface')
    contact = SubElement(surface, 'contact')
    SubElement(contact, 'collide_without_contact').text = 'true'

    SubElement(model, 'static').text = '1'
    return model

def createFieldWorld(name, params, meshes=True, textures=True):
    parser = XMLParser(ns_clean=True, remove_blank_text=True)

    tree = parse('empty.world', parser)
    sdf = tree.getroot()

    # le asigna el nombre al world
    world = sdf.find('world')
    world.set('name', name)
    world.find('state').set('world_name', name)
        
    # agrega el suelo
    ground = parse('ground.model', parser).getroot()
    groundVisual = ground.find('link').find('visual')
    if textures:
        material = Element('material')
        script = SubElement(material, 'script')
        SubElement(script, 'uri').text = 'model://field_ground_plane/materials/scripts'
        SubElement(script, 'uri').text = 'model://field_ground_plane/materials/textures'
        SubElement(script, 'name').text = 'FieldGroundPlane/Image'
    else:
        material = GROUND.createElement()
    groundVisual.append(material)
    groundVisualSize = Element('size')
    groundVisualSize.text = "%d %d" % (params.width, params.depth)
    groundVisual.find('geometry').find('plane').append(groundVisualSize)
    groundCollision = ground.find('link').find('collision')
    groundCollisionSize = Element('size')
    groundCollisionSize.text = "%d %d" % (params.width, params.depth)
    groundCollision.find('geometry').find('plane').append(groundCollisionSize)
    addModel(world, ground, Pose(0, 0, 0, 0, 0, 0))

    # agrega las líneas de cultivos
    start = - params.width / 2.0 + params.getSideland()
    if -start * 2 > params.width:
        raise Exception("Demasiadas filas de cultivos")
    count = 1
    while count <= params.lineNum:
        # modelo para línea de cultivo
        crop = createPlants(
            params.ridge, 
            params.depth - 2 * params.headland,
            params.cropHeight,
            GREEN, "crop_line", meshes)
        crop.set('name', 'crop' + str(count))
        addModel(world, crop, Pose(start + params.ridge / 2.0, 0, params.cropHeight / 2.0, 0, 0, 0))
        count += 1
        start += params.getRidgeFurrow()

    tree.write(name + '.world', pretty_print=True, encoding='utf-8', xml_declaration=True)

"""
params = FieldParameters(
    width=20, depth=30, lineNum=38, headland=6,
    ridge=0.24, furrow=0.28, cropHeight=0.3)
createFieldWorld("small_field", params, meshes=False, textures=False)
"""
params = FieldParameters(
    width=42.4, depth=35.2, lineNum=76, headland=9,
    ridge=0.24, furrow=0.28, cropHeight=0.3)
createFieldWorld("field_plants", params, meshes=True, textures=True)
