from pikepdf import Pdf
import json

def merge(pdf_files: list[str], output_filename: str):
    output_pdf = Pdf.new()
    for file in pdf_files:
        pdf = Pdf.open(file)
        output_pdf.pages.extend(pdf.pages)
    output_pdf.save(output_filename)

def json_to_html_code(json_filename: str) -> str:
    with open(json_filename, 'r', encoding='utf-8') as json_file:
        json_content = json.load(json_file)
    '''
    TODO
    remove following two lines
    '''
    if type(json_content) is not dict:
        return '<p>invalid value</p>'
    '''
    TODO
    rewrite following code
    '''
    html_code = '<table border="1">'
    html_code += '<thead><tr><th width="50%">KEY</th><th width="50%">VALUE</th></tr></thead>'
    html_code += '<tbody>'
    for key in json_content:
        html_code += f'<tr><td>{key}</td><td>{json_content[key]}</td></tr>'
    html_code += '</tbody>'
    html_code += '</table>'
    return html_code

from fpdf import FPDF, HTMLMixin

class PDF(FPDF, HTMLMixin):
    def __init__(self):
        super().__init__()
        self.add_font('yahei', fname='MicrosoftYaHeiMono-CP950.ttf', uni=True)
        self.add_font('yahei', 'B', fname='MicrosoftYaHeiMono-CP950.ttf', uni=True)
        self.set_font('yahei', size=14)

def html_code_to_pdf(html_code: str, output_filename: str):
    pdf = PDF()
    pdf.add_page()
    pdf.write_html(html_code)
    pdf.output(output_filename)

def json_to_pdf(json_filename: str, output_filename: str):
    html_code = json_to_html_code(json_filename)
    html_code_to_pdf(html_code, output_filename)
