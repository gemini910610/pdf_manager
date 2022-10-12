import os
from pikepdf import Pdf
import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import json
from json2html import *

#pdfMerge([<filename_1>,<filename_2>, ... ])

def pdfMerge(f_list):
    output = Pdf.new()
    for f_name in f_list:
        Pdf_content = Pdf.open(f_name)
        output.pages.extend(Pdf_content.pages)
    output.save('output.pdf')

def htmlToPdf(filename):
    loader = QtWebEngineWidgets.QWebEngineView()
    loader.setZoomFactor(1)
    loader.page().pdfPrintingFinished.connect(lambda *args: print('finished:', args))
    loader.load(QtCore.QUrl(filename))
    def emit_pdf(finished):
        loader.show()
        loader.page().printToPdf("output.pdf")
    loader.loadFinished.connect(emit_pdf)
    
def jsonToHtml(filename):
    jsonfile = open("sample.json")
    infoFromJson = json.load(jsonfile)
    htmlfile = open("j2h.html", 'w')
    htmlfile.write(json2html.convert(json = infoFromJson))
    htmlfile.close()

#jsonToPdf(<filename>)

def jsonToPdf(filename):
    jsonToHtml(filename)
    url = os.getcwd().replace("\\","/")+"/j2h.html"
    print(url)
    htmlToPdf(url)


app = QtWidgets.QApplication(sys.argv)
#jsonToPdf("sample.json")
print("convert_suceess")
app.exec()
