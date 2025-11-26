# -*- coding: utf-8 -*-
import shutil
import os
import datetime
import time
from os import path


def main():
    # make a duplicate of an existing file
    if path.exists("sample.txt"):
    # get the path to the file in the current directory
        src = path.realpath("sample.txt")

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

    # Get the modification time
    t = time.ctime(path.getmtime("sample.txt.bak"))
    print(t)
    print(datetime.datetime.fromtimestamp(path.getmtime("sample.txt.bak")))

    if path.exists("sample.txt.bk"):
        os.remove("sample.txt.bk")
    os.rename('sample.txt.bak', 'sample.txt.bk')

if __name__ == "__main__":
    main()