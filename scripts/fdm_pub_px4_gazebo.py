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
fdm_sock=None
socket_pub = context.socket(zmq.PUB)
addr="tcp://%s:%d" % (config.zmq_pub_drone_fdm)
print("publishing to: ",addr)
socket_pub.bind(addr)

def init():
    global fdm_sock
    udp = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
    udp.bind(('127.0.0.1', 11341)) #the port is internal in the virt machine also refenced at runtmux.sh
    fdm_sock=udp

def reader():
    data=fdm_sock.recv(1024)
    fdm=map(float,data.strip().split())
    ps=position_struct
    ps['posx'],ps['posy'],ps['posz'],ps['roll'],ps['pitch'],ps['yaw']=fdm
    #converting to unreal coordinates
    
    #convert to degrees
    ps['roll']*=180.0/np.pi
    ps['pitch']*=180.0/np.pi
    ps['yaw']=ps['yaw']*180.0/np.pi

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
    init()
    loop = asyncio.get_event_loop()
    loop.add_reader(fdm_sock,reader) 
    tasks=[printer(),pub_position_struct()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
