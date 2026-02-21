#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>

/* this can serve as the ls command implementation in c language */

#if 1
void listdir(const char *pathname)
{
	DIR  *dp;
	struct dirent	*dirp;
	char PATH[259] = {0};

	if ((dp = opendir(pathname)) == NULL)
		return;
	while(( dirp = readdir(dp)) != NULL)
	{

		if(dirp->d_type == DT_DIR)
		{
			if( (strcmp(dirp->d_name,".") == 0) || (strcmp(dirp->d_name, "..") == 0) )
				continue;

			printf("%s%s\n", pathname, dirp->d_name);
			snprintf(PATH, sizeof(PATH)-1, "%s%s/",pathname,dirp->d_name);
			listdir(PATH);
		}
		else
		{
			printf("%s%s\n", pathname, dirp->d_name);
		}
	}
	closedir(dp);	
}
#endif

int main(int argc, char *argv[])
{
	DIR  *dp;
	struct dirent	*dirp;

	if( argc !=2 )
	{
		printf("Please provide the directory to list out\n");
		exit(1);
	}

	listdir(argv[1]);

	exit(0);
}

