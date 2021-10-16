# Base docker image
#FROM nvidia/vulkan:1.1.121-cuda-10.1-alpha
########################### for vulkan support taken from https://github.com/NVIDIA/nvidia-docker/issues/631 
########################### edowson commented on Jul 14, 2019
#FROM nvidia/cuda:10.1-base-ubuntu18.04
FROM nvidia/cuda:11.0-base
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends wget
ENV NVIDIA_DRIVER_CAPABILITIES compute,graphics,utility
#ENV TZ=Europe/Kiev
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
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
 && rm -rf /var/lib/apt/lists/*



######################################################
ENV QT_X11_NO_MITSHM 1
RUN apt-get -y install sudo
RUN adduser --disabled-password --gecos '' --shell /bin/bash docker
RUN echo "export PS1=\\\\\\\\w\\$" >> /etc/bash.bashrc
RUN echo "docker ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers 
RUN mkdir /local
COPY ./ure5.tgz /local/
RUN chown -R docker:docker /local
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
RUN /home/docker/miniconda/bin/conda create -y --name py37 python=3.7.3 \
 && /home/docker/miniconda/bin/conda clean -ya
ENV CONDA_DEFAULT_ENV=py37
ENV CONDA_PREFIX=/home/docker/miniconda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:$PATH
RUN /home/docker/miniconda/bin/conda install conda-build=3.18.9=py37_3 \
 && /home/docker/miniconda/bin/conda clean -ya
###################################################################################################
USER root
RUN apt-get update
RUN apt-get install -y dirmngr gnupg apt-transport-https ca-certificates
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
RUN sh -c 'echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic main" > /etc/apt/sources.list.d/mono-official-stable.list'
RUN apt-get update
RUN apt-get install -y mono-complete 


#UE4
RUN cd /local && tar xzf ure5.tgz
RUN apt-get update && apt-get install -y build-essential
USER docker
#RUN cd /local/UnrealEngine && ./Setup.sh && ./GenerateProjectFiles.sh && make
RUN cd /local/UnrealEngine && ./Setup.sh 
RUN cd /local/UnrealEngine && ./GenerateProjectFiles.sh
#RUN sudo ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN cd /local/UnrealEngine && make

USER root
RUN apt-get install -y tmux
RUN wget -o out.deb https://go.microsoft.com/fwlink/?LinkID=760868
RUN apt-get install -y elfutils
#RUN apt-get install -y ./out.deb
