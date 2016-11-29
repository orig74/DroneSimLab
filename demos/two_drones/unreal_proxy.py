# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import phandlers as ph
import zmq,pickle,time,cv2
import numpy as np
import config
import sys,os
sys.path.append(os.path.dirname(__file__)+'/../')
from common import convertions

context = zmq.Context()

show_cv=False
pub_cv=True

socket_sub = context.socket(zmq.SUB)
adr,port=config.zmq_pub_drone_fdm
socket_sub.connect('tcp://%s:%d'%config.zmq_pub_drone_fdm)
socket_sub.setsockopt(zmq.SUBSCRIBE,config.topic_sitl_position_report)

socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://*:%d" % config.zmq_pub_unreal_proxy[1] )


start=time.time()
def main_loop(gworld):
    iter_cnt=0
    print('-- actors --')
    for p in ph.GetActorsNames(gworld):
        print(p)
    print('-- textures --')
    drone_textures=[]
    drone_textures.append(ph.GetTextureByName('/Game/TextureRenderTarget2D'))
    drone_textures.append(ph.GetTextureByName('/Game/TextureRenderTarget2D_2'))
    if not all(drone_textures):
        print("Error, Could not find all textures")
        while 1:
            yield
    drone_actors=[]
    drone_actors.append(ph.FindActorByName(gworld,'Parrot_Drone_6'))
    drone_actors.append(ph.FindActorByName(gworld,'Parrot_Drone2'))
    if not all(drone_actors):
        print("Error, Could not find all drone actors")
        while 1:
            yield
    
    for _ in range(10): #need to send it a few time don't know why.
        socket_pub.send_multipart([config.topic_unreal_state,b'main_loop'])
        yield
    drone_start_positions_unreal=[np.array(ph.GetActorLocation(drone_actor)) for drone_actor in drone_actors]
    drone_start_positions_lon_lat=[None for _ in drone_actors]

    positions_struct=None
    while 1:
        while len(zmq.select([socket_sub],[],[],0)[0])>0: #the wile is to flush all massages
            topic, msg = socket_sub.recv_multipart()
            positions_struct=pickle.loads(msg)
        if positions_struct is not None: #meanning new message
            for drone_index in positions_struct:
                drone_pos=positions_struct[drone_index]
                if drone_start_positions_lon_lat[drone_index] is None:
                    drone_start_positions_lon_lat[drone_index]=drone_pos.copy()
                dx,dy=convertions.latlon_rad_dist_meters(
                        drone_start_positions_lon_lat[drone_index]['lat'],drone_start_positions_lon_lat[drone_index]['lon'],
                        drone_pos['lat'],drone_pos['lon'])
                alt=(drone_pos['alt']-drone_start_positions_lon_lat[drone_index]['alt'])*100 #*100 convert to centimeters
                alt+=drone_start_positions_unreal[drone_index][2]
                dx=dx*100+drone_start_positions_unreal[drone_index][0]
                dy=dy*100+drone_start_positions_unreal[drone_index][1]
                #if iter_cnt==0:
                #    import ipdb;ipdb.set_trace()
                if (iter_cnt%10)==0:
                    print('===>',dx,dy)
                ph.SetActorLocation(drone_actors[drone_index],(dx,dy,alt))
                ph.SetActorRotation(drone_actors[drone_index],(drone_pos['roll'],drone_pos['pitch'],drone_pos['yaw']))
            positions_struct=None
        yield
        for drone_index in range(config.n_drones):
            img=cv2.resize(ph.GetTextureData(drone_textures[drone_index]),(256,256),cv2.INTER_LINEAR)
            if pub_cv:
                socket_pub.send_multipart([config.topic_unreal_drone_rgb_camera%drone_index,pickle.dumps(img,-1)])
            if show_cv:
                cv2.imshow('drone camera %d'%drone_index,img)
                cv2.waitKey(1)
        iter_cnt+=1

def kill():
    print('done!')
    socket_pub.send_multipart([config.topic_unreal_state,b'kill'])
    if show_cv:
        cv2.destroyAllWindows()
        for _ in range(10):
            cv2.waitKey(10)
