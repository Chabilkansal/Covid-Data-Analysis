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


# In[ ]:





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


# coviddf2[coviddf2['State'] == 'Delhi']

# coviddf3[coviddf3['District_Key']=='DL_Delhi']

# coviddf4[coviddf4['District_Key']=='DL_Delhi']


# In[ ]:





# In[ ]:





# In[20]:


date = datetime.date(2020,4,26)
coviddf2.iloc[0,0].date() == date


# In[ ]:





# In[21]:


start =datetime.date(2020,4,29)
end = datetime.date(2021,8,14)
date_list = [start]
cur = start
count=1
while cur < end:
    if count % 2==1:
        cur = cur + datetime.timedelta(days=3)
    else:
        cur = cur + datetime.timedelta(days=4)
    count = count+1
    date_list.append(cur)
date_list


# In[22]:


coviddf3 = coviddf2[coviddf2['Date'].isin(date_list)]
coviddf3


# In[23]:


coviddf3.reset_index(drop=True,inplace=True)
coviddf3


# In[24]:


coviddf3[(coviddf3['District']=='Chittorgarh')]


# In[25]:


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


# In[26]:


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
    if coviddf3.iloc[i,8] == None:
        print(f'state: {coviddf3.iloc[i,1]},dist: {coviddf3.iloc[i,2]}, key: {coviddf3.iloc[i,8]}')
end = time.time()
print(end - start)


# In[27]:


len(coviddf3['District_Key'].unique())


# In[28]:


coviddf3[coviddf3['District'] =='Hamirpur']


# In[29]:


coviddf3


# In[30]:


coviddf3.isnull().sum()


# In[31]:


coviddf3.drop(['Tested'],axis=1,inplace=True)


# In[32]:


delhi_df = coviddf3[coviddf3['District_Key'] == 'DL_Delhi']
delhi_df


# In[33]:


delhi_df.iloc[1,3] - delhi_df.iloc[0,3]


# In[34]:


coviddf4 = coviddf3.copy()
coviddf4


# In[35]:


coviddf4['Active'] = coviddf4['Confirmed'] - coviddf4['Recovered'] - coviddf4['Deceased']
coviddf4


# In[36]:


coviddf4['Active_Weekly'] = np.nan
coviddf4


# In[37]:


coviddf4.iloc[1,9] = coviddf4.iloc[1,8]


# In[38]:


i=2
while i < len(coviddf4):
# for i in range(1,len(coviddf4)):
    if coviddf4.iloc[i,7] == coviddf4.iloc[i-1,7]:
        coviddf4.iloc[i,9] = int(coviddf4.iloc[i,8] - coviddf4.iloc[i-2,8])
    else:
        i = i + 1
        coviddf4.iloc[i,9] = int(coviddf4.iloc[i,8])
    i = i + 1


# In[39]:


coviddf4


# In[40]:


coviddf4[coviddf4['District_Key'] == 'DL_Delhi']


# In[41]:


coviddf4.isnull().sum()


# In[42]:


len(coviddf4['District_Key'].unique())


# In[43]:


coviddf5 = coviddf4.dropna()


# In[44]:


coviddf5


# In[45]:


len(coviddf5['District_Key'].unique())


# In[ ]:





# In[46]:


coviddf5 = coviddf5[['District_Key','Active_Weekly']]
coviddf5


# In[47]:


coviddf5['Week_ID'] = np.nan
coviddf5


# In[48]:


count=1
for i in range(len(coviddf5)):
    if coviddf5.iloc[i,0] != coviddf5.iloc[i-1,0]:
        count = 1
    coviddf5.iloc[i,2] = count
    count += 1


# In[49]:


coviddf5


# In[50]:


coviddf5 = coviddf5.astype({"Week_ID": int})
coviddf5


# In[51]:


delhi_df = coviddf5[coviddf5['District_Key']=='DL_Delhi']
delhi_df


# In[52]:


delhi_df['Active_Weekly'].max()


# In[53]:


