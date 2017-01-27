tmux  new-session -d
tmux set -g pane-border-status top
tmux split-window -v
tmux split-window -v
tmux select-pane -t 1
tmux send-keys "printf '\033]2;ardupilot sitl\033\\'" ENTER 
tmux send-keys "cd /dronelab/ardupilot/ArduCopter/ && ../Tools/autotest/sim_vehicle.py -w" ENTER
tmux select-pane -t 2
tmux send-keys "PATH=/miniconda/bin:\$PATH" ENTER
tmux send-keys "printf '\033]2;fdm_pub\033\\'" ENTER
tmux send-keys "cd /DroneLab/scripts/" ENTER
tmux send-keys "python3 fdm_pub_ardupilot.py --config_path=$UNREAL_PROXY_PATH" ENTER
#tmux send-keys "python3 fdm_pub_ardupilot.py --config_path=/dronelab/demos/unreal_proxies/two_drones" ENTER
#tmux set -w pane-border-format "#{pane_index} sending fdm to unreal engine"
tmux select-pane -t 0
tmux send-keys "printf '\033]2;main\033\\'" ENTER
tmux send-keys "PATH=/miniconda/bin:\$PATH" ENTER
tmux send-keys "export UNREAL_PROXY_PATH=$UNREAL_PROXY_PATH" ENTER
tmux send-keys "cd $DEMO_PATH" ENTER
tmux send-keys "export DRONE_NUM=$DRONE_NUM" ENTER

tmux set -g pane-border-format "#{pane_index} #T"
tmux att

