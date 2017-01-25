#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import os

## TODO: check prerequisits
# tmux docker nvidia

games_path='https://studweb.cosc.canterbury.ac.nz/~oga13/ue4_games/'
os.system('curl -o baked_games/game_demo.md5 '+games_path+game_demo.md5)

## TODO: check if game_demo.tgz exists and if md5 sum ok other wize download
os.system('curl -o baked_games/game_demo.md5 '+games_path+game_demo.md5)
## TODO: check md5sum again

## TODO: build docker images if neccessy


