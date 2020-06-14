#!/bin/bash
xhost + local:

DRONE_LAB_DIR=`python -c "import os;print(os.path.abspath(os.path.dirname('$0/../../../')))"`
PROJECT_FILES_DIR="${PROJECT_FILES_DIR:=/local/learn/ur4}"
echo $PROJECT_FILES_DIR
#WORKSAPCE=~/projects
echo "----------------"
echo $DRONE_LAB_DIR

## 
#echo "if you get errors like docker: Error response from daemon: mkdir ....: permission denied."
#echo "try to 'chmod o+x thedir' and the ../"

chmod o+x $DRONE_LAB_DIR
chmod o+x $DRONE_LAB_DIR/dockers
##
#-v $DRONE_LAB_DIR/dockers/docker_home:/home/docker \
docker run --rm -it \
  --gpus all \
  --ipc=host \
  --user="$(id -u):$(id -g)" \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=$DISPLAY \
  --volume="$HOME:/home/host" \
  -e NVIDIA_VISIBLE_DEVICES=0 \
  --privileged \
  -v $DRONE_LAB_DIR:/DroneLab  \
  -v $PROJECT_FILES_DIR:/project_files \
  --net=host \
  python3_dev "/bin/bash"


