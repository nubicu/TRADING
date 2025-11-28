# -*- coding: utf-8 -*-
import shutil
import os
import datetime
import time
from os import path
from pathlib import Path


def main():
    # make a duplicate of an existing file
    data_file = Path(__file__).parent / 'sample.txt'
    if data_file.exists():
        # get the absolute path to the file next to this script
        src = str(data_file.resolve())

    #separate the path from the filter
    head, tail = path.split(src)
    print("path:" + head)
    print("file:" + tail)

    #let's make a backup copy by appending "bak" to the name
    dst = src + ".bak"
    # now use the shell to make a copy of the file
    shutil.copy(src, dst)

    #copy over the permissions, modification
    shutil.copystat(src, dst)

    # Get the modification time for the backup file
    t = time.ctime(path.getmtime(dst))
    print(t)
    print(datetime.datetime.fromtimestamp(path.getmtime(dst)))

    bk = src + ".bk"
    if path.exists(bk):
        os.remove(bk)
    os.rename(dst, bk)

if __name__ == "__main__":
    main()