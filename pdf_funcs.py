import os
from pikepdf import Pdf

#pdfMerge([<filename_1>,<filename_2>, ... ])

def pdfMerge(f_list):
    output = Pdf.new()
    for f_name in f_list:
        Pdf_content = Pdf.open(f_name)
        output.pages.extend(Pdf_content.pages)
    output.save('output.pdf')
