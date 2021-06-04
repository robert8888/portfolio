from django.http import JsonResponse
from portfolio.utils.validate_google_captcha import validate_captcha
from app_owner.models import Contact, ContactEmail
import json


def process(req):
    contact = Contact.objects.instance_of(ContactEmail).filter(show_on_index = True)
    email = contact[0].email if len(contact) else None
    if email is None:
        return JsonResponse({
            'success': False
        })

    json_data = json.loads(req.body)

    if(validate_captcha(json_data['captchaToken'])):
        return JsonResponse({
            'success': True,
            'data': {
                'email': email,
            }
        })
    else :
        return JsonResponse({
            'success': False
        })
