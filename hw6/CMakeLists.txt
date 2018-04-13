cmake_minimum_required(VERSION 2.8.3)
project(hw6)

find_package(catkin REQUIRED COMPONENTS
  actionlib
  move_base_msgs
  roscpp
  rospy
  sensor_msgs
  std_msgs
  geometry_msgs
  people_msgs
  tf
)


catkin_package(
 INCLUDE_DIRS include
 LIBRARIES hw6
 CATKIN_DEPENDS actionlib move_base_msgs roscpp rospy sensor_msgs std_msgs geometry_msgs people_msgs tf
 DEPENDS system_lib
)

include_directories(
 include
  ${catkin_INCLUDE_DIRS}
)

add_executable(move_client src/move_client.cpp)
add_executable(people_follow src/people_follow.cpp)
target_link_libraries(move_client ${catkin_LIBRARIES})
target_link_libraries(people_follow ${catkin_LIBRARIES})
add_dependencies(move_client ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
add_dependencies(people_follow ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
