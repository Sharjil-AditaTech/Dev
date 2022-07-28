from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = getattr(settings,"STATIC_LOCATION","STATIC_URL")
    default_acl = 'public-read'


class Media_Storage1(S3Boto3Storage):
    location = getattr(settings,"MEDIAFILES_LOCATION","MEDIA_URL")
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = False


class Media_Storage2(S3Boto3Storage):
    location = getattr(settings,"MEDIAFILES_OTHER_LOCATION","OTHERS_URL")
    default_acl = 'public-read'
    file_overwrite = False



