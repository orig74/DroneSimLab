#!/bin/bash
tmux send-keys -t 1 "rosrun control_test ue4_bridge.py" ENTER
tmux send-keys -t 2 "rosrun image_view image_view image:=rgb_camera_0" ENTER
sleep 1
xdotool windowactivate --sync `xdotool search --name ".*rgb_camera.*" | tail -n 1`
xdotool windowactivate --sync `xdotool search --name "Unreal.*" | head -n 1` key --delay 1000 alt+p
rosrun control_test offb2.py
xdotool windowactivate --sync `xdotool search --name "Unreal.*" | head -n 1` key --delay 1000 Escape
