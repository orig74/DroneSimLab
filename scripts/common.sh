# common functions
function run_inside_script {
tmux send-keys "tmux send-keys \"source /DroneLab/scripts/$1\" ENTER" ENTER
}

function kill_images {
docker ps -all |grep $1 | awk -- '{ print $1 }' | xargs docker stop
docker ps -all |grep $1 | awk -- '{ print $1 }' | xargs docker rm 
}


