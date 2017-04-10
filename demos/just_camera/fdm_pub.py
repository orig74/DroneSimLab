# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import socket
import pickle
import zmq
import sys
import asyncio
import numpy as np
import argparse,imp

parser = argparse.ArgumentParser()
parser.add_argument("--config_path", help="config.py file path")
args = parser.parse_args()

config=imp.load_module("config",*imp.find_module('config',[args.config_path]))

context = zmq.Context()
position_struct={}
socket_pub = context.socket(zmq.PUB)
addr="tcp://%s:%d" % (config.zmq_pub_drone_fdm)
print("publishing to: ",addr)
socket_pub.bind(addr)

@asyncio.coroutine
def reader():
    ########## init
    ps=position_struct
    ps['posx'],ps['posy'],ps['posz'],ps['roll'],ps['pitch'],ps['yaw']=[0]*6
    ps['pitch']=90 
    ######### climb
    for _ in range(300):
        ps['posz']+=.01
        yield from asyncio.sleep(1/30.0) #30Hz
    for _ in range(100):
        ps['posx']+=.01
        yield from asyncio.sleep(1/30.0) #30Hz
    for _ in range(100):
        ps['posy']+=.01
        yield from asyncio.sleep(1/30.0) #30Hz
    for _ in range(100):
        ps['posx']-=.01
        yield from asyncio.sleep(1/30.0) #30Hz
    for _ in range(100):
        ps['posy']-=.01
        yield from asyncio.sleep(1/30.0) #30Hz
        
    while 1:
        yield from asyncio.sleep(1/30.0) #30Hz


@asyncio.coroutine
def printer():
    while 1:
        print('-->',position_struct)
        yield from asyncio.sleep(1)

@asyncio.coroutine
def pub_position_struct():
    while 1:
        if len(position_struct)>0:
            socket_pub.send_multipart([config.topic_sitl_position_report,pickle.dumps(position_struct,-1)])
        yield from asyncio.sleep(1/30.0) #30Hz




if __name__=="__main__":
    loop = asyncio.get_event_loop()
    tasks=[printer(),pub_position_struct(),reader()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
