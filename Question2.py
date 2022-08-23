#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import json


# In[3]:


f = open('Outputs/neighbor-districts-modified.json')

data = json.load(f)

f.close()


# In[4]:


# data


# In[5]:


len(data)


# In[7]:


df = pd.DataFrame(columns=['node1','node2'])
# df


# In[8]:


list1 = []
for k,v in data.items():
    list1.append(k)
    for neigh in v:
        if neigh not in list1:
            df.loc[len(df.index)] = [k,neigh]


# In[9]:


# df


# In[ ]:


df.to_csv('Outputs/edge-graph.csv',index=False)

