# Base docker image
FROM ubuntu:16.04

#ADD https://dl.google.com/linux/direct/google-talkplugin_current_amd64.deb /src/google-talkplugin_current_amd64.deb

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y update
RUN apt-get -y install chromium-browser
RUN apt-get -y install python-scipy gawk git python-pip  
RUN echo "export PS1=\\\\\\\\w\\$" >> /etc/bash.bashrc
RUN apt-get -y install xterm
RUN pip install --upgrade pip
#RUN pip install future pymavlink MAVProxy
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:george-edison55/cmake-3.x -y
RUN apt-get update
RUN apt-get -y install cmake 
RUN apt-get -y install build-essential
RUN apt-get -y install gcc
RUN apt-get -y install clang
RUN apt-get -y install unzip
RUN apt-get -y install python-empy
RUN pip install catkin_pkg
RUN apt-get -y install openjdk-8-jdk
RUN apt-get -y install ant

######## nvidia part ######
#identify nvidia driver by running nvidia-smi
#download from http://www.nvidia.com/download/driverResults.aspx/111596/en-us
#ADD NVIDIA-Linux-x86_64-352.63.run /tmp/NVIDIA-DRIVER.run
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y keyboard-configuration
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nvidia-367
#RUN pip install pymavlink
#RUN pip install MAVProxy
RUN pip install future pymavlink==2.0.6 MAVProxy
RUN pip install dronekit
RUN pip install dronekit-sitl
RUN git clone https://github.com/mavlink/mavlink
RUN pip install lxml
RUN cd mavlink && git submodule init && git submodule update && cd pymavlink && python setup.py build && python setup.py install
