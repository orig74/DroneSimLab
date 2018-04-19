#!/bin/bash

#game defenitions
GAME_PATH=/project_files/Ocean1_packed/LinuxNoEditor/

PACKED_NAME=Oceantest1

ENTRY_POINT=unreal_proxy
ENTRY_PATH=/DroneLab/demos/openrov/unreal_proxy/
ROS_VERSION=kinetic
DEMO_PATH=/DroneLab/demos/openrov
DRONESIMLAB_PATH=../../


#cleanning prev run
tmux kill-session -t dronelab
source /DroneLab/scripts/common.sh

kill_images ros_image_indigo
kill_images ros_image_kinetic
kill_images python3_dev
tmux new-session -d -s dronelab

tmux send-keys "cd $DRONESIMLAB_PATH/dockers/ros_image_kinetic/ && ./run_image.sh" ENTER
tmux send-keys "export UNREAL_PROXY_PATH=$DEMO_PATH/unreal_proxy/" ENTER
tmux send-keys "export DEMO_PATH=$DEMO_PATH" ENTER
tmux send-keys "cd $DEMO_PATH" ENTER
tmux send-keys "source run_tmux_openrov.sh" ENTER

tmux new-window -n unreal
tmux send-keys "cd $DRONESIMLAB_PATH/dockers/python3_dev && ./run_image.sh" ENTER
tmux send-keys "export PATH=/miniconda/bin:\$PATH" ENTER
tmux send-keys "cd ${DEMO_PATH}" ENTER
tmux send-keys "python3 /DroneLab/UE4PyhtonBridge/set_path.py --entry_point $ENTRY_POINT --entry_path $ENTRY_PATH --packed_game_name $PACKED_NAME --packed_game_path $GAME_PATH" ENTER
tmux send-keys "cd ${GAME_PATH}" ENTER
tmux send-keys "DISPLAY=:0.0 ./run.sh" ENTER

tmux select-window -t 0
tmux att
