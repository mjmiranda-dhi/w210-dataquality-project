
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

#Import ploty
import plotly 
import pandas as pd
import numpy as np
import re
import plotly.plotly as py
import plotly.graph_objs as go
#import plotly.figure_factory as ff
from plotly.tools import FigureFactory as ff
import igraph
from igraph import *
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *
plotly.offline.init_notebook_mode()


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

            #kickoff model run
            pre_data = process_data(request)
            #pre_data = 'dummy pre data'

            #generate pre-processing data viz
            pre_data = preprocess_data_viz(request)
            

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

def process_data(request):
    form_file = request.FILES['file']
    filename = form_file.name
    filepath = 'tmp/' + filename

    #lets try running the model here? does this need to be async?
    apply_model.run(filepath)
    print("DONE RUNNING MODEL")
    #fake processing here
    # print("processing processing")
    # pre_data = backend.preprocess_data("testfilename")
    # print(pre_data)
    # data = {
    #     'pre_viz': pre_data.get('viz'),
    #     'pre_stats': pre_data.get('stats'),
    #     'html': '<div>Hello World</div>'
    # }
    # time.sleep(5)
    data = {}
    return data

def preprocess_data_viz(request):
    form_file = request.FILES['file']
    filename = form_file.name
    filepath = 'tmp/' + filename
    
    #1 Load data and structure for further process
    #Please change your director for the input files
    input_data_pd = pd.read_csv(filepath, delimiter = ",")
    input_data_pd = input_data_pd.replace(np.nan,'', regex=True)
    hierarchy_col = ['level_1', 'level_2', 'level_3', 'level_4', 'level_5', 'level_6', 'level_7']
    input_data_pd['combined'] = ''

    for i in hierarchy_col:
        input_data_pd['combined'] = input_data_pd['combined'].astype(str) +'**'+ input_data_pd[i].astype(str)

    input_data_pd['combined'] = input_data_pd['combined'].apply(lambda x: re.sub(r'.*Best Buy', 'Best Buy', x))

    #Main Cell for creating levels
    #Find all the unique combinations
    n_levels = len(hierarchy_col)
    tree_data = input_data_pd['combined'].unique()


    # #Clean Errors in the raw data
    # for i in range(len(tree_data)):
    #     tree_data[i] = unicode(tree_data[i], errors='ignore')

    levels = []
    for i in range(0,n_levels):
        levels.append([])
    total_level = 0

    #Not sure the purpose
    pair_len = []
    for i in range(len(tree_data)):  
        current_data_pre = tree_data[i].split("**")
        current_data = []
        for i in current_data_pre:
            if i not in '':
                current_data.append(i)

        for i in range(n_levels):
            if len(current_data) > i and current_data[i] not in levels[i]:
                levels[i].append(current_data[i])

    #First Graph
    data_matrix = [['Level', 'Category Count']]

    for i in range(n_levels):
        data_matrix.append(['Level %d' % (i+1), len(levels[i])])   

    #data_matrix
    table = ff.create_table(data_matrix)
    #iplot(table, filename='simple_table')

    #Use the code below if want to generate HTML instead
                            #NOTE: need to write to uploads/static
    plotly.offline.plot(table, filename='uploads/static/img/viz_pre_table.html', auto_open=False)
    #TODO eventually this needs to be loaded and displayed, how????
    time.sleep(10)    

    data = {
        # NOTE: to display, we need to use /static/img not uploads/static/img
        'pre_viz': '/static/img/viz_pre_table.html',
        'pre_stats': 'tmp/viz_pre_table.html',
        'html': '<div>Hello World</div>'
    }

    print(data)
    return data
