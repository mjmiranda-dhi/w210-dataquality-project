#Import ploty
import plotly 
import pandas as pd
import numpy as np
import re
import plotly 
plotly.tools.set_credentials_file(username='judofighter25', api_key='2peX3o9wbzRxT5vM2azA')

plotly.tools.set_config_file(world_readable=False,
                             sharing='private')

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import igraph
from igraph import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *
plotly.offline.init_notebook_mode()


#1 Load data and structure for further process
#Please change your director for the input files
input_data_pd = pd.read_csv("/Users/Maximus/Desktop/Master of Information and Data Science\
/W210 Capstone/Attachments_201721/modified_input.csv", delimiter = ",")

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


#Clean Errors in the raw data
for i in range(len(tree_data)):
  tree_data[i] = unicode(tree_data[i], errors='ignore')

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
plotly.offline.plot(table, filename='file.html')


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
  current_data = tree_data[i].split("**")
  current_data = filter(None, current_data)

  
  ##Update
  if current_data[0] not in root_node_list and current_data[0] != '':
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
v_label = map(str, range(total_category))
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


###########################
###########################
def make_annotations(pos, text, font_size=7, font_color='rgb(250,250,250)'):
    L=len(pos)
    if len(text)!=L:
        raise ValueError('The lists pos and text must have the same len')
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
############################
############################
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
              annotations=make_annotations(position, v_label),
              font=dict(size=12),
              showlegend=False,
              xaxis=go.XAxis(axis),
              yaxis=go.YAxis(axis),          
              margin=dict(l=40, r=40, b=85, t=100),  #dict(l=40, r=40, b=85, t=100)
              hovermode='closest',
              plot_bgcolor='rgb(64,64,64)')   
              

data=go.Data([lines, dots])
fig=dict(data=data, layout=layout)
fig['layout'].update(annotations=make_annotations(position, levels_v2)) #v_label

#iplot(fig, filename='Graph_Plot')

plotly.offline.plot(fig, filename='tree_graph.html')