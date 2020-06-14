# Base docker image
FROM nvidia/cuda:10.1-base-ubuntu18.04
ENV NVIDIA_DRIVER_CAPABILITIES compute,graphics,utility

RUN apt-get update && apt-get install -y --no-install-recommends wget
# Install Vulkan SDK
RUN wget -qO - http://packages.lunarg.com/lunarg-signing-key-pub.asc | apt-key add - && \
wget -qO /etc/apt/sources.list.d/lunarg-vulkan-1.1.121-bionic.list http://packages.lunarg.com/vulkan/1.1.121/lunarg-vulkan-1.1.121-bionic.list && \
apt update && apt install -y vulkan-sdk && apt upgrade -y && apt autoremove -y

COPY nvidia_icd.json /etc/vulkan/icd.d/nvidia_icd.json


RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
	cmake \
	xterm \
	unzip \
	vim \
    gawk \
    xterm \
    build-essential \
    tmux \
    software-properties-common \
    sudo \
    python-pip \
    libgtk2.0-dev \
    pkg-config \
 && rm -rf /var/lib/apt/lists/*


RUN echo "export PS1=\\\\\\\\w\\$" >> /etc/bash.bashrc

######## python3 ##########

RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test
RUN apt-get -y update
RUN apt-get -y upgrade libstdc++6

######## user settings ######
ENV QT_X11_NO_MITSHM 1
RUN adduser --disabled-password --gecos '' --shell /bin/bash docker
RUN echo "export PS1=\\\\\\\\w\\$" >> /etc/bash.bashrc
RUN echo "docker ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers 

###  gstreamer ######
RUN apt-get install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools

USER docker
ENV HOME=/home/docker
RUN chmod 777 /home/docker
########################################################
#install miniconda
RUN curl -o ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py38_4.8.2-Linux-x86_64.sh \
 && chmod +x ~/miniconda.sh \
 && ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh
ENV PATH=/home/docker/miniconda/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false

# Create a Python 3.7 environment
RUN conda create -y --name py37 python=3.7.3 \
 && conda clean -ya
ENV CONDA_DEFAULT_ENV=py37
ENV CONDA_PREFIX=/home/docker/miniconda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:$PATH
RUN /home/docker/miniconda/bin/conda install conda-build=3.18.9=py37_3 \
 && /home/docker/miniconda/bin/conda clean -ya

RUN conda install -y pyzmq
RUN pip install --upgrade pip
RUN pip install pymavlink
RUN pip install cffi 
RUN pip install opencv-python
RUN pip install opencv-contrib-python
RUN pip install dill
RUN pip install pygame
RUN pip install scipy



