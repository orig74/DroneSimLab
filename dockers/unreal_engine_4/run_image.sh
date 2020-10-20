#!/bin/bash
xhost + local:

DRONE_LAB_DIR=`python -c "import os;print(os.path.abspath(os.path.dirname('$0/../../../')))"`

if [ -z $PROJECT_FILES_DIR ]; then
	echo "ERROR!!! No PROJECT_FILES_DIR variable found setting to /local/learn/ur4"
	PROJECT_FILES_DIR=/local/learn/ur4
fi

#WORKSAPCE=~/projects
echo "----------------"
echo $DRONE_LAB_DIR

## 
#echo "if you get errors like docker: Error response from daemon: mkdir ....: permission denied."
#echo "try to 'chmod o+x thedir' and the ../"

chmod o+x $DRONE_LAB_DIR
chmod o+x $DRONE_LAB_DIR/dockers
##
docker run -it --gpus all --name unreal_engine \
-v $DRONE_LAB_DIR:/DroneLab  \
-v `readlink -f ~`:/home/host \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-v $PROJECT_FILES_DIR:/project_files \
-e DISPLAY=$DISPLAY \
-e USERNAME=docker \
-e USER=docker \
-e HOME=/home/docker \
-u $UID \
--net=host \
--privileged \
unreal_engine_4 "/bin/bash"

#--net host \
#make posix_sitl_default jmavsim

#-v $DRONE_LAB_DIR/dockers/docker_home:/home/docker \
