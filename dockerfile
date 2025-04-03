FROM python:3.8

# Set the working directory inside the container; prevents a `cd'
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

RUN apt update && \
    apt install -y ffmpeg libsm6 libxext6 sudo gstreamer1.0-tools

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/image.sh /app/run_crop_image.sh


CMD ["sh", "-c", "/app/image.sh & /app/run_crop_image.sh"]