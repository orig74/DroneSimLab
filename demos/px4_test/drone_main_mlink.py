# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from pymavlink import mavutil
import numpy as np
import zmq
import sys
import time
import pickle
import zmq,sys,os
import config

topic_postition=config.topic_sitl_position_report


context = zmq.Context()
socket_pub = context.socket(zmq.PUB)

socket_pub.bind("tcp://*:%d" % config.zmq_pub_drone_main[1] )

mav1 = mavutil.mavlink_connection('udp:127.0.0.1:14550')

print("Waiting for HEARTBEAT")
mav1.wait_heartbeat()
print("Heartbeat from APM (system %u component %u)" % (mav1.target_system, mav1.target_system))
print("vtype=",mav1.field('HEARTBEAT', 'autopilot', None)==mavutil.mavlink.MAV_AUTOPILOT_PX4)


event = mavutil.periodic_event(0.3)
freq=30
pub_position_event = mavutil.periodic_event(freq)


def get_position_struct(mav):
    d={}
    d['posz']=-mav.messages['LOCAL_POSITION_NED'].z
    d['posx']=mav.messages['LOCAL_POSITION_NED'].x
    d['posy']=mav.messages['LOCAL_POSITION_NED'].y
    d['yaw']=0#np.degrees(sm.yaw) #todo...
    d['roll']=0#np.degrees(sm.roll)
    d['pitch']=0#np.degrees(sm.pitch)
    return d

def mission_thread():
    mav1.param_fetch_all()
    yield
    mav1.arducopter_arm()
    yield
    mav1.mav.command_long_send(mav1.target_system, mav1.target_component,
                                   mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0,
                                   0, 0,1, 0, 47.3977419, 8.5455939, 500)
    yield
    values = [ 50 ] * 8
    #values[1]=1700
    mav1.mav.rc_channels_override_send(mav1.target_system, mav1.target_component, *values)
    yield
    for _ in range(5):
        yield
    print('-------- set mode')
    mav1.set_mode('POSCTL')
    for _ in range(5):
        yield
    #mav1.set_mode('POSCTL')

    mav1.mav.command_long_send(mav1.target_system, mav1.target_component,
                                   mavutil.mavlink.MAV_CMD_NAV_LAND, 0,
                                   0, 0, 0, 0, 47.3977419, 8.5455939, 0)
    while 1:
        yield
 

mthread=mission_thread()
start=time.time()

##############################################
pcnt=5
def print_cnt(*args,**kargs):
    global pcnt
    if pcnt>=0: 
        print(*args,**kargs)
    pcnt-=1

unreal_state=None
evt_cnt=0
while True:
    mav1.recv_msg()
    if 'VFR_HUD' in mav1.messages:
        if event.trigger():
            #print(mav1.messages['VFR_HUD'].alt)
            #print(mav1.messages.keys())
            #print(mav1.messages['GLOBAL_POSITION_INT'])
            #print(mav1.messages['LOCAL_POSITION_NED'])
            #print(mav1.messages['SIMSTATE'])
            print('X:%(posx).1f\tY:%(posy).1f\tZ:%(posz).1f\tYW:%(yaw).0f\tPI:%(pitch).1f\tRL:%(roll).1f'%pos)
            #print('Z:%(posz).1f'%pos)
            #print(mav1.messages['VFR_HUD'])
            next(mthread)
            #if evt_cnt==2:
            #    import ipdb;ipdb.set_trace()
            #evt_cnt+=1

        elif pub_position_event.trigger(): #30Hz
            pos=get_position_struct(mav1)
            socket_pub.send_multipart([topic_postition,pickle.dumps(pos,-1)])
            print_cnt('source form mavlink')
    time.sleep(0.001)
    
