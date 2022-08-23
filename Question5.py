#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta


# In[2]:


## Reading the vaccination data
vaccine_df = pd.read_csv('vaccine_data_new.csv')
vaccine_df


# In[3]:


## Finding the last dates of all weeks from 16-1-2021 (as vaccination dateset starts from this date) to last date 14-8-2021
# last date taken as standard last date throughout the Assignment 
start =datetime.date(2021,1,16)
end = datetime.date(2021,8,14)
date_list = []
cur = start
while cur < end:
    cur = cur + datetime.timedelta(days=7)
    date_list.append(str(cur.strftime("%d/%m/%Y")))
date_list


# In[4]:


# As in our vaccination dataset for every date 4th columns represents number of first dose administered and 5th column represents
# number of second dose administered so adding their index to datelist
new_date_list = []
for i in date_list:
    new_date_list.append(i+'.3')
    new_date_list.append(i+'.4')
new_date_list


# In[5]:


vaccine_df.columns


# In[6]:


# Now we only need the following columns from vaccination data : as for weekly number of first/second doses we will just 
# subtract previous weeks data from present weeks data
column_list = ['S No', 'State_Code', 'State', 'District_Key', 'Cowin Key', 'District']+new_date_list

column_list


# In[7]:


# Separating only the usefull columns from vaccination data
vaccine_df2 = vaccine_df.loc[:,column_list]
vaccine_df2


# In[8]:


# Creating a list with first dose dates and second dose dates
first_dose_column_list = []
second_dose_column_list = []
for i in date_list:
    first_dose_column_list.append(i+'.3')
    second_dose_column_list.append(i+'.4')


# In[9]:


first_dose_column_list


# In[10]:


second_dose_column_list


# In[11]:


vaccine_df2


# In[12]:


## Melting the columns containing first dose data for every date present in first_dose_column_list
vaccine_df3 = pd.melt(vaccine_df2,id_vars=['S No','State_Code','State','District_Key','Cowin Key','District'],
        value_vars=first_dose_column_list, value_name = 'First_Dose',var_name = 'Date')
vaccine_df3


# In[13]:


# the output shows us the number of first dose administered for district nicobars till date 23/01/2021 (i.e first week)
# the output shows us the number of first dose administered for district nicobars till date 30/01/2021 (i.e first+second week)
# the output shows us the number of first dose administered for district nicobars till date 06/02/2021 (i.e first+second+third week)
# ...and so on

# so to find number of first doses administered in week 2 we will just subtract first dose(date:30/01/2021)-first dose(date:23/01/2021)
# and similarly for other weeks
vaccine_df3[vaccine_df3['District_Key']=='AN_Nicobars']


# In[14]:


## Melting the columns containing second dose data for every date present in second_dose_column_list

vaccine_df4 = pd.melt(vaccine_df2,id_vars=['S No','State_Code','State','District_Key','Cowin Key','District'],
        value_vars=second_dose_column_list, value_name = 'Second_Dose',var_name = 'Date')
vaccine_df4


# In[15]:


# the output shows us the number of second dose administered for district nicobars till date 23/01/2021 (i.e first week)
# the output shows us the number of second dose administered for district nicobars till date 30/01/2021 (i.e first+second week)
# the output shows us the number of second dose administered for district nicobars till date 06/02/2021 (i.e first+second+third week)
# ...and so on
vaccine_df4[vaccine_df4['District_Key']=='AN_Nicobars']


# In[16]:


## Adding second dose column to the dataframe containing first dose column
vaccine_df3['Second_Dose'] = vaccine_df4['Second_Dose']
vaccine_df3


# In[17]:


# The output of this line shows that for some districts like (Gandhinagar) there are two entries for every date
# so to find the actual first/second doses administered data in such Gandhinagar we have to add such rows data
# One way of doing this can be using groupby as shown ahead
vaccine_df3[vaccine_df3['District_Key'] == 'GJ_Gandhinagar']


# In[18]:


# Dropping irrelevant columns
vaccine_df5 = vaccine_df3.drop(['S No','State_Code','State','Cowin Key','District'],axis=1)
vaccine_df5


# In[19]:


# Changing the type of date column from object to datetime
vaccine_df5['Date'] = vaccine_df5['Date'].str.split('.').str[0]

vaccine_df5['Date'] = pd.to_datetime(vaccine_df5['Date'],format='%d/%m/%Y')
vaccine_df5


# In[20]:


