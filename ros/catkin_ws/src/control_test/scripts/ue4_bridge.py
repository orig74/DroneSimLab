#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
print('running on python3')
import rospy,sys
sys.path.append("/home/docker/catkin_ws/devel/lib/python3.4/dist-packages")
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import zmq
import struct
import cv2
import numpy as np

sys.path.append("/DroneLab/demos/px4_gazebo")
import config

context = zmq.Context()
zmq_sub = context.socket(zmq.SUB)
addr="tcp://%s:%d" % (config.zmq_pub_unreal_proxy)
zmq_sub.connect(addr)
topic=(config.topic_unreal_drone_rgb_camera.decode()%0).encode()#had to do encode decode for python version earlier then 3.5
print('topic is',topic)
zmq_sub.setsockopt(zmq.SUBSCRIBE,topic)
zmq_sub.setsockopt(zmq.SUBSCRIBE,topic+b'down') 
zmq_sub.setsockopt(zmq.SUBSCRIBE,topic+b'depth') 
cvshow=False
cvbridge=CvBridge()

def listener():

    rospy.init_node('ue4_bridge', anonymous=True, log_level=rospy.DEBUG)
    rate=rospy.Rate(1000)
    rospy.loginfo('starting...')
    publishers={}
    start=rospy.get_time()
    while not rospy.is_shutdown():
        while len(zmq.select([zmq_sub],[],[],0)[0])>0:
            topic, shape, data = zmq_sub.recv_multipart()
            #rospy.loginfo(rospy.get_caller_id() + ' got topic %s', topic)
            topic=topic.decode()
            if topic not in publishers:
                publishers[topic]=rospy.Publisher(topic,Image,queue_size=2)
            #import pdb;pdb.set_trace()
            shape=struct.unpack('lll',shape)
            img=np.fromstring(data,'uint8').reshape(shape)
            if 'depth' not in topic:
                publishers[topic].publish(cvbridge.cv2_to_imgmsg(img,'bgr8'))
            if cvshow:
                if 'depth' in topic:
                    cv2.imshow(topic,img)
                else:
                    cv2.imshow(topic,cv2.resize(cv2.resize(img,(1024,1024)),(512,512)))
                cv2.waitKey(1)
        rate.sleep()

       
if __name__ == '__main__':
    listener()
