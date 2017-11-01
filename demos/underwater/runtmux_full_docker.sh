#!/bin/bash
PROJECT_NAME=Oceantest1
#DOCKER_IMAGE=ros_image_kinetic
DEMO_PATH=/DroneLab/demos/underwater/
CATKIN_WS_PATH=/home/docker/catkin_ws_uwsim

#cleanning prev run
tmux kill-session -t dronelab
source ../../scripts/common.sh

kill_images ros_indigo
kill_images python3_dev
tmux new-session -d -s dronelab

#tmux send-keys "cd ../../dockers/ros_image_indigo/ && ./run_image.sh " ENTER
tmux send-keys "cd ../../dockers/ros_image_kinetic/ && ./run_image.sh " ENTER
tmux send-keys "export UNREAL_PROXY_PATH=/DroneLab/demos/unreal_proxies/underwater_g500" ENTER
tmux send-keys "export CATKIN_WS_PATH=$CATKIN_WS_PATH" ENTER
tmux send-keys "export ROS_MAIN_SCRIPT=$ROS_MAIN_SCRIPT" ENTER
tmux send-keys "export DEMO_PATH=$DEMO_PATH" ENTER
tmux send-keys "cd $DEMO_PATH" ENTER
tmux send-keys "source run_tmux_g500.sh" ENTER
#run_inside_script "./run_rosmain.sh"

tmux new-window -n unreal
tmux send-keys "cd ../../dockers/unreal_engine_4 && ./attach.sh" ENTER
tmux send-keys "cd /project_files/${PROJECT_NAME}" ENTER
tmux send-keys "./run.sh"

tmux select-window -t 0
tmux set -g mouse on
tmux att
