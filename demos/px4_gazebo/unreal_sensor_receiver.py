# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import config
import pickle
import zmq
import sys
import asyncio
import cv2,time
import numpy as np

context = zmq.Context()
socket_sub = context.socket(zmq.SUB)
addr="tcp://%s:%d" % (config.zmq_pub_unreal_proxy)
socket_sub.connect(addr)
topic=(config.topic_unreal_drone_rgb_camera.decode()%0).encode()#had to do encode decode for python version earlier then 3.5
print('topic is',topic)
socket_sub.setsockopt(zmq.SUBSCRIBE,topic)
socket_sub.setsockopt(zmq.SUBSCRIBE,topic+b'down') 
socket_sub.setsockopt(zmq.SUBSCRIBE,topic+b'depth') 

msg=None
def reader():
    global msg
    topic, msg = socket_sub.recv_multipart()
    print(time.time(),"got topic",topic)
    

@asyncio.coroutine
def image_viewer():
    global msg
    while 1:
        yield from asyncio.sleep(1/100.0) #sleep 10 mili
        #yield 
        if msg is not None:
            img=pickle.loads(msg)
            print(time.time(),img.shape)
            #cv2.imshow('drone camer rgb',img)
            #cv2.waitKey(1)
            msg=None


#direct approch works well
if 1 and __name__=="__main__":
    while 1:
        while len(zmq.select([socket_sub],[],[],0)[0])>0:
            topic, msg = socket_sub.recv_multipart()
            topic=topic.decode()
            img=pickle.loads(msg)
            if 'depth' in topic:
                cv2.imshow(topic,img)
            else:
                cv2.imshow(topic,cv2.resize(cv2.resize(img,(1024,1024)),(512,512)))
            cv2.waitKey(1)
        time.sleep(0.001)


i#print(time.time(),"got ",topic)

#not working well need debug
if 0 and __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.add_reader(socket_sub.fd,reader) 
    tasks=[image_viewer()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