# sorting values according to district_key and date
vaccine_df6 = vaccine_df5.sort_values(by=['District_Key','Date'])
vaccine_df6


# In[21]:


vaccine_df6.reset_index(drop=True,inplace=True)
vaccine_df6


# In[22]:


# Using Groupby to handle district with multiple entries to find actual first/second dose data
vaccine_df7 = vaccine_df6.groupby(['District_Key','Date']).sum()
vaccine_df7


# In[23]:


vaccine_df8 = vaccine_df7.reset_index()
vaccine_df8


# In[24]:


## the output shows that districts (like Gandhinagar) now have only one entry for every data in dataframe
vaccine_df8[vaccine_df8['District_Key'] == 'GJ_Gandhinagar']


# In[25]:


# Adding null columns for storing the weekly first/second dose data in future
vaccine_df8['Weekly_First_Dose'] = np.nan
vaccine_df8['Weekly_Second_Dose'] = np.nan
vaccine_df8


# In[26]:


# First week (17-1-2021 to 23-1-2021) values are same as 23-01-2021 values as data is cumulative
vaccine_df8.iloc[0,4] = vaccine_df6.iloc[0,2]
vaccine_df8.iloc[0,5] = vaccine_df6.iloc[0,3]
vaccine_df8


# In[27]:


# For finding every weeks data for each district, subtract last weeks data from present weeks data
# For first week's data of every district use 23-01-2021 data
for i in range(1,len(vaccine_df8)):
    if vaccine_df8.iloc[i,0] == vaccine_df8.iloc[i-1,0]:
        vaccine_df8.iloc[i,4] = int(vaccine_df8.iloc[i,2] - vaccine_df8.iloc[i-1,2])
        vaccine_df8.iloc[i,5] = int(vaccine_df8.iloc[i,3] - vaccine_df8.iloc[i-1,3])
    else:
        vaccine_df8.iloc[i,4] = int(vaccine_df8.iloc[i,2])
        vaccine_df8.iloc[i,5] = int(vaccine_df8.iloc[i,3])


# In[28]:


vaccine_df8


# In[29]:


# Separating results from complete dataset
week_district_result = vaccine_df8[['District_Key','Weekly_First_Dose','Weekly_Second_Dose']]
week_district_result


# In[30]:


# Changing the type as number people vaccinated can't be fractional
week_district_result= week_district_result.astype({"Weekly_First_Dose": int,"Weekly_Second_Dose": int})
week_district_result


# In[31]:


# Adding null column to store weekid
week_district_result['Week_ID'] = np.nan
week_district_result


# In[32]:


# Filling weekid's for every district
count=1
for i in range(len(week_district_result)):
    if week_district_result.iloc[i,0] != week_district_result.iloc[i-1,0]:
        count = 1
    week_district_result.iloc[i,3] = count
    count += 1


# In[33]:


week_district_result


# In[34]:


week_district_result = week_district_result.astype({"Week_ID": int})
week_district_result


# In[35]:


# Changing the name of columns in resulting dataframe 
week_district_result.columns = ['districtid', 'dose1', 'dose2', 'weekid']
week_district_result


# In[36]:


# Storing the result
# district-weekly-vaccinated-count-time.csv contains number of first/second doses administered in every week for all districts
week_district_result.to_csv('Outputs/district-weekly-vaccinated-count-time.csv',index=False)


# ## Now finding number of first/second doses administered monthly for every district
# 

# In[37]:


## Finding the last dates of all months from 16-1-2021 (as vaccination dateset starts from this date) to last date 14-8-2021
# last date taken as standard last date throughout the Assignment 
## 14/02/2021 is last date of first month, 14/03/2021 is last date of second month and so on
start =datetime.date(2021,1,14)
end = datetime.date(2021,8,14)
date_list = []
cur = start
while cur < end:
    cur = cur + relativedelta(months=+1)
    date_list.append(str(cur.strftime("%d/%m/%Y")))
date_list


# In[38]:


# As in our vaccination dataset for every date 4th columns represents number of first dose administered and 5th column represents
# number of second dose administered so adding their index to datelist
month_date_list = []
for i in date_list:
    month_date_list.append(i+'.3')
    month_date_list.append(i+'.4')
month_date_list


# In[39]:


month_column_list = ['S No', 'State_Code', 'State', 'District_Key', 'Cowin Key', 'District'] + month_date_list
month_column_list


# In[40]:


