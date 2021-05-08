from django.http import HttpResponseRedirect, HttpResponse
import boto3
import os
import re

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_URL = os.getenv('AWS_URL')
AWS_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')
AWS_S3_REGION_NAME = 'eu-central-1'

def s3proxy(req):
    try:
        path = req.GET.get('p', None)

        if not path:
            return HttpResponse(status=404)

        response = generatePresignedUrl(path)
        return HttpResponseRedirect(response)
    except:
        return HttpResponse(status=404)

def replaceImgUrl(html):
    img_path = "(?:"+AWS_URL+")(.*\.(?:png|jpg|jpeg|gif))"
    pattern = "(<img.*?src=\")"+img_path+".*\""
    transformed_html = re.sub(pattern, "\\1/s3image?p=\\2\"", html)
    return transformed_html

def generatePresignedUrl(path):
    s3_client = boto3.client('s3',
        aws_access_key_id= AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME,
    )

    response = s3_client.generate_presigned_url(
        ClientMethod = 'get_object',
        Params={
            'Bucket': AWS_STORAGE_BUCKET_NAME,
            'Key': path
        }, ExpiresIn=172800
    )

    if AWS_CUSTOM_DOMAIN:
        response = response.replace(AWS_URL, 'https://' + AWS_CUSTOM_DOMAIN + '/')

    return response