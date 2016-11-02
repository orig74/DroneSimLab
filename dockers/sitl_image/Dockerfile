# Base docker image
FROM ubuntu:14.04

#ADD https://dl.google.com/linux/direct/google-talkplugin_current_amd64.deb /src/google-talkplugin_current_amd64.deb

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install chromium-browser
RUN apt-get -y install python-matplotlib python-serial python-wxgtk2.8 python-wxtools python-lxml
RUN apt-get -y install python-scipy python-opencv ccache gawk git python-pip python-pexpect
RUN pip install future pymavlink MAVProxy
RUN echo "export PS1=\\\\\\\\w\\$" >> /etc/bash.bashrc
RUN apt-get -y install xterm
