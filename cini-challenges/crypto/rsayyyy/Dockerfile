FROM ubuntu:bionic-20181204
RUN apt-get -y update
# RUN apt-get -y upgrade
RUN apt-get -y install xinetd

RUN groupadd -g 1000 challenge && useradd -g challenge -m -u 1000 challenge -s /bin/bash

ADD server /
ADD xinetd.conf /etc/xinetd.d/server

RUN chmod +x /server

CMD xinetd -d -dontfork
