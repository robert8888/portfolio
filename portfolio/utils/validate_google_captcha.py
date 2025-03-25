# import requests
# import json
# import os
#
# gcaptcha_key = os.getenv("GCAPTCHA_SECRET_KEY")
# gcaptcha_url = os.getenv('GCAPTCHA_VALIDATION_URL')
#
# def validate_captcha(token):
#     print("DEBUG-validate captcha",  token, gcaptcha_key)
#     captchaData = {
#         "secret" :  gcaptcha_key,
#         "response" : token
#     }
#     headers = {"Content-Type": "application/x-www-form-urlencoded"}
#
#     res = requests.post(gcaptcha_url, data = captchaData, headers = headers);
#
#     print("DEBUG-validate captcha", res.json())
#
#     return res.status_code == 200 and res.json()['success']

import requests
import requests
import os

gcaptcha_key = os.getenv("GCAPTCHA_SECRET_KEY")
gcaptcha_url = os.getenv("GCAPTCHA_VALIDATION_URL")

def validate_captcha(token):
    print("DEBUG-validate captcha", token, gcaptcha_key)

    params = {
        "secret": gcaptcha_key,
        "response": token
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    res = requests.post(gcaptcha_url, params=params, headers=headers)

    print("DEBUG-validate captcha response:", res.json())

    return res.status_code == 200 and res.json().get("success", False)
