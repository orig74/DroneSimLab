#!/bin/bash

source ../../scripts/common.sh

kill_images python3_dev 
tmux kill-session -t dronelab
