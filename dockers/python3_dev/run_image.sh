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
docker run -it \
-v $DRONE_LAB_DIR:/DroneLab  \
-v $DRONE_LAB_DIR/dockers/docker_home:/home/docker \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-v $PROJECT_FILES_DIR:/project_files \
-v `readlink -f ~`:/home/host \
-e DISPLAY=$DISPLAY \
-e USERNAME=docker \
-e USER=docker \
-e HOME=/home/docker \
-u $UID \
--net=host \
--privileged \
python3_dev "/bin/bash"

#--net host \
#make posix_sitl_default jmavsim

