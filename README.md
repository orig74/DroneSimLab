# DroneLab
SITL ArduCopter with Unreal Engine 4  

#building the dronelab environment:
### DroneLab
$ git clone https://github.com/orig74/DroneLab.git
### ardupilot
$ git clone https://github.com/ArduPilot/ardupilot.git
###UE4Pyserver
Folow instalation instractions of  [UE4Pyserver](https://github.com/orig74/UE4PyServer)  
### Building docker images for the SITL
$ cd DroneLab/dockers/sitl_image
run:  
$ ./build

## Running The simple_flight Demo
$cd DroneLab/demos/simple_flight
edit the runtmux.sh file to match your path installations, it's the lines at the beginning of the file containing the "/local" prefix

## Demo:  
[demo](https://youtu.be/4dplKATTkMw")

##Contact Me:  
oga13@uclive.ac.nz  
