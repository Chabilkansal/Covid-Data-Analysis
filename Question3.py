#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime
import time
from dateutil.relativedelta import relativedelta


# In[2]:


coviddf = pd.read_csv('districts.csv')
# coviddf


# In[3]:


vaccinedf = pd.read_csv('cowin_vaccine_data_districtwise.csv')
# vaccinedf


# In[4]:


vaccinedf[(vaccinedf['State'] == 'Uttarakhand') & (vaccinedf['District'] == 'Dehradun')].iloc[0]['District_Key']


# In[5]:


coviddf[coviddf['District'] == 'Evacuees']


# In[6]:


coviddf[(coviddf['State'] == 'Maharashtra') & (coviddf['District'] == 'Unknown')]


# In[7]:


vaccinedf_district_data = vaccinedf[['District','State','District_Key']]
# vaccinedf_district_data


# In[8]:


vaccine_dict = dict(zip(vaccinedf_district_data['District'], vaccinedf_district_data['District_Key']))
# vaccine_dict


# In[9]:


# vaccine_dict


# In[10]:


state_dict = dict(zip(vaccinedf['State'], vaccinedf['State_Code']))
# state_dict


# In[11]:


# coviddf


# In[12]:


coviddf['District_Key'] = np.nan
# coviddf


# In[13]:


coviddf.info()


# In[14]:


coviddf['Date'] = pd.to_datetime(coviddf['Date'], format = '%Y-%m-%d')
# coviddf


# In[15]:


lastdate = '2021-08-14'
lastdate = datetime.datetime.strptime(lastdate, "%Y-%m-%d")
coviddf2 = coviddf[coviddf['Date']<=lastdate]
# coviddf2


# In[16]:


coviddf2 = coviddf2.sort_values(['State','District'])
# coviddf2


# In[17]:


starttime = time.time()
for i in range(1,len(coviddf2)):
    if coviddf2.iloc[i,1] == coviddf2.iloc[i-1,1] and coviddf2.iloc[i,2] == coviddf2.iloc[i-1,2]:
        if coviddf2.iloc[i,3] < coviddf2.iloc[i-1,3]:
            coviddf2.iloc[i,3] = coviddf2.iloc[i-1,3]
endtime = time.time()
# print(endtime-starttime)


# In[18]:


# coviddf2


# In[19]:


start =datetime.date(2020,5,2)
end = datetime.date(2021,8,14)
date_list = [start]
cur = start
while cur < end:
    cur = cur + datetime.timedelta(days=7)
    date_list.append(cur)
# date_list


# In[20]:


coviddf3 = coviddf2[coviddf2['Date'].isin(date_list)]
# coviddf3


# In[21]:


coviddf3.reset_index(drop=True,inplace=True)
# coviddf3


# In[22]:


coviddf3[(coviddf3['District']=='Chittorgarh')]


# In[23]:


def dup_district_to_districtkey(state,dist):
    if state == 'Bihar' and dist == 'Aurangabad':
        return 'BR_Aurangabad'
    if state == 'Maharashtra' and dist == 'Aurangabad':
        return 'MH_Aurangabad'
    if state == 'Karnataka'and dist == 'Bijapur':
        return 'KN_Bijapur'
    if state == 'Chhattisgarh' and dist == 'Bijapur':
        return 'CT_Bijapur'
    if state == 'Chhattisgarh' and dist == 'Balrampur':
        return 'CT_Balrampur'
    if state == 'Uttar Pradesh' and dist == 'Balrampur':
        return 'UP_Balrampur'
    if state == 'Chhattisgarh' and dist == 'Bilaspur':
        return 'CT_Bilaspur'
    if state == 'Himachal Pradesh' and dist == 'Bilaspur':
        return 'HP_Bilaspur'
    if state == 'Himachal Pradesh' and dist == 'Hamirpur':
        return 'HP_Hamirpur'
    if state == 'Uttar Pradesh' and dist == 'Hamirpur':
        return 'UP_Hamirpur'
    if state == 'Rajasthan' and dist == 'Pratapgarh':
        return 'RJ_Pratapgarh'
    if state == 'Uttar Pradesh' and dist == 'Pratapgarh':
        return 'UP_Pratapgarh'


# In[24]:


