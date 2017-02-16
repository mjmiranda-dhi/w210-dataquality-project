from django.shortcuts import render
from django.http import HttpResponse

from uploads.models import Document
from uploads.forms import DocumentForm
from . import filehandler #import write_file_to_disk, save_file

import datetime

def index(request):
    return HttpResponse("Hello, world, I am index in /uploads")

def dq(request):
    if request.method== 'POST':
        #this is the part of the view that gets called when someone sees the below upload dialog and attempts to POST a file
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            something = request.FILES['file']
            filename = something.name
            docfile = Document(file=something, filename=filename, creation_date=datetime.datetime.now())           
            print(docfile.creation_date)
            print(docfile.filename)
            destination = 'tmp/' + filename
            filehandler.write_file_to_disk(something, destination)
        return HttpResponse('file written to ' + destination)
    else:
        #this is the part of the view that is brought up first (to show file upload dialog)
        form = DocumentForm()
    return render(request, 'uploads/dq.html', {'form':form})
        
