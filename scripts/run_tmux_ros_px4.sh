

tmux  new-session -d
tmux set -g pane-border-status top
tmux split-window -h
tmux split-window -v
tmux send-keys "printf '\033]2;roscore\033\\'" ENTER
tmux send-keys roscore ENTER
sleep 3
tmux split-window -v
tmux send-keys "printf '\033]2;mavros\033\\'" ENTER
tmux send-keys "source /DroneLab/scripts/install_mavros.sh" ENTER
tmux send-keys "source /ros/catkin_mavros/devel/setup.bash" ENTER
tmux send-keys "sleep 3" ENTER #need some delay dont know why
tmux send-keys "source ~/.bashrc" ENTER
tmux send-keys "roslaunch mavros px4.launch fcu_url:=udp://:14540@127.0.0.1:14557" ENTER
tmux select-pane -t 1
tmux send-keys "printf '\033]2;gazebo\033\\'" ENTER
tmux send-keys "cd /DroneLab/PX4/Firmware" ENTER
tmux send-keys "export SITL_POSITION_PORT=11341" ENTER

#remark the nexline to load gazebo gui client for debug prpose
tmux send-keys "export HEADLESS=True" ENTER

tmux send-keys "make posix_sitl_default gazebo" ENTER
#tmux set -w pane-border-format "#{pane_index} gazebo"
tmux select-pane -t 0
tmux send-keys "printf '\033]2;catkin window\033\\'" ENTER
tmux send-keys "source /DroneLab/scripts/set_catkin_env.sh" ENTER
tmux send-keys "$ROS_MAIN_SCRIPT" ENTER
#tmux send-keys "cd /DroneLab/demos/px4_gazebo/" ENTER
#tmux send-keys "./run_rosmain.sh" ENTER
tmux split-window -v
tmux send-keys "source /DroneLab/scripts/set_catkin_env.sh" ENTER
tmux send-keys "printf '\033]2;catkin window\033\\'" ENTER
tmux send-keys "rosrun ue4_bridge ue4_bridge.py" ENTER
tmux split-window -v
tmux send-keys "printf '\033]2;catkin window\033\\'" ENTER
#tmux send-keys "rosrun image_view image_view image:=rgb_camera_0" ENTER
tmux split-window -v
tmux send-keys "printf '\033]2;fdm zmq publish to ue4\033\\'" ENTER
tmux send-keys "cd /DroneLab/scripts/" ENTER
tmux send-keys "PATH=/miniconda/bin:\$PATH python3 fdm_pub_px4_gazebo.py --config_path=$UNREAL_PROXY_PATH" ENTER

tmux select-pane -t 5
tmux split-window -v
tmux send-keys "printf '\033]2;slam\033\\'" ENTER
#
#tmux set -w pane-border-format "#{pane_index} sending fdm to unreal engine"
tmux select-pane -t 0
tmux set -g pane-border-format "#{pane_index} #T"
tmux att
