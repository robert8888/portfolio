import requests
import json
import os

gcaptcha_key = os.getenv("GCAPTCHA_SECRET_KEY")
gcaptcha_url = os.getenv('GCAPTCHA_VALIDATION_URL')

def validate_captcha(token):
    print("DEBUG-validate captcha",  token, gcaptcha_key)
    captchaData = {
        "secret" :  gcaptcha_key,
        "response" : token
    }
    # captchaData = {
    #     "secret": "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe",
    #     "response": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
    # }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    res = requests.post(gcaptcha_url, data = captchaData, headers = headers);

    print("DEBUG-validate captcha", res.json())

    return res.status_code == 200 and res.json()['success']

