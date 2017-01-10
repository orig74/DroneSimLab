#!/bin/bash
PROJECT_NAME=testprj7_14_4
PROJECT_PATH=/local/learn/ur4/${PROJECT_NAME}
PROJECT_FILE=${PROJECT_PATH}/${PROJECT_NAME}.uproject
UE4PATH=/local/ori/GameEngines/UnrealEngine/Engine
ARDUPILOT_PATH=/local/dronelabdata/ardupilot
DEMO_PATH=/DroneLab/demos/two_drones/


BUILD_TOOL=Binaries/DotNET/UnrealBuildTool.exe
#cleanning prev run
tmux kill-session -t dronelab
docker ps -all |grep sitl_image  | cut -d" " -f 1 | xargs docker stop $1
docker ps -all |grep sitl_image  | cut -d" " -f 1 | xargs docker rm $1

function run_python_dev {
tmux send-keys "cd ../../dockers/python3_dev && ./run_image.sh" ENTER
tmux send-keys "cd /DroneLab/demos/two_drones" ENTER
}

tmux new-session -d -s dronelab
#tmux send-keys "python drone_main.py" ENTER
tmux split-window -h
tmux split-window -v
tmux send-keys "cd ../../dockers/unreal_engine_4 && ./attach.sh" ENTER
tmux send-keys "cd /project_files/${PROJECT_NAME}/Plugins/UE4PyServer/Source/PyServer" ENTER
tmux send-keys "python config.py --entry_point=unreal_proxy --entry_path=$DEMO_PATH" ENTER
tmux select-pane -t 0
tmux split-window -v
tmux select-pane -t 2
tmux split-window -v

tmux select-pane -t 2
tmux send-keys "cd ../../dockers/sitl_image/ && ./run_instance.sh 0" ENTER
tmux select-pane -t 3
tmux send-keys "cd ../../dockers/sitl_image/ && ./run_instance.sh 1" ENTER

tmux select-pane -t 0
tmux split-window -v
tmux select-pane -t 0
run_python_dev
tmux send-keys "python3 drone_mother.py" ENTER
tmux select-pane -t 1
run_python_dev
tmux send-keys "python3 drone_son.py 1" ENTER 
tmux select-pane -t 2
run_python_dev
tmux send-keys "python3 fdm_pub.py" ENTER 

#tmux send-keys "./run.sh" ENTER 
#tmux select-window -t 0
tmux att

