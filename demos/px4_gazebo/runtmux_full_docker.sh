#!/bin/bash
PROJECT_NAME=testprj7_14_4
DOCKER_IMAGE=ros_image_indigo
DEMO_PATH=/DroneLab/demos/px4_gazebo/

#cleanning prev run
tmux kill-server
source ../../scripts/common.sh

kill_images ros_image_indigo
kill_images python3_dev
tmux new-session -d -s dronelab

tmux send-keys "cd ../../dockers/ros_image_indigo/ && ./run_image.sh " ENTER
tmux send-keys "export UNREAL_PROXY_PATH=/DroneLab/demos/unreal_proxies/two_drones" ENTER
tmux send-keys "export ROS_MAIN_SCRIPT=/DroneLab/demos/px4_gazebo/run_rosmain.sh" ENTER
tmux send-keys "source /DroneLab/scripts/run_tmux_ros_px4.sh" ENTER
#run_inside_script "./run_rosmain.sh"

tmux new-window -n unreal
tmux send-keys "cd ../../dockers/unreal_engine_4 && ./attach.sh" ENTER
tmux send-keys "cd /project_files/${PROJECT_NAME}" ENTER
tmux send-keys "./run.sh"

tmux select-window -t 0
tmux att

