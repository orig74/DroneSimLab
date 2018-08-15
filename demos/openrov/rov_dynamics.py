# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from pydy.codegen.ode_function_generators import generate_ode_function
from sympy import *
import numpy as np
import rospy
import tf 

from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Quaternion


#loading dynamics
(forcing_vector,\
        coordinates,
        mass_matrix,
        speeds,
        constants,
        specified)=eval(open('notebooks/forcing_vector.srepr','rb').read())

right_hand_side = generate_ode_function(forcing_vector, coordinates,
                                        speeds, constants,
                                        mass_matrix=mass_matrix,
                                        specifieds=specified)

#MKS units
#constants = [Wx,Wh,T1,T2,Bh,Bw,m_b,v_b,mu,g]+I
#parag rov
#numerical_constants = np.array([
#                            0.03,  # T1 [m]
#                            0.03,  # T2 [m]
#                            0.1,  # T3 [m]
#                            0.15,  # T4 [m]
#                            0.03,  # T5 [m]
#                            0.03,  # T6 [m]
#                            0.08,  # Bh [m]
#                            0.01,  # Bw [m]
#                            1.0,  # m_b [kg]
#                            0.001 ,  # v_b [M^3]
#                            0.3,  # mu
#                            0.2,  # mu_r
#                            9.8,  # g MKS
#                            0.5,  # Ixx [kg*m^2]
#                            0.5,  # Iyy [kg*m^2]
#                            0.5,  # Izz [kg*m^2]
#                               ]
#) 

#openrov
numerical_constants = np.array([ #openrov
                            0.1,  # Wx [m]
                            0.15,  # Wh [m]
                            0.1,  # T1 [m]
                            0.05,  # T2 [m]
                            0.08,  # Bh [m]
                            0.01,  # Bw [m]
                            2.65,  # m_b [kg]
                            0.001 * 2.66  ,  # v_b [M^3] slightly more boyent then havy
                            5.9,  # mu
                            0.2,  # mu_r
                            9.8,  # g MKS
                            0.5,  # Ixx [kg*m^2]
                            0.5,  # Iyy [kg*m^2]
                            0.5,  # Izz [kg*m^2]
                               ]
                            ) 

thruster_filt_coef=0.2
thruster_control_to_force_ratio=0.3

def test_dynamics():
    x0 = np.zeros(12)
    numerical_specified=[0.8,0.5,0,0]
    print(right_hand_side(x0, 0.0, numerical_specified, numerical_constants))


if 0 and  __name__=='__main__':
    test_dynamics()


def updateThrusters(data):
    global thrusters
    thrusters=data.data 

def pub_position_struct(xx,pub_pose,cnt):
    pose = Pose()
    pose.position.x,pose.position.y,pose.position.z=xx[:3]

    
    orientation = tf.transformations.quaternion_from_euler(xx[3], xx[4], xx[5], 'szxy')
    pose.orientation.x = orientation[0]
    pose.orientation.y = orientation[1]
    pose.orientation.z = orientation[2]
    pose.orientation.w = orientation[3]

    # Broadcast transform
    #br = tf.TransformBroadcaster()
    #br.sendTransform(xx[:3], orientation, rospy.Time.now(), "parag_rov", "world")
    pub_pose.publish(pose)

if 1 and  __name__=='__main__':
    rospy.init_node("rov_dynamics")
    fps=30
    r = rospy.Rate(fps)
    xx = np.zeros(12)
    #thrusters=[0,0,0,0] ### can be also only 3 thrusters depending on type of ROV
    thrusters = None
    thrusters_filt=np.zeros(4)
    rospy.Subscriber('/thrusters',Float64MultiArray, updateThrusters)
    pub_pose= rospy.Publisher('open_rov', Pose)
    cnt=0
    while not rospy.is_shutdown():
        #now=rospy.Time.now()
        if thrusters is not None: #whait for input to start the simulation
            thrusters_force=thruster_control_to_force_ratio*np.array(thrusters)
            thrusters_filt = thrusters_filt*(1-thruster_filt_coef) + thruster_filt_coef*thrusters_force
            sim_time=cnt*1.0/fps
            x_dot=right_hand_side(xx, sim_time, thrusters_filt, numerical_constants)
            xx=xx+x_dot*1.0/fps
            pub_position_struct(xx,pub_pose,cnt)
        if cnt%30==0:
            print('---',cnt,':',xx)
        r.sleep()
        cnt+=1

if 0 and __name__=='__main__':
    rospy.init_node("rov_dynamics")
    refpoint = [  8.11856463e-01,   2.01675307e+00,  -2.22135131e+00,
            -3.65542704e-04,  -1.21102869e-01,   8.05301680e+00,
            -5.49220666e-05,   1.20856560e-04,   1.28878739e-01,
            -2.37508712e-03,   1.11925048e-02,   4.66256052e-06]

    refpoint[0]-=2
    refpoint[2]-=1
    fps=30
    r = rospy.Rate(fps)
    pub_pose= rospy.Publisher('open_rov', Pose)
    cnt=0

    while not rospy.is_shutdown():
        pub_position_struct(refpoint,pub_pose,cnt)
        
        cnt+=1
        r.sleep()
