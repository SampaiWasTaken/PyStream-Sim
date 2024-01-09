#!/bin/bash
sudo wondershaper/wondershaper -a enp0s3 -c
sudo wondershaper/wondershaper -a enp0s3 -d 3770 -u 50000
sleep 130
sudo wondershaper/wondershaper -a enp0s3 -c
exit 0