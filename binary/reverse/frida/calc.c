#include <stdio.h>

int main()
{
	const unsigned long long N = 0x19965;
	unsigned long long t[1+N];
	int i;

	for (i = 0; i < 5; i++) {
		t[i] = i * i + 0x2345;
	}
	for (i = 5; i <= N; i++) {
		t[i] = t[i-5] * 0x1234 + (t[i-1] - t[i-2]) + (t[i-3] - t[i-4]);
	}

	printf("%llu\n", t[N]);

	return 0;
}
