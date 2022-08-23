#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime


# In[2]:


df = pd.read_csv('vaccine_data_new.csv')
df


# In[3]:


census_df = pd.read_excel('DDW_PCA0000_2011_Indiastatedist.xlsx')
census_df


# In[4]:


# Changing the data types of last week columns
vaccine_df_copy = df.copy()

vaccine_df_copy['14/08/2021.3'] = pd.to_numeric(vaccine_df_copy['14/08/2021.3'])
vaccine_df_copy['13/08/2021.3'] = pd.to_numeric(vaccine_df_copy['13/08/2021.3'])
vaccine_df_copy['12/08/2021.3'] = pd.to_numeric(vaccine_df_copy['12/08/2021.3'])
vaccine_df_copy['11/08/2021.3'] = pd.to_numeric(vaccine_df_copy['11/08/2021.3'])
vaccine_df_copy['10/08/2021.3'] = pd.to_numeric(vaccine_df_copy['10/08/2021.3'])
vaccine_df_copy['09/08/2021.3'] = pd.to_numeric(vaccine_df_copy['09/08/2021.3'])
vaccine_df_copy['08/08/2021.3'] = pd.to_numeric(vaccine_df_copy['08/08/2021.3'])
vaccine_df_copy['07/08/2021.3'] = pd.to_numeric(vaccine_df_copy['07/08/2021.3'])
vaccine_df_copy


# In[5]:


# Creating a temporary datafram for storing the results
# Also adding state list to it
newdf = pd.DataFrame()

newdf['State'] = df['State'].unique()
newdf


# In[6]:


# First_Dose stores the total number of first doses adiministered in each state till 14-8-2021
# First_Dose_Vaccination_Rate stores the average vaccination rate of last week (8-8-2021 to 14-8-2021)
newdf['First_Dose'] = np.nan
newdf['First_Dose_Vaccination_Rate'] = np.nan
newdf


# In[7]:


# Filling the first_dose adn first_dose_vaccination_rate column values 
# For finding the total first doses administered of each state adding all its district vaccination data
# For finding the vaccination rate of each state calculating the number of first doses on 
# 08/08/2021 (by subtracting 07/08/2021 first dose value from 08/08/2021 first dose value as data is cumulative),
# 09/08/2021 (by subtracting 08/08/2021 first dose value from 09/08/2021 first dose value as data is cumulative),
# and so on till 14/08/2021. Then dividing their sum by 7 to calculate weeks average

for i in range(len(newdf)):
    tempdf = vaccine_df_copy[vaccine_df_copy['State'] == newdf.iloc[i,0]]
    sumdf = tempdf.sum(axis=0)
    week_sum_vaccination_rate = 0
    for j in range(14,7,-1):
        if j>10:
            week_sum_vaccination_rate += (pd.to_numeric(sumdf.loc[str(j)+'/08/2021.3']) - pd.to_numeric(sumdf.loc[str(j-1)+'/08/2021.3']))
        elif j==10:
            week_sum_vaccination_rate += (pd.to_numeric(sumdf.loc[str(j)+'/08/2021.3']) - pd.to_numeric(sumdf.loc['0'+str(j-1)+'/08/2021.3']))
        else:
            week_sum_vaccination_rate += (pd.to_numeric(sumdf.loc['0'+str(j)+'/08/2021.3']) - pd.to_numeric(sumdf.loc['0'+str(j-1)+'/08/2021.3']))
    week_avg_vaccination_rate = week_sum_vaccination_rate / 7
    newdf.iloc[i,1] = pd.to_numeric(sumdf.loc['14/08/2021.3'])
    newdf.iloc[i,2] = week_avg_vaccination_rate
newdf


# In[8]:


# Separating the state census data to find population of each state
state_census = census_df[census_df['Level'] == 'STATE']
state_census


# In[9]:


newdf


# In[10]:


newdf['Population'] = np.nan
newdf


# In[11]:


# Converting state names in newdf to uppercase so that names can match with state census data
newdf['State'] = newdf['State'].apply(lambda x: x.upper())
newdf


# In[12]:


# Replacing names of state in newdf according to their state names in state census data
newdf.replace('ANDAMAN AND NICOBAR ISLANDS', 'ANDAMAN & NICOBAR ISLANDS',inplace=True)
newdf.replace('DELHI', 'NCT OF DELHI',inplace=True)


# In[13]:


newdf


# In[14]:


# Filling population of each state from state census data
# Also printing the names if the states for which population data was not found in state census data
for i in newdf.index:
    try:
        newdf.iloc[i,3] = int(state_census[state_census['Name'] == newdf.iloc[i,0]].iloc[0]['TOT_P'])
    except:
        print(newdf.iloc[i,0])


# In[15]:


newdf


# In[16]:


# As UT DADRA & NAGAR HAVELI AND DAMAN & DIU population data is available in census data but separately adding both values
newdf.iloc[7,3] = state_census[state_census['Name']=='DADRA & NAGAR HAVELI'].iloc[0]['TOT_P'] + state_census[state_census['Name']=='DAMAN & DIU'].iloc[0]['TOT_P']


# In[17]:


newdf


# In[18]:


# Dropping the states for which population data was not found in census data
newdf.dropna(inplace=True)


# In[19]:


newdf


# In[20]:


newdf.reset_index(drop=True,inplace=True)


# In[21]:


newdf


# In[22]:


state_result_df = newdf.copy()


# In[23]:


# Finding the number of people left for vaccination in each state
state_result_df['Population_Left'] = state_result_df['Population'] - state_result_df['First_Dose']
state_result_df


# In[24]:


# Finding the number of days required to vaccinate the remaining population of each state for that states last week's 
# (08/08/2021 to 14/08/2021) vaccination rate
state_result_df['Days_Required'] = state_result_df['Population_Left'] / state_result_df['First_Dose_Vaccination_Rate']
state_result_df


# In[25]:


# Rounding off days required
state_result_df['Days_Required'] = state_result_df['Days_Required'].apply(np.ceil)
state_result_df


# In[26]:


# Changing type of days_required to int
state_result_df = state_result_df.astype({'Days_Required': 'int32'})
state_result_df


# In[27]:


# Finding the date till which the vaccination will be completed in each state
state_result_df['Vaccination_Completion_Date'] = state_result_df['Days_Required'].apply(lambda x: datetime.date(2021,8,14) + datetime.timedelta(days = x))
state_result_df


# In[28]:


state_result_df.drop(['First_Dose','Population','Days_Required'],axis=1,inplace=True)
state_result_df


# In[29]:


state_result_df = state_result_df[['State','Population_Left','First_Dose_Vaccination_Rate','Vaccination_Completion_Date']]
state_result_df


# In[30]:


state_result_df.columns = ['stateid', 'populationleft', 'rateofvaccination', 'date']
state_result_df


# In[31]:


state_result_df.to_csv('Outputs/complete-vaccination.csv',index=False)

