
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from uploads.models import Document
from uploads.forms import DocumentForm
from . import filehandler #import write_file_to_disk, save_file
from . import backend
import time
import datetime

#filedownloads
import os, tempfile, zipfile
from wsgiref.util import FileWrapper
from django.conf import settings
import mimetypes

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
            model_data = process_data(request)
            #pre_data = 'dummy pre data'
            print("model data", model_data)

            #generate pre-processing data viz
            pre_data = preprocess_data_viz(request)
            post_data = postprocess_data_viz(model_data['processed_filename'])            

            #process file: maybe this will be the handler for showing the progress bar or something
            #filehandler.process_file(form_file)

            #return HttpResponse('file written to ' + destination)
            return render(request, 'uploads/results.html', 
                {'form':form, 'filename':filename, 'pre_data':pre_data,
                'model_data':model_data, 'post_data':post_data})
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

def send_file(request):
    filename     = "/static/img/output.csv" # Select your file here.
    download_name ="output.csv"
    wrapper      = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response     = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response

def process_data(request):
    form_file = request.FILES['file']
    filename = form_file.name
    filepath = 'tmp/' + filename
    summary_df = None
    demo = False
    #tmp
    if 'master_products_5per_modified.csv' in filename:
        demo = True

    #lets try running the model here? does this need to be async?
    if not demo:
        summary_df = apply_model.run_full(filepath)
        decimals = pd.Series([2, 2], index=['SZ_mean', 'SZ_std'])
        summary_df = summary_df.round(decimals)

        #Generating Initial First Table To Inspect Data
        table_s = ff.create_table(summary_df)
        table_s.layout.margin.update({'t':50, 'l':50})
        table_s.layout.update({'title': 'Summary Statistics'})
        #Use the code below if want to generate HTML instead
        plotly.offline.plot(table_s, filename='/static/img/file_stat.html', auto_open=False)

    print("DONE RUNNING MODEL")

    if not demo:
        data = {
            'processed_filename':'uploads/static/img/output.csv',
            'model_summary':'uploads/static/img/static/img/master_products_5per_modified_file_stat.html',
            'testing_text':'this is sample model text'
        }
    else:
        data = {
            'processed_filename':'uploads/static/img/master_products_5per_modified_model_output.csv',
            'model_summary':'/static/img/master_products_5per_modified_file_stat.html',
            'testing_text':'this is sample model text'
        }
    return data

def preprocess_data_viz(request):
    form_file = request.FILES['file']
    filename = form_file.name
    filepath = 'tmp/' + filename
    demo = False
    #mvp
    if filename == 'master_products_5per_modified.csv':
        demo = True

    stats_filename = 'viz_pre_table.html'
    graph_filename = 'viz_pre_tree_graph.html'
    return viz_process_data(filepath, stats_filename, graph_filename, demo)

def postprocess_data_viz(filepath):
    print("POSTPROCESS FILEPATH", filepath)
    stats_filename = 'viz_post_table.html'
    graph_filename = 'viz_post_tree_graph.html'
    demo = False
    #mvp
    if filepath == 'master_products_5per_modified.csv':
        demo = True
    return viz_process_data(filepath, stats_filename, graph_filename, demo)

def viz_process_data(filepath, stats_filename, graph_filename, demo):
    #1 Load data and structure for further process
    #Please change your director for the input files
    if demo:
        if 'master_products_5per_modified' in filepath:
            if "pre" in stats_filename:
                data = {
                    #MVP
                    'stats': '/static/img/master_products_5per_modified_viz_pre_table.html',
                    'graph': '/static/img/master_products_5per_modified_viz_pre_tree_graph.html',
                }
                return data
            else:
                data = {
                    #MVP
                    'stats': '/static/img/master_products_5per_modified_viz_post_table.html',
                    'graph': '/static/img/master_products_5per_modified_viz_post_tree_graph.html',
                }
                return data

    input_data_pd = pd.read_csv(open(filepath,'r'), delimiter = ",") #, encoding='cp857')
    input_data_pd = input_data_pd.replace(np.nan,'', regex=True)
    hierarchy_col = ['level_1', 'level_2', 'level_3', 'level_4'] #, 'level_5', 'level_6', 'level_7']
    input_data_pd['combined'] = ''

    for i in hierarchy_col:
        input_data_pd['combined'] = input_data_pd['combined'].astype(str) +'**'+ input_data_pd[i].astype(str)

    input_data_pd['combined'] = input_data_pd['combined'].apply(lambda x: re.sub(r'.*Best Buy', 'Best Buy', x))

    #Main Cell for creating levels
    #Find all the unique combinations
    n_levels = len(hierarchy_col)
    tree_data = input_data_pd['combined'].unique()


    # #Clean Errors in the raw data
    #for i in range(len(tree_data)):
    #    tree_data[i] = unicode(tree_data[i], errors='ignore')

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
    table.layout.margin.update({'t':50, 'l':50})
    table.layout.update({'title': 'Unique values in each level of the hierarchy'})
    #iplot(table, filename='simple_table')

    #Use the code below if want to generate HTML instead
                            #NOTE: need to write to uploads/static
    write_stats_filename = 'uploads/static/img/' + stats_filename 
    plotly.offline.plot(table, filename=write_stats_filename, auto_open=False)
    #TODO eventually this needs to be loaded and displayed, how????
    #time.sleep(10)    


    #### CREATE GRAPH
    ##############################################
    #####        Graph Model        ##############
    #############################################

    tracker = {}
    #levels_v2: A flat list of values for labeling
    levels_v2 =  [item for sublist in levels for item in sublist]

    root_node_list = []
    root_node_counter = 0
    edge_list = []

    for i in range(len(tree_data)):
        temp = tree_data[i].split("**")
    #current_data = filter(None, current_data)
        current_data = []
        for i in temp:
            if i != '':
                current_data.append(i)
  
