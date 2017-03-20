# Base docker image
FROM ubuntu:16.04
RUN pwd
RUN apt-get -y update
RUN apt-get -y install gawk git   
RUN echo "export PS1=\\\\\\\\w\\$" >> /etc/bash.bashrc
RUN apt-get -y install xterm
RUN apt-get -y install build-essential

RUN apt-get -y install curl 
RUN apt-get -y install vim 
RUN apt-get -y install wget tmux 

######## python3 ##########
RUN apt-get -y install curl
RUN curl -o /miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh
RUN /bin/bash /miniconda.sh -b -p /miniconda
RUN PATH=/miniconda/bin conda install -y pyzmq
RUN PATH=/miniconda/bin conda install -c https://conda.binstar.org/menpo opencv3 
RUN PATH=/miniconda/bin:$PATH pip install pymavlink
RUN PATH=/miniconda/bin:$PATH pip install cffi 


RUN apt-get install -y software-properties-common

######## nvidia part ######
ARG GDRIVER
COPY install_graphic_driver.sh /install_graphic_driver.sh
RUN chmod +x /install_graphic_driver.sh 
RUN GDRIVER=$GDRIVER /install_graphic_driver.sh

######## user settings ######
ENV QT_X11_NO_MITSHM 1
ARG UID
RUN useradd -u $UID docker
RUN echo "docker:docker" | chpasswd
RUN echo "root:root" | chpasswd
RUN echo "docker ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers 

