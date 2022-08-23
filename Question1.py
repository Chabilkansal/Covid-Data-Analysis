#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
import numpy as np
from copy import deepcopy
import difflib


# In[2]:


f = open('./1630261414_neighbor-districtsjson_/neighbor-districts.json',)

data = json.load(f)

f.close()


# In[3]:


# data


# In[4]:


df = pd.read_csv('cowin_vaccine_data_districtwise.csv')
# df


# In[5]:


newdata = deepcopy(data)


# In[6]:


def most_frequent(List):
    return max(set(List), key = List.count)


# In[7]:


newdata['mohali/Q2037672'] = newdata['sahibzada_ajit_singh_nagar/Q2037672']
for i in newdata['mohali/Q2037672']:
    newdata[i] = newdata[i] + ['mohali/Q2037672']
    newdata[i] = list(set(newdata[i]) - set(['sahibzada_ajit_singh_nagar/Q2037672']))
del newdata['sahibzada_ajit_singh_nagar/Q2037672']


newdata['west_champaran/Q100124'] = newdata['pashchim_champaran/Q100124']
for i in newdata['west_champaran/Q100124']:
    newdata[i] = newdata[i] + ['west_champaran/Q100124']
    newdata[i] = list(set(newdata[i]) - set(['pashchim_champaran/Q100124']))
del newdata['pashchim_champaran/Q100124']


newdata['ayodhya/Q1814132'] = newdata['faizabad/Q1814132']
for i in newdata['ayodhya/Q1814132']:
    newdata[i] = newdata[i] + ['ayodhya/Q1814132']
    newdata[i] = list(set(newdata[i]) - set(['faizabad/Q1814132']))
del newdata['faizabad/Q1814132']


newdata['bhadohi/Q127533'] = newdata['sant_ravidas_nagar/Q127533']
for i in newdata['bhadohi/Q127533']:
    newdata[i] = newdata[i] + ['bhadohi/Q127533']
    newdata[i] = list(set(newdata[i]) - set(['sant_ravidas_nagar/Q127533']))
del newdata['sant_ravidas_nagar/Q127533']


newdata['balasore/Q2022279'] = newdata['baleshwar/Q2022279']
for i in newdata['balasore/Q2022279']:
    newdata[i] = newdata[i] + ['balasore/Q2022279']
    newdata[i] = list(set(newdata[i]) - set(['baleshwar/Q2022279']))
del newdata['baleshwar/Q2022279']


newdata['ranga_reddy/Q15388'] = newdata['rangareddy/Q15388']
for i in newdata['ranga_reddy/Q15388']:
    newdata[i] = newdata[i] + ['ranga_reddy/Q15388']
    newdata[i] = list(set(newdata[i]) - set(['rangareddy/Q15388']))
del newdata['rangareddy/Q15388']


newdata['karbi_anglong/Q42558'] = newdata['east_karbi_anglong/Q42558']
for i in newdata['karbi_anglong/Q42558']:
    newdata[i] = newdata[i] + ['karbi_anglong/Q42558']
    newdata[i] = list(set(newdata[i]) - set(['east_karbi_anglong/Q42558']))
del newdata['east_karbi_anglong/Q42558']


newdata['vijayapura/Q1727570'] = newdata['bijapur_district/Q1727570']
for i in newdata['vijayapura/Q1727570']:
    newdata[i] = newdata[i] + ['vijayapura/Q1727570']
    newdata[i] = list(set(newdata[i]) - set(['bijapur_district/Q1727570']))
del newdata['bijapur_district/Q1727570']


newdata['palakkad/Q1535742'] = newdata['palghat/Q1535742']
for i in newdata['palakkad/Q1535742']:
    newdata[i] = newdata[i] + ['palakkad/Q1535742']
    newdata[i] = list(set(newdata[i]) - set(['palghat/Q1535742']))
del newdata['palghat/Q1535742']


newdata['subarnapur/Q1473957'] = newdata['sonapur/Q1473957']
for i in newdata['subarnapur/Q1473957']:
    newdata[i] = newdata[i] + ['subarnapur/Q1473957']
    newdata[i] = list(set(newdata[i]) - set(['sonapur/Q1473957']))
