# weed_robot_gazebo

Simulation of the weeding robot in Gazebo.

To run the simulation use [launch/gazebo.launch](launch/gazebo.launch).
This launcher loads the robot model from the xacro file [urdf/gazebo.xacro](urdf/gazebo.xacro), which in turn uses the robot description from the package **weed_robot_description**.
If the parameter value *meshes:=false* is used, a simplified model consisting of basic geometric shapes is loaded, which makes the simulation considerably less resource-consuming.

![Screenshot](img/gazebo.png)

The [src/world_odom_publisher.cpp](src/world_odom_publisher.cpp) node was implemented that publishes the *ground-truth* of the odometry obtained from the actual robot location in Gazebo.

The folder [meshes](meshes) contains 3D meshes in STL format of 3 soybean plants of different sizes and shapes.
These meshes are separated in subfolders by resolution level.
The simulation scenarios [worlds/field_plants.world](worlds/field_plants.world) and [worlds/field_small_plants.world](worlds/field_small_plants.world) use these meshes in their lower resolution version.

The script [utils/world_generator.py](utils/world_generator.py) can be used to generate *world* simulation scenarios.
Field characteristics such as dimensions, headlands, furrow widths, etc. can be configured.
On the other hand, crop rows can be generated with simple boxes or with plant meshes and the soil can be generated with or without using texture.

The package [ackermann_steering_controller](http://wiki.ros.org/ackermann_steering_controller) is used for the control of the robot.
It subscribes to the topic */ackermann_steering_controller/cmd_vel* where messages of type [geometry_msgs/Twist Message](http://docs.ros.org/melodic/api/geometry_msgs/html/msg/Twist.html) are received. 
Of these messages only the **linear.x** and **angular.z** components are used, the rest are ignored.

To command the robot with the keyboard the package [teleop_twist_keyboard](http://wiki.ros.org/teleop_twist_keyboard) can be used redirecting the topic in which it publishes as follows:

```
$ rosrun teleop_twist_keyboard teleop_twist_keyboard.py cmd_vel:=/ackermann_steering_controller/cmd_vel
```
