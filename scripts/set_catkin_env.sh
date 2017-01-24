# seting catkin env run using source
source /ros/catkin_mavros/devel/setup.bash
export ROS_PACKAGE_PATH=/ros/catkin_ws/src:$ROS_PACKAGE_PATH
cd /ros/catkin_ws && catkin_make

