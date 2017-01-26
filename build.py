#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import os,sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--skip_ue4_editor", help="skip install and build unreal engine editor",default=False,action='store_true')
args = parser.parse_args()

print('skip unreal engine option =',args.skip_ue4_editor)
###params 
req_docker_images=['ros_image_indigo','python3_dev','sitl_image']
if not args.skip_ue4_editor:
    req_docker_images.append('unreal_engine_4')


## TODO: check prerequisits
# tmux docker nvidia 

#git update sub modules

games_path='https://studweb.cosc.canterbury.ac.nz/~oga13/ue4_games/'
games_names=['game_demo']

print("update submodules...")

submodules=map(lambda x:x.split('=')[1].strip(),os.popen('grep path .gitmodules').readlines())
for submodule in submodules:
    if args.skip_ue4_editor and 'UnrealEngine' in submodule:
        continue
    print('updating submodule:', submodule)
    assert(os.system("git submodule update --init --recursive "+submodule)==0)

print("downloading baked games...")

for game_name in games_names:
    md5=os.popen('curl '+games_path+'game_demo.md5').read().split()[0]
    assert(len(md5)==32)
    game_local_dir='baked_games/'+game_name
    if not os.path.isdir(game_local_dir):
        os.makedirs(game_local_dir)
    if not os.path.isfile(game_local_dir+'/done'):
        cmd="curl -o "+game_local_dir+'/'+game_name+'.tgz '+games_path+'/'+game_name+'.tgz'
        print('Downloading command:',cmd) 
        assert(os.system(cmd)==0)
        assert(os.system("cd "+game_local_dir+" && tar xzf "+game_name+'.tgz')==0)
        assert(os.system("rm "+game_local_dir+'/'+game_name+'.tgz')==0)
        open(game_local_dir+'/done','w')

print("building docker images...")

assert(os.system("docker images > /dev/null")==0) #just to see if have the right preveliges
current_docker_images=map(lambda x:x.strip(),os.popen('docker images |cut -d" " -f 1').readlines())

for docker_image in req_docker_images:
    if docker_image not in current_docker_images:
        print('building image ',docker_image)
        assert(os.system('cd dockers/'+docker_image+' && ./build')==0) 

print("done!")
