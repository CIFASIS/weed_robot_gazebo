cmake_minimum_required(VERSION 2.8.3)
project(weed_robot_gazebo)

## Package
find_package(catkin REQUIRED COMPONENTS
  roscpp
  gazebo_ros 
  roslaunch
)

find_package(gazebo REQUIRED)

find_package(std_msgs REQUIRED)

catkin_package(
  DEPENDS roscpp gazebo_ros 
)

add_compile_options(-std=c++11)

## Build
include_directories(
  ${Boost_INCLUDE_DIR} 
  ${catkin_INCLUDE_DIRS}
  ${GAZEBO_INCLUDE_DIRS}
  ${std_msgs_INCLUDE_DIRS}
)

link_directories(${GAZEBO_LIBRARY_DIRS})

##

add_library(world_odom_publisher SHARED src/world_odom_publisher.cpp)
target_link_libraries(world_odom_publisher ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})

