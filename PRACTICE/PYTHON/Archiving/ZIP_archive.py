# -*- coding: utf-8 -*-
import os
import shutil
from zipfile import ZipFile
from os import path


def main():
    # Check if file exists
    if path.exists("sample.txt"):
    # get the path to the file in the current directory
        src = path.realpath("sample.txt")
    # rename the original file
    os.rename("sample.txt", "career.sample.txt")
    # now put things into a ZIP archive
    root_dir, tail = path.split(src)
    shutil.make_archive("sample archive", "zip", root_dir)
    # more fine-grained control over ZIP files
    with ZipFile("testsample.zip", "w") as newzip:
        newzip.write("career.sample.txt")
        newzip.write("sample.txt.bk")

if __name__ == "__main__":
    main()