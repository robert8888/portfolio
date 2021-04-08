# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.conf import settings
import tempfile
import os
from portfolio.s3proxy import generatePresignedUrl

from puppeteer_pdf import render_pdf_from_template


def process(req, slug):
    context = {
        'photo_url': generatePresignedUrl('media/upload/2021/03/15/fake-me.png')
    }
    try:
        output_file = os.path.join(settings.BASE_DIR, 'static', 'cv_temp.pdf')

        pdf = render_pdf_from_template(
            input_template='pdf/'+id+'.html',
            header_template='',
            footer_template='',
            context=context,
            cmd_options={
                'format': 'A4',
                'scale': '1',
                'marginTop': '0',
                'marginLeft': '0',
                'marginRight': '0',
                'marginBottom': '0',
                'printBackground': True,
                'preferCSSPageSize': True,
                'output': output_file,
                'pageRanges': 1
            }
        )
        if os.path.exists(output_file):
            os.remove(output_file)

        response = HttpResponse(pdf, content_type='application/pdf;')
        response['Content-Disposition'] = 'filename=cv-2.pdf'

        return response
    except:
        return HttpResponseRedirect('/404')