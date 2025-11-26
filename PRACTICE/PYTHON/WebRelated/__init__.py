# -*- coding: utf-8 -*-
#
# read the data from the URL and write it in a file
import urllib.request

# open a connection to a URL using urllib
#webUrl = urllib.request.urlopen('https://www.youtube.com/user/nubicu')
webUrl = urllib.request.urlopen('https://www.olx.ro/imobiliare/apartamente-garsoniere-de-vanzare/' +
'3-camere/iasi_39939/?search%5Bfilter_enum_compartimentare%5D%5B0%5D=decomandat&search%5Bfilter_float_m%3Afrom%5D=60' +
'&search%5Bfilter_enum_floor%5D%5B0%5D=fl_1&search%5Bfilter_enum_floor%5D%5B1%5D=fl_2&search%5Bfilter_enum_floor%5D%5B2%5D' +
'=fl_3')

print("Execution started")

# open the file for writing
fisier = open("testfile.txt", "w")

#get the result code and write it in the file
fisier.write("result code: " + str(webUrl.getcode()))
fisier.close()

fisier = open("testfile.txt", "ab")
# read the data from the URL and write it in the file
data = webUrl.read()

fisier.write(data)
#fisier.write(data.decode('utf-8').strip('\x00'))

# close the writing operations in the file
fisier.close()

print("Execution finished!")
