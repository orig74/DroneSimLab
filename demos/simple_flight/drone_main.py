# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from pymavlink import mavutil
import numpy as np
import zmq
import sys
import time
import pickle

zmq_port = "5556"
topic_postition=b'position'

context = zmq.Context()
zmq_socket = context.socket(zmq.PUB)
zmq_socket.bind("tcp://*:%s" % zmq_port)

mav1 = mavutil.mavlink_connection('udp:127.0.0.1:14561')

print("Waiting for HEARTBEAT")
mav1.wait_heartbeat()
print("Heartbeat from APM (system %u component %u)" % (mav1.target_system, mav1.target_system))

mav1.arducopter_arm()
mav1.set_mode('LOITER')

event = mavutil.periodic_event(0.3)
freq=30
pub_position_event = mavutil.periodic_event(freq)

def set_rcs(rc1, rc2, rc3, rc4):
    global mav1
    values = [ 65535 ] * 8
    values[0] = rc1
    values[1] = rc2
    values[2] = rc3
    values[3] = rc4
    mav1.mav.rc_channels_override_send(mav1.target_system, mav1.target_component, *values)

def get_position_struct(mav):
    d={}
    d['posz']=mav1.messages['VFR_HUD'].alt
    sm=mav1.messages['SIMSTATE']
    home=mav1.messages['HOME']
    lng_factor=np.cos(np.radians(sm.lng/1.0e7))
    earth_rad_m=6371000.0
    deg_len_m=earth_rad_m*np.pi/180.0
    d['posx']=(sm.lng-home.lon)/1.0e7*lng_factor*deg_len_m
    d['posy']=(sm.lat-home.lat)/1.0e7*deg_len_m
    d['yaw']=np.degrees(sm.yaw)
    d['roll']=np.degrees(sm.roll)
    d['pitch']=np.degrees(sm.pitch)
    return d

def mission_thread():
    print('--0--')
    set_rcs(1500,1500,1550,1500)
    for i in range(freq*10):
        yield
    print('--1--')
    set_rcs(1500,1550,1500,1500)
    for i in range(freq*10):
        yield
    print('--2--')
    set_rcs(1500,1450,1500,1500)
    for i in range(freq*10):
        yield
    print('--3--')
    set_rcs(1500,1500,1450,1500)
    while 1:
        yield


mthread=mission_thread()
start=time.time()
import socket,select
direct_udp = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
direct_udp.bind(('127.0.0.1', 19988))


udp_position=None
while True:
    mav1.recv_msg()
    if event.trigger():
        #print(mav1.messages['VFR_HUD'].alt)
        #print(mav1.messages.keys())
        #print(mav1.messages['HOME'])
        #print(mav1.messages['SIMSTATE'])
        
        print('X:%(posx).1f\tY:%(posy).1f\tZ:%(posz).1f\tYW:%(yaw).0f\tPI:%(pitch).1f\tRL:%(roll).1f'%get_position_struct(mav1))
    elif pub_position_event.trigger(): #30Hz
        if udp_position is None:
            pos=get_position_struct(mav1)
        else:
            pos=udp_position
        #print('%.2f'%(time.time()-start),'X:%(posx).2f\tY:%(posy).2f\tZ:%(posz).2f\tYW:%(yaw).0f\tPI:%(pitch).1f\tRL:%(roll).1f'%pos)
        zmq_socket.send_multipart([topic_postition,pickle.dumps(pos,-1)])
        next(mthread)
    else: 
        #time.sleep(0.01)
        if len(select.select([direct_udp],[],[],0)[0])>0:
            u=list(map(float,direct_udp.recv(1024).split()))
            
            udp_position={'posx':u[0],'posy':u[1],'posz':-u[2],'roll':u[3],'pitch':u[4],'yaw':u[5]}

    
