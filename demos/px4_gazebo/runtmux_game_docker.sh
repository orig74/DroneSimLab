#!/bin/bash

#game defenitions
GAME_PATH=/DroneLab/baked_games/game_demo/LinuxNoEditor/
ENTRY_POINT=unreal_proxy
ENTRY_PATH=../unreal_proxies/two_drones/
PACKED_NAME=testprj7_14_4
if [ -z "$CATKIN_WS_PATH"]; then
CATKIN_WS_PATH=/DroneLab/demos/px4_gazebo/demo_catkin_ws ;
fi
if [ -z "$ROS_MAIN_SCRIPT"]; then
ROS_MAIN_SCRIPT=/DroneLab/demos/px4_gazebo/run_rosmain.sh ;
fi

DOCKER_IMAGE=ros_indigo
DEMO_PATH=/DroneLab/demos/px4_gazebo/

#cleanning prev run
tmux kill-server
source ../../scripts/common.sh

kill_images ros_image_indigo
kill_images python3_dev
tmux new-session -d -s dronelab

tmux send-keys "cd ../../dockers/ros_image_indigo/ && ./run_image.sh " ENTER
tmux send-keys "export UNREAL_PROXY_PATH=/DroneLab/demos/unreal_proxies/two_drones" ENTER
tmux send-keys "export ROS_MAIN_SCRIPT=$ROS_MAIN_SCRIPT" ENTER
tmux send-keys "export CATKIN_WS_PATH=$CATKIN_WS_PATH" ENTER
tmux send-keys "source /DroneLab/scripts/run_tmux_ros_px4.sh" ENTER
#run_inside_script "./run_rosmain.sh"

tmux new-window -n unreal
tmux send-keys "cd ../../dockers/python3_dev && ./run_image.sh" ENTER
tmux send-keys "export PATH=/miniconda/bin:\$PATH" ENTER
tmux send-keys "cd ${DEMO_PATH}" ENTER
tmux send-keys "python3 ../../UE4PyhtonBridge/set_path.py --entry_point $ENTRY_POINT --entry_path $ENTRY_PATH --packed_game_name $PACKED_NAME --packed_game_path $GAME_PATH" ENTER
tmux send-keys "cd ${GAME_PATH}" ENTER
tmux send-keys "DISPLAY=:0.0 ./run.sh" ENTER

tmux select-window -t 0
tmux set -g mouse on
tmux att
