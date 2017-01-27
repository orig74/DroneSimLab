#!/bin/bash
ENTRY_POINT=unreal_proxy
ENTRY_PATH=../unreal_proxies/two_drones/
PROJECT_PATH=/project_files/testprj7_14_4/
UE4PATH=/local/UnrealEngine
python3 ../../UE4PyhtonBridge/set_path.py --entry_point $ENTRY_POINT --entry_path $ENTRY_PATH --project_path $PROJECT_PATH --ue4path $UE4PATH
