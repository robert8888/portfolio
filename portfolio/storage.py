from storages.backends.s3boto3 import S3Boto3Storage
import os

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    default_acl = 'private'
    custom_domain = os.getenv('AWS_S3_CUSTOM_DOMAIN')

class AssetStorage(S3Boto3Storage):
    location = 'assets'
    file_overwrite = True
    default_acl = 'private'
    custom_domain = os.getenv('AWS_S3_CUSTOM_DOMAIN')