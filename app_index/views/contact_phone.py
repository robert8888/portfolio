from django.http import JsonResponse
from app_index.utils.validateGoogleCaptcha import validateCaptcha
import json


def contactPhone(req):
    body_unicode = req.body.decode('utf-8')
    json_data = json.loads(req.body)

    if(validateCaptcha(json_data['captchaToken'])):
        return JsonResponse({
            'success': True,
            'number': 733508985
        })
    else :
        return JsonResponse({
            'success': False
        })
