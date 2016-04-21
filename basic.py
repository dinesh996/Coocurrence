import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import itertools

#loading json into df
main_df= pd.read_json("products_22_03.json")


#making tags into a singular item list.
tags= main_df.loc[:,'tags']
tags=list(tags)
tags=[i for j in tags for i in j]
tags_set= set(tags)
tags_list=list(tags_set)
tags_list.remove('')
tags_list.remove('.')


#Making graph and adding nodes in it.
tags_graph= nx.Graph()
tags_graph.add_nodes_from(tags_list)


#Making co-occurence matrix:
m1= pd.DataFrame(index= main_df.index, columns= tags_list)
for i,j in zip(m1.index,main_df.loc[:,'tags']):
        for k in j:
            m1.loc[i,k]=1

m1= m1.fillna(0)
cooc= m1.T.dot(m1)
np.fill_diagonal(cooc.values,0)


#Making Marginal Count Matrix
Marginal_counts= pd.Series(cooc.sum(axis=1))


#Total Counts
Total_counts= (Marginal_counts.sum()/2)



# Probability Calculation.
# a is #favourble events, b is #Total events.
def probability_cal(a,b):
	return a/b



# Denoising:
# Defining NMI
def NMI(mut_ab,a_alone,b_alone,total):
     return np.log(cal_probab(mut_ab,total)/(cal_probab(a_alone,total)*cal_probab(b_alone,total)))/np.log(1/cal_probab(mut_ab,total))



#Denoising Algorithm

NMI_matrix= pd.DataFrame(index= cooc1.index, columns= cooc1.columns)
NMI_margin_counts= Marginal_counts.copy()
Total_counts= pd.Series(Total_counts, index=Marginal_counts)
NMI_Total_counts= Total_counts.copy()
cooc1=cooc.copy()

# For differentiating several concepts.
# What's the condition for convergence of our cooc1 matrix.
for i in range(8):
    NMI_margin= pd.Series(cooc1.sum(axis=1),index= cooc1.index)
    NMI_Total= NMI_margin.sum()/2
    for i in cooc1.index:
        for j in cooc1.columns:
            NMI_matrix.loc[i,j]= nmi(cooc1.loc[i,j], NMI_margin[i], NMI_margin[j], NMI_Total)
    NMI_matrix =NMI_matrix[NMI_matrix>0.001]
    NMI_matrix= NMI_matrix.fillna(0)
    cooc1= NMI_matrix*cooc1

cooc1= cooc1.fillna(0)


# Making list of all edges with it's weight.
edge_list=[]
for i in cooc1.index:
    for j in cooc1.columns:
        if (cooc1.loc[i,j]>0):
            l1= [i,j,cooc1.loc[i,j]]
            edge_list.append(l1)


#Adding Edges to the graph.
tags_graph.add_weighted_edges_from(edge_list)





# Grow-Shrink Greedy Algorithm.



if __name__='__main__':
