FROM ubuntu:bionic-20181204
RUN apt-get -y update
RUN apt-get -y install xinetd

RUN groupadd -g 1000 challenge && useradd -g challenge -m -u 1000 challenge -s /bin/bash

ADD safe_to_smash /
ADD xinetd.conf /etc/xinetd.d/sum
ADD libc-2.27.so /lib/x86_64-linux-gnu/libc.so.6

RUN chmod +x /safe_to_smash

CMD xinetd -d -dontfork
