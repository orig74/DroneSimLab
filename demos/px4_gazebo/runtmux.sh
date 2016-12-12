#!/bin/bash
LD_LIBRARY_PATH=/local/ori/GameEngines/UnrealEngine/Engine/Binaries/Linux/
PATH="/local/ori/anaconda3/bin:$PATH"
UE4PATH=/local/ori/GameEngines/UnrealEngine
PROJECT_NAME=testprj6
PROJECT_PATH=/local/learn/ur4/${PROJECT_NAME}
PROJECT_FILE=${PROJECT_PATH}/${PROJECT_NAME}.uproject
UE4PATH=/local/ori/GameEngines/UnrealEngine/Engine
#PX4_PATH=/local/dronelabdata/PX4
BUILD_TOOL=Binaries/DotNET/UnrealBuildTool.exe
DOCKER_IMAGE=ros_image_indigo
#cleanning prev run
tmux kill-server

docker ps -all |grep ros_image_indigo | awk -- '{ print $1 }' | xargs docker stop
docker ps -all |grep ros_image_indigo | awk -- '{ print $1 }' | xargs docker rm 

tmux new-session -d -s dronelab
#tmux send-keys "python drone_main_mlink.py"
tmux send-keys "cd ../../dockers/ros_image_indigo/ && ./run_image.sh " ENTER
#tmux send-keys "tmux new-session -d -s drone_instance" ENTER
tmux send-keys "tmux  new-session -d" ENTER
tmux send-keys "tmux split-window -h" ENTER
tmux send-keys "tmux split-window -v" ENTER
tmux send-keys "tmux send-keys \"roscore\" ENTER" ENTER
tmux send-keys "tmux split-window -v" ENTER
tmux send-keys "tmux send-keys \"source /DroneLab/scripts/install_mavros.sh\" ENTER" ENTER
tmux send-keys "tmux send-keys \"source /ros/catkin_mavros/devel/setup.bash\" ENTER" ENTER
tmux send-keys 'tmux send-keys "sleep 3" ENTER' ENTER #need some delay dont know why
tmux send-keys 'tmux send-keys "roslaunch mavros px4.launch fcu_url:=\"udp://:14540@127.0.0.1:14557\"" ENTER' ENTER
#tmux send-keys "cd /PX4/Firmware" ENTER
tmux send-keys 'tmux select-pane -t 1' ENTER
tmux send-keys 'tmux send-keys "cd /DroneLab/PX4/Firmware" ENTER' ENTER 
tmux send-keys 'tmux send-keys "export SITL_POSITION_PORT=11341" ENTER' ENTER 
tmux send-keys 'tmux send-keys "make posix_sitl_default gazebo" ENTER' ENTER
tmux send-keys 'tmux select-pane -t 0' ENTER
#tmux send-keys "tmux send-keys \"source /ros/catkin_ws/devel/setup.bash\" ENTER" ENTER
tmux send-keys "tmux send-keys \"source /ros/catkin_mavros/devel/setup.bash\" ENTER" ENTER
tmux send-keys 'tmux send-keys "ROS_PACKAGE_PATH=/ros/catkin_ws/src:$ROS_PACKAGE_PATH" ENTER' ENTER
tmux send-keys 'tmux send-keys "cd /ros/catkin_ws && catkin_make" ENTER' ENTER
tmux send-keys 'tmux send-keys "rosrun control_test offb2.py"' ENTER
tmux send-keys "tmux att" ENTER


tmux new-window -n unreal
tmux send-keys "export DEMO_DIR=${PWD}" ENTER
tmux send-keys "cd ${PROJECT_PATH}/Plugins/UE4PyServer/Source/PyServer" ENTER
tmux send-keys "python config.py --entry_point=unreal_proxy --entry_path=\$DEMO_DIR" ENTER


#tmux send-keys "make posix_sitl_default jmavsim" 
#tmux split-window -v
#tmux send-keys "export DEMO_DIR=${PWD}" ENTER
#tmux send-keys "cd ${PROJECT_PATH}/Plugins/UE4PyServer/Source/PyServer" ENTER
#tmux send-keys "python config.py --entry_point=unreal_proxy --entry_path=\$DEMO_DIR" ENTER
#tmux send-keys "./run.sh" 
#tmux select-window -t 0
tmux att