dist_list = []
wave1_list = []
wave2_list = []
for dist in coviddf5['District_Key'].unique():
    tempdf = coviddf5[coviddf5['District_Key']==dist]
    max_cases = 0
    pmax_cases = 0
    count = 0
    case_list = []
    week_list = []
    dist_list.append(dist)
#     temp_max = tempdf.iloc[0,1]
    for i in range(len(tempdf)):
        p_cases = tempdf.iloc[i,1]
        if p_cases>max_cases:
            max_cases = p_cases
            max_weekid = tempdf.iloc[i,2]
        if max_cases == pmax_cases and max_cases != 0:
            count = count + 1
        else:
            count = 0
        if pmax_cases != max_cases:
            pmax_cases = max_cases
        if count==8:
            case_list.append(max_cases)
            week_list.append(max_weekid)
            count = 0
            max_cases = 0
            pmax_cases = 0
#     print(f'{dist}: {week_list} {case_list}')
    if len(week_list) < 2:
        if len(week_list) < 1:
            wave1_list.append(-1)
            wave2_list.append(-1)
        else:
            if week_list[0] < 100:
                wave1_list.append(week_list[0])
                wave2_list.append(-1)
            else:
                wave2_list.append(week_list[0])
                wave1_list.append(-1)
    else:
        idx = np.argsort(case_list)
#         print(f'{dist}: {idx}')
        wave1 = week_list[idx[-1]]
        wave2 = week_list[idx[-2]]
        if wave2 < wave1:
            wave1, wave2 = wave2, wave1
        if wave1 > 100:
            wave2 = wave1
            wave1 = -1
        if wave2 < 100:
            wave1 = wave2
            wave2 = -1
        wave1_list.append(wave1)
        wave2_list.append(wave2)
        


# In[54]:


dist_list


# In[55]:


wave1_list


# In[56]:


district_waves_df = pd.DataFrame({'districtid':dist_list,'wave1 − weekid':wave1_list,'wave2 − weekid':wave2_list})
district_waves_df


# ## Now doing this two find peaking months for each district

# In[57]:


coviddf2


# In[ ]:





# In[58]:


start =datetime.date(2020,4,14)
end = datetime.date(2021,8,14)
month_date_list = []
cur = start
while cur < end:
    cur = cur + relativedelta(months=+1)
    month_date_list.append(cur)
month_date_list


# In[59]:


coviddf3 = coviddf2[coviddf2['Date'].isin(month_date_list)]
coviddf3


# In[60]:


coviddf3.reset_index(drop=True,inplace=True)
coviddf3


# In[61]:


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
print(end - start)


# In[62]:


coviddf3


# In[63]:


len(coviddf3['District_Key'].unique())


# In[64]:


coviddf3.drop(['Tested'],axis=1,inplace=True)


# In[65]:


coviddf4 = coviddf3.copy()
coviddf4


# In[66]:


coviddf4['Active'] = coviddf4['Confirmed'] - coviddf4['Recovered'] - coviddf4['Deceased']
coviddf4


# In[67]:


coviddf4['Active_Monthly'] = np.nan
coviddf4


# In[68]:


coviddf4.iloc[0,9] = coviddf4.iloc[0,8]


# In[69]:


for i in range(1,len(coviddf4)):
    if coviddf4.iloc[i,7] == coviddf4.iloc[i-1,7]:
        coviddf4.iloc[i,9] = int(coviddf4.iloc[i,8] - coviddf4.iloc[i-1,8])
    else:
        coviddf4.iloc[i,9] = int(coviddf4.iloc[i,8])


# In[70]:


coviddf4


# In[71]:


len(coviddf4['District_Key'].unique())


# In[72]:


coviddf5 = coviddf4[['District_Key','Active_Monthly']]
coviddf5


# In[73]:


coviddf5['Month_ID'] = np.nan
coviddf5


# In[74]:


count=1
for i in range(len(coviddf5)):
    if coviddf5.iloc[i,0] != coviddf5.iloc[i-1,0]:
        count = 1
    coviddf5.iloc[i,2] = count
    count += 1


# In[75]:


coviddf5


# In[76]:


coviddf5 = coviddf5.astype({"Month_ID": int})
coviddf5


# In[77]:


coviddf5['Month_ID'].max()


