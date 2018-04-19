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
                            1.0 * 3,  # m_b [kg]
                            0.001 * 3  ,  # v_b [M^3]
                            5.9,  # mu
                            0.2,  # mu_r
                            9.8,  # g MKS
                            0.5,  # Ixx [kg*m^2]
                            0.5,  # Iyy [kg*m^2]
                            0.5,  # Izz [kg*m^2]
                               ]
                            ) 

thruster_filt_coef=0.2


def test_dynamics():
    x0 = np.zeros(12)
    numerical_specified=[0.8,0.5,0,0]
    print(right_hand_side(x0, 0.0, numerical_specified, numerical_constants))


if 0 and  __name__=='__main__':
    test_dynamics()


def updateThrusters(data):
    global thrusters
    thrusters=data.data 

def pub_position_struct(xx,pub_pos,cnt):
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
    thrusters=[0,0,0,0] ### can be also only 3 thrusters depending on type of ROV
    thrusters_filt=np.array(thrusters)
    rospy.Subscriber('/thrusters',Float64MultiArray, updateThrusters)
    pub_pose= rospy.Publisher('open_rov', Pose)
    cnt=0
    while not rospy.is_shutdown():
        #now=rospy.Time.now()
        thrusters_filt = thrusters_filt*(1-thruster_filt_coef) + thruster_filt_coef*np.array(thrusters)
        sim_time=cnt*1.0/fps
        x_dot=right_hand_side(xx, sim_time, thrusters_filt, numerical_constants)
        xx=xx+x_dot*1.0/fps
        pub_position_struct(xx,pub_pose,cnt)
        r.sleep()
        cnt+=1