##Update
        if current_data and current_data[0] not in root_node_list and current_data[0] != '':
            root_node_list.append(current_data[0])
            tracker[root_node_counter] = [current_data[0]]
            root_node_counter += 1
  
  
        location = 0
        for j in range(len(current_data) - 1):
    
        #Incrementing location to match the number with the 
        #Hireachical path
            if j > 0:
                location += len(levels[j-1])
    
        #Find location in the list to update the coordinate for the pair
   
            a = levels[j].index(current_data[j]) + location
            b = levels[j+1].index(current_data[j+1]) + location + len(levels[j])
    
            pairs = (a, b)

            if pairs not in edge_list:
                edge_list.append(pairs)
      #tracker.append(current_data[:j+1])
    
    #Find way to find first records
            if b not in tracker:
                tracker[b] = current_data[:j+2]

    ################
    total_category = len(levels_v2)
    #v_label = map(str, range(total_category))

    v_label = []
    for i in range(1,total_category+1):
        v_label.append(str(i))
    
    G = Graph(n = total_category, directed=True)

    #edge_list
    G.add_edges(edge_list)
    lay = G.layout()
    position = {k: lay[k] for k in range(total_category)}


    Y = [position[k][1] for k in range(total_category)]
    M = max(Y)


    #There are edges connecting the vertices
    es = EdgeSeq(G) # sequence of edges
    E = [e.tuple for e in G.es] # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [3*M-position[k][1] for k in range(L)]  #2
    Xe = []
    Ye = []

    for edge in E:
        Xe+=[position[edge[0]][0],position[edge[1]][0], None]
        Ye+=[3*M-position[edge[0]][1],3*M-position[edge[1]][1], None] 

    labels = v_label
    #### END CREATE GRAPH

    long_name = []
    for i in range(len(tracker)):
        long_name.append(' - '.join(tracker[i]))  

    ###############################################
    lines = go.Scatter(x=Xe,
                       y=Ye,
                       mode='lines',
                       line=dict(color='rgb(255,255,0)', width=1),  #rgb(210,210,210)/ 128X3 2nd best
                       hoverinfo='none'
                       )

    dots = go.Scatter(x=Xn,
                      y=Yn,
                      mode='markers',
                      name='',
                      marker=dict(symbol='dot',
                      size=14, 
                      color='#606060',    #'#DB4551', #6175c1
                      line=dict(color='rgb(32,32,32)', width=1)
                      ),
                      text= long_name,  #levels_v2,
                      #Any combination of "x", "y", "z", "text", "name" joined with a "+" OR "all" or "none" or "skip".
                      textfont={"size":15},
                      hoverinfo='text+name',  
                      opacity=0.9)
###########################
    axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,)

    layout = dict(title= 'Overall Data Structure',  
                  annotations=make_annotations(position, v_label,labels,M,position),
                  font=dict(size=12),
                  showlegend=False,
                  xaxis=go.XAxis(axis),
                  yaxis=go.YAxis(axis),          
                  margin=dict(l=40, r=40, b=85, t=100),  #dict(l=40, r=40, b=85, t=100)
                  hovermode='closest',
                  plot_bgcolor='rgb(64,64,64)')   
              

    data=go.Data([lines, dots])
    fig=dict(data=data, layout=layout)
    fig['layout'].update(annotations=make_annotations(position, levels_v2, labels,M,position)) #v_label

    #iplot(fig, filename='Graph_Plot')

    write_graph_filename = 'uploads/static/img/' + graph_filename
    plotly.offline.plot(fig, filename=write_graph_filename, auto_open=False)

    data = {
        # NOTE: to display, we need to use /static/img not uploads/static/img
        'stats': '/static/img/'+stats_filename,
        'graph': '/static/img/'+graph_filename,
        'html': '<div>Hello World</div>'
    }
    time.sleep(5)

    print(data)
    return data


#### FOR GRAPH
def make_annotations(pos, text, labels, M,position, font_size=7, font_color='rgb(250,250,250)'):
    L=len(pos)
    #if len(textv)!=L:
        #raise ValueError('The lists pos and text must have the same len')
    annotations = go.Annotations()
    for k in range(L):
        annotations.append(
            go.Annotation(
                text=labels[k], # or replace labels with a different list for the text within the circle  
                x=pos[k][0], y=3*M-position[k][1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    return annotations 
