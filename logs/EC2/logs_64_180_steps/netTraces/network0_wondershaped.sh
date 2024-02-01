#!/bin/bash
sudo wondershaper/wondershaper -a enp0s3 -c
sudo wondershaper/wondershaper -a enp0s3 -d 0 -u 50000
sleep 120
sudo wondershaper/wondershaper -a enp0s3 -c
exit 0