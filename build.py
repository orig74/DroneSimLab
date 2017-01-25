#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import os

###params 



## TODO: check prerequisits
# tmux docker nvidia 

#git update sub modules

games_path='https://studweb.cosc.canterbury.ac.nz/~oga13/ue4_games/'
games_names=['game_demo']

print("update submodules...")

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

assert(os.system("docker images > /dev/null")==0)) #just to see if have the right preveliges
current_docker_images=map(lambda x:x.strip(),os.popen('docker images |cut -d" " -f 1').readlines())

#os.system('curl -o baked_games/game_demo.md5 '+games_path+game_demo.md5)

## TODO: check if game_demo.tgz exists and if md5 sum ok other wize download
#os.system('curl -o baked_games/game_demo.md5 '+games_path+game_demo.md5)
## TODO: check md5sum again

## TODO: build docker images if neccessy


