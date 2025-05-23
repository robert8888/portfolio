from django.http import JsonResponse
from portfolio.utils.validate_google_captcha import validate_captcha
from app_owner.models import Contact, ContactNumber
import json

def process(req):
    print("req")
    contact_number = Contact.objects.instance_of(ContactNumber);
    number = contact_number[0].number if len(contact_number) else None

    if number is None:
        return JsonResponse({
            'success': False
        })

    body_unicode = req.body.decode('utf-8')
    json_data = json.loads(req.body)

    if(validate_captcha(json_data['captchaToken'])):
        return JsonResponse({
            'success': True,
            'data': {
                'number': number,
            }
        })
    else :
        return JsonResponse({
            'success': False
        })
