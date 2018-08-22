#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import sys,os,time
sys.path.append('unreal_proxy')
import zmq
import struct
import cv2,os
import numpy as np
import config
from subprocess import Popen,PIPE

context = zmq.Context()
zmq_sub = context.socket(zmq.SUB)
addr="tcp://%s:%d" % (config.zmq_pub_unreal_proxy)
zmq_sub.connect(addr)
topicm=config.topic_unreal_drone_rgb_camera%0
topicl=config.topic_unreal_drone_rgb_camera%0+b'l'
topicr=config.topic_unreal_drone_rgb_camera%0+b'r'
print('topicm is',topicm)
zmq_sub.setsockopt(zmq.SUBSCRIBE,topicm)
zmq_sub.setsockopt(zmq.SUBSCRIBE,topicl)
zmq_sub.setsockopt(zmq.SUBSCRIBE,topicr)
#zmq_sub.setsockopt(zmq.SUBSCRIBE,topic+b'down') 
#zmq_sub.setsockopt(zmq.SUBSCRIBE,topic+b'depth') 
cvshow=1
#cvshow=False
gst=1
test=0

#gst-launch-1.0 -e -v udpsrc port=5600 ! application/x-rtp, payload=96 ! rtph264depay ! avdec_h264 ! autovideosink
#gst-launch-1.0 -v videotestsrc ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=127.0.0.1 port=5600
#cmd="gst-launch-1.0 {}! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=127.0.0.1 port=5600"
#cmd="gst-launch-1.0 {}! x264enc tune=zerolatency bitrate=2000 ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host=127.0.0.1 port=5600"
cmd="gst-launch-1.0 {}! x264enc tune=zerolatency  bitrate=2500 ! rtph264pay ! udpsink host=127.0.0.1 port=5600"
#gstsrc = '-v videotestsrc ! video/x-raw,framerate=20/1 '
#gstsrc='-v filesrc location=/dev/stdin ! "video/x-raw,format=RGB8P,width={},height={},framerate=30/1" '.format(1920,1080)

#gstsrc='filesrc location=/dev/stdin ! videoparse width=1920 height=1080 framerate=24/1 format=15 ! videoconvert '

#sx,sy=1920,1080
sx,sy=1280,720
#gstsrc = 'filesrc location=/dev/stdin ! videoparse width={} height={} framerate=30/1 format=15 ! autovideoconvert '.format(sx,sy) #! autovideosink'
gstsrc = 'fdsrc ! videoparse width={} height={} framerate=30/1 format=15 ! videoconvert ! video/x-raw, format=I420'.format(sx,sy) #! autovideosink'

cmd = cmd.format(gstsrc)

if gst:
    p = Popen(cmd, shell=True, bufsize=1024*10,stdin=PIPE, stdout=sys.stdout, close_fds=False)
    stdin=p.stdin

print('start...')
def listener():
    cnt=0
    while 1:
        while len(zmq.select([zmq_sub],[],[],0.001)[0])>0:
            topic, shape, data = zmq_sub.recv_multipart()
            #topic=topic.decode()
            shape=struct.unpack('lll',shape)
            if cvshow:
                img=np.fromstring(data,'uint8').reshape(shape)
                #if 'depth' in topic:
                #    cv2.imshow(topic,img)
                #else:
                #cv2.imshow(topic,cv2.resize(cv2.resize(img,(1920/2,1080/2)),(512,512)))
                img_shrk = img[::2,::2]
                cv2.imshow(topic.decode(),img)
                cv2.waitKey(1)
            if topic==topicm and gst:
                stdin.write(data)
            ### test
        time.sleep(0.010)
        if cnt%20==0:
            print('send...',cnt)
        if test:
            time.sleep(0.020)
            stdin.write(b'23\xff'*(sx*sy))
        cnt+=1


       
if __name__ == '__main__':
    listener()
