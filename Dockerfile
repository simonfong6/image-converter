FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y python3.5 \
                       python3-pip

RUN pip3 install imageio rawpy flask flask-cors