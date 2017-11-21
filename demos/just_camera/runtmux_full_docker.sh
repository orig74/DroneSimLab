#!/bin/bash
PROJECT_NAME=Oceantest1
CATKIN_WS_PATH=/DroneLab/demos/px4_gazebo/demo_catkin_ws
if [ -z "$CATKIN_WS_PATH"]; then
CATKIN_WS_PATH=/DroneLab/demos/px4_gazebo/demo_catkin_ws ;
fi
if [ -z "$ROS_MAIN_SCRIPT"]; then
ROS_MAIN_SCRIPT=/DroneLab/demos/px4_gazebo/run_rosmain.sh ;
fi

if [ -z "$ROS_VERSION" ]; then
	#ROS_VERSION=indigo
	ROS_VERSION=kinetic
fi


DEMO_PATH=/DroneLab/demos/just_camera/


#cleanning prev run
tmux kill-session -t dronelab
source ../../scripts/common.sh

kill_images ros_indigo
kill_images ros_kinetic
kill_images python3_dev
tmux new-session -d -s dronelab

#tmux send-keys "cd ../../dockers/ros_image_indigo/ && ./run_image.sh " ENTER
tmux send-keys "cd ../../dockers/ros_image_kinetic/ && ./run_image.sh " ENTER
tmux send-keys "export UNREAL_PROXY_PATH=/DroneLab/demos/unreal_proxies/two_drones" ENTER
tmux send-keys "export CATKIN_WS_PATH=$CATKIN_WS_PATH" ENTER
tmux send-keys "export ROS_MAIN_SCRIPT=$ROS_MAIN_SCRIPT" ENTER
tmux send-keys "cd ${DEMO_PATH} && source just_camera.sh" ENTER
#run_inside_script "./run_rosmain.sh"

tmux new-window -n unreal
tmux send-keys "cd ../../dockers/unreal_engine_4 && ./attach.sh" ENTER
tmux send-keys "cd /project_files/${PROJECT_NAME}" ENTER
#tmux send-keys "./run.sh"

tmux select-window -t 0
tmux set -g mouse on
tmux att
