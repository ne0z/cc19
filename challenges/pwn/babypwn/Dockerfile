FROM ubuntu:xenial-20190122
RUN apt-get -y update
# RUN apt-get -y upgrade
RUN apt-get -y install xinetd

RUN groupadd -g 1000 challenge && useradd -g challenge -m -u 1000 challenge -s /bin/bash

ADD babypwn /
ADD flag.txt /
ADD xinetd.conf /etc/xinetd.d/babypwn

RUN chmod +x /babypwn

CMD xinetd -d -dontfork
