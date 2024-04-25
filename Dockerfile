# System
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Installing Dependancies
RUN apt update
RUN apt-get clean

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install ffmpeg -y
RUN apt-get install -y git wget python3-dev python3-pip unzip

RUN python3 -m pip install pip --upgrade
RUN pip3 install ultralytics
RUN pip3 install supervision==2.19.0
RUN pip3 install opencv-python-headless
RUN apt-get update
RUN apt install -y cmake curl

# Install dependancies of your application here
# RUN pip3 install <dependancy1>
# RUN apt install <dependancy2>
ENV PYTHONIOENCODING=utf8
RUN echo "$FOO $BAR $PYTHONIOENCODING"

# Copy neccessary file like inference program etc to docker image
# COPY data/ /yolo/