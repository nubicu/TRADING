#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

int main(int argc, char *argv[])
{
    int fd = -1;
    char buffer[10] = {0};
    int ret = 0;

    if(argc != 2)
    {
        printf("Please provide the filename as argument to read\n");
        exit(EXIT_FAILURE);
    }

    fd = open("./test.txt", O_RDONLY);

    if(fd == -1)
    {
		/* /usr/include/errno.h */
		/* /usr/include/asm-generic/errno-base.h */


        printf("Error in opening the file  error_num=%d  %s\n", errno, strerror(errno) );
        exit(EXIT_FAILURE);
    }

    while ((ret = read(fd, (void *)buffer, sizeof(buffer)-1 )) >0 )
    {
        printf("%s", buffer);
        memset(buffer, 0 , sizeof(buffer));
    }

    close(fd);

    return EXIT_SUCCESS;
}
