#!/bin/bash
docker run -it --init \
  --gpus 'all,"capabilities=graphics,utility,display,video,compute"' \
  --device=/dev/snd \
  -e PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native -v ${XDG_RUNTIME_DIR}/pulse/native:${XDG_RUNTIME_DIR}/pulse/native -v ~/.config/pulse/cookie:/root/.config/pulse/cookie --group-add $(getent group audio | cut -d: -f3)\
  --user="$(id -u):$(id -g)" \
  --name ue5 \
  --volume="/local/learn/ue5:/project_files" \
  --ipc=host \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=$DISPLAY \
  -e NVIDIA_VISIBLE_DEVICES=0 \
  --volume="$HOME:/home/user" \
  unreal_engine_5 /bin/bash
#  --privileged \
#--gpus 'all,"capabilities=all"' \
