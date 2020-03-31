cmake_minimum_required(VERSION 2.8.3)
project(weed_robot_gazebo)

## Package
find_package(catkin REQUIRED COMPONENTS roslaunch)

catkin_package()

add_compile_options(-std=c++11)
