#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import os,sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--skip_ue4_editor", help="skip install and build unreal engine editor",default=False,action='store_true')
args = parser.parse_args()

print('skip unreal engine option =',args.skip_ue4_editor)
###params 
req_docker_images=['ros_image_indigo','ros_image_kinetic','python3_dev','sitl_image']
if not args.skip_ue4_editor:
    req_docker_images.append('unreal_engine_4')


## TODO: check prerequisits
# tmux docker nvidia 

#git update sub modules

games_path='https://studweb.cosc.canterbury.ac.nz/~oga13/ue4_games/'
games_names=['game_demo']

def run_shell(cmd,failmsg):
    ret=os.system(cmd)
    if ret!=0:
        print('Error: ',failmsg)
        sys.exit(-1)

print("update submodules...")

submodules=map(lambda x:x.split('=')[1].strip(),os.popen('grep path .gitmodules').readlines())
for submodule in submodules:
    if args.skip_ue4_editor and 'UnrealEngine' in submodule:
        continue
    print('updating submodule:', submodule)
    run_shell("git submodule update --init --recursive "+submodule,
        'failed updataing submodules.. please check you connection')
    


print("downloading baked games...")

for game_name in games_names:
    md5=os.popen('curl '+games_path+game_name+'.md5').read().split()[0]
    assert(len(md5)==32)
    game_local_dir='baked_games/'+game_name
    if not os.path.isdir(game_local_dir):
        os.makedirs(game_local_dir)
    if not os.path.isfile(game_local_dir+'/done'):
        cmd="curl -o "+game_local_dir+'/'+game_name+'.tgz '+games_path+'/'+game_name+'.tgz'
        print('Downloading command:',cmd) 
        run_shell(cmd,'Failed downloading game '+game_name)
        run_shell("cd "+game_local_dir+" && tar xzf "+game_name+'.tgz','fail extracting game')
        run_shell("rm "+game_local_dir+'/'+game_name+'.tgz','fail rm')
        open(game_local_dir+'/done','w')

print("building docker images...")

run_shell("docker images > /dev/null",'Fail running docker images, do you have the right previlages?'
        '\ntry running:\ndocker images') 
current_docker_images=map(lambda x:x.strip(),os.popen('docker images |cut -d" " -f 1').readlines())

if 'unreal_engine_4' in req_docker_images:
    run_shell("cd dockers/unreal_engine_4 && ./prep_unreal",'Error: faild to prepare unreal for installation')
    

for docker_image in req_docker_images:
    if docker_image not in current_docker_images:
        print('building image ',docker_image)
        run_shell('cd dockers/'+docker_image+' && ../build > /tmp/dbuild.log 2>&1',
            'Error: failed bulding docker image '+docker_image+' please look at the log file /tmp/dbuild.log')

print("install ros...")
#if not os.path.isdir('ros/catkin_mavros'):
#    os.mkdir('ros/catkin_mavros')
run_shell('''cd dockers/ros_image_kinetic && ./run_image.sh '-c "/DroneLab/scripts/make_catkin.sh"' ''',
        'Error: faild installing ros')

print("done!")
