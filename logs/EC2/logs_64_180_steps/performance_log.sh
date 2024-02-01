#!/bin/bash
sudo docker stats --no-stream --all --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"  > "PerformanceLogs.txt"
sleep 1
while true
do
#outputs the docker stats with a different format in a file 
sudo docker stats --no-stream --all --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"  >> "PerformanceLogs.txt"
#docker stats --no-stream | tee --append stats.txt; 
sleep 1
done
exit 0