
cmake_minimum_required(VERSION 3.0.2)
project(parcel_sorting)
find_package(catkin REQUIRED COMPONENTS rospy std_msgs gazebo_ros gazebo_msgs)
catkin_package()
install(PROGRAMS scripts/web_bridge_node.py scripts/letter_spawner_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
