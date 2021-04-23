from django.http import JsonResponse
from portfolio.utils.validateGoogleCaptcha import validateCaptcha
from django.utils.translation import gettext_lazy, gettext
from ..utils.email_sender import send as send_email
import json
import re
import os



def process(req):
    body_unicode = req.body.decode('utf-8')
    json_data = json.loads(req.body)

    data = {
        'captcha': json_data['gRrecaptchaRresponse'],
        'emailField': json_data['emailField'],
        'subjectField': json_data['subjectField'],
        'messageField': json_data['messageField'],
    }

    validate = {
        'success': validateCaptcha(data['captcha']),
        'errors': []
    }

    if(validate['success'] == False) :
        validate['errors'].append({
            'message': gettext_lazy("Google Recaptcha authorization fail")
        })
        return JsonResponse(validate)

    validate = Validation(data)

    if validate["success"] == True:
        send(data, req)

    return JsonResponse(validate)

def Validation(data):
    validate = {
        'success': True,
        'errors': []
    }

    rules = [{
        "field" : "emailField",
        "pattern" : "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        "message": gettext("Email address not valid"),
    }, {
        "field" : "subjectField",
        "pattern" : ".{6,}$",
        "message": gettext("Subject value too short, min 6 chars"),
    }, {
        "field" : "messageField",
        "pattern" : ".{20,}$",
        "message": gettext("Message value too short, min 20 chars"),
    }]

    for rule in rules:
        if not re.search(rule['pattern'], data[rule['field']]):
            validate['errors'].append({
                'message': rule['message'],
                'field': rule['field']
            })

    if len(validate['errors']) != 0 :
        validate['success'] = False

    return validate


def send(data, req):
    context = {
        'path': req.get_host(),
        'from':  data['emailField'],
        'message':  data['messageField'],
        'subject':  data['subjectField'],
    }

    template_names = {
        'html': 'email_contact_form_html.html',
        'plain': 'email_contact_form_plain.html',
    }

    send_email(req, context, template_names)
