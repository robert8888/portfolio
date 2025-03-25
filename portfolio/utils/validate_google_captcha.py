import requests
import json
import os

gcaptcha_key = os.getenv("GCAPTCHA_SECRET_KEY")
gcaptcha_url = os.getenv('GCAPTCHA_VALIDATION_URL')

def validate_captcha(token):
    captchaData = {
        "secret" :  gcaptcha_key,
        "response" : token
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    res = requests.post(gcaptcha_url, data = captchaData, headers = headers);

    return res.status_code == 200 and res.json()['success']

