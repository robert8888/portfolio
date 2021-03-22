from django.http import JsonResponse
from portfolio.utils.validateGoogleCaptcha import validateCaptcha
from app_owner.models import Contact, ContactNumber
import json


def process(req):
    contact_number = Contact.objects.instance_of(ContactNumber)
    number = contact_number[0].number if len(contact_number) else None
    if number is None:
        return JsonResponse({
            'success': False
        })

    body_unicode = req.body.decode('utf-8')
    json_data = json.loads(req.body)

    if(validateCaptcha(json_data['captchaToken'])):
        return JsonResponse({
            'success': True,
            'number': number
        })
    else :
        return JsonResponse({
            'success': False
        })
