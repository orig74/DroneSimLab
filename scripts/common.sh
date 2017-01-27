# common functions
function run_inside_script {
tmux send-keys "tmux send-keys \"source /DroneLab/scripts/$1\" ENTER" ENTER
}

function kill_images {
docker ps -a |grep $1 | awk -- '{ print $1 }' | xargs docker rm -f 
}


