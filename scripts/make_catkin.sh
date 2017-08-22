#!/bin/bash
#based on
#http://dev.px4.io/ros-mavros-installation.html
if [ ! -d /DroneLab/ros/catkin_ws/build ] ; then
#source /opt/ros/indigo/setup.bash
source /opt/ros/kinetic/setup.bash
cd /DroneLab/ros/catkin_ws
catkin_make install && cd build && make install
else
	echo "no need to install catkin"
fi
