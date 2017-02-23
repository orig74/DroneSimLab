#!/bin/bash
sleep 3
tmux send-keys -t 2 "cd /DroneLab/demos/px4_gazebo && roslaunch ./image_view.launch" ENTER
sleep 1
xdotool windowactivate --sync `xdotool search --name ".*rgb_camera.*" | tail -n 1`
xdotool windowactivate --sync `xdotool search --name "Unreal.*" | head -n 1` key --delay 1000 alt+p

### init slam part
#SLAM_CMD="ORB_SLAM2 RGBD /tmp/ORB_SLAM2/Vocabulary/ORBvoc.txt /tmp/ORB_SLAM2/Examples/RGB-D/TUM1.yaml"
SLAM_CMD="ORB_SLAM2 RGBD /tmp/ORB_SLAM2/Vocabulary/ORBvoc.txt ./ue4.yaml"
ORB_SLAM_DEMO_PATH=/DroneLab/demos/px4_gazebo/orb_slam_ros
tmux send-keys -t 6 "cd $ORB_SLAM_DEMO_PATH" ENTER
ORB_PATH_EXPR="ROS_PACKAGE_PATH=${ROS_PACKAGE_PATH}:$ORB_SLAM_DEMO_PATH"
tmux send-keys -t 6 "$ORB_PATH_EXPR ./build_ros.sh && $ORB_PATH_EXPR rosrun $SLAM_CMD " ENTER 
#tmux send-keys -t 6 "$ORB_PATH_EXPR rosrun $SLAM_CMD" ENTER

rosrun control_test offb2.py
xdotool windowactivate --sync `xdotool search --name "Unreal.*" | head -n 1` key --delay 1000 Escape

#export ROS_PACKAGE_PATH=${ROS_PACKAGE_PATH}:/DroneLab/demos/px4_gazebo/orb_slam_ros
#rosrun ORB_SLAM2 RGBD /tmp/ORB_SLAM2/Vocabulary/ORBvoc.txt /tmp/ORB_SLAM2/Examples/RGB-D/TUM1.yaml

