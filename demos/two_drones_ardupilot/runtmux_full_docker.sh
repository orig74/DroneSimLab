#!/bin/bash
UNREAL_PROXY_PATH=/dronelab/demos/unreal_proxies/two_drones
DEMO_PATH=/dronelab/demos/two_drones_ardupilot

tmux kill-server
source ../../scripts/common.sh
kill_images python_dev
kill_images sitl_image

if [ `docker ps | grep -v unreal_engine |wc -l` -gt 1 ]; then 
    echo "ERROR: Make sure no other docker images other then unreal_engine are running (counting on sequencial IP addresses)";
    echo "use docker rm and docker ps to remove other docker containers"
    exit 0
fi

function init_drone {
tmux send-keys "cd ../../dockers/sitl_image && ./run_image.sh" ENTER
tmux send-keys "export UNREAL_PROXY_PATH=$UNREAL_PROXY_PATH" ENTER
tmux send-keys "export DEMO_PATH=$DEMO_PATH" ENTER
tmux send-keys "export DRONE_NUM=$1" ENTER
tmux send-keys "cd /dronelab/scripts/ && source run_tmux_ardupilot.sh" ENTER
}

#cleanning prev run

tmux new-session -d -s dronelab
#tmux send-keys "python drone_main.py" ENTER
tmux send-keys "cd ../../dockers/unreal_engine_4 && ./attach.sh" ENTER
tmux new-window 
tmux split-window -h
tmux select-pane -t 0
init_drone 0
tmux select-pane -t 1
init_drone 1

#tmux send-keys "./run.sh" ENTER 
#tmux select-window -t 0
tmux set -g mouse on
tmux att

