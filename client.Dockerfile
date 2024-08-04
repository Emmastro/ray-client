FROM ubuntu:20.04
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install ray
# TODO: change the address to the IP of the head node
CMD ["ray", "start", "--address=192.168.1.2:6379"]
