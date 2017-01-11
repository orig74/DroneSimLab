# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import phandlers as ph
import zmq,pickle,time,cv2
import numpy as np
import config

context = zmq.Context()
socket_sub = context.socket(zmq.SUB)
socket_sub.connect('tcp://%s:%d'%config.zmq_pub_drone_main)
socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://*:%d" % config.zmq_pub_unreal_proxy[1] )

socket_sub.setsockopt(zmq.SUBSCRIBE,config.topic_sitl_position_report)

start=time.time()

def main_loop(gworld):
    drone_actor=ph.FindActorByName(gworld,'Parrot_Drone_6',1)
    #drone_camera_actor=ph.FindActorByName(gworld,'SceneCapture2Ddrone',1)
    if drone_actor is None:# or drone_camera_actor is None:
        print('ERROR: could not find drone_actor')
        while 1:
            yield
    for _ in range(10): #need to send it a few time don't know why.
        socket_pub.send_multipart([config.topic_unreal_state,b'main_loop'])
        yield
    drone_start_pos=np.array(ph.GetActorLocation(drone_actor))
    position=None
    while 1:
        while len(zmq.select([socket_sub],[],[],0)[0])>0:
            topic, msg = socket_sub.recv_multipart()
            position=pickle.loads(msg)
        if position is not None:
            new_pos=drone_start_pos+np.array([position['posx'],position['posy'],position['posz']])*100 #turn to cm
            ph.SetActorLocation(drone_actor,new_pos)
            ph.SetActorRotation(drone_actor,(position['roll'],position['pitch'],position['yaw']))
            #incase of gimabl
            #ph.SetActorRotation(drone_camera_actor,(-position['roll'],-position['pitch'],-position['yaw']))
            position=None
        yield
        img1=cv2.resize(ph.GetTextureImg(),(512,512),cv2.INTER_LINEAR)
        cv2.imshow('camera 1',img1)
        cv2.waitKey(1)

def kill():
    print('done!')
    socket_pub.send_multipart([config.topic_unreal_state,b'kill'])
    cv2.destroyAllWindows()
    for _ in range(10):
        cv2.waitKey(10)
