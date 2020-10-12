FROM ubuntu:18.04
COPY . ./mnt
RUN apt update && apt install python3 python3-pip -y && pip3 install numpy
CMD ["sleep", "infinity"]
