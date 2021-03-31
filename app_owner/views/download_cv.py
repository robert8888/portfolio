# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile


def process(req, id):
    # Rendered
    html_string = render_to_string('pdf/cv_dark.html', {'test': 'value'})
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf;')
    response['Content-Disposition'] = 'filename=cv-2.pdf'

    return response
