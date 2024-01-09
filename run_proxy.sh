#!/bin/bash
#run_proxy.sh $num_containers simTime trace1 trace2 trace3 ... 
argc=$#
argv=("$@")
#Create proxy container
sudo docker run --name ns --rm -d sampaiwastaken/athena-networksim:latest $@
#Create docker network bridge
sudo docker network create ns_bridge
sudo docker network connect ns_bridge ns
#Copy relevant traces into proxy container
for ((j=2; j<argc; j++));
do
        sudo docker cp "netTraces/${argv[j]}.json" "ns:/src/netTraces/"
    done
#Create client containers and connect them to the proxy network
for i in $(seq 1 $1)
    do 
        sudo docker run --name c$i -d tfarzad/ppt-lc-client2:latest 
        sudo docker network connect ns_bridge c$i
    done
#Copy index into client containers and run them
for i in $(seq 1 $1)
    do 
        sudo docker cp index.html c$i:/home/seluser/ppt/player/dashjs/
        sudo docker exec -d c$i python3 ./ppt.py file:///home/seluser/ppt/player/dashjs/index.html $2
    done
sleep $2
#Copy logs from client containers
for i in $(seq 1 $1)
    do
        sudo docker cp c$i:/home/seluser/chrome_debug.log logs/c$i.log
    done
#Remove client containers
for i in $(seq 1 $1)
    do 
        sudo docker rm -f c$i
    done
sudo docker cp ns:/src/clientLogs/ clientLogs
#remove proxy container
sudo docker rm -f ns
sudo docker network rm ns_bridge
exit 0
