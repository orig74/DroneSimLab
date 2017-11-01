#!/usr/bin/env python

from std_msgs.msg import Float64MultiArray 
import sys, os
import rospy

#import services
from std_srvs.srv import Empty

#if len(sys.argv) != 4: 
#	sys.exit("Usage: "+sys.argv[0]+" <thrusters_topic>")
 

thrusters_topic='/g500/thrusters_input'

pub = rospy.Publisher(thrusters_topic, Float64MultiArray)
rospy.init_node('manuver')
rospy.wait_for_service('/dynamics/reset')
reset=rospy.ServiceProxy('/dynamics/reset', Empty)
r=rospy.Rate(0.5)

cnt=0
def cycle():
    return int(cnt%40/10)

while not rospy.is_shutdown():
    thrusters=[0,0,0,0,0]
    msg = Float64MultiArray()
    if cycle()==0:            
        thrusters[2]=thrusters[3]=+0.2
    if cycle()==1:
        thrusters[2]=thrusters[3]=-0.2
    if cycle()==2:
        thrusters[0]=-0.4
        thrusters[1]=0.4
    if cycle()==3:
        thrusters[0]=0.4
        thrusters[1]=-0.4
    msg.data = thrusters
    pub.publish(msg)
    r.sleep()
    cnt+=1
