# DroneLab
SITL ArduCopter with Unreal Engine 4  

#building the DroneLab environment:
### DroneLab
$ git clone https://github.com/orig74/DroneLab.git
### ardupilot
$ git clone https://github.com/ArduPilot/ardupilot.git  
I added a patch to the ardupilot SITL code to work directly with the SITL data to be able to update the drone state in real-time.  
from  the Ardupilot dir run:  
$ git apply ../DroneLab/external/ardupilot.patch  
you should replace the ../DroneLab to the installation directory of Dronelab
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
