#!/bin/bash
docker run -it --init \
  --gpus all \
  --ipc=host \
  --user="$(id -u):$(id -g)" \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=$DISPLAY \
  --volume="/local/learn/ur4:/project_files" \
  --volume="$HOME:/home/user" \
  -e NVIDIA_VISIBLE_DEVICES=0 \
  --privileged \
  unreal_engine_4_24 /bin/bash
