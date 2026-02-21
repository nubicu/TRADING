#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>

void sig_handler(int signum)
{
    printf("Alarm delivered signum is %d\n", signum);
    system("/bin/ls");
}

int main()
{
    alarm(5);
    signal(SIGALRM, sig_handler);

//start executing from this line only if not exited in signal handler.
    for(;;)
	sleep(1);
	
    return 0;
}
