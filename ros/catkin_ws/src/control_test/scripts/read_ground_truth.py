#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import rospy,sys
from std_msgs.msg import String
sys.path.append("/home/docker/catkin_ws/devel/lib/python2.7/dist-packages")
from mavros_msgs.msg import State,PositionTarget,HilControls
from mavros_msgs.srv import SetMode,CommandBool
from geometry_msgs.msg  import PoseStamped,Point

state=None

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)
    global state 
    state=data
    print state.connected,state.mode

def hil_callback(data):
    print data

def listener():

    rospy.init_node('listener', anonymous=True)
    #rate=rospy.Rate(1)

    rospy.Subscriber('mavros/state', State, callback)
    rospy.Subscriber('mavros/hil_controls/hil_controls', HilControls, hil_callback)
    rospy.spin() 
       
if __name__ == '__main__':
    listener()
