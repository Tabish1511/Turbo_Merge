from django.db import models
from django.contrib.auth.models import User

class PDFDoc(models. Model):
    upload = models.FileField(upload_to='')
    custom_integer = models.IntegerField(choices=[(0, 'Zero'),(1, 'One'), (2, 'Two'), (3, 'Three')], null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    key = models.CharField(max_length=36, blank=True, null=True)

    def __str__(self):
        return self.upload.name
    
