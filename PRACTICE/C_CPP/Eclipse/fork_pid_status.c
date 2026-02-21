#include <stdio.h>
#include <unistd.h>

int main()
{
	pid_t pid;

	if( (pid = fork()) > 0)  //Parent process
	{
		sleep(30);
	}
	else    //Child Process
	{
		sleep(30);
	}

	return 0;
}
