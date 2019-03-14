CC=gcc
CFLAGS=-Wall -no-pie -fno-stack-protector -z execstack -g

all: poet.c
	$(CC) $(CFLAGS) -o distrib/poet poet.c

clean:
	rm distrib/poet

