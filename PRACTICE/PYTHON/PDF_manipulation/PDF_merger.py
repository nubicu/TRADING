# -*- coding: utf-8 -*-
import time
import os
from PyPDF2 import PdfFileMerger

# pdfs = ['test1.pdf', 'test2.pdf']

allPDFs = [a for a in os.listdir() if a.endswith(".pdf")]

dtFname = time.strftime("%Y%m%d_%H%M%S")
merger = PdfFileMerger()

for pdf in allPDFs:
    merger.append(pdf)

merger.write(dtFname + ".pdf")