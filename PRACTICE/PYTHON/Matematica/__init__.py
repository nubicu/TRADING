#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class DoubleHashing(object):
    def __init__(self, data=list()):
        self.data = data
        self.fx = int(input("module fx:\t"))
        self.gx = int(input("module gx:\t"))
        self.fx_data = list()
        self.gx_data = list()
        self.hashTabel = list()
        self.steps = list()
        self.setModes()
        for i in range(self.fx):
            self.hashTabel.append(None)
            self.steps.append(None)
        self.createHashTabel()
        self.printToFile()

    def setModes(self):
        for i in self.data:
            self.fx_data.append(i % self.fx)
            self.gx_data.append(self.gx - i % self.gx)

    def createHashTabel(self):
        i = 0
        while i < len(self.data):
            j = 0
            while j < 100:
                temp = (self.fx_data[i] + self.gx_data[i] * j) % self.fx
                if(self.hashTabel[temp] is None):
                    self.hashTabel[temp] = self.data[i]
                    self.steps[temp] = j
                    break
                j += 1
            i += 1

    def printHashtabel(self):
        res = ""
        res += "data\t Fx\t Gx\n"
        for i in range(0, len(self.data)):
            res += "{}\t {} \t{}\n".format(self.data[i], self.fx_data[i], self.gx_data[i])
        res += "-" * 10
        res += '\n'
        for i in range(0, len(self.hashTabel)):
            res += "{}.\t {}\t{}\n".format(i, self.hashTabel[i], self.steps[i])
            print(str(i), str(self.hashTabel[i]), sep = '\t')
        return res

    def printToFile(self, fName="log1"):
        fName = fName + "_" + str(self.fx) + '_' + str(self.gx)
        x = open(fName, "w")
        x.write(self.printHashtabel())


def main():
    #enter here the data you want to hash
    data = [70, 16, 23, 3, 24, 38, 60, 115, 46, 98, 99]
#    DoubleHashing(data)

    arr = [1, 101, 2, 3, 100, 4, 5]
    msis = [elem for elem in arr]

    for x in range(1, len(arr), 1):
        for y in range(0, x, 1):
            if arr[x] > arr[y]:
                msis[x] += arr[y]

    print(max(msis))

if __name__ == "__main__":
    main()