# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import zmq,pickle,time,os
import struct
import config
from Wrappers import phandlers as ph
import numpy as np
import cv2

#needed texture objects in the unreal project
#drone_texture_names=['/Game/TextureRenderTarget2D_0']
drone_texture_names=['/Game/bluerov_main','/Game/bluerovstereo1','/Game/bluerovstereo2' ]

#drone_textures_depth_names=['/Game/TextureRenderTarget2D_depth']
drone_textures_depth_names=[]
#needed actors
#drone_actors_names=['g500_robot']
drone_actors_names=['BlueRov1']


context = zmq.Context()

show_cv=False
pub_cv=True

drone_subs=[]

if 'CAMERA_RIG_PITCH' in os.environ and os.environ['CAMERA_RIG_PITCH']:
    pitch=float(os.environ['CAMERA_RIG_PITCH'])
else:
    pitch=0


############### need to be updated for mu;tiple drones
socket_sub = context.socket(zmq.SUB)
drone_ip,port=config.zmq_pub_drone_fdm
#drone_ip='172.17.0.%d'%(ind+2) #172.17.0.1 for the docker host and 172.17.0.2 for first drone etc...
addr='tcp://%s:%d'%(drone_ip,port)
print("connecting to",addr)
socket_sub.connect(addr)
socket_sub.setsockopt(zmq.SUBSCRIBE,config.topic_sitl_position_report)
drone_subs.append(socket_sub)

socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://%s:%d" % config.zmq_pub_unreal_proxy )


start=time.time()


def main_loop(gworld):
    frame_cnt = 0
    print('-- actors list --',gworld)
    for p in ph.GetActorsNames(gworld,1024*1000):
        print(p)
    print('-- textures --')
    print('-- starting openrov simulation --')
    drone_textures=[]
    for tn in drone_texture_names:
        drone_textures.append(ph.GetTextureByName(tn))
    drone_textures_depth=[]
    for tn in drone_textures_depth_names:
        drone_textures_depth.append(ph.GetTextureByName(tn))

    if not all(drone_textures):
        print("Error, Could not find all textures")
        while 1:
            yield
    drone_actors=[]
    for drn in drone_actors_names:
        drone_actors.append(ph.FindActorByName(gworld,drn))

    if not all(drone_actors):
        print("Error, Could not find all drone actors")
        while 1:
            yield
    
    #change cameras angle
    for cam_name in ['SceneCaptureBROV1left','SceneCaptureBROV1right']: 
        #ca=ph.FindActorByName(gworld,'SceneCaptureBROV1left')
        ca=ph.FindActorByName(gworld,cam_name)
        #ph.SetActorRotation(ca,(1,-1,1)) #left
        #ph.SetActorRotation(ca,(1,-1,89)) #forward
        #ph.SetActorRotation(ca,(1,-89,89)) #down (pitch -90)
        #pitch range >=1  <=89
        #pitch=45
        #pitch=1
        ph.SetActorRotation(ca,(1,-pitch,89))

        yield
        #ph.SetActorRotation(caml,(1,1,89)) #facing down
        print('camera ' +cam_name + ' rotation ---',ph.GetActorRotation(ca))

    #print('--- ',caml)



    for _ in range(10): #need to send it a few time don't know why.
        print('sending state main loop')
        socket_pub.send_multipart([config.topic_unreal_state,b'main_loop'])
        yield
    drone_start_positions=[np.array(ph.GetActorLocation(drone_actor)) for drone_actor in drone_actors]
    positions=[None for _ in range(config.n_drones)]
    while 1:
        for drone_index in range(config.n_drones):
            socket_sub=drone_subs[drone_index]
            drone_actor=drone_actors[drone_index]
            while len(zmq.select([socket_sub],[],[],0)[0])>0:
                topic, msg = socket_sub.recv_multipart()
                positions[drone_index]=pickle.loads(msg)
                #print('-----',positions[drone_index])

            position=positions[drone_index]
            if position is not None:
                new_pos=drone_start_positions[drone_index]+np.array([position['posx'],position['posy'],position['posz']])*100 #turn to cm
                #print('-----',drone_index,position)
                ph.SetActorLocation(drone_actor,new_pos)
                ph.SetActorRotation(drone_actor,(position['roll'],position['pitch'],position['yaw']))
                positions[drone_index]=None
        yield
        #for drone_index in range(config.n_drones):
            #img=cv2.resize(ph.GetTextureData(drone_textures[drone_index]),(1024,1024),cv2.INTER_LINEAR)
        topics=[]
        imgs=[]

        img=ph.GetTextureData(drone_textures[0])
        imgr=ph.GetTextureData(drone_textures[1])
        imgl=ph.GetTextureData(drone_textures[2])
        topics.append(config.topic_unreal_drone_rgb_camera%0)
        topics.append(config.topic_unreal_drone_rgb_camera%0+b'l')
        topics.append(config.topic_unreal_drone_rgb_camera%0+b'r')
        imgs=[img,imgl,imgr]
        

        #if drone_index<len(drone_textures_depth):
        #    img_depth=ph.GetTextureData16f(drone_textures_depth[drone_index],channels=[0,1,2,3]) #depth data will be in A componnent
            #img_depth=ph.GetTextureData(drone_textures_depth[drone_index],channels=[2]) #depth data will be in red componnent
        #    topics.append(config.topic_unreal_drone_rgb_camera%drone_index+b'depth')
        #    imgs.append(img_depth)

        if pub_cv:
            for topic,img in zip(topics,imgs):
                #socket_pub.send_multipart([topic,pickle.dumps(img,2)])
                #print('--->',img[:].max(),img[:].min())
                #rgb=img[...,::-1]
                socket_pub.send_multipart([topic,struct.pack('llll',*img.shape,frame_cnt),img.tostring()])
                #socket_pub.send_multipart([topic,pickle.dumps(img,-1)])

        if show_cv:
            cv2.imshow('drone camera %d'%drone_index,img)
            cv2.waitKey(1)

        frame_cnt += 1

def kill():
    print('done!')
    socket_pub.send_multipart([config.topic_unreal_state,b'kill'])
    if show_cv:
        cv2.destroyAllWindows()
        for _ in range(10):
            cv2.waitKey(10)



if __name__=="__main__":
    while 1:
        for drone_index in range(config.n_drones):
            socket_sub=drone_subs[drone_index]
            while len(zmq.select([socket_sub],[],[],0)[0])>0:
                topic, msg = socket_sub.recv_multipart()
                print("got ",topic)
