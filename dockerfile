FROM python:3.8

WORKDIR /data

# Install necessary packages
RUN apt update && \
    # apt install -y ffmpeg libsm6 libxext6 && \
    pip install -r /data/requirements.txt

# Copy the scripts into the container
COPY ./image.sh /usr/local/bin/image.sh
COPY ./run_crop_image.sh /usr/local/bin/run_crop_image.sh

# Make the scripts executable
RUN chmod +x /usr/local/bin/image.sh /usr/local/bin/run_crop_image.sh

# Set the entry point to run both scripts in parallel
CMD ["sh", "-c", "./usr/local/bin/image.sh & ./usr/local/bin/run_crop_image.sh"]
