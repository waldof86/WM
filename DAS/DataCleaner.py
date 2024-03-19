# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 23:01:07 2020

@author: Marcos Buccellato
"""
import json
import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
from CleaningLibrary import synonym_sustitution,find_nearest_match
    
G = nx.Graph()
data = pd.read_excel (r'results_profiles.xlsx')
data['Educación'] = [json.loads(obj) for obj in [obj for obj in data['Educación'].values]]     
data['Trabajos'] = [json.loads(obj) for obj in [obj for obj in data['Trabajos'].values]]     


syn_dict = pd.read_csv("Institutions.csv") 
forb_inst =["Autónomo"]
inst= []
for person in data.index:   
    prs_name=data['Nombre'][person]
    G.add_node(prs_name, tipo='Persona')
    for degree in data['Educación'][person]:
        insti = synonym_sustitution(syn_dict,degree['institution'].strip())
        if (insti not in inst) and (insti !='') and (insti not in forb_inst):
            G.add_node(insti, tipo='Institución')
            inst.append(insti)
        if (insti  !='') and (insti not in forb_inst):
            if not (G.has_edge(prs_name,insti)) : 
                G.add_edge(prs_name,insti, v=1)
            else :
                G.add_edge(prs_name,insti,v=G[prs_name][insti]['v']+1)
                
    for trabajo in data['Trabajos'][person]:
        comp = synonym_sustitution(syn_dict,trabajo['company']['name'].strip())
        if (comp not in inst) and (comp !='')  and (comp not in forb_inst):
            G.add_node(comp, tipo='Institución' )
            inst.append(comp)
        if (comp !='') and (comp not in forb_inst):
            if not (G.has_edge(prs_name,comp)) : 
                G.add_edge(prs_name,comp, v=1)
            else :
                G.add_edge(prs_name,comp,v=G[prs_name][comp]['v']+1)

simil_analisis = find_nearest_match(inst,0.5,1000)

personas = [x for x,y in G.nodes(data=True) if y['tipo']=="Persona"]
instituciones = [x for x,y in G.nodes(data=True) if y['tipo']=="Institución"]

import matplotlib.pyplot as plt
plt.figure(figsize=(20, 20))
pos = nx.spring_layout(G,k=0.1,iterations=20)


#Grafo Bipartito

plt.title("Actores e Instituciones")
node_size = [[G.degree(v)*40,10][not (nx.get_node_attributes(G, 'tipo')[v]=="Institución")] for v in G]
node_color = [0.0005*[1, 2][nx.get_node_attributes(G, 'tipo')[v]=="Institución"] for v in G]
edge_width = [1.5*G[u][v]['v'] for u,v in G.edges()]
#nx.draw_networkx(G, pos,font_size=7, node_color=node_color, node_size=node_size,alpha=0.7,width=edge_width,edge_color='.4');

node_size = [[G.degree(v)*10,10][not (nx.get_node_attributes(G, 'tipo')[v]=="Persona")] for v in personas]
node_alpha = [[G.degree(v)*0.1,10][not (nx.get_node_attributes(G, 'tipo')[v]=="Institución")] for v in instituciones]
nx.draw_networkx_nodes(G, pos, instituciones, node_color="b", node_size=200,alpha=node_alpha, label=instituciones)
nx.draw_networkx_nodes(G, pos, personas, node_color="r", node_size=node_size,alpha=0.8)
edges=nx.draw_networkx_edges(G,pos,width=edge_width)
nx.draw_networkx_labels(G, pos, font_size=6)
edge_labels = nx.draw_networkx_edge_labels(G, pos,font_size=6)
#Grafo Proyectando las personas que |están relacionadas por pertenencias institucionales en general

plt.title("Proyección de relaciones entre actores en base a vínculos institucionales")
P =bipartite.weighted_projected_graph(G, personas,False)
edge_width = [1.5*P[u][v]['weight'] for u,v in P.edges()]
node_size = [P.degree(v)*100 for v in P]
plt.figure(figsize=(8, 8))
nx.draw_networkx(P,pos,font_size=7,alpha=0.7,width=edge_width,node_size=node_size)
#nx.draw_networkx_edge_labels(P, pos, font_size=6)
plt.show()


nx.write_gexf(G, "Bipartite-Gephi.gexf")
nx.write_gexf(G, "Bipartite-Proy-Person-Gephi.gexf")

'''
############################plotly########################################

from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import plotly.graph_objs as go
import chart_studio.plotly as plotly
import chart_studio as cs

for n, p in pos.items():
    G.nodes[n]['pos'] = p
    
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G.edges(): 
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])
    
node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='RdBu',
        reversescale=True,
        color=[],
        size=15,
        colorbar=dict(
            thickness=10,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)))

for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])

for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['color']+=tuple([len(adjacencies[1])])
    node_info = adjacencies[0] +' # of connections: '+str(len(adjacencies[1]))
    node_trace['text']+=tuple([node_info])

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>AT&T network connections',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="No. of connections",
                    showarrow=False,
                    xref="paper", yref="paper") ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))


#cs.tools.set_credentials_file(username='mbuccellato', api_key='RF0aUxXJIgWbxX3ZD6sZ')
#iplot(fig,"mbuccellato",filename="Network Graph.html")

iplot(fig)
#plotly.plot(fig)
'''

####################EDUCACIÓN##########################################3
    
G = nx.MultiGraph()


inst= []
for person in data.index:   
    prs_name=data['Nombre'][person]
    G.add_node(prs_name, tipo='Persona')
    for degree in data['Educación'][person]:
        insti = synonym_sustitution(syn_dict,degree['institution'].strip())
        if (insti not in inst) and (insti !='') and (insti not in forb_inst):
            G.add_node(insti, tipo='Institución')
            inst.append(insti)
        if (insti  !='') and (insti not in forb_inst):
            if not (G.has_edge(prs_name,insti)) : 
                G.add_edge(prs_name,insti, label=degree['degree'])
            else :
                G.add_edge(prs_name,insti,label=degree['degree'])

simil_analisis = find_nearest_match(inst,0.5,1000)

personas = [x for x,y in G.nodes(data=True) if y['tipo']=="Persona"]

import matplotlib.pyplot as plt
plt.figure(figsize=(20, 20))
pos = nx.spring_layout(G,k=0.1,iterations=20)

#Grafo Bipartito
plt.title("Actores e Instituciones Educativas")
node_size = [[G.degree(v)*40,10][not (nx.get_node_attributes(G, 'tipo')[v]=="Institución")] for v in G]
node_color = [0.0005*[1, 2][nx.get_node_attributes(G, 'tipo')[v]=="Persona"] for v in G]
edge_width = 1.5
nx.draw_networkx(G, pos,font_size=7, node_color=node_color,node_size=node_size,alpha=0.7,width=edge_width,edge_color='.4');
nx.draw_networkx_edge_labels(G, pos, font_size=6)

##############################################333
