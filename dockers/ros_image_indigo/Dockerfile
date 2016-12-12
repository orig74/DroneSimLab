# Base docker image
FROM ubuntu:14.04

#ADD https://dl.google.com/linux/direct/google-talkplugin_current_amd64.deb /src/google-talkplugin_current_amd64.deb

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y update
RUN apt-get -y install python-scipy gawk git python-pip  
RUN echo "export PS1=\\\\\\\\w\\$" >> /etc/bash.bashrc
RUN apt-get -y install xterm
RUN pip install --upgrade pip
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:george-edison55/cmake-3.x -y
RUN apt-get update
RUN apt-get -y install cmake 
RUN apt-get -y install build-essential
RUN apt-get -y install gcc
RUN apt-get -y install clang
RUN apt-get -y install unzip

######## nvidia part ######
#identify nvidia driver by running nvidia-smi
#download from http://www.nvidia.com/download/driverResults.aspx/111596/en-us
#ADD NVIDIA-Linux-x86_64-352.63.run /tmp/NVIDIA-DRIVER.run
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nvidia-367
RUN update-locale LANG=C LANGUAGE=C LC_ALL=C LC_MESSAGES=POSIX
RUN echo "deb http://packages.ros.org/ros/ubuntu trusty main" > /etc/apt/sources.list.d/ros-latest.list
RUN apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 0xB01FA116
RUN apt-get -y update
RUN apt-get -y install ros-indigo-desktop
RUN apt-get -y install python-wstool python-rosinstall-generator python-catkin-tools
RUN apt-get -y install curl 
RUN bash -c "curl -ssL http://get.gazebosim.org | sh"
RUN apt-get -y install ros-indigo-gazebo7-ros-pkgs
RUN apt-get -y install ros-indigo-roslaunch
RUN apt-get -y install gazebo7
RUN apt-get -y install libgazebo7-dev
RUN apt-get -y install libprotoc-dev 
RUN apt-get -y install protobuf-compiler
RUN apt-get -y install vim terminator 
RUN apt-get -y install ros-indigo-control-toolbox
RUN apt-get -y install openssl libssl-dev
RUN apt-get -y install wget tmux 
RUN pip install ipdb rpdb
RUN apt-get -y install python3-pip 
RUN pip3 install pyzmq
ENV QT_X11_NO_MITSHM 1
ARG UID=360154
RUN useradd -u $UID docker
RUN echo "docker:docker" | chpasswd
RUN echo "docker ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers 
# Some QT-Apps/Gazebo don't not show controls without this
#RUN echo "docker:*:360154:9500:docker:/home/docker:/bin/bash >> /etc/passwd-"
