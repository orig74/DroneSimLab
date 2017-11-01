mkdir ../dockers/docker_home/catkin_ws_uwsim
cd ../dockers/docker_home/catkin_ws_uwsim
echo "- other: {local-name: /opt/ros/groovy/share/ros}" > .rosinstall 
echo "- other: {local-name: /opt/ros/groovy/share}" >> .rosinstall
echo "- other: {local-name: /opt/ros/groovy/stacks}" >> .rosinstall
echo "- setup-file: {local-name: /opt/ros/groovy/setup.sh}" >> .rosinstall
echo "- git: {local-name: src/underwater_simulation," >> .rosinstall
echo "        uri: 'https://github.com/uji-ros-pkg/underwater_simulation.git', version: kinetic-devel}" >> .rosinstall
rosws update
rosdep install --from-paths src --ignore-src --rosdistro kinetic -y
catkin_make install

