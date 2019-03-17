CC=gcc
CFLAGS=-g -fstack-protector -zexecstack
#-zexecstack
# You can temporarily disable PIE to debug with GDB: add -no-pie

safe_to_smash:
	$(CC) $(CFLAGS) safe_to_smash.c -o safe_to_smash

all: safe_to_smash

clean:
	rm -f safe_to_smash
