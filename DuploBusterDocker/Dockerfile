FROM arm64v8/ros:humble-ros-base

RUN echo "Updating package manager database and install usefull softwares"
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    netcat \
    vim \
    ssh \
    cmatrix \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ros_ws
RUN echo "export ROS_MASTER_URI=http://10.42.0.39:11311/" >> "/root/.bashrc"
RUN echo "export ROS_HOSTNAME=10.42.0.39" >> "/root/.bashrc"
RUN echo "export ROS_IP=10.42.0.39" >> "/root/.bashrc"
RUN echo "export ROS_DOMAIN_ID=1" >> "/root/.bashrc"

RUN echo "source /ros_ws/load.sh" >> "/root/.bashrc"
