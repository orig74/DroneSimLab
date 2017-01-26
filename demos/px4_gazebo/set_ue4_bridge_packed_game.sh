#!/bin/bash
ENTRY_POINT=unreal_proxy
ENTRY_PATH=../unreal_proxies/two_drones/
PACKED_PATH=../../baked_games/game_demo/LinuxNoEditor
PACKED_NAME=testprj7_14_4
python3 ../../UE4PyhtonBridge/set_path.py --entry_point $ENTRY_POINT --entry_path $ENTRY_PATH --packed_game_name $PACKED_NAME --packed_game_path $PACKED_PATH 
