# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from std_msgs.msg import Float64MultiArray
import termios, fcntl, sys, os
import rospy
sys.path.append('./unreal_proxy')
import config
import zmq,pickle

fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)


context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%d" % config.zmq_remote_thrasters[1])

pub = rospy.Publisher('/thrusters', Float64MultiArray)

rospy.init_node('keyboard_control')
factor=40
try:
    thrusters=[0,0,0,0]
    while not rospy.is_shutdown():
        while len(zmq.select([socket],[],[],0)[0])>0:
            msg=socket.recv()
            thrusters=[i*factor for i in pickle.loads(msg)]
            if len(thrusters)<4:
                thrusters.append(thrusters[-1])
            #revers thruster 3&4
            thrusters[3]=-thrusters[3]
            thrusters[2]=-thrusters[2]
            print('thruster',thrusters)    
        msg = Float64MultiArray()
        try:
            c = sys.stdin.read(1)
            if c=='1': #forward
                thrusters[0]=thrusters[1]=0.3*factor
            if c=='q': #back
                thrusters[0]=thrusters[1]=-0.3*factor
            if c=='a': #up
                thrusters[2]=thrusters[3]=0.3*factor
            if c=='z': #down
                thrusters[2]=thrusters[3]=-0.3*factor
            if c=='x': #yaw left
                thrusters[0]=-0.3*factor
                thrusters[1]=0.3*factor
            if c=='c': #yaw right
                thrusters[0]=0.3*factor
                thrusters[1]=-0.3*factor
            if c=='v': #idle
                thrusters=[0,0,0,0]
            if c!='':
                print('%c'%c)
        except IOError:
            pass

        msg.data = thrusters
        pub.publish(msg)
        rospy.sleep(0.05)
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)




