#!/bin/bash
xdotool windowactivate --sync `xdotool search --name ".*rgb_camera.*" | tail -n 1`
xdotool windowactivate --sync `xdotool search --name "Unreal.*" | head -n 1` key --delay 1000 alt+p
rosrun control_test offb2.py
xdotool windowactivate --sync `xdotool search --name "Unreal.*" | head -n 1` key --delay 1000 Escape
