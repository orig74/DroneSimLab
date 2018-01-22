# Base docker image
FROM ubuntu:xenial

RUN apt-get -y update
RUN apt-get -y install build-essential
RUN apt-get -y install cmake 
RUN apt-get -y install xterm
RUN apt-get -y install unzip
RUN apt-get -y install curl 
RUN apt-get -y install vim 

############### Python3 ##############################
RUN curl -o /miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh
RUN /bin/bash /miniconda.sh -b -p /miniconda
RUN PATH=/miniconda/bin conda install -y pyzmq
RUN PATH=/miniconda/bin conda install -c menpo opencv3=3.2.0

######################################################
ENV QT_X11_NO_MITSHM 1
ARG UID
RUN apt-get -y install sudo
RUN useradd -u $UID docker
RUN echo "export PS1=\\\\\\\\w\\$" >> /etc/bash.bashrc
RUN echo "docker:docker" | chpasswd
RUN echo "root:root" | chpasswd
RUN echo "docker ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers 
RUN mkdir /local
COPY ./ure4.tgz /local/
RUN chown -R docker:docker /local
RUN mkdir /home/docker
RUN chown -R docker:docker /home/docker
# NOTE: This is a hack because of a bug in mono: https://bugzilla.xamarin.com/show_bug.cgi?id=30360
RUN apt-get -y install tzdata
RUN apt-get -y update
RUN apt-get -y install libxss-dev 
RUN unlink /etc/localtime
RUN ln -s /usr/share/zoneinfo/Etc/GMT /etc/localtime
USER docker
RUN cd /local && tar xzf ure4.tgz
RUN cd /local/UnrealEngine && ./Setup.sh && ./GenerateProjectFiles.sh && make

######## nvidia part ######
USER root
######## nvidia part ######
ARG GDRIVER
RUN apt-get -y update
RUN apt-get install -y software-properties-common
COPY install_graphic_driver.sh /install_graphic_driver.sh
RUN chmod +x /install_graphic_driver.sh
RUN GDRIVER=$GDRIVER /install_graphic_driver.sh

RUN echo "export PATH=/miniconda/bin:$PATH" >> /etc/bash.bashrc
