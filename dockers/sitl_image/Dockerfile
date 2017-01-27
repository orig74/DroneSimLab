# Base docker image
FROM ubuntu:14.04

RUN apt-get -y update 
#RUN apt-get -y install chromium-browser
#RUN apt-get -y install python-matplotlib python-serial python-wxgtk2.8 python-wxtools python-lxml
#RUN apt-get -y install python-scipy python-opencv 
#RUN apt-get -y install ccache gawk git python-pip python-pexpect
RUN apt-get -y install python-pip
RUN apt-get -y install ccache gawk git python-pexpect python-lxml
RUN apt-get -y install python-dev
RUN pip install future pymavlink MAVProxy
RUN echo "export PS1=\\\\\\\\w\\$" >> /etc/bash.bashrc
#RUN apt-get -y install xterm
RUN mkdir -p /.tilecache/SRTM
RUN chmod -R 777 /.tilecache

#install tmux new version
RUN apt-get -y install libevent1-dev libncurses5-dev
ENV LC_CTYPE=C.UTF-8
RUN cd /tmp && git clone https://github.com/tmux/tmux.git && cd tmux && git checkout tags/2.3
RUN apt-get -y install automake
RUN apt-get -y install pkg-config
RUN cd /tmp/tmux && sh ./autogen.sh && ./configure && make install

#python3
#RUN apt-get -y install python3-dev python3-pip
#RUN apt-get -y install libzmq3-dev
#RUN pip3 install pyzmq

RUN apt-get -y install curl
RUN curl -o /miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh
RUN /bin/bash /miniconda.sh -b -p /miniconda
RUN PATH=/miniconda/bin conda install -y pyzmq
RUN apt-get -y update 
RUN apt-get -y install libgtk2.0-dev
RUN apt-get -y install pkg-config
RUN PATH=/miniconda/bin conda install -c https://conda.binstar.org/menpo opencv3 

RUN apt-get -y install build-essential
RUN PATH=/miniconda/bin:$PATH pip install pymavlink

### normal user settings
ARG UID
RUN useradd -u $UID docker
RUN echo "docker:docker" | chpasswd
RUN echo "root:root" | chpasswd
RUN echo "docker ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers


#
