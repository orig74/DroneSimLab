# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from pymavlink import mavutil
import numpy as np
import zmq
import sys
import time
import pickle
import sys
import cv2
import os
import shutil
import hsv_track
import sys
import demo_config
import struct
show_cv=True

sys.path.append(os.environ['UNREAL_PROXY_PATH'])
import config

drone_num=int(os.environ['DRONE_NUM'])
#drone_num=0
print('I am mother ',drone_num)
save_path='/tmp/drone_images'
#save_path=None


if save_path is not None:
    if os.path.isdir(save_path):
        shutil.rmtree(save_path)
    os.mkdir(save_path)

topic_postition=config.topic_sitl_position_report

context = zmq.Context()
socket_sub = context.socket(zmq.SUB)
socket_sub.connect('tcp://%s:%d'%config.zmq_pub_unreal_proxy)

socket_sub.setsockopt(zmq.SUBSCRIBE,config.topic_unreal_state)
socket_sub.setsockopt(zmq.SUBSCRIBE,config.topic_unreal_drone_rgb_camera%drone_num)

mav1 = mavutil.mavlink_connection('udp:127.0.0.1:%d'%(14551+0*10))
print("Waiting for HEARTBEAT")
mav1.wait_heartbeat()
print("Heartbeat from APM (system %u component %u)" % (mav1.target_system, mav1.target_component))


event = mavutil.periodic_event(0.3)
event1hz = mavutil.periodic_event(1)
freq=30
pub_position_event = mavutil.periodic_event(freq)

def set_rcs(rc1, rc2, rc3, rc4):
    global mav1
    values = [ 1500 ] * 8
    values[0] = rc1
    values[1] = rc2
    values[2] = rc3
    values[3] = rc4
    mav1.mav.rc_channels_override_send(mav1.target_system, mav1.target_component, *values)

def get_position_struct(mav):
    if not 'VFR_HUD' in mav1.messages:
        return None
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
    print('---> send disarm')
    mav1.arducopter_disarm()
    yield
    mav1.param_fetch_all()
    yield
    if not mav1.motors_armed():
        yield
        mav1.param_set_send(b'SIM_WIND_SPD',demo_config.wind_speed)
        mav1.param_set_send(b'SIM_WIND_TURB',demo_config.wind_turbulence)
        yield
        set_rcs(1500,1500,1000,1500)
        yield
        print('gps fix',mav1.messages['HOME'].fix_type)
        yield
        print('arming ....')
        mav1.set_mode('LOITER')
        yield
        while not mav1.motors_armed():
            mav1.arducopter_arm()
            yield
    yield
    while mav1.flightmode!='LOITER':
        print('waiting for loiter...',mav1.flightmode)
        mav1.set_mode('LOITER')
        yield
    print('--0--')
    set_rcs(1500,1500,1700,1500)
    while mav1.messages['VFR_HUD'].alt<5:
        yield
    print('--1--')
    set_rcs(1500,1600,1500,1500)
    for i in range(25):
        yield
    print('--2--')
    set_rcs(1500,1400,1500,1500)
    for i in range(25):
        yield
    print('--3-')
    set_rcs(1500,1500,1300,1500)
    yield
    while 1:
        if mav1.motors_armed and mav1.messages['VFR_HUD'].alt<0.5:
            mav1.arducopter_disarm()
        yield


mthread=mission_thread()
start=time.time()


udp_position=None

#############
pcnt=5
def print_cnt(*args,**kargs):
    global pcnt
    if pcnt>=0: 
        print(*args,**kargs)
    pcnt-=1

#################################

unreal_state=None
img_cnt=0
pos=None

while True:
    mav1.recv_msg()
    while(len(zmq.select([socket_sub],[],[],0)[0])>0):
        data= socket_sub.recv_multipart()
        topic=data[0]
        if topic==config.topic_unreal_state:
            #print('got unreal engine state:',msg)
            unreal_state=data[1]
        if topic==(config.topic_unreal_drone_rgb_camera%drone_num):
            #img=pickle.loads(msg)
            shape=struct.unpack('lll',data[1])
            img=np.fromstring(data[2],'uint8').reshape(shape)
            img=cv2.resize(img,(512,512))

            if show_cv:
                cv2.imshow('Drone %d'%drone_num,hsv_track.find_red(img))
                cv2.waitKey(1)
            if save_path is not None:
                cv2.imwrite(save_path+'/img%06d.png'%img_cnt,img)
            img_cnt+=1
    if unreal_state==b'kill':
        mthread=mission_thread()
    #    break
    
    if event.trigger() and pos is not None:
        print('X:%(posx).1f\tY:%(posy).1f\tZ:%(posz).1f\tYW:%(yaw).0f\tPI:%(pitch).1f\tRL:%(roll).1f'%pos)

    if event1hz.trigger():
        if unreal_state==b'main_loop':
            next(mthread) 
            print('mode',mav1.flightmode) 
    elif pub_position_event.trigger(): #30Hz
        if udp_position is None:
            pos=get_position_struct(mav1)
            print_cnt('source form mavlink')
        else:
            pos=udp_position
            print_cnt('source from udp patch')
            #print('%.2f'%(time.time()-start),'X:%(posx).2f\tY:%(posy).2f\tZ:%(posz).2f\tYW:%(yaw).0f\tPI:%(pitch).1f\tRL:%(roll).1f'%pos)
    else: 
        pass
    time.sleep(0.001)
    
