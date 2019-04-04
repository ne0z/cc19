CC=gcc
CFLAGS=-Wall -no-pie -fno-stack-protector -z execstack -g

all: sum.c
	$(CC) $(CFLAGS) -o distrib/sum sum.c
	cp sum.c distrib/

clean:
	rm distrib/sum