start = time.time()
for i in range(len(coviddf3)):
    if (coviddf3.iloc[i,2] in vaccine_dict.keys()):
        if coviddf3.iloc[i,2] in ['Aurangabad','Bijapur','Balrampur','Bilaspur','Hamirpur','Pratapgarh']:
            coviddf3.iloc[i,8] = dup_district_to_districtkey(coviddf3.iloc[i,1],coviddf3.iloc[i,2])
        else:
            coviddf3.iloc[i,8] = vaccine_dict[coviddf3.iloc[i,2]]
    elif (coviddf3.iloc[i,2] == 'Unknown') or (coviddf3.iloc[i,2]==coviddf3.iloc[i,1]):
        coviddf3.iloc[i,8] = state_dict[coviddf3.iloc[i,1]] + '_'+ coviddf3.iloc[i,1]
    else:
        coviddf3.iloc[i,8] = state_dict[coviddf3.iloc[i,1]] + '_'+ coviddf3.iloc[i,2]
end = time.time()
# print(end - start)


# In[25]:


coviddf3[coviddf3['District'] =='Hamirpur']


# In[26]:


# coviddf3


# In[27]:


coviddf3.isnull().sum()


# In[28]:


coviddf3.drop(['Tested'],axis=1,inplace=True)


# In[29]:


delhi_df = coviddf3[coviddf3['District_Key'] == 'DL_Delhi']
# delhi_df


# In[30]:


delhi_df.iloc[1,3] - delhi_df.iloc[0,3]


# In[31]:


coviddf4 = coviddf3.copy()
# coviddf4


# In[32]:


coviddf4['Confirmed_Weekly'] = np.nan
# coviddf4


# In[33]:


coviddf4.iloc[0,8] = coviddf4.iloc[0,3]


# In[34]:


for i in range(1,len(coviddf4)):
    if coviddf4.iloc[i,7] == coviddf4.iloc[i-1,7]:
        coviddf4.iloc[i,8] = int(coviddf4.iloc[i,3] - coviddf4.iloc[i-1,3])
    else:
        coviddf4.iloc[i,8] = int(coviddf4.iloc[i,3])


# In[35]:


# coviddf4


# In[36]:


coviddf4[coviddf4['Confirmed']<0]


# In[37]:


coviddf4.isnull().sum()


# In[38]:


coviddf4[coviddf4['District_Key']=='DL_Delhi']


# In[39]:


week_resultdf = coviddf4[['District_Key','Confirmed_Weekly']]
# week_resultdf


# In[40]:


week_resultdf = week_resultdf.astype({"Confirmed_Weekly": int})
# week_resultdf


# In[41]:


week_resultdf['Week_ID'] = np.nan
# week_resultdf


# In[42]:


count=1
for i in range(len(week_resultdf)):
    if week_resultdf.iloc[i,0] != week_resultdf.iloc[i-1,0]:
        count = 1
    week_resultdf.iloc[i,2] = count
    count += 1


# In[43]:


# week_resultdf


# In[44]:


week_resultdf = week_resultdf.astype({"Week_ID": int})
# week_resultdf


# In[45]:


week_resultdf['Week_ID'].max()


# In[46]:


week_resultdf[week_resultdf['District_Key'] == 'HP_Hamirpur']


# In[47]:


week_resultdf.columns = ['districtid','cases', 'weekid']
# week_resultdf


# In[48]:


week_resultdf.to_csv('Outputs/week-cases-time.csv',index=False)


# ## Now Doing this for monthly data 

# In[49]:


lastdate = '2021-08-24'
lastdate = datetime.datetime.strptime(lastdate, "%Y-%m-%d")
coviddf2 = coviddf[coviddf['Date']<=lastdate]
# coviddf2


# In[50]:


coviddf2 = coviddf2.sort_values(['State','District'])
# coviddf2


# In[51]:


starttime = time.time()
for i in range(1,len(coviddf2)):
    if coviddf2.iloc[i,1] == coviddf2.iloc[i-1,1] and coviddf2.iloc[i,2] == coviddf2.iloc[i-1,2]:
        if coviddf2.iloc[i,3] < coviddf2.iloc[i-1,3]:
            coviddf2.iloc[i,3] = coviddf2.iloc[i-1,3]
