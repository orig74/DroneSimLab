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
    #local_pos_pub=rospy.Publisher('mavros/setpoint_position/local',PoseStamped,queue_size=2)
    local_posi_raw_pub=rospy.Publisher('mavros/setpoint_raw/local',PositionTarget,queue_size=2)
    #local_vel_pub=rospy.Publisher('mavros/setpoint_position/local',PoseStamped,queue_size=2)
    set_mode_cmd=rospy.ServiceProxy('mavros/set_mode',SetMode)
    arm_cmd=rospy.ServiceProxy('mavros/cmd/arming',CommandBool)
    
    newpos = PositionTarget()
    newpos.position.z=5
    newpos.velocity.x=0
    newpos.velocity.y=0
    newpos.velocity.z=0


    #set_mode_cmd('POSITION CONTROL','')
    for _ in range(10):
        rate.sleep()
    service_timeout = 30
    rospy.wait_for_service('mavros/cmd/arming', service_timeout)
    rospy.wait_for_service('mavros/set_mode', service_timeout)
    for _ in range(100):
        rate.sleep()
        local_posi_raw_pub.publish(newpos)
        
    mymode='OFFBOARD'
    last_req=rospy.get_time()
    start_time=last_req
    #print '---',rospy.get_time(),start_time
    cnt=0
    while rospy.get_time()-start_time<70:
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
            local_posi_raw_pub.publish(newpos)
        else:
            newpos.position.z=0
            local_posi_raw_pub.publish(newpos)
        rate.sleep()
        if cnt%50==0:
            print('state',state)
        cnt+=1
       
if __name__ == '__main__':
    listener()
