set_catikin () {
tmux send-keys "cd $DEMO_PATH" ENTER
}

tmux new-session -d
tmux set -g pane-border-status top
tmux split-window -h
tmux split-window -v
tmux send-keys "printf '\033]2;roscore\033\\'" ENTER
tmux send-keys roscore ENTER
sleep 3
tmux split-window -v
tmux send-keys "printf '\033]2;pos info\033\\'" ENTER
set_catikin
tmux send-keys "sleep 3" ENTER #need some delay dont know why
tmux send-keys "rostopic echo " ENTER

tmux select-pane -t 1
tmux send-keys "printf '\033]2;rov_dynamics\033\\'" ENTER
set_catikin
tmux send-keys "python rov_dynamics.py" ENTER

tmux split-window -v
set_catikin
tmux send-keys "python keyboard_control.py" ENTER
#tmux set -w pane-border-format "#{pane_index} gazebo"
tmux select-pane -t 0
tmux send-keys "printf '\033]2;catkin window\033\\'" ENTER


tmux split-window -v
tmux send-keys "printf '\033]2;catkin window\033\\'" ENTER
tmux send-keys "export ROS_PACKAGE_PATH=\$ROS_PACKAGE_PATH:/ros/catkin_ws" ENTER
tmux send-keys "rosrun ue4_bridge ue4_bridge.py" ENTER

tmux split-window -v
tmux send-keys "printf '\033]2;catkin window\033\\'" ENTER
tmux send-keys "rosrun image_view image_view image:=rgb_camera_0" ENTER

tmux split-window -v
tmux send-keys "printf '\033]2;fdm zmq publish to ue4\033\\'" ENTER
tmux send-keys "python fdm_pub_underwater.py --config_path=$UNREAL_PROXY_PATH" ENTER
#tmux send-keys "cd " ENTER
#tmux send-keys "PATH=/miniconda/bin:\$PATH python3 fdm_pub_underwater.py --config_path=$UNREAL_PROXY_PATH" ENTER

tmux select-pane -t 5
tmux split-window -v
tmux send-keys "printf '\033]2;general\033\\'" ENTER
#
#tmux set -w pane-border-format "#{pane_index} sending fdm to unreal engine"
tmux select-pane -t 0
tmux set -g pane-border-format "#{pane_index} #T"
tmux att
