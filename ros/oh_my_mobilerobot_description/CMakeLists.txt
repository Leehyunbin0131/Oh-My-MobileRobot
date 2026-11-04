cmake_minimum_required(VERSION 3.5)
project(oh_my_mobilerobot_description LANGUAGES NONE)

if("$ENV{ROS_VERSION}" STREQUAL "1")
  find_package(catkin REQUIRED)
  catkin_package()
  set(description_share_destination "${CATKIN_PACKAGE_SHARE_DESTINATION}")
elseif("$ENV{ROS_VERSION}" STREQUAL "2")
  find_package(ament_cmake REQUIRED)
  set(description_share_destination "share/${PROJECT_NAME}")
else()
  message(FATAL_ERROR "Source a ROS 1 or ROS 2 environment before building this package (ROS_VERSION must be 1 or 2).")
endif()

install(DIRECTORY urdf meshes config launch rviz
  DESTINATION "${description_share_destination}")
install(FILES LICENSE NOTICE
  DESTINATION "${description_share_destination}")

if("$ENV{ROS_VERSION}" STREQUAL "2")
  ament_package()
endif()
