#!/bin/bash
##apt-get -y update
#DRIVER_NAME=`apt-cache search nvidia |grep $GDRIVER | head -n1 |cut -d" " -f1`
DRIVER_NAME=""

add-apt-repository -y ppa:graphics-drivers/ppa
apt update
DRIVER_NAME=$(python3 << END
import os,sys
nvidia_pkgs=os.popen('apt-cache search nvidia- | grep driver | cut -d " " -f 1').read().split('\n')
for pkg in nvidia_pkgs:
  if pkg.startswith('nvidia-') and "$GDRIVER" in os.popen('apt-cache show package '+pkg+' |grep Version').read():
     print(pkg)
     print('found nvidia: '+pkg,file=sys.stderr)
     break
  else:
     print(pkg,file=sys.stderr)
END
)

echo "************** DRIVER_NAME= " $DRIVER_NAME

if [ "$DRIVER_NAME" == "" ] ; then
	echo "Error nvidia Driver $GDRIVER not found on guest machine" >&2
	echo "Try install the latest nvidia driver (using ppa) on your host machine" >&2
	exit -1
fi
DEBIAN_FRONTEND=noninteractive apt-get install -y $DRIVER_NAME
update-locale LANG=C LANGUAGE=C LC_ALL=C LC_MESSAGES=POSIX
echo "Installed nvidia driver version is:" $DRIVER_NAME $GDRIVER

