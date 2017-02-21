#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import rospy,sys
sys.path.append("/home/docker/catkin_ws/devel/lib/python3.4/dist-packages")
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo


import zmq
import struct
import cv2,os
import numpy as np

sys.path.append(os.environ['UNREAL_PROXY_PATH'])
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
            #rospy.loginfo('topic is..%s',topic)
            if topic not in publishers:
                if 'depth' not in topic:
                    publishers[topic]=rospy.Publisher(topic,Image,queue_size=2)
                else:
                    publishers[topic+'_rgb8']=rospy.Publisher(topic+'_rgb8',Image,queue_size=2)
                    publishers[topic+'_range_mm']=rospy.Publisher(topic+'_range_mm',Image,queue_size=2)
                    publishers[topic+'_cam_info']=rospy.Publisher(topic+'_cam_info',CameraInfo,queue_size=2)

            #import pdb;pdb.set_trace()
            shape=struct.unpack('lll',shape)
            if 'depth' not in topic:
                img=np.fromstring(data,'uint8').reshape(shape)
                publishers[topic].publish(cvbridge.cv2_to_imgmsg(img,'bgr8'))
            else:
                #img is in the format of RGBA A store depth in cm and all in float16 format
                tstamp=rospy.get_rostime() 
                img=np.fromstring(data,'float16').reshape(shape)
                img_max_val = 5.0 #assuming I right
                depth_camera_img_rgb = (img[:,:,[2,1,0]].clip(0,img_max_val)/img_max_val*255).astype('uint8')
                img_rgb=cvbridge.cv2_to_imgmsg(depth_camera_img_rgb,'bgr8')
                img_rgb.header.stamp=tstamp
                publishers[topic+'_rgb8'].publish(img_rgb)

                #conversions to be compatible with intel realsense camera
                depth_err_val=65504
                depth_img_f16=img[:,:,3]
                #max_distance=64#m
                depth_img_f16[depth_img_f16==depth_err_val]=0
                depth_final_mm=(depth_img_f16*10).astype('uint16') #cm to mm
                img_depth=cvbridge.cv2_to_imgmsg(depth_final_mm,'mono16')
                img_depth.header.stamp=tstamp
                publishers[topic+'_range_mm'].publish(img_depth)
                cam_info = CameraInfo()
                cam_info.header.stamp=tstamp
                cam_info.distortion_model='plumb_bob' 
                cam_info.D=[0.0]*6

                cam_info.K=[    160.0,  0.0,    160.0, 
                                0.0,    160.0,  120.0,
                                0.0,    0.0,    1.0]

                cam_info.R=[1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

                cam_info.P=[    160.0,  0.0,    160.0,  0,
                                0.0,    160.0,  120.0,  0,
                                0.0,    0.0,    1.0  ,  0]
                cam_info.header.frame_id='camera_depth_optical_frame'
                cam_info.height = 240
                cam_info.width = 320

                publishers[topic+'_cam_info'].publish(cam_info)



            if cvshow:
                if 'depth' in topic:
                    clip_dist_cm=30*100
                    aaa=img.max()
                    inds2=img==aaa
                    img=img.clip(0,clip_dist_cm)
                    #img=np.fromstring(data,'uint8').reshape(shape)
                    rospy.loginfo('maxmin %f %f'%(img.max(),img.min()))
                    img=img.astype('float')/clip_dist_cm*255
                    img[inds2]=255
                    #import pdb;pdb.set_trace()
                    cv2.imshow(topic,img.astype('uint8'))
                else:
                    cv2.imshow(topic,cv2.resize(cv2.resize(img,(1024,1024)),(512,512)))
                cv2.waitKey(1)
        rate.sleep()


if __name__ == '__main__':
    listener()
