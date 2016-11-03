# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import phandlers as ph
import zmq,pickle
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)
zmq_port = "5556"
socket.connect('tcp://127.0.0.1:'+zmq_port)
socket.setsockopt(zmq.SUBSCRIBE,b'position')


def main_loop(gworld):
    drone_actor=ph.FindActorByName(gworld,'Parrot_Drone_6',1)
    if drone_actor is None:
        print('ERROR: could not find drone_actor')
        while 1:
            yield
    drone_start_pos=np.array(ph.GetActorLocation(drone_actor))

    position=None
    while 1:
        print('in main loop')
        
        while len(zmq.select([socket],[],[],0)[0])>0:
            topic, msg = socket.recv_multipart()
            position=pickle.loads(msg)
        if position is not None:
            new_pos=drone_start_pos+np.array([position['posx'],position['posy'],position['posz']])*100 #turn to cm
            ph.SetActorLocation(drone_actor,new_pos)
        yield

def kill():
    print('done!')