# Separating only useful columns from vaccination dataset
vaccine_df2 = vaccine_df.loc[:,month_column_list]
vaccine_df2


# In[41]:


# Creating a list with first dose dates and second dose dates
first_dose_month_column_list = []
second_dose_month_column_list = []
for i in date_list:
    first_dose_month_column_list.append(i+'.3')
    second_dose_month_column_list.append(i+'.4')


# In[42]:


first_dose_month_column_list


# In[43]:


second_dose_month_column_list


# In[44]:


## Melting the columns containing first dose data for every date present in first_dose_column_list

vaccine_df3 = pd.melt(vaccine_df2,id_vars=['S No','State_Code','State','District_Key','Cowin Key','District'],
        value_vars=first_dose_month_column_list, value_name = 'First_Dose',var_name = 'Date')
vaccine_df3


# In[45]:


# first row shows the number of first dose administered in district nicobar till 14/02/2021 (i.e in first month)
# second row shows the number of first dose administered in district nicobar till 14/03/2021 (i.e in first+second month)
# third row shows the number of first dose administered in district nicobar till 14/04/2021 (i.e first+second_third month)
# and so on
vaccine_df3[vaccine_df3['District_Key']=='AN_Nicobars']


# In[46]:


## Melting the columns containing second dose data for every date present in second_dose_column_list

vaccine_df4 = pd.melt(vaccine_df2,id_vars=['S No','State_Code','State','District_Key','Cowin Key','District'],
        value_vars=second_dose_month_column_list, value_name = 'Second_Dose',var_name = 'Date')
vaccine_df4


# In[47]:


# first row shows the number of second dose administered in district nicobar till 14/02/2021 (i.e in first month)
# second row shows the number of second dose administered in district nicobar till 14/03/2021 (i.e in first+second month)
# third row shows the number of second dose administered in district nicobar till 14/04/2021 (i.e first+second_third month)
# and so on
vaccine_df4[vaccine_df4['District_Key']=='AN_Nicobars']


# In[48]:


# Adding second dose data to dataframe containing first dose data as well
vaccine_df3['Second_Dose'] = vaccine_df4['Second_Dose']
vaccine_df3


# In[49]:


# As seen earlier some districts (like Gandhinagar) have two entries for every date, so dealing with it in similar manner using
# groupby
vaccine_df3[vaccine_df3['District_Key'] == 'GJ_Gandhinagar']


# In[50]:


vaccine_df5 = vaccine_df3.drop(['S No','State_Code','State','Cowin Key','District'],axis=1)
vaccine_df5


# In[51]:


vaccine_df5['Date'] = vaccine_df5['Date'].str.split('.').str[0]

vaccine_df5['Date'] = pd.to_datetime(vaccine_df5['Date'],format='%d/%m/%Y')
vaccine_df5


# In[52]:


vaccine_df6 = vaccine_df5.sort_values(by=['District_Key','Date'])
vaccine_df6


# In[53]:


vaccine_df6.reset_index(drop=True,inplace=True)
vaccine_df6


# In[54]:


vaccine_df7 = vaccine_df6.groupby(['District_Key','Date']).sum()
vaccine_df7


# In[55]:


vaccine_df8 = vaccine_df7.reset_index()
vaccine_df8


# In[56]:


# the ouput shows now Gandhinagar has only one entry for every date 
vaccine_df8[vaccine_df8['District_Key'] == 'GJ_Gandhinagar']


# In[57]:


vaccine_df8['Monthly_First_Dose'] = np.nan
vaccine_df8['Monthly_Second_Dose'] = np.nan
vaccine_df8


# In[58]:


vaccine_df8.iloc[0,4] = vaccine_df6.iloc[0,2]
vaccine_df8.iloc[0,5] = vaccine_df6.iloc[0,3]
vaccine_df8


# In[59]:


# To find the number of first/second dose administered every month subtract current month vaccination data from previous months 
# vaccination data
# And for first month of every district using the value of first month (date 14-2-2021) as it is
for i in range(1,len(vaccine_df8)):
    if vaccine_df8.iloc[i,0] == vaccine_df8.iloc[i-1,0]:
        vaccine_df8.iloc[i,4] = int(vaccine_df8.iloc[i,2] - vaccine_df8.iloc[i-1,2])
        vaccine_df8.iloc[i,5] = int(vaccine_df8.iloc[i,3] - vaccine_df8.iloc[i-1,3])
    else:
        vaccine_df8.iloc[i,4] = int(vaccine_df8.iloc[i,2])
        vaccine_df8.iloc[i,5] = int(vaccine_df8.iloc[i,3])
