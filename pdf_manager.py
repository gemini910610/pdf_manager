from pikepdf import Pdf
import json
from json2html import json2html

def merge(pdf_files: list[str], output_filename: str):
    output_pdf = Pdf.new()
    for file in pdf_files:
        pdf = Pdf.open(file)
        output_pdf.pages.extend(pdf.pages)
    output_pdf.save(output_filename)

def json_to_html(json_filename: str) -> str:
    '''
    TODO
    do not use json2html
    table example: (children of first tr need to set width)
    <table>
        <thead>
            <tr>
                <th width="50%">Header 1</th>
                <th width="50%">Header 2</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>cell 1</td><td>cell 2</td></tr>
            <tr><td>cell 3</td><td>cell 4</td></tr>
        </tbody>
    </table>
    '''
    with open(json_filename) as json_file:
        json_content = json.load(json_file)
    return json2html.convert(json_content)

'''
convert to pdf from code
need to generate html code from json without json2html
'''
from fpdf import FPDF, HTMLMixin

class PDF(FPDF, HTMLMixin):
    def __init__(self):
        super().__init__()

def html_code_to_pdf(html_code: str, output_filename: str):
    pdf = PDF()
    pdf.add_page()
    pdf.write_html(html_code)
    pdf.output(output_filename)

'''
convert to pdf from file
can use json2html to generate html code and write it into .html file
remember to delete .html file after convert success
'''
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
def html_file_to_pdf(html_filename: str, output_filename: str):
    loader = QWebEngineView()
    loader.load(QUrl(html_filename))
    def output_pdf():
        loader.page().printToPdf(output_filename)
        '''
        TODO
        remove following two lines
        '''
        loader.show()
        loader.close()
    loader.loadFinished.connect(output_pdf)
