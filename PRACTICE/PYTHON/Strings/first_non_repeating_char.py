# -*- coding: utf-8 -*-
# A Python program to find first non-repeating character from
# a stream of characters
MAX_CHAR = 256


def findFirstNonRepeating():
    # inDLL[x] contains pointer to a DLL node if x is present
    # in DLL. If x is not present, then inDLL[x] is NULL
    inDLL = [] * MAX_CHAR

    # repeated[x] is true if x is repeated two or more times.
    # If x is not seen so far or x is seen only once. then
    # repeated[x] is false
    repeated = [False] * MAX_CHAR

    # Let us consider following stream and see the process
    stream = "geeksforgeeksandgeeksquizfor"
    for i in range(len(stream)):
        x = stream[i]
        print("Reading " + x + " from stream")

        # We process this character only if it has not occurred
        # or occurred only once. repeated[x] is true if x is
        # repeated twice or more.s
        if not repeated[ord(x)]:

            # If the character is not in DLL, then add this
            # at the end of DLL
            if not x in inDLL:
                inDLL.append(x)
            else:
                inDLL.remove(x)

        if len(inDLL) != 0:
            print("First non-repeating character so far is ")
            print(str(inDLL[0]))

# Driver program
findFirstNonRepeating()