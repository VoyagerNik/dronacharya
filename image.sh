\#!/bin/bash

output_dir="./dproj/ip2"
max_files=15  # Keep exactly 15 most recent images

counter=1
while true; do
  # Calculate which file to overwrite (1-15)
  file_to_overwrite=$(( (counter - 1) % max_files + 1 ))
  
  # New filename keeps original number but content is newest capture
  filename="$output_dir/image${counter}.jpg"
  
  # Temporary name for atomic write
  tempname="$output_dir/image${counter}.tmp.jpg"

  # Capture image (1 frame)
  gst-launch-1.0 -e v4l2src device=/dev/video0 num-buffers=1 \
    ! video/x-raw,width=960,height=540,framerate=10/1 \
    ! videoconvert \
    ! jpegenc quality=85 \
    ! filesink location="$tempname"

  # Atomic move (replaces old file if exists)
  mv -f "$tempname" "$filename"
  
  # Remove the oldest file (if we've passed max_files)
  if (( counter > max_files )); then
    oldest=$(( counter - max_files ))
    rm -f "$output_dir/image${oldest}.jpg"
  fi

  echo "Saved: $filename (Overwrote position $file_to_overwrite)"
  ((counter++))
  sleep 2.5  # Wait 2.5 seconds before next capture
done
