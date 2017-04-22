from django.contrib import admin
from .models import UploadFile 
from .forms import UploadFileForm

# Register your models here.

class UploadFileAdmin(admin.ModelAdmin):
	list_display = ["userName", "timestamp", "fileOrig", "uploadSuccessful"]
	form = UploadFileForm
#	class Meta:
#		model = UploadFile

admin.site.register(UploadFile, UploadFileAdmin)