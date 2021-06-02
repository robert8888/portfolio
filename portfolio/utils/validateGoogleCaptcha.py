import requests
import json
import os

gcaptcha_key = os.getenv("GCAPTCHA_SECRET_KEY")
gcaptcha_url = os.getenv('GCAPTCHA_VALIDATION_URL')

def validateCaptcha(token):
    print(token)
    captchaData = {
        "secret" :  gcaptcha_key,
        "response" : token
    }

    res = requests.post(gcaptcha_url, data = captchaData)

    print(res)
    validate = {
        'success': False,
        'errors': []
    }

    return res.status_code == 200 and res.json()['success']
