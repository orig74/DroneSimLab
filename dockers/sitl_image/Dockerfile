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
