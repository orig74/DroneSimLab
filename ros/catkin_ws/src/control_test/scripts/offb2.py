#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import rospy,sys
from std_msgs.msg import String
sys.path.append("/home/docker/catkin_ws/devel/lib/python2.7/dist-packages")
from mavros_msgs.msg import State,PositionTarget
from mavros_msgs.srv import SetMode,CommandBool
from geometry_msgs.msg  import PoseStamped,Point

state=None

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)
    global state 
    state=data
    #print state.connected,state.mode
def listener():

    rospy.init_node('listener', anonymous=True)
    rate=rospy.Rate(20)

    rospy.Subscriber('mavros/state', State, callback)
    local_pos_pub=rospy.Publisher('mavros/setpoint_position/local',PoseStamped,queue_size=2)
    local_posi_raw_pub=rospy.Publisher('mavros/setpoint_raw/local',PositionTarget,queue_size=2)
    #local_vel_pub=rospy.Publisher('mavros/setpoint_position/local',PoseStamped,queue_size=2)
    set_mode_cmd=rospy.ServiceProxy('mavros/set_mode',SetMode)
    arm_cmd=rospy.ServiceProxy('mavros/cmd/arming',CommandBool)
    newpos=PoseStamped()
    newpos.pose.position.z=4.0#=Point(0,0,2)
    #set_mode_cmd('POSITION CONTROL','')
    #for _ in range(10):
    #    rate.sleep()
    newvel=PositionTarget()
    newvel.velocity.x=1.0
    newvel.type_mask=newvel.FRAME_LOCAL_NED | newvel.IGNORE_AFX | newvel.IGNORE_AFY |newvel.IGNORE_AFZ
    newvel.type_mask=newvel.type_mask | newvel.IGNORE_PX | newvel.IGNORE_PY | newvel.IGNORE_PZ
    for _ in range(100):
        rate.sleep()
        local_pos_pub.publish(newpos);
        
    mymode='OFFBOARD'
    last_req=rospy.get_time()
    start_time=last_req;
    #print '---',rospy.get_time(),start_time
    while rospy.get_time()-start_time<50:
        if rospy.get_time()-last_req>5:
            if state.mode != mymode:
                set_mode_cmd(0,mymode) 
                rospy.loginfo('setting mode...')
            elif not state.armed:
                arm_cmd(True)
                rospy.loginfo('arming...')
            last_req=rospy.get_time()
        dt=rospy.get_time()-start_time
        if dt<20:
            local_pos_pub.publish(newpos);
        elif 20<dt<30 :
            local_posi_raw_pub.publish(newvel); 
        elif 30<dt<40 :
            newvel.velocity.x=-1.0
            local_posi_raw_pub.publish(newvel); 
        else:
            newpos.pose.position.z=0
            local_pos_pub.publish(newpos);
        rate.sleep()
       
if __name__ == '__main__':
    listener()