# In[78]:


coviddf5[coviddf5['District_Key'] == 'WB_West Bengal']


# In[79]:


dist_list = []
wave1_list = []
wave2_list = []
for dist in coviddf5['District_Key'].unique():
    tempdf = coviddf5[coviddf5['District_Key']==dist]
    max_cases = 0
    pmax_cases = 0
    count = 0
    case_list = []
    month_list = []
    dist_list.append(dist)
#     temp_max = tempdf.iloc[0,1]
    for i in range(len(tempdf)):
        p_cases = tempdf.iloc[i,1]
        if p_cases>max_cases:
            max_cases = p_cases
            max_monthid = tempdf.iloc[i,2]
        if max_cases == pmax_cases and max_cases != 0:
            count = count + 1
        else:
            count = 0
        if pmax_cases != max_cases:
            pmax_cases = max_cases
        if count==2:
            case_list.append(max_cases)
            month_list.append(max_monthid)
            count = 0
            max_cases = 0
            pmax_cases = 0
#     print(f'{dist}: {week_list} {case_list}')
    if len(month_list) < 2:
        if len(month_list) < 1:
            wave1_list.append(-1)
            wave2_list.append(-1)
        else:
            if month_list[0] < 11:
                wave1_list.append(month_list[0])
                wave2_list.append(-1)
            else:
                wave2_list.append(month_list[0])
                wave1_list.append(-1)
    else:
        idx = np.argsort(case_list)
#         print(f'{dist}: {idx}')
        wave1 = month_list[idx[-1]]
        wave2 = month_list[idx[-2]]
        if wave2 < wave1:
            wave1, wave2 = wave2, wave1
        if wave1 > 11:
            wave2 = wave1
            wave1 = -1
        if wave2 < 11:
            wave1 = wave2
            wave2 = -1
        wave1_list.append(wave1)
        wave2_list.append(wave2)


# In[80]:


len(dist_list)


# In[81]:


wave1_list


# In[82]:


wave2_list


# In[83]:


district_waves_df


# In[84]:


district_waves_df['wave1 − monthid'] = np.nan
district_waves_df['wave2 − monthid'] = np.nan


# In[85]:


district_waves_df


# In[86]:


district_waves_df.reset_index(drop=True,inplace=True)


# In[87]:


dist_list


# In[88]:


for i in range(len(dist_list)):
    try:
        ind = district_waves_df[district_waves_df['districtid']==dist_list[i]].index
#         print(dist_list[i])
#         print(ind[0])

        district_waves_df.iloc[ind[0],3] = wave1_list[i]
        district_waves_df.iloc[ind[0],4] = wave2_list[i]
    except:
        pass
# district_waves_df


# In[89]:


district_waves_df


# In[90]:


district_waves_df.fillna(-1,inplace=True)
district_waves_df


# In[91]:


district_waves_df = district_waves_df.astype({"wave1 − monthid": int,"wave2 − monthid": int})
district_waves_df


# In[147]:


district_waves_df.to_csv('Outputs/district-peaks.csv',index=False)


# ## Now finding peaking weeks for every state

# In[92]:


coviddf2


# In[93]:


coviddf3 = coviddf2.reset_index(drop=True)


# In[94]:


coviddf3['Active'] = coviddf3['Confirmed'] - coviddf3['Recovered']- coviddf3['Deceased']
coviddf3


# In[95]:


coviddf3 = coviddf3[['Date','State','Active']]
coviddf3


# In[96]:


coviddf4 = coviddf3.groupby(['Date','State']).sum()
coviddf4


# In[97]:


coviddf4.reset_index(inplace = True)
coviddf4


# In[98]:


coviddf4 = coviddf4.sort_values(['State','Date'])
coviddf4


# In[99]:


coviddf4.reset_index(drop=True,inplace=True)
coviddf4


# In[100]:


start =datetime.date(2020,4,29)
end = datetime.date(2021,8,14)
date_list = [start]
cur = start
count=1
while cur < end:
    if count % 2==1:
        cur = cur + datetime.timedelta(days=3)
    else:
        cur = cur + datetime.timedelta(days=4)
    count = count+1
    date_list.append(cur)
