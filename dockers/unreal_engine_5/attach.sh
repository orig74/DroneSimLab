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
docker start ue5 
docker attach ue5