del newdata['sonapur/Q1473957']


newdata['Beed/Q814037'] = newdata['bid/Q814037']
for i in newdata['Beed/Q814037']:
    newdata[i] = newdata[i] + ['Beed/Q814037']
    newdata[i] = list(set(newdata[i]) - set(['bid/Q814037']))
del newdata['bid/Q814037']


# In[8]:


for k,v in newdata.items():
    newv = []
    for curdis in v:
        distname = curdis.split('/')[0]
        distname = distname.title()
        if distname.find('_District') != -1:
            distname = distname.replace('_District','')
        if distname.find('_') != -1:
            distname = distname.replace('_',' ')
        if distname in df['District'].unique():
            newdf = df[df['District'] == distname]
            if newdf.shape[0] > 1:
                curr_neigh_list = newdata[curdis]
                states_of_curr_neigh_dist = []
                if curr_neigh_list[0].find('/Q') != -1:
                    for curr_neigh in curr_neigh_list:
                        curr_neigh_dist = curr_neigh.split('/')[0]
                        curr_neigh_dist = curr_neigh_dist.title()
                        if curr_neigh_dist.find('_District') != -1:
                            curr_neigh_dist = curr_neigh_dist.replace('_District','')
                        if curr_neigh_dist.find('_') != -1:
                            curr_neigh_dist = curr_neigh_dist.replace('_',' ')
                        if curr_neigh_dist in df['District'].unique():
                            curr_neigh_dist_df = df[df['District'] == curr_neigh_dist]
                            if curr_neigh_dist_df.shape[0] == 1:
                                states_of_curr_neigh_dist.append(curr_neigh_dist_df.iloc[0]['District_Key'][0:2])
                        else:
                            close_curr_neigh_dist = difflib.get_close_matches(curr_neigh_dist, df['District'][1:],cutoff=0.7)
                            if len(close_curr_neigh_dist)>0:
                                curr_neigh_dist_df = df[df['District'] == close_curr_neigh_dist[0]]
                                states_of_curr_neigh_dist.append(curr_neigh_dist_df.iloc[0]['District_Key'][0:2])
                else:
                    for curr_neigh in curr_neigh_list:
                        states_of_curr_neigh_dist.append(curr_neigh[0:2])
                most_freq_state_code = most_frequent(states_of_curr_neigh_dist)
                for ind in range(newdf.shape[0]):
                    if newdf.iloc[ind]['District_Key'][0:2] == most_freq_state_code:
                        newv.append(newdf.iloc[ind]['District_Key'])

            else:   
                newv.append(newdf.iloc[0]['District_Key'])
        else:
            close_dist = difflib.get_close_matches(distname, df['District'][1:],cutoff=0.7)
            if len(close_dist)>0:
                newdf = df[df['District'] == close_dist[0]]
                newv.append(newdf.iloc[0]['District_Key'])
#             else:
#                 print(k,' ',distname)
    
    newdata[k] = newv

newdata


# In[9]:


# f = open('values_modified_neighbours.json','w')
  
# json.dump(newdata, f, indent = 6)

# f.close()


# In[10]:


# f = open('values_modified_neighbours.json',)

# newdata = json.load(f)

# f.close()


# In[11]:


newdata


# In[12]:


for k in list(newdata):
    distname = k.split('/')[0]
    distname = distname.title()
    if distname.find('_District') != -1:
        distname = distname.replace('_District','')
    if distname.find('_') != -1:
            distname = distname.replace('_',' ')
    if distname in df['District'].unique():
        newdf = df[df['District'] == distname]
        if newdf.shape[0] > 1:
            curr_neigh_list = newdata[k]
            states_of_curr_neigh_dist = []
            for curr_neigh in curr_neigh_list:
                states_of_curr_neigh_dist.append(curr_neigh[0:2])
            most_freq_state_code = most_frequent(states_of_curr_neigh_dist)
            for ind in range(newdf.shape[0]):
                if newdf.iloc[ind]['District_Key'][0:2] == most_freq_state_code:
                    newdata[newdf.iloc[ind]['District_Key']] = newdata[k]
        else:
            newdata[newdf.iloc[0]['District_Key']] = newdata[k]
        del newdata[k]
    else:
        close_dist = difflib.get_close_matches(distname, df['District'][1:],cutoff=0.7)
        if len(close_dist)>0:
            newdf = df[df['District'] == close_dist[0]]
            newdata[newdf.iloc[0]['District_Key']] = newdata[k]
            del newdata[k]

