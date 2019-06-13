#!/usr/bin/python3

import urllib.request
import re
import PyPDF2 as pdf

def get_cirriculum_sheet(major, years=("19", "20")):
    sheet = urllib.request.urlopen('https://flowcharts.calpoly.edu/downloads/curric/{}-{}.{}.pdf'.format(years[0], years[1], major))
    with open("CIR_LOADED.pdf", "wb") as f:
        f.write(sheet.read())
    with open("CIR_LOADED.pdf", "rb") as f:
        sheet = pdf.PdfFileReader(f)
        print("Number of pages: {}".format(sheet.getNumPages()))
        # for i in range(sheet.getNumPages()):
        for i in range(1):
            page = sheet.getPage(i)
            print("============ Extracted Text =============")
            pageText = page.extractText()
            print(re.findall(r"[A-Z]{3,4}.*[0-9]{3}.*\n", pageText))

get_cirriculum_sheet("Mathematics")
print("\n=====\n")
get_cirriculum_sheet("Computer%20Science")
