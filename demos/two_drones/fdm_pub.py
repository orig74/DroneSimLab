# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import config
import socket
import pickle
import zmq
import sys
sys.path.append('..')
from common import fdm
import asyncio

context = zmq.Context()
position_struct={}
fdm_socks=[]
socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://%s:%d" % (config.zmq_pub_drone_fdm))

fd=open('pos.txt','w')

def init():
    for drone_num in range(config.n_drones):
        udp = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        udp.bind(('127.0.0.1', 5503+drone_num*10))
        fdm_socks.append(udp)
    return fdm_socks

def reader(sock,ind):
    data=sock.recv(1024)
    cfdm=fdm.fdm_from_buf(data)
    if not ind in position_struct:
        position_struct[ind]={}
    ps=position_struct[ind]
    ps['lon']=cfdm[0].longitude
    ps['lat']=cfdm[0].latitude
    ps['alt']=cfdm[0].altitude #above sea level
    ps['roll']=cfdm[0].phi
    ps['pitch']=cfdm[0].theta
    ps['yaw']=cfdm[0].psi
    if ind==0:
        print('%.10f,%.10f,%.7f'%(ps['lon'],ps['lat'], ps['alt']),file=fd)
        fd.flush()

@asyncio.coroutine
def printer():
    while 1:
        print('-->',position_struct)
        yield from asyncio.sleep(1)

@asyncio.coroutine
def pub_position_struct():
    while 1:
        socket_pub.send_multipart([config.topic_sitl_position_report,pickle.dumps(position_struct,-1)])
        yield from asyncio.sleep(1/30.0) #30Hz




if __name__=="__main__":
    init()
    loop = asyncio.get_event_loop()
    for ind,sock in enumerate(fdm_socks):
        loop.add_reader(sock,reader,sock,ind) 
    tasks=[printer(),pub_position_struct()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
