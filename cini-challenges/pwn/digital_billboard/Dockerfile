FROM ubuntu:bionic-20181204

RUN groupadd -g 1000 challenge && useradd -g challenge -m -u 1000 challenge -s /bin/bash

ADD server /
ADD billboard.so /
ADD flag.txt /

WORKDIR /

CMD ["/server"]
