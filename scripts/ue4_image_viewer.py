#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
print('running on python3')
import sys,os
sys.path.append(os.environ['CONFIG_PATH'])
import zmq
import struct
import cv2,os
import numpy as np
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
cvshow=True

def listener():
    while 1:
        while len(zmq.select([zmq_sub],[],[],0.001)[0])>0:
            topic, shape, data = zmq_sub.recv_multipart()
            topic=topic.decode()
            shape=struct.unpack('lll',shape)
            img=np.fromstring(data,'uint8').reshape(shape)
            if cvshow:
                if 'depth' in topic:
                    cv2.imshow(topic,img)
                else:
                    cv2.imshow(topic,cv2.resize(cv2.resize(img,(1024,1024)),(512,512)))
                cv2.waitKey(1)
       
if __name__ == '__main__':
    listener()
