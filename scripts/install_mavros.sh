#!/bin/bash
#based on
#http://dev.px4.io/ros-mavros-installation.html
WORK_SPACE_ROOT=/ros

if [ ! -d $WORK_SPACE_ROOT/catkin_mavros/src ] ; then
sudo rosdep init
rosdep update
source /opt/ros/indigo/setup.bash
mkdir -p $WORK_SPACE_ROOT/catkin_mavros/src
cd $WORK_SPACE_ROOT/catkin_mavros
catkin init
wstool init $WORK_SPACE_ROOT/catkin_mavros/src
rosinstall_generator --upstream mavros | tee /tmp/mavros.rosinstall
sleep 1
rosinstall_generator mavlink | tee -a /tmp/mavros.rosinstall
sleep 1
wstool merge -t src /tmp/mavros.rosinstall
sleep 1
wstool update -t src
sleep 1
rosdep install --from-paths src --ignore-src --rosdistro indigo -y
sleep 1
catkin build
else
	echo "no need to install mavros ($WORK_SPACE_ROOT/catkin_mavros/src exists)"
fi
