from django.shortcuts import render, get_object_or_404
from .forms import UploadFileForm
from .models import UploadFile

#from django.core.files.storage import FileSystemStorage

def index(request):
	if request.user.is_authenticated():
		pass
	
	if request.method == "POST":
		print(request.POST)

	form = UploadFileForm()
	uploadedFiles = UploadFile.uploaded.all()

	context = {
		"form": form,
		"uploadedFiles": uploadedFiles,
	}
	
	return render(request, "demo.html", context)


def upload_list(request):
	uploadedFiles = UploadFile.uploaded.all()
	
	context = {
		"uploadedFiles": uploadedFiles,
	}
	
	return render(request, "list.html", context)


def upload_detail_for_user(request, userName):
	file = get_object_or_404(UploadFile,
		userName=userName,
		uploadSuccessful=True
		)

	context = {
		"userName": userName,
		"file": file,
	}
	
	return render(request, "list.html", context)


def fail_list(request):
	failedFiles = UploadFile.failed.all()

	context = {
		"failedFiles": failedFiles,
	}

	return render(request, "list.html", context)