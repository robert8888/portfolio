# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import os


from puppeteer_pdf import render_pdf_from_template
from puppeteer_pdf.views import PDFResponse


def process(req, id):
#     html_string = render_to_string('pdf/cv_simple.html', {'test': 'value'})
#     html = HTML(string=html_string, base_url=req.build_absolute_uri('/'), encoding = "Latina-2")
#     pdf_file = html.write_pdf()

#     response = HttpResponse(pdf_file, content_type='application/pdf;')
#     response['Content-Disposition'] = 'filename=cv-2.pdf'
#
#     return response

    pdf = render_pdf_from_template(
        input_template='pdf/cv_simple.html',
        header_template='',
        footer_template='',
        context={},
        cmd_options={
            'format': 'A4',
            'scale': '1',
            'marginTop': '0',
            'marginLeft': '0',
            'marginRight': '0',
            'marginBottom': '0',
            'preferCSSPageSize': True,
            'output': './static/cv_temp.pdf'
        }
    )
    os.remove('./static/cv_temp.pdf')
    response = HttpResponse(pdf, content_type='application/pdf;')
    response['Content-Disposition'] = 'filename=cv-2.pdf'
    return response