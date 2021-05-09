from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import get_storage_class
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

    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        super(AssetStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        self.local_storage._save(name, content)
        super(AssetStorage, self).save(name, self.local_storage._open(name))
        return name