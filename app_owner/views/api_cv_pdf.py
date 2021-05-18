# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.template.loader import render_to_string
from portfolio.s3proxy import generatePresignedUrl
from puppeteer_pdf import render_pdf_from_template
from django.conf import settings
from .get_cv_pdf_data import process as get_cv_data
from django.utils.translation import get_language
from portfolio.utils.validateGoogleCaptcha import validateCaptcha
from portfolio.utils.readConfigJson import readConfigJson
from ..utils.email_sender import send as send_email
import tempfile
import os
import datetime
import json
import pydash as py_
import bleach

class CvPdf(View):
    def render_cv_pdf(self, context, tpl_path):
        try:
            output_temp_file = os.path.join(settings.BASE_DIR, 'static', 'cv_temp.pdf')

            pdf = render_pdf_from_template(
                input_template= tpl_path,
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

            download_name = context['cv'].data.get_download_name
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            filename = f'filename={download_name}-{get_language().upper()}-{current_date}.pdf'

            response = HttpResponse(pdf, content_type='application/pdf;')
            response['Content-Disposition'] = filename

            return response
        except BaseException as error:
            raise BaseException('Template render error')


    def post(self, req):
        try:
            body_unicode = req.body.decode('utf-8')
            post_data = json.loads(req.body)

            if not validateCaptcha(post_data['captchaToken']):
                 return HttpResponse(status=403)

            response = get_cv_data(req, {
                'templateId': post_data['templateId'],
                'colorProfileId': post_data['colorProfileId'],
                'default': True,
            })

            if not response.success:
                raise Exception('cv data not found for slug' + slug)

            context = {
                'cv': response.data.cv
            }

            template = py_.find(readConfigJson(['templates', 'TEMPLATES.json']).get('pdf', None), {'slug': post_data['templateId']})

            self.send_confirm_email(req, post_data)

            return self.render_cv_pdf(context, template['path'])
        except BaseException as error:
            print(error)
            return JsonResponse({'success': False, 'errors': [str(error)]})


    def get(self, req, slug):
        try:
            print(slug)
            response = get_cv_data(req, {
                'slug': slug
            })
            context = {
                'cv': response.data.cv
            }
            tpl_path = response.data.cv.template

            return self.render_cv_pdf(context, tpl_path)
        except BaseException as error:
            print('error', error)
            return HttpResponseRedirect('/404')

    def send_confirm_email(self, req, data):
        try:
            context = {
                'path': req.get_host(),
                'subject': 'Cv was downloaded',
                'email':  bleach.clean(data['recruiterEmail']),
                'company':  bleach.clean(data['recruiterCompany']),
            }

            template_names = {
                'html': 'email_cv_download_html.html',
                'plain': 'email_cv_download_plain.html',
            }

            send_email(req, context, template_names)
        except:
            print('Cv download confirm email sending error')