endtime = time.time()
# print(endtime-starttime)


# In[52]:


# coviddf2


# In[53]:


start =datetime.date(2020,4,23)
end = datetime.date(2021,8,14)
date_list = [start]
cur = start
while cur < end:
    cur = cur + relativedelta(months=+1)
    date_list.append(cur)
# date_list


# In[54]:


coviddf3 = coviddf2[coviddf2['Date'].isin(date_list)]
# coviddf3


# In[55]:


coviddf3.reset_index(drop=True,inplace=True)
# coviddf3


# In[56]:


start = time.time()
for i in range(len(coviddf3)):
    if (coviddf3.iloc[i,2] in vaccine_dict.keys()):
        if coviddf3.iloc[i,2] in ['Aurangabad','Bijapur','Balrampur','Bilaspur','Hamirpur','Pratapgarh']:
            coviddf3.iloc[i,8] = dup_district_to_districtkey(coviddf3.iloc[i,1],coviddf3.iloc[i,2])
        else:
            coviddf3.iloc[i,8] = vaccine_dict[coviddf3.iloc[i,2]]
    elif (coviddf3.iloc[i,2] == 'Unknown') or (coviddf3.iloc[i,2]==coviddf3.iloc[i,1]):
        coviddf3.iloc[i,8] = state_dict[coviddf3.iloc[i,1]] + '_'+ coviddf3.iloc[i,1]
    else:
        coviddf3.iloc[i,8] = state_dict[coviddf3.iloc[i,1]] + '_'+ coviddf3.iloc[i,2]
end = time.time()
# print(end - start)


# In[57]:


# coviddf3
# 

# In[58]:


coviddf3.isnull().sum()


# In[59]:


coviddf3.drop(['Tested'],axis=1,inplace=True)


# In[60]:


delhi_df = coviddf3[coviddf3['District_Key'] == 'DL_Delhi']
# delhi_df


# In[61]:


delhi_df.iloc[1,3] - delhi_df.iloc[0,3]


# In[62]:


coviddf4 = coviddf3.copy()
# coviddf4


# In[63]:


coviddf4['Confirmed_Monthly'] = np.nan
# coviddf4


# In[64]:


coviddf4.iloc[0,8] = coviddf4.iloc[0,3]

for i in range(1,len(coviddf4)):
    if coviddf4.iloc[i,7] == coviddf4.iloc[i-1,7]:
        coviddf4.iloc[i,8] = int(coviddf4.iloc[i,3] - coviddf4.iloc[i-1,3])
    else:
        coviddf4.iloc[i,8] = int(coviddf4.iloc[i,3])


# In[65]:


# coviddf4


# In[66]:


coviddf4[coviddf4['Confirmed']<0]


# In[67]:


coviddf4.isnull().sum()


# In[68]:


coviddf4[coviddf4['District_Key']=='DL_Delhi']


# In[69]:


month_resultdf = coviddf4[['District_Key','Confirmed_Monthly']]
# month_resultdf


# In[70]:


month_resultdf = month_resultdf.astype({"Confirmed_Monthly": int})
# month_resultdf


# In[71]:


month_resultdf['Month_ID'] = np.nan
# month_resultdf


# In[72]:


count=1
for i in range(len(month_resultdf)):
    if month_resultdf.iloc[i,0] != month_resultdf.iloc[i-1,0]:
        count = 1
    month_resultdf.iloc[i,2] = count
    count += 1


# In[73]:


# month_resultdf


# In[74]:


month_resultdf = month_resultdf.astype({"Month_ID": int})
# month_resultdf


# In[75]:


month_resultdf.columns = ['districtid', 'cases','monthid']
# month_resultdf


# In[76]:


month_resultdf.to_csv('Outputs/month-cases-time.csv',index=False)


# ## Now finding total confirmed cases for each district

# In[77]:


overall_resultdf = month_resultdf[['districtid','cases']]
# overall_resultdf


# In[78]:


overall_resultdf = overall_resultdf.groupby('districtid').sum()
# overall_resultdf


# In[79]:


overall_resultdf.reset_index(inplace=True)
# overall_resultdf


# In[80]:


overall_resultdf.to_csv('Outputs/overall-cases-time.csv',index=False)

