from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from uploads.models import Document
from uploads.forms import DocumentForm
from . import filehandler #import write_file_to_disk, save_file
from . import backend
import time
import datetime

#for running model
from . import apply_model

#for services (django rest framework)
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view


#for services - testing
@api_view(['GET']) # , 'POST'])
def backend_details(request):
    if request.method == 'GET':
        print("backend_details::get called")
        return Response({
            'test': 'this is a test string',
            'junk': 'contains junk'
        })

#for services - testing

def index(request):
    return HttpResponse("Hello, world, I am index in /uploads")

def dq(request):
    status = 200
    if request.method== 'POST':
        #this is the part of the view that gets called when someone sees the below upload dialog and attempts to POST a file
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # do we really want to write to disk just in case?
            form_file = request.FILES['file']
            filename = form_file.name
            docfile = Document(file=form_file, filename=filename, creation_date=datetime.datetime.now())           
            print(docfile.creation_date)
            print(docfile.filename)
            destination = 'tmp/' + filename
            filehandler.write_file_to_disk(form_file, destination)

            pre_data = preprocess_data(request)
            #pre_data = 'dummy pre data'

            #process file: maybe this will be the handler for showing the progress bar or something
            #filehandler.process_file(form_file)

            #return HttpResponse('file written to ' + destination)
            return render(request, 'uploads/results.html', {'form':form, 'filename':filename, 'pre_data':pre_data})
        else:
            print("This is some kind of error")
    else:
        #this is the part of the view that is brought up first (to show file upload dialog)
        form = DocumentForm()
    return render(request, 'uploads/dq.html', {'form':form}, status=status)
        
def results(request):
    return render(request, 'uploads/results.html', {'form':form, 'filename':filename}, status=status)

def home(request):
    form = DocumentForm()
    return render(request, 'uploads/dq.html', {'form':form})

def about(request):
    return render(request, 'uploads/about.html', {})

def contact(request):
    return render(request, 'uploads/contact.html', {})

def preprocess_data(request):
    form_file = request.FILES['file']
    filename = form_file.name
    filepath = 'tmp/' + filename

    #lets try running the model here? does this need to be async?
    apply_model.run(filepath)
    print("DONE RUNNING MODEL")
    #fake processing here
    print("processing processing")
    pre_data = backend.preprocess_data("testfilename")
    print(pre_data)
    data = {
        'pre_viz': pre_data.get('viz'),
        'pre_stats': pre_data.get('stats')
    }
    time.sleep(5)
    return data
