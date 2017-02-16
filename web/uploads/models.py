from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to='fileuploads/')
    filename = models.CharField(max_length=200) 
    creation_date = models.DateTimeField(auto_now_add=True)  #denotes when the object first created
    def __str__(self):
        return self.filename
