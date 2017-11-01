#!/bin/bash

source ../../scripts/common.sh

kill_images ros_image_indigo
kill_images ros_image_kinetic
kill_images python3_dev

tmux kill-session -t dronelab
