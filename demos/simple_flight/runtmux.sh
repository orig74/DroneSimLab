#!/bin/bash
LD_LIBRARY_PATH=/local/ori/GameEngines/UnrealEngine/Engine/Binaries/Linux/
PATH="/local/ori/anaconda3/bin:$PATH"
UE4PATH=/local/ori/GameEngines/UnrealEngine
#PROJECT_NAME=testplugin
PROJECT_NAME=testprj6
PROJECT_PATH=/local/learn/ur4/${PROJECT_NAME}
PROJECT_FILE=${PROJECT_PATH}/${PROJECT_NAME}.uproject
UE4PATH=/local/ori/GameEngines/UnrealEngine/Engine


BUILD_TOOL=Binaries/DotNET/UnrealBuildTool.exe
#cleanning prev run
tmux kill-session -t dronelab
docker ps |grep sitl_image  | cut -d" " -f 1 | xargs docker stop $1

tmux new-session -d -s dronelab
tmux split-window -h
tmux send-keys "cd ../../dockers/sitl_image/ && ./run_instance.sh 1" ENTER
tmux split-window -v
tmux send-keys "export DEMO_DIR=${PWD}" ENTER
tmux send-keys "cd ${PROJECT_PATH}/Plugins/UE4PyServer/Source/PyServer" ENTER
tmux send-keys "python config.py --entry_point=unreal_proxy --entry_path=\$DEMO_DIR" ENTER
tmux send-keys "./run.sh" 
#tmux select-window -t 0
tmux att