newdata


# In[13]:


len(newdata)


# In[14]:


# f = open('key_modified_neighbours.json','w')
  
# json.dump(newdata, f, indent = 6)

# f.close()


# In[15]:


newjson = deepcopy(newdata)


# In[16]:


newjson['JH_West Singhbhum'] = newjson['JH_East Singhbhum']
for i in newjson['JH_West Singhbhum']:
    newjson[i] = newjson[i] + ['JH_West Singhbhum']


newjson['WB_Cooch Behar'] = newjson['kochbihar/Q2728658']
for i in newjson['kochbihar/Q2728658']:
    newjson[i] = newjson[i] + ['WB_Cooch Behar']
del newjson['kochbihar/Q2728658']


newjson['AP_S.P.S. Nellore'] = newjson['sri_potti_sriramulu_nellore/Q15383']
for i in newjson['sri_potti_sriramulu_nellore/Q15383']:
    newjson[i] = newjson[i] + ['AP_S.P.S. Nellore']
del newjson['sri_potti_sriramulu_nellore/Q15383']


newjson['PB_Sri Muktsar Sahib'] = newjson['muktsar/Q1947359']
for i in newjson['muktsar/Q1947359']:
    newjson[i] = newjson[i] + ['PB_Sri Muktsar Sahib']
del newjson['muktsar/Q1947359']


newjson['GJ_Dang'] = newjson['the_dangs/Q1135616']
for i in newjson['the_dangs/Q1135616']:
    newjson[i] = newjson[i] + ['GJ_Dang']
del newjson['the_dangs/Q1135616']


newjson['UP_Amroha'] = newjson['jyotiba_phule_nagar/Q1891677']
for i in newjson['jyotiba_phule_nagar/Q1891677']:
    newjson[i] = newjson[i] + ['UP_Amroha']
del newjson['jyotiba_phule_nagar/Q1891677']


newjson['UP_Lakhimpur Kheri'] = newjson['kheri/Q1755447']
for i in newjson['kheri/Q1755447']:
    newjson[i] = newjson[i] + ['UP_Lakhimpur Kheri']
del newjson['kheri/Q1755447']


newjson['BR_Kaimur'] = newjson['kaimur_(bhabua)/Q77367']
for i in newjson['kaimur_(bhabua)/Q77367']:
    newjson[i] = newjson[i] + ['BR_Kaimur']
del newjson['kaimur_(bhabua)/Q77367']


newjson['WB_Hooghly'] = newjson['hugli/Q548518']
for i in newjson['hugli/Q548518']:
    newjson[i] = newjson[i] + ['WB_Hooghly']
del newjson['hugli/Q548518']


newjson['JH_East Singhbhum'] = newjson['purbi_singhbhum/Q2452921']
for i in newjson['purbi_singhbhum/Q2452921']:
    newjson[i] = newjson[i] + ['JH_East Singhbhum']
del newjson['purbi_singhbhum/Q2452921']


newjson['CT_Dakshin Bastar Dantewada'] = newjson['dantewada/Q100211']
for i in newjson['dantewada/Q100211']:
    newjson[i] = newjson[i] + ['CT_Dakshin Bastar Dantewada']
del newjson['dantewada/Q100211']


newjson['KA_Belagavi'] = newjson['belgaum_district/Q815464']
for i in newjson['belgaum_district/Q815464']:
    newjson[i] = newjson[i] + ['KA_Belagavi']
del newjson['belgaum_district/Q815464']


