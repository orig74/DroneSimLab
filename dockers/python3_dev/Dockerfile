# Base docker image
FROM ubuntu:16.04

#ADD https://dl.google.com/linux/direct/google-talkplugin_current_amd64.deb /src/google-talkplugin_current_amd64.deb
RUN pwd
RUN apt-get -y update
RUN apt-get -y install gawk git   
RUN echo "export PS1=\\\\\\\\w\\$" >> /etc/bash.bashrc
RUN apt-get -y install xterm
#RUN apt-get install -y software-properties-common
#RUN apt-get -y install cmake 
RUN apt-get -y install build-essential
#RUN apt-get -y install gcc
#RUN apt-get -y install clang
#RUN apt-get -y install unzip

######## nvidia part ######
ARG GDRIVER
RUN apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y $GDRIVER
RUN update-locale LANG=C LANGUAGE=C LC_ALL=C LC_MESSAGES=POSIX
RUN apt-get -y install curl 
RUN apt-get -y install vim 
#terminator 
#RUN apt-get -y install openssl libssl-dev
RUN apt-get -y install wget tmux 
#RUN apt-get -y install python3-pip 
#RUN pip3 install pyzmq
############################## install opencv3 and numpy for python3
#RUN apt-get install -y libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
#RUN apt-get install -y libgtk2.0-dev libatlas-base-dev gfortran 
#RUN apt-get install -y python3-dev
#RUN git clone https://github.com/Itseez/opencv.git
#RUN cd /opencv && git checkout 3.0.0
#RUN git clone https://github.com/Itseez/opencv_contrib.git
#RUN cd /opencv_contrib && git checkout 3.0.0
#RUN pip3 install numpy
#RUN cd /opencv && mkdir build
#RUN cd /opencv/build && cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local \
#  -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib/modules -D PYTHON3_PACKAGES_PATH=/usr/local/lib/python3.5/dist-packages .. && make -j4
#RUN cd /opencv/build && make install

#python3
RUN apt-get -y install curl
RUN curl -o /miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh
RUN /bin/bash /miniconda.sh -b -p /miniconda
RUN PATH=/miniconda/bin conda install -y pyzmq
RUN PATH=/miniconda/bin conda install -c https://conda.binstar.org/menpo opencv3 
RUN PATH=/miniconda/bin:$PATH pip install pymavlink



######################################################
#RUN apt-get install -y python3-matplotlib python3-scipy
#RUN pip3 install jupyter
#RUN pip3 install pymavlink
#RUN pip3 install cffi 

ENV QT_X11_NO_MITSHM 1
ARG UID
RUN useradd -u $UID docker
RUN echo "docker:docker" | chpasswd
RUN echo "root:root" | chpasswd
RUN echo "docker ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers 

