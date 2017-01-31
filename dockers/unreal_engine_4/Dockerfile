# Base docker image
FROM ubuntu:xenial

#ADD https://dl.google.com/linux/direct/google-talkplugin_current_amd64.deb /src/google-talkplugin_current_amd64.deb

RUN apt-get -y update
RUN apt-get -y install build-essential
RUN apt-get -y install cmake 
RUN apt-get -y install xterm
RUN apt-get -y install unzip
RUN apt-get -y install curl 
RUN apt-get -y install vim 
#RUN apt-get -y install openssl libssl-dev
#RUN apt-get -y install wget tmux 

############### Python3 ##############################
RUN curl -o /miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh
RUN /bin/bash /miniconda.sh -b -p /miniconda
RUN PATH=/miniconda/bin conda install -y pyzmq
RUN PATH=/miniconda/bin conda install -c https://conda.binstar.org/menpo opencv3 

###################################################### install unreal engine 4
# copied dependencies from UnrealEngine/Engine/Build/BatchFiles/Linux/Setup.sh to avoid need to use sudo in line 106
#RUN apt-get install -y \
#mono-xbuild \
#       mono-dmcs \
#       libmono-microsoft-build-tasks-v4.0-4.0-cil \
#       libmono-system-data-datasetextensions4.0-cil \
#       libmono-system-web-extensions4.0-cil \
#       libmono-system-management4.0-cil \
#       libmono-system-xml-linq4.0-cil \
#       libmono-corlib4.5-cil \
#       libmono-windowsbase4.0-cil \
#       libmono-system-io-compression4.0-cil \
#       libmono-system-io-compression-filesystem4.0-cil \
#       libmono-system-runtime4.0-cil \
#       mono-devel \
#       clang-3.8


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
#RUN chown -R docker:docker /UnrealEngine
USER docker
RUN cd /local && tar xzf ure4.tgz
RUN cd /local/UnrealEngine && ./Setup.sh && ./GenerateProjectFiles.sh && make

######## nvidia part ######
#identify nvidia driver by running nvidia-smi
#download from http://www.nvidia.com/download/driverResults.aspx/111596/en-us
#ADD NVIDIA-Linux-x86_64-352.63.run /tmp/NVIDIA-DRIVER.run
USER root
#ARG GDRIVER=nvidia-367
ARG GDRIVER
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y $GDRIVER
RUN update-locale LANG=C LANGUAGE=C LC_ALL=C LC_MESSAGES=POSIX


RUN echo "export PATH=/miniconda/bin:$PATH" >> /etc/bash.bashrc

