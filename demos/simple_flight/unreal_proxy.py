# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import phandlers as ph
import zmq,pickle,time,cv2
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)
zmq_port = "5556"
socket.connect('tcp://127.0.0.1:'+zmq_port)
socket.setsockopt(zmq.SUBSCRIBE,b'position')
start=time.time()

def main_loop(gworld):
    drone_actor=ph.FindActorByName(gworld,'Parrot_Drone_6',1)
    if drone_actor is None:
        print('ERROR: could not find drone_actor')
        while 1:
            yield
    
    drone_start_pos=np.array(ph.GetActorLocation(drone_actor))
    position=None
    while 1:
        while len(zmq.select([socket],[],[],0)[0])>0:
            topic, msg = socket.recv_multipart()
            position=pickle.loads(msg)
        if position is not None:
            new_pos=drone_start_pos+np.array([position['posx'],position['posy'],position['posz']])*100 #turn to cm
            #print('-->',time.time()-start,new_pos)
            ph.SetActorLocation(drone_actor,new_pos)
            ph.SetActorRotation(drone_actor,(np.radians(position['roll']),np.radians(position['pitch']),np.radians(position['yaw'])))
            position=None
        yield
        img1=cv2.resize(ph.GetTextureImg(),(512,512),cv2.INTER_LINEAR)
        cv2.imshow('camera 1',img1)
        cv2.waitKey(1)

def kill():
    print('done!')
    cv2.destroyAllWindows()
    for _ in range(10):
        cv2.waitKey(10)