vaccine_df8


# In[60]:


monthly_district_result = vaccine_df8[['District_Key','Monthly_First_Dose','Monthly_Second_Dose']]
monthly_district_result


# In[61]:


monthly_district_result= monthly_district_result.astype({"Monthly_First_Dose": int,"Monthly_Second_Dose": int})
monthly_district_result


# In[62]:


monthly_district_result['Month_ID'] = np.nan
monthly_district_result


# In[63]:


# filling monthid for each district
count=1
for i in range(len(monthly_district_result)):
    if monthly_district_result.iloc[i,0] != monthly_district_result.iloc[i-1,0]:
        count = 1
    monthly_district_result.iloc[i,3] = count
    count += 1
monthly_district_result


# In[64]:


monthly_district_result = monthly_district_result.astype({"Month_ID": int})
monthly_district_result


# In[65]:


monthly_district_result.columns = ['districtid', 'dose1', 'dose2', 'monthid']
monthly_district_result


# In[66]:


# Storing the result
# district-monthly-vaccinated-count-time.csv contains number of first/second doses administered in every month for all districts
monthly_district_result.to_csv('Outputs/district-monthly-vaccinated-count-time.csv',index=False)


# ## Now finding number of first/second dose adminitered overall for every district

# In[67]:


overall_district_result = monthly_district_result[['districtid','dose1','dose2']]
overall_district_result


# In[68]:


# To find number of first/second doses administered in every district in total just summing first/second doses administered
# for all months
overall_district_result = overall_district_result.groupby('districtid').sum()
overall_district_result


# In[69]:


overall_district_result.reset_index(inplace=True)
overall_district_result


# In[70]:


# Storing the result
# district-overall-vaccinated-count-time.csv contains number of first/second doses administered overall for each districts
overall_district_result.to_csv('Outputs/district-overall-vaccinated-count-time.csv',index=False)


# ## Now finding number of first/second doses administered weekly for every state

# In[71]:


'''to find the number of first/second doses administered weekly for every state, summing the first/second dose values present 
in each district of that state'''
week_district_result


# In[72]:


weekly_state_result = week_district_result.copy()


# In[73]:


# Separating the stateid's from district id's
weekly_state_result['stateid'] = weekly_state_result['districtid'].str.split('_').str[0]
weekly_state_result


# In[74]:


weekly_state_result.drop(['districtid'], axis = 1, inplace = True)
weekly_state_result


# In[75]:


# for every state summing all of its districts data
weekly_state_result = weekly_state_result.groupby(['stateid','weekid']).sum()
weekly_state_result


# In[76]:


weekly_state_result.reset_index(inplace=True)
weekly_state_result


# In[77]:


weekly_state_result.to_csv('Outputs/state-weekly-vaccinated-count-time.csv',index=False)


# ## Now finding number of first/second doses administered monthly for every state

# In[78]:


'''Similar to weekly vaccine data for states , adding vaccination data of all districts for every month of that state'''
monthly_district_result


# In[79]:


monthly_state_result = monthly_district_result.copy()


# In[80]:


monthly_state_result['stateid'] = monthly_state_result['districtid'].str.split('_').str[0]
monthly_state_result


# In[81]:


monthly_state_result.drop(['districtid'], axis = 1, inplace = True)
monthly_state_result


# In[82]:


monthly_state_result = monthly_state_result.groupby(['stateid','monthid']).sum()
monthly_state_result


# In[83]:


monthly_state_result.reset_index(inplace=True)
monthly_state_result


# In[84]:


monthly_state_result.to_csv('Outputs/state-monthly-vaccinated-count-time.csv',index=False)


# ## Now finding number of first/second doses administered overall for every state

# In[85]:


overall_district_result


# In[86]:


overall_state_result = overall_district_result.copy()


# In[87]:


overall_state_result['stateid'] = overall_state_result['districtid'].str.split('_').str[0]
overall_state_result


# In[88]:


overall_state_result.drop(['districtid'], axis = 1, inplace = True)
overall_state_result


# In[89]:


overall_state_result = overall_state_result.groupby(['stateid']).sum()
overall_state_result


# In[90]:


overall_state_result.reset_index(inplace=True)
overall_state_result


# In[91]:


overall_state_result.to_csv('Outputs/state-overall-vaccinated-count-time.csv',index=False)


# In[ ]:




