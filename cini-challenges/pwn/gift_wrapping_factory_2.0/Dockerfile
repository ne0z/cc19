FROM ubuntu:artful-20171116

RUN groupadd -g 1000 challenge && useradd -g challenge -m -u 1000 challenge -s /bin/bash

ADD server /
ADD giftwrapper2.so /
ADD flag.txt /

WORKDIR /

CMD ["/server"]
