# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from portfolio.s3proxy import generatePresignedUrl
from puppeteer_pdf import render_pdf_from_template
from django.conf import settings
import tempfile
import os
from .get_cv_pdf_data import process as get_cv_data

def process(req, slug):
    try:
        response = get_cv_data(req, slug)
        if not response.success:
            raise Exception('cv data not found for slug' + slug)

        context = {
            'cv': response.data.cv
        }
#         print(response.data.cv.data.get_download_name)
        output_temp_file = os.path.join(settings.BASE_DIR, 'static', 'cv_temp.pdf')

        pdf = render_pdf_from_template(
            input_template=response.data.cv.template,
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
                'output': output_temp_file,
                'pageRanges': 1
            }
        )
        if os.path.exists(output_temp_file):
            os.remove(output_temp_file)

        filename = f'filename={response.data.cv.data.get_download_name}.pdf'

        response = HttpResponse(pdf, content_type='application/pdf;')
        response['Content-Disposition'] = filename

        return response
    except BaseException as error:
        print('error', error)
        return HttpResponseRedirect('/404')