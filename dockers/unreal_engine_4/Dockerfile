# Base docker image
FROM ubuntu:16.04

#ADD https://dl.google.com/linux/direct/google-talkplugin_current_amd64.deb /src/google-talkplugin_current_amd64.deb

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y update
RUN apt-get -y install python-scipy gawk git python-pip  
RUN echo "export PS1=\\\\\\\\w\\$" >> /etc/bash.bashrc
RUN apt-get -y install xterm
RUN pip install --upgrade pip
RUN apt-get install -y software-properties-common
#RUN add-apt-repository ppa:george-edison55/cmake-3.x -y
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

#ARG GDRIVER=nvidia-367
ARG GDRIVER
RUN apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y $GDRIVER
RUN update-locale LANG=C LANGUAGE=C LC_ALL=C LC_MESSAGES=POSIX
RUN apt-get -y install curl 
RUN apt-get -y install vim terminator 
RUN apt-get -y install openssl libssl-dev
RUN apt-get -y install wget tmux 
RUN pip install ipdb rpdb
RUN apt-get -y install python3-pip 
RUN pip3 install pyzmq
############################## install opencv3 and numpy for python3
RUN apt-get install -y libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
RUN apt-get install -y libgtk2.0-dev libatlas-base-dev gfortran 
RUN apt-get install -y python3-dev
RUN git clone https://github.com/Itseez/opencv.git
RUN cd /opencv && git checkout 3.0.0
RUN git clone https://github.com/Itseez/opencv_contrib.git
RUN cd /opencv_contrib && git checkout 3.0.0
RUN pip3 install numpy
RUN cd /opencv && mkdir build
RUN cd /opencv/build && cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib/modules -D PYTHON3_PACKAGES_PATH=/usr/local/lib/python3.5/dist-packages .. && make -j4
RUN cd /opencv/build && make install
###################################################### install unreal engine 4
# copied dependencies from UnrealEngine/Engine/Build/BatchFiles/Linux/Setup.sh to avoid need to use sudo in line 106
RUN apt-get install -y \
mono-xbuild \
       mono-dmcs \
       libmono-microsoft-build-tasks-v4.0-4.0-cil \
       libmono-system-data-datasetextensions4.0-cil \
       libmono-system-web-extensions4.0-cil \
       libmono-system-management4.0-cil \
       libmono-system-xml-linq4.0-cil \
       libmono-corlib4.5-cil \
       libmono-windowsbase4.0-cil \
       libmono-system-io-compression4.0-cil \
       libmono-system-io-compression-filesystem4.0-cil \
       libmono-system-runtime4.0-cil \
       mono-devel \
       clang-3.8



######################################################
ENV QT_X11_NO_MITSHM 1
ARG UID
RUN useradd -u $UID docker
RUN echo "docker:docker" | chpasswd
RUN echo "root:root" | chpasswd
RUN echo "docker ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers 
RUN mkdir /local
COPY ./ure4.tgz /local/
RUN chown -R docker:docker /local
#RUN chown -R docker:docker /UnrealEngine
USER docker
RUN cd /local && tar xzf ure4.tgz
RUN cd /local/UnrealEngine && ./Setup.sh && ./GenerateProjectFiles.sh && make

