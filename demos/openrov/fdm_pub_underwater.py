# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import socket
import pickle
import zmq
import sys
import numpy as np
import argparse,imp
import rospy
import tf
from geometry_msgs.msg import Pose

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

def callback(data):
    #print('got',data.position)
    ps=position_struct
    ps['posx'],ps['posy'],ps['posz']=data.position.x,data.position.y,data.position.z
    quaternion = (
	data.orientation.x,
	data.orientation.y,
	data.orientation.z,
	data.orientation.w)
    #ps['posz']=-ps['posz']
    euler = tf.transformations.euler_from_quaternion(quaternion,'szxy')
    #roll = euler[0]/np.pi*180-90
    #pitch = euler[1]/np.pi*180
    pitch = euler[1]/np.pi*180
    roll = euler[0]/np.pi*180
    yaw = euler[2]/np.pi*180

    ps['roll'],ps['pitch'],ps['yaw']=roll,pitch,yaw
    
    #ps['roll']+=90 #for g500

def printer():
    print('-->',position_struct)

def pub_position_struct():
    if len(position_struct)>0:
        #print('---------------',position_struct)
        socket_pub.send_multipart([config.topic_sitl_position_report,pickle.dumps(position_struct,-1)])



if __name__=="__main__":
    rospy.init_node('fdm_pub')
    r = rospy.Rate(30)
    rospy.Subscriber("/open_rov", Pose, callback)
    cnt=0
    while not rospy.is_shutdown():
        if cnt%15==0:
            printer()
        pub_position_struct()
        r.sleep()
        cnt+=1
    