date_list


# In[101]:


coviddf5 = coviddf4[coviddf4['Date'].isin(date_list)]
coviddf5


# In[102]:


coviddf5.reset_index(drop=True,inplace=True)
coviddf5


# In[103]:


coviddf5['Active_Weekly'] = np.nan
coviddf5


# In[104]:


coviddf5.iloc[1,3] = coviddf5.iloc[1,2]
coviddf5


# In[ ]:





# In[105]:


i=2
while i < len(coviddf5):
# for i in range(1,len(coviddf4)):
    if coviddf5.iloc[i,1] == coviddf5.iloc[i-1,1]:
        coviddf5.iloc[i,3] = int(coviddf5.iloc[i,2] - coviddf5.iloc[i-2,2])
    else:
        i = i + 1
        coviddf5.iloc[i,3] = int(coviddf5.iloc[i,2])
    i = i + 1


# In[106]:


coviddf5


# In[107]:


coviddf5 = coviddf5.dropna()
coviddf5


# In[108]:


coviddf5 = coviddf5[['State','Active_Weekly']]
coviddf5


# In[109]:


coviddf5['Week_ID'] = np.nan
coviddf5


# In[110]:


count=1
for i in range(len(coviddf5)):
    if coviddf5.iloc[i,0] != coviddf5.iloc[i-1,0]:
        count = 1
    coviddf5.iloc[i,2] = count
    count += 1


# In[111]:


coviddf5


# In[112]:


coviddf5 = coviddf5.astype({'Week_ID':int})
coviddf5


# In[113]:


state_list = []
wave1_list = []
wave2_list = []
for stat in coviddf5['State'].unique():
    tempdf = coviddf5[coviddf5['State']==stat]
    max_cases = 0
    pmax_cases = 0
    count = 0
    case_list = []
    week_list = []
    state_list.append(stat)
#     temp_max = tempdf.iloc[0,1]
    for i in range(len(tempdf)):
        p_cases = tempdf.iloc[i,1]
        if p_cases>max_cases:
            max_cases = p_cases
            max_weekid = tempdf.iloc[i,2]
        if max_cases == pmax_cases and max_cases != 0:
            count = count + 1
        else:
            count = 0
        if pmax_cases != max_cases:
            pmax_cases = max_cases
        if count==8:
            case_list.append(max_cases)
            week_list.append(max_weekid)
            count = 0
            max_cases = 0
            pmax_cases = 0
#     print(f'{dist}: {week_list} {case_list}')
    if len(week_list) < 2:
        if len(week_list) < 1:
            wave1_list.append(-1)
            wave2_list.append(-1)
        else:
            if week_list[0] < 100:
                wave1_list.append(week_list[0])
                wave2_list.append(-1)
            else:
                wave2_list.append(week_list[0])
                wave1_list.append(-1)
    else:
        idx = np.argsort(case_list)
#         print(f'{dist}: {idx}')
        wave1 = week_list[idx[-1]]
        wave2 = week_list[idx[-2]]
        if wave2 < wave1:
            wave1, wave2 = wave2, wave1
        if wave1 > 100:
            wave2 = wave1
            wave1 = -1
        if wave2 < 100:
            wave1 = wave2
            wave2 = -1
        wave1_list.append(wave1)
        wave2_list.append(wave2)
        


# In[114]:


state_list


# In[115]:


wave1_list


# In[116]:


wave2_list


# In[117]:


state_waves_df = pd.DataFrame({'stateid':state_list,'wave1 − weekid':wave1_list,'wave2 − weekid':wave2_list})
state_waves_df


# ## Now doing this two find peaking months for each state

# In[118]:


coviddf2


# In[119]:


coviddf3 = coviddf2.reset_index(drop=True)


# In[120]:


coviddf3['Active'] = coviddf3['Confirmed'] - coviddf3['Recovered']- coviddf3['Deceased']
coviddf3


# In[121]:


coviddf3 = coviddf3[['Date','State','Active']]
coviddf3


# In[122]:


coviddf4 = coviddf3.groupby(['Date','State']).sum()
coviddf4


