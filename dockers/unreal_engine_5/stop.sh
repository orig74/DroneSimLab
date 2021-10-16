#!/bin/bash
docker rm `docker ps -a |grep unreal_en | awk '{ printf $1 }'`
