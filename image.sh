#!/usr/bin/env bash
sudo /usr/bin/gst-launch-1.0 nvarguscamerasrc sensor_id=0 ! \
    'video/x-raw(memory:NVMM),width=1920, height=1080, framerate=30/1' ! \
    nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=540' ! \
    nvjpegenc ! multifilesink location=/app/ip2/image%d.jpg max-files=5 post-messages=true next-file=2