newjson['AP_Y.S.R. Kadapa'] = newjson['ysr/Q15342']
for i in newjson['ysr/Q15342']:
    newjson[i] = newjson[i] + ['AP_Y.S.R. Kadapa']
del newjson['ysr/Q15342']


# In[17]:


# f = open('manual_change_neighbours.json','w')
  
# json.dump(newjson, f, indent = 6)

# f.close()


# In[18]:


del newjson['konkan_division/Q6268840']
del newjson['niwari/Q63563797']
del newjson['noklak/Q48731903']
del newjson['mumbai_suburban/Q2085374']
del newjson['mohali/Q2037672']


# In[19]:


# f = open('spell-corrected-neighbor-districts.json','w')
  
# json.dump(newjson, f, indent = 6)

# f.close()


# In[20]:


coviddf = pd.read_csv('districts.csv')
coviddf


# In[21]:


merge_state_list = []
for cur_state in coviddf['State'].unique():
    cur_state_districts = coviddf[coviddf['State']==cur_state]['District'].unique()
    if (len(cur_state_districts)==1) and (cur_state_districts[0] =='Unknown'):
        merge_state_list.append(cur_state)
#         print(f'unknown district {cur_state}')
    if (len(cur_state_districts)==1) and (cur_state_districts[0] ==cur_state):
        merge_state_list.append(cur_state)
#         print(f'state district {cur_state}')


# In[22]:


merge_state_list


# In[23]:


merge_state_list = list(set(merge_state_list) - set(['Andaman and Nicobar Islands','Lakshadweep','Chandigarh']))
merge_state_list


# In[24]:


df[df['State']=='Delhi']['District_Key']


# In[25]:


mergejson = deepcopy(newjson)


# In[26]:


def merge_districts(jsondata, state):
    dist_list = list(df[df['State']==state]['District_Key'])
    state_code = list(df[df['State'] == state]['State_Code'])[0]
    new_dist = state_code + '_' + state
    new_dist_neigh = []
    
    old_dists_neigh = []
    for dist in dist_list:
        old_dists_neigh += jsondata[dist]
    for dist in old_dists_neigh:
        jsondata[dist] = list(set(jsondata[dist]) - set(dist_list))
        jsondata[dist] = list(set(jsondata[dist]) - set([new_dist]))
        jsondata[dist] = jsondata[dist] + [new_dist]
    
    
    for dist in dist_list:
        new_dist_neigh += jsondata[dist]
    new_dist_neigh = list(set(new_dist_neigh) - set(dist_list))
    new_dist_neigh = list(set(new_dist_neigh) - set([new_dist]))
    jsondata[new_dist] = new_dist_neigh
    for dist in dist_list:
        del jsondata[dist]


# In[27]:


for state in merge_state_list:
#     print(state)
    merge_districts(mergejson,state)


# In[28]:


# f = open('merged-neighbor-districts.json','w')
  
# json.dump(mergejson, f, indent = 6)

# f.close()


# In[29]:


len(mergejson)


# # Merge Vaccination csv

# In[ ]:





# In[30]:


del_dist = list(set(df['District'].unique())-set(coviddf['District'].unique()))
del_dist


# In[31]:


list(set(coviddf['District'].unique())-set(df['District'].unique()))


# In[32]:


del_json = deepcopy(mergejson)


# In[33]:


def deleteDist(jsondata,dist_key):
    try:
        neigh_list = jsondata[dist_key]
        for neigh in neigh_list:
            jsondata[neigh] = list(set(jsondata[neigh]) - set([dist_key]))
        del jsondata[dist_key]
    except:
        pass


# In[34]:


for dist in del_dist[1:]:
    newdf = df[df['District'] == dist]
    if newdf.shape[0]>1:
        # print(f'Duplicates {dist}')
    deleteDist(del_json, newdf.iloc[0]['District_Key'])


# In[35]:


len(del_json)


# In[36]:


f = open('Outputs/neighbor-districts-modified.json','w')
  
json.dump(del_json, f, indent = 6)

f.close()

