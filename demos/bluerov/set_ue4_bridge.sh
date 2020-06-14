#!/bin/bash
DRONESIMLAB_PATH=$HOME/projects/DroneSimLab
ENTRY_POINT=unreal_proxy
ENTRY_PATH=unreal_proxy/
PROJECT_PATH=/project_files/Oceantest1/
UE4PATH=/local/UnrealEngine
python3 $DRONESIMLAB_PATH/UE4PyhtonBridge/set_path.py --entry_point $ENTRY_POINT --entry_path $ENTRY_PATH --project_path $PROJECT_PATH --ue4path $UE4PATH
