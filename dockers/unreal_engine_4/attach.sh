#!/bin/bash
xhost + local:

DRONE_LAB_DIR=`python -c "import os;print(os.path.abspath(os.path.dirname('$0/../../../')))"`
#WORKSAPCE=~/projects
echo "----------------"
echo $DRONE_LAB_DIR

## 
chmod o+x $DRONE_LAB_DIR
chmod o+x $DRONE_LAB_DIR/dockers
##
docker start unreal_engine 
docker attach unreal_engine
