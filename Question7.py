#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime


# In[2]:


# Reading vaccination data in vaccine_df
vaccine_df = pd.read_csv('vaccine_data_new.csv')
vaccine_df


# In[3]:


vaccine_df3 = vaccine_df.copy()


# In[4]:


# Creating a temporary Dataframe for storing district_wise total number 
# of Covishield vaccinated persons (either 1 or 2 doses) to total number of Covaxin vaccinated persons
tempdf = vaccine_df3[['State','District','District_Key','14/08/2021.8','14/08/2021.9']]
tempdf


# In[5]:


tempdf.columns = ['State','District','District_Key','Covaxin','Covishield']
tempdf


# In[6]:


# Changing data type to numeric for mathematical computations in future
tempdf['Covaxin'] = pd.to_numeric(tempdf['Covaxin'])
tempdf['Covishield'] = pd.to_numeric(tempdf['Covishield'])
tempdf.info()


# ### Two Cells below show how some districts multiple rows for vaccination data, for this we will add these rows to find actual vaccination data for these districts

# In[7]:


tempdf[tempdf['District_Key']=='GJ_Gandhinagar']


# In[8]:


val_counts = tempdf['District_Key'].value_counts()
val_counts[val_counts>1]


# In[9]:


# Using Groupby to add multiplt rows of same district
tempdf = tempdf.groupby('District_Key').sum()
tempdf


# In[10]:


tempdf.reset_index(inplace = True)
tempdf


# In[11]:


# Finding the ratio of both vaccines for each district
tempdf['Vaccine_Ratio'] = tempdf['Covishield'] / tempdf['Covaxin']
tempdf


# In[12]:


# Rounding up the ratio values to three decimal places
tempdf['Vaccine_Ratio'] = tempdf['Vaccine_Ratio'].apply(lambda x: '%.3f' % x)
tempdf


# In[13]:


district_result_df = tempdf.copy()
district_result_df


# In[14]:


district_result_df.drop(['Covaxin','Covishield'],axis=1,inplace=True)
district_result_df


# In[15]:


district_result_df.columns = ['districtid', 'vaccineratio']
district_result_df


# In[16]:


# Storing the result in district-vaccine-type-ratio.csv 
district_result_df.to_csv('Outputs/district-vaccine-type-ratio.csv',index=True)


# ## Now Doing this for state

# In[17]:


vaccine_df3


# In[18]:


# Creating a temporary dataframe to store the vaccination data for each state
tempdf = pd.DataFrame()
tempdf['State'] = vaccine_df3['State'].unique()
tempdf


# In[19]:


tempdf['Covaxin'] = np.nan
tempdf['Covishield'] = np.nan
tempdf


# In[20]:


# Filling covaxin/covishield data for each state
# As vaccine_df contains data district wise so adding covaxin/covishield data of all the district for a particular state
for i in range(len(tempdf)):
    newdf = vaccine_df3[vaccine_df3['State'] == tempdf.iloc[i,0]]
    sumdf = newdf.sum(axis=0)
    tempdf.iloc[i,1] = pd.to_numeric(sumdf.loc['14/08/2021.8'])
    tempdf.iloc[i,2] = pd.to_numeric(sumdf.loc['14/08/2021.9'])
tempdf


# In[21]:


# Finding the ratio of both vaccines for each state
tempdf['Vaccine_Ratio'] = tempdf['Covishield'] / tempdf['Covaxin']
tempdf


# In[22]:


# Rounding up the ratios to three decimal places
tempdf['Vaccine_Ratio'] = tempdf['Vaccine_Ratio'].apply(lambda x: '%.3f' % x)
tempdf


# In[23]:


state_result_df = tempdf.copy()
state_result_df


# In[24]:


state_result_df.drop(['Covaxin','Covishield'],axis = 1,inplace = True)
state_result_df


# In[25]:


state_result_df.columns = ['stateid', 'vaccineratio']
state_result_df


# In[26]:


# Storing the result in state-vaccine-type-ratio.csv 
state_result_df.to_csv('Outputs/state-vaccine-type-ratio.csv',index=True)


# ## Now doing this for India

# In[27]:


tempdf = pd.DataFrame()
tempdf['Country'] = ['India']
tempdf


# In[28]:


# Finding the covaxin/covishield data for India by summing of all districts
tempdf['Covaxin'] = vaccine_df3['14/08/2021.8'].sum()
tempdf['Covishield'] = vaccine_df3['14/08/2021.9'].sum()
tempdf


# In[29]:


# Finding the ratio of both vaccines for India
tempdf['Vaccine_Ratio'] = tempdf['Covishield'] / tempdf['Covaxin']
tempdf


# In[30]:


india_result_df = tempdf.copy()
india_result_df


# In[31]:


india_result_df.drop(['Covaxin','Covishield'],axis=1,inplace=True)
india_result_df


# In[32]:


india_result_df.columns = ['countryid', 'vaccineratio']
india_result_df


# In[33]:


# Storing the result in india-vaccine-type-ratio.csv 
india_result_df.to_csv('Outputs/india-vaccine-type-ratio.csv',index=True)

