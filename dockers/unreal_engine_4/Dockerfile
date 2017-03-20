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
RUN PATH=/miniconda/bin conda install -c https://conda.binstar.org/menpo opencv3 


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
USER docker
RUN cd /local && tar xzf ure4.tgz
RUN cd /local/UnrealEngine && ./Setup.sh && ./GenerateProjectFiles.sh && make

######## nvidia part ######
USER root
######## nvidia part ######
ARG GDRIVER
COPY install_graphic_driver.sh /install_graphic_driver.sh
RUN chmod +x /install_graphic_driver.sh
RUN GDRIVER=$GDRIVER /install_graphic_driver.sh


RUN echo "export PATH=/miniconda/bin:$PATH" >> /etc/bash.bashrc

