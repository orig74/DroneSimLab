

tmux  new-session -d
tmux set -g pane-border-status top
tmux split-window -h
tmux split-window -v
tmux send-keys "printf '\033]2;roscore\033\\'" ENTER
tmux send-keys roscore ENTER
sleep 3
tmux split-window -v
tmux send-keys "printf '\033]2;mavros\033\\'" ENTER
tmux select-pane -t 1
tmux send-keys "printf '\033]2;gazebo\033\\'" ENTER

tmux select-pane -t 0
tmux send-keys "printf '\033]2;catkin window\033\\'" ENTER
tmux split-window -v
tmux send-keys "source /DroneLab/scripts/set_catkin_env.sh" ENTER
tmux send-keys "printf '\033]2;catkin window\033\\'" ENTER
tmux send-keys "rosrun ue4_bridge ue4_bridge.py" ENTER
tmux split-window -v
tmux send-keys "printf '\033]2;catkin window\033\\'" ENTER
tmux send-keys "rosrun image_view image_view image:=rgb_camera_0" ENTER
#tmux send-keys "rosrun image_view video_recorder image:=rgb_camera_0 ~fps=30" ENTER
tmux split-window -v
tmux send-keys "printf '\033]2;fdm zmq publish to ue4\033\\'" ENTER
#tmux send-keys "cd ${DEMO_PATH}" ENTER
tmux send-keys "PATH=/miniconda/bin:\$PATH python3 fdm_pub2.py --config_path=$UNREAL_PROXY_PATH" ENTER
tmux select-pane -t 5
tmux split-window -v
tmux send-keys "printf '\033]2;slam\033\\'" ENTER
tmux select-pane -t 0
tmux set -g pane-border-format "#{pane_index} #T"
tmux att
