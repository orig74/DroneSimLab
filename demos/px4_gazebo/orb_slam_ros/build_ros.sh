echo "Building ROS nodes"

cd ORB_SLAM2
mkdir build
cd build
#cmake .. -DROS_BUILD_TYPE=Release -DPROJECT_SOURCE_DIR=/tmp/ORB_SLAM2/Examples/ROS/src
cmake .. -DROS_BUILD_TYPE=Release -DPROJECT_SOURCE_DIR=/tmp/ORB_SLAM2/Examples/ROS/ORB_SLAM2
make -j
