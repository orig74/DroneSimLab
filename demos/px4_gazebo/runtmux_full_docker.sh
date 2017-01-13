#!/bin/bash
PROJECT_NAME=testprj7_14_4
DOCKER_IMAGE=ros_image_indigo
DEMO_PATH=/DroneLab/demos/px4_gazebo/

#cleanning prev run
tmux kill-server

docker ps -all |grep ros_image_indigo | awk -- '{ print $1 }' | xargs docker stop
docker ps -all |grep ros_image_indigo | awk -- '{ print $1 }' | xargs docker rm 

function set_catkin_env {
tmux send-keys "tmux send-keys \"source /ros/catkin_mavros/devel/setup.bash\" ENTER" ENTER
tmux send-keys 'tmux send-keys "ROS_PACKAGE_PATH=/ros/catkin_ws/src:$ROS_PACKAGE_PATH" ENTER' ENTER
tmux send-keys 'tmux send-keys "cd /ros/catkin_ws && catkin_make" ENTER' ENTER

}

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
set_catkin_env
tmux send-keys 'tmux send-keys "cd /DroneLab/demos/px4_gazebo/" ENTER' ENTER
tmux send-keys 'tmux send-keys ./run_rosmain.sh' ENTER
tmux send-keys 'tmux split-window -v' ENTER
set_catkin_env
tmux send-keys 'tmux send-keys "rosrun control_test ue4_bridge.py" ENTER' ENTER
tmux send-keys 'tmux split-window -v' ENTER
tmux send-keys 'tmux send-keys "rosrun image_view image_view image:=rgb_camera_0" ENTER' ENTER
tmux send-keys 'tmux split-window -v' ENTER
tmux send-keys 'tmux send-keys "cd /DroneLab/demos/px4_gazebo/" ENTER' ENTER
tmux send-keys 'tmux send-keys "python3 fdm_pub.py" ENTER' ENTER
tmux send-keys 'tmux select-pane -t 0' ENTER

tmux send-keys "tmux att" ENTER


tmux new-window -n unreal
tmux send-keys "cd ../../dockers/unreal_engine_4 && ./attach.sh" ENTER
tmux send-keys "cd /project_files/${PROJECT_NAME}/Plugins/UE4PyServer/Source/PyServer" ENTER
tmux send-keys "python config.py --entry_point=unreal_proxy --entry_path=$DEMO_PATH" ENTER
tmux send-keys "./run.sh"

tmux select-window -t 0
tmux att

