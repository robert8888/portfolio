from django.http import JsonResponse
from index_app.utils.validateGoogleCaptcha import validateCaptcha
import json
import re


def contactForm(req):
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

    print(validate)

    if(validate['success'] == False) :
        validate['errors'].append({
            'message': "Google Recaptcha authorization fail"
        })
        return JsonResponse(validate)

    validate = Validation(data)

    if validate["success"] == True:
        update(data)

    return JsonResponse(validate)

def Validation(data):
    validate = {
        'success': True,
        'errors': []
    }

    rules = [{
        "field" : "emailField",
        "pattern" : "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        "message": "Email address not valid",
    }, {
        "field" : "subjectField",
        "pattern" : ".{6,}$",
        "message": "Subject value too short, min 6 chars",
    }, {
        "field" : "messageField",
        "pattern" : ".{20,}$",
        "message": "Message value too short, min 20 chars",
    }]

    print(data)
    for rule in rules:
        if not re.search(rule['pattern'], data[rule['field']]):
            validate['errors'].append({
                'message': rule['message'],
                'field': rule['field']
            })

    if len(validate['errors']) != 0 :
        validate['success'] = False

    return validate

def update(data):
    pass