# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import socket,select,os,time
import pickle
import zmq
import sys
import numpy as np
import argparse,imp

parser = argparse.ArgumentParser()
parser.add_argument("--config_path", help="config.py file path")
args = parser.parse_args()

config=imp.load_module("config",*imp.find_module('config',[args.config_path]))

context = zmq.Context()
socket_pub = context.socket(zmq.PUB)
addr="tcp://%s:%d" % (config.zmq_pub_drone_fdm)
print("publishing to: ",addr)
socket_pub.bind(addr)

def printer(ps):
    print('-->',ps)


if __name__=="__main__":
    cnt=0
    ps={}
    sock = socket.socket(socket.AF_INET, # Internet
                                 socket.SOCK_DGRAM) # UDP
    sock.bind(('127.0.0.1', int(os.environ['SITL_POSITION_PORT'])))
    while True:
        while len(select.select([sock],[],[],0)[0]):
            data, _ = sock.recvfrom(1024)
            ps['posy'],ps['posx'],ps['posz'], ps['roll'],ps['pitch'],ps['yaw']=map(float,data.split())
            ps['roll']+=90.0
            ps['posz']=-ps['posz']
            ps['posx']=-ps['posx']
        if cnt%15==0:
            printer(ps)
        if len(ps)>0:
            socket_pub.send_multipart([config.topic_sitl_position_report,pickle.dumps(ps,-1)])
        time.sleep(20.0/1000)
        cnt+=1
    
