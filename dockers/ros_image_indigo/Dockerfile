#Base docker image
FROM ubuntu:14.04

#ADD https://dl.google.com/linux/direct/google-talkplugin_current_amd64.deb /src/google-talkplugin_current_amd64.deb

#RUN apt-get -y update && apt-get -y upgrade
RUN pwd
RUN apt-get -y update
RUN apt-get -y install python-scipy gawk git python-pip  
RUN echo "export PS1=\\\\\\\\w\\$" >> /etc/bash.bashrc
RUN apt-get -y install xterm
RUN pip install --upgrade pip
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:george-edison55/cmake-3.x -y
#RUN apt-get update
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
RUN apt-get -y install wget
#RUN pip install ipdb rpdb
#RUN apt-get -y install python3-pip 
#RUN pip3 install pyzmq
############################## install opencv3 and numpy for python3
#RUN apt-get install -y libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
#RUN apt-get install -y libgtk2.0-dev libatlas-base-dev gfortran 
#RUN apt-get install -y python3.4-dev
#RUN git clone https://github.com/Itseez/opencv.git
#RUN cd /opencv && git checkout 3.0.0
#RUN git clone https://github.com/Itseez/opencv_contrib.git
#RUN cd /opencv_contrib && git checkout 3.0.0
#RUN pip3 install numpy
#RUN cd /opencv && mkdir build
#RUN cd /opencv/build && cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local \
#  -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib/modules -D PYTHON3_PACKAGES_PATH=/usr/local/lib/python3.4/dist-packages .. && make -j4
#RUN cd /opencv/build && make install
############sudo apt-get install ros-indigo-image-view##########################################
# Some QT-Apps/Gazebo don't not show controls without this
RUN apt-get install -y python-zmq
#RUN apt-get install -y python3-yaml
#RUN pip3 install rospkg
#RUN pip3 install catkin_pkg
#RUN apt-get -y update
RUN apt-get -y install ros-indigo-image-view2
RUN apt-get -y install wmctrl xdotool
#### tmux new version
RUN apt-get -y install libevent1-dev libncurses5-dev
ENV LC_CTYPE=C.UTF-8
RUN cd /tmp && git clone https://github.com/tmux/tmux.git && cd tmux && git checkout tags/2.3
RUN apt-get -y install automake
RUN cd /tmp/tmux && sh ./autogen.sh && ./configure && make install
#RUN pip install msgpack-python

RUN apt-get -y install ros-indigo-mavros ros-indigo-mavros-extras

#to enable copy paste in tmux mouse on https://coderwall.com/p/4b0d0a/how-to-copy-and-paste-with-tmux-on-ubuntu
RUN apt-get -y install xclip

ENV QT_X11_NO_MITSHM 1
ARG UID
#=360154
RUN useradd -u $UID docker
RUN echo "docker:docker" | chpasswd
RUN echo "docker ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers 
#RUN echo "docker:*:360154:9500:docker:/home/docker:/bin/bash >> /etc/passwd-"

