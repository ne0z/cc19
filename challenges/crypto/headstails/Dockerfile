FROM ubuntu:bionic-20181204

RUN apt-get update && apt-get install -y python
RUN useradd headstails
RUN mkdir /app
COPY src/headstails.py /app/

USER headstails
CMD /app/headstails.py
