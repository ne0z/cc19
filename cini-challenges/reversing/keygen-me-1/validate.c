#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
	const char *key = argv[1];
	size_t len = strlen(key);
	size_t i;
	unsigned int tot = 0;
	unsigned long long m;
	unsigned int r;

	i = 0;
	while (i < len - 1) {
		char k = key[i];
		int w = (k <= 0x39 ? k - 0x30 : (k > 0x40 && k <= 0x5A) ? k - 0x37 : 0);
		i++;
		tot += i * (w + 1);
	}
	printf("tot %x\n", tot);
	m = 0x38e38e39 * tot;
	r = m >> 32;
	r = tot - ((r >> 3) + (r & ~3U)) >> 2;
	printf("%x %c\n", r, r);
	return 0;
}
