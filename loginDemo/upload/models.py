from django.db import models
from loginDemo.aws.backend import *

class UploadImage(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(storage=Media_Storage1())