# In[123]:


coviddf4.reset_index(inplace = True)
coviddf4


# In[124]:


coviddf4 = coviddf4.sort_values(['State','Date'])
coviddf4


# In[125]:


coviddf4.reset_index(drop=True,inplace=True)
coviddf4


# In[126]:


start =datetime.date(2020,4,14)
end = datetime.date(2021,8,14)
month_date_list = []
cur = start
while cur < end:
    cur = cur + relativedelta(months=+1)
    month_date_list.append(cur)
month_date_list


# In[127]:


coviddf5 = coviddf4[coviddf4['Date'].isin(month_date_list)]
coviddf5


# In[128]:


coviddf5.reset_index(drop=True,inplace=True)
coviddf5


# In[129]:


coviddf5['Active_Monthly'] = np.nan
coviddf5


# In[130]:


coviddf5.iloc[0,3] = coviddf5.iloc[0,2]
coviddf5


# In[131]:


for i in range(1,len(coviddf5)):
    if coviddf5.iloc[i,1] == coviddf5.iloc[i-1,1]:
        coviddf5.iloc[i,3] = int(coviddf5.iloc[i,2] - coviddf5.iloc[i-1,2])
    else:
        coviddf5.iloc[i,3] = int(coviddf5.iloc[i,2])


# In[132]:


coviddf5


# In[133]:


coviddf5 = coviddf5.dropna()
coviddf5


# In[134]:


coviddf5 = coviddf5[['State','Active_Monthly']]
coviddf5


# In[135]:


coviddf5['Month_ID'] = np.nan
coviddf5


# In[136]:


count=1
for i in range(len(coviddf5)):
    if coviddf5.iloc[i,0] != coviddf5.iloc[i-1,0]:
        count = 1
    coviddf5.iloc[i,2] = count
    count += 1


# In[137]:


coviddf5


# In[138]:


coviddf5 = coviddf5.astype({'Month_ID':int})
coviddf5


# In[139]:


state_list = []
wave1_list = []
wave2_list = []
for stat in coviddf5['State'].unique():
    tempdf = coviddf5[coviddf5['State']==stat]
    max_cases = 0
    pmax_cases = 0
    count = 0
    case_list = []
    month_list = []
    state_list.append(stat)
#     temp_max = tempdf.iloc[0,1]
    for i in range(len(tempdf)):
        p_cases = tempdf.iloc[i,1]
        if p_cases>max_cases:
            max_cases = p_cases
            max_monthid = tempdf.iloc[i,2]
        if max_cases == pmax_cases and max_cases != 0:
            count = count + 1
        else:
            count = 0
        if pmax_cases != max_cases:
            pmax_cases = max_cases
        if count==2:
            case_list.append(max_cases)
            month_list.append(max_monthid)
            count = 0
            max_cases = 0
            pmax_cases = 0
#     print(f'{dist}: {week_list} {case_list}')
    if len(month_list) < 2:
        if len(month_list) < 1:
            wave1_list.append(-1)
            wave2_list.append(-1)
        else:
            if month_list[0] < 11:
                wave1_list.append(month_list[0])
                wave2_list.append(-1)
            else:
                wave2_list.append(month_list[0])
                wave1_list.append(-1)
    else:
        idx = np.argsort(case_list)
#         print(f'{dist}: {idx}')
        wave1 = month_list[idx[-1]]
        wave2 = month_list[idx[-2]]
        if wave2 < wave1:
            wave1, wave2 = wave2, wave1
        if wave1 > 11:
            wave2 = wave1
            wave1 = -1
        if wave2 < 11:
            wave1 = wave2
            wave2 = -1
        wave1_list.append(wave1)
        wave2_list.append(wave2)


# In[140]:


state_list


# In[141]:


wave1_list


# In[142]:


wave2_list


# In[143]:


state_waves_df


# In[144]:


len(state_list)


# In[145]:


state_waves_df['wave1 − monthid'] = wave1_list
state_waves_df['wave2 − monthid'] = wave2_list
state_waves_df


# In[ ]:


state_waves_df.to_csv('Outputs/state-peaks.csv',index=False)

