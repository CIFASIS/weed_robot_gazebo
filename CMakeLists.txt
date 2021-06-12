cmake_minimum_required(VERSION 2.8.3)
project(weed_robot_gazebo)

add_compile_options(-std=c++11)

## Package
find_package(catkin REQUIRED
  COMPONENTS
    roscpp
    gazebo_ros
    roslaunch
    angles
    control_toolbox
    gazebo_ros_control
    hardware_interface
    joint_limits_interface
)

find_package(gazebo REQUIRED)

find_package(std_msgs REQUIRED)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES weed_robot_gazebo
  CATKIN_DEPENDS
    roscpp
    gazebo_ros
    angles
    control_toolbox
    gazebo_ros_control
    hardware_interface
    joint_limits_interface
)

## Build
include_directories(
  include
  ${Boost_INCLUDE_DIR} 
  ${catkin_INCLUDE_DIRS}
  ${GAZEBO_INCLUDE_DIRS}
  ${std_msgs_INCLUDE_DIRS}
)

link_directories(${GAZEBO_LIBRARY_DIRS})

##

add_library(steer_bot_hardware_gazebo SHARED src/steer_bot_hardware_gazebo.cpp)
target_link_libraries(steer_bot_hardware_gazebo ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})

add_library(world_odom_publisher SHARED src/world_odom_publisher.cpp)
target_link_libraries(world_odom_publisher ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})

##

install(TARGETS steer_bot_hardware_gazebo
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY include/
   DESTINATION ${CATKIN_GLOBAL_INCLUDE_DESTINATION}
   FILES_MATCHING PATTERN "*.h"
)
install (FILES steer_bot_hardware_gazebo_plugins.xml
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
