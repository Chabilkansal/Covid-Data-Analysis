#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime


# In[2]:


# Reading vaccination data in df
df = pd.read_csv('vaccine_data_new.csv')
df


# In[3]:


# Reading Population Census data in census_df
census_df = pd.read_excel('DDW_PCA0000_2011_Indiastatedist.xlsx')
census_df


# In[4]:


# Creating a temporary Dataframe for storing district_wise first dose and second dose data
newdf = pd.DataFrame()
newdf['State'] = df['State']
newdf['District'] = df['District']
newdf['District_Key'] = df['District_Key']
newdf


# In[5]:


newdf.drop_duplicates(inplace=True)


# In[6]:


newdf


# In[7]:


# As the vaccination data is cumulative so to find the number of female/males vaccinated of a district only taking the last 
# date's data is enough.
# Taking 14 August 2021 as standard last date for entire assignment.
vaccine_df_copy = df.copy()

#Converting last date number of female/male vaccinated columns to numeric

vaccine_df_copy['14/08/2021.5'] = pd.to_numeric(vaccine_df_copy['14/08/2021.5'])
vaccine_df_copy['14/08/2021.6'] = pd.to_numeric(vaccine_df_copy['14/08/2021.6'])
vaccine_df_copy


# In[8]:


newdf.reset_index(drop=True,inplace=True)


# In[9]:


newdf


# In[10]:


# Creating null columns for storing number of males/females vaccinated data in future
newdf['Males_Vaccinated'] = np.nan
newdf['Females_Vaccinated'] = np.nan
newdf


# In[11]:


# We can see below that using just district key for identifying unique district is not enough in some cases
# So we have to add vaccine data for such district to calculate actual number of first/second doses
vaccine_df_copy[vaccine_df_copy['District_Key'] == 'GJ_Gandhinagar']


# In[12]:


# Filling number of males/females vaccinated data from vaccination data (vaccine_df_copy) also as mentioned earlier 
# adding the vaccine data for districts with multiple entries (example: Gandhinagar and Gandhinagar Corporation) by suming both values
for i in range(len(newdf)):
    try:
        tempdf = vaccine_df_copy[(vaccine_df_copy['State'] == newdf.iloc[i,0])&(vaccine_df_copy['District'] == newdf.iloc[i,1])]
        sumdf = tempdf.sum(axis=0)
        newdf.iloc[i,3] = pd.to_numeric(sumdf.loc['14/08/2021.5'])
        newdf.iloc[i,4] = pd.to_numeric(sumdf.loc['14/08/2021.6'])
    except:
        print(newdf.iloc[i,0],' ',newdf.iloc[i,1])
newdf


# In[13]:


newdf.isnull().sum()


# In[14]:


#Lowering the case of the district names and changing their names according to census data
newdf['District'] = newdf['District'].str.lower()
newdf


# In[15]:


# As many district's in vaccination and census data have different spellings so we need to convert any one to match other
# this function maps the name of districts from vaccination data to names of same district in census data
# this will be used to change names of vaccination data 

def corrected_name( x ):
    if(x=="ahmedabad"):
        x = "ahmadabad"
    if(x=="ahmednagar"):
        x = "ahmadnagar"
    if(x=="bagalkote"):
        x = "bagalkot"
    if(x=="bandipora"):
        x = "bandipore"
    if(x=="barabanki"):
        x = "bara banki"
    if(x=="buldhana"):
        x = "buldana"
    if(x=="chikkamagaluru"):
        x = "chikmagalur"
    if(x=="chittorgarh"):
        x = "chittaurgarh"
    if(x=="dadra and nagar haveli"):
        x = "dadra & nagar haveli"
    if(x=="darjeeling"):
        x = "darjiling"
    if(x=="dahod"):
        x = "dohad"
    if(x=="gurugram"):
        x = "gurgaon"
    if(x=="haridwar"):
        x = "hardwar"
    if(x=="janjgir champa"):
        x = "janjgir - champa"
    if(x=="kanyakumari"):
        x = "kanniyakumari"
    if(x=="khandwa"):
        x = "khandwa (east nimar)"
    if(x=="khargone"):
        x = "khargone (west nimar)"
    if(x=="kutch"):
        x = "kachchh"
    if(x=="lahaul and spiti"):
        x = "lahul & spiti"
    if(x=="leh"):
        x = "leh(ladakh)"
    if(x=="mahabubnagar"):
        x = "mahbubnagar"
    if(x=="mysuru"):
        x = "mysore"
    if(x=="north 24 parganas"):
        x = "north twenty four parganas"
    if(x=="south 24 parganas"):
        x = "south twenty four parganas"
    if(x=="north and middle andaman"):
        x = "north  & middle andaman"
    if(x=="panchmahal"):
        x = "panch mahals"
    if(x=="shopiyan"):
        x = "shupiyan"
    if(x=="y.s.r. kadapa"):
        x = "y.s.r."
    if(x=="bengaluru urban"):
        x = "bangalore"
    if(x=="aizwal"):
        x = "aizawl"
    if(x=="rae bareilly"):
        x = "rae bareli"
    if(x=='angul'):
        x = 'anugul'
    if(x=='ashok nagar'):
        x = 'ashoknagar'
    if(x=='budgam'):
        x = 'badgam'
    if(x=='bageshwar'):
        x = 'baleshwar'
    if(x=='banaskantha'):
        x = 'banas kantha'
    if(x=='bengaluru rural'):
        x = 'bangalore rural'
    if(x=='bangalore urban'):
        x = 'bengaluru urban'
    if(x=='baramulla'):
        x = 'baramula'
    if(x=='boudh'):
        x = 'baudh'
    if(x=='belagavi'):
        x = 'belgaum'
    if(x=='ballari'):
        x = 'bellary'
    if(x=='bametara'):
        x = 'bemetara'
    if(x=='beed'):
        x = 'bid'
    if(x=='biswanath'):
        x = 'bishwanath'
    if(x=='chamarajanagara'):
        x = 'chamarajanagar'
    if(x=='dantewada'):
        x = 'dakshin bastar dantewada'
    if(x=='deogarh'):
        x = 'debagarh'
    if(x=='devbhumi dwarka'):
        x = 'devbhumi dwaraka'
    if(x=='dholpur'):
        x = 'dhaulpur'
#     if(x=='east delhi'):
#         x = "delhi"
    if(x=='east karbi anglong'):
        x = 'karbi anglong'
    if(x=='ayodhya'):
        x = 'faizabad'
    if(x=='fategarh sahib'):
        x = 'fatehgarh sahib'
    if(x=='ferozepur'):
        x = 'firozpur'
    if(x=='gondia'):
        x = 'gondiya'
    if(x=='hooghly'):
        x = 'hugli'
    if(x=='jagatsinghpur'):
        x = 'jagatsinghapur'
    if(x=='jajpur'):
        x = 'jajapur'
    if(x=='jalore'):
        x = 'jalor'
    if(x=='janjgir-champa'):
        x = 'janjgir champa'
    if(x=='jhunjhunu'):
        x = 'jhunjhunun'
    if(x=='amroha'):
        x = 'jyotiba phule nagar'
    if(x=='kabirdham'):
        x = 'kabeerdham'
    if(x=='kaimur'):
        x = 'kaimur (bhabua)'
    if(x=='kanchipuram'):
        x = 'kancheepuram'
    if(x=='lakhimpur kheri'):
        x = 'kheri'
    if(x=='cooch behar'):
        x = 'koch bihar'
    if(x=='koderma'):
        x = 'kodarma'
    if(x=='komaram bheem'):
        x = 'komram bheem'
    if(x=='konkan division'): #not found
        x = 'konkan division'
    if(x=='lahul and spiti'):
        x = 'lahaul and spiti'
    if(x=='mehsana'):
        x = 'mahesana'
    if(x=='maharajganj'):
        x = 'mahrajganj'
    if(x=='malda'):
        x = 'maldah'
    if(x=='marigaon'):
        x = 'morigaon'
    if(x=='medchal–malkajgiri'):
        x = 'medchal malkajgiri'
    if(x=='sri muktsar sahib'): #not found
        x = 'muktsar'
#     if(x=='mumbai city'):
#         x = 'mumbai'
#     if x== 'mumbai suburban':
#         x = 'mumbai'
    if x== 'nandubar':
        x = 'nandurbar'
    if x== 'narsinghpur':
        x = 'narsimhapur'
    if x== 'nav sari':
        x = 'navsari'
#     if x=='new delhi' :
#         x = 'delhi'
    if x== 'noklak': #not found
        x = 'noklak'
#     if x== 'north delhi':
#         x = 'delhi'
#     if x== 'north east delhi':
#         x = 'delhi'
#     if x== 'north west delhi':
#         x = 'delhi'
    if x== 'pakaur':
        x = 'pakur'
    if x== 'palghat':
        x = 'palghar'
    if x== 'panch mahal':
        x = 'panchmahal'
    if x== 'west champaran':
        x = 'pashchim champaran'
    if x== 'west singhbhum':
        x = 'pashchimi singhbhum'
    if x== 'pattanamtitta':
        x = 'pathanamthitta'
    if x== 'east champaran':
        x = 'purba champaran'
    if x== 'east singhbhum':
        x = 'purbi singhbhum'
    if x== 'purulia':
        x = 'puruliya'
    if x== 'rajauri':
        x = 'rajouri'
    if x== 'ranga reddy':
        x = 'rangareddy'
    if x== 'ri-bhoi':
        x = 'ribhoi'
    if x== 'sabarkantha':
        x = 'sabar kantha'
    if x== 's.a.s. nagar':
        x = 'sahibzada ajit singh nagar'
    if x== 'sait kibir nagar':
        x = 'sant kabir nagar'
    if x== 'bhadohi':
        x = 'sant ravidas nagar (bhadohi)'
    if x== 'sepahijala':
        x = 'sipahijala'
    if x== 'seraikela kharsawan':
        x = 'saraikela-kharsawan'
    if x== 'shahdara': #not found
        x = 'shahdara'
    if x== 'shaheed bhagat singh nagar':
        x = 'shahid bhagat singh nagar'
    if x== 'sharawasti':
        x = 'shrawasti'
    if x== 'shivamogga':
        x = 'shimoga'
    if x== 'shopian':
        x = 'shopiyan'
    if x== 'siddharth nagar':
        x = 'siddharthnagar'
    if x== 'sivagangai':
        x = 'sivaganga'
    if x== 'sonapur':
        x = 'subarnapur'
#     if x== 'south delhi':
#         x = 'delhi'
#     if x== 'south east delhi':
#         x = 'delhi'
    if x== 'south salmara-mankachar':
        x = 'south salmara mankachar'
#     if x== 'south west delhi':
#         x = 'delhi'
    if x== 'sri ganganagar':
        x = 'ganganagar'
    if x== 's.p.s. nellore':
        x = 'sri potti sriramulu nellore'
    if x== 'dang':
        x = 'the dangs'
    if x== 'nilgiris':
        x = 'the nilgiris'
    if x== 'thoothukudi':
        x = 'thoothukkudi'
    if x== 'tiruchchirappalli':
        x = 'tiruchirappalli'
    if x== 'tirunelveli kattabo':
        x = 'tirunelveli'
    if x== 'tiruvanamalai':
        x = 'tiruvannamalai'
    if x== 'tumakuru':
        x = 'tumkur'
    if x== 'west delhi':
        x = 'delhi'
    if x== 'yadagiri':
        x = 'yadadri bhuvanagiri'
    return x


# In[16]:


# Using above function to map district names
newdf['District'] = newdf['District'].apply(corrected_name)
newdf


# In[17]:


# Separating district population data from complete census data
district_census = census_df[census_df['Level'] == 'DISTRICT']
district_census


# In[18]:


# Lowering the case of the names of the district in census data so that they can match with our vaccination data
district_census['Name'] = district_census['Name'].str.lower()
district_census['Name'] = district_census['Name'].str.strip()
district_census


# In[19]:


# Creating  a null columns for storing the population data in future
newdf['Male_Pop'] = np.nan
newdf['Female_Pop'] = np.nan
newdf


# In[20]:


newdf.reset_index(drop=True,inplace=True)
newdf


# ### Below Cell shows that there are same name districts in our data (newdf) so after filling the population data from district census we have to manually correct some population values later

# In[21]:


val_count = newdf['District'].value_counts()

val_count[val_count>1]


# In[22]:


# Filling the population values from district_census data in our newdf
# Also printing the names of the district's not present in census data
for i in newdf.index:
    try:
        newdf.iloc[i,6] = int(district_census[district_census['Name'] == newdf.iloc[i,1].strip()].iloc[0]['TOT_F'])
        newdf.iloc[i,5] = int(district_census[district_census['Name'] == newdf.iloc[i,1].strip()].iloc[0]['TOT_M'])
    except:
        print(newdf.iloc[i,1])


# In[23]:


newdf


# In[24]:


newdf.isnull().sum()


# In[25]:


# Deleting the rows of the district that are not present in census data
district_result_df = newdf.dropna()
district_result_df


# In[26]:


district_result_df.reset_index(drop=True,inplace=True)


# In[27]:


district_result_df


# ### Duplicate Disticts
# Balrampur     
# Hamirpur      
# Bilaspur      
# Pratapgarh    
# Aurangabad  
# ### Manually Correcting duplicate district population values from census csv file

# census data contains only balrampur district of Uttar Pradesh so drop balrampur district of Chattisgarh

# In[28]:


# census data contains balrampur district of Uttar Pradesh only so dropping  balrampur district of Chattisgarh
district_result_df[(district_result_df['State'] == 'Chhattisgarh') &(district_result_df['District'] == 'balrampur')]


# In[29]:


district_result_df.drop([97],axis=0,inplace=True)


# In[30]:


district_result_df.reset_index(drop=True,inplace=True)
district_result_df


# ### Correcting remaining duplicate district population values manually

# In[31]:


district_result_df[(district_result_df['State'] == 'Uttar Pradesh') &(district_result_df['District'] == 'hamirpur')]


# In[32]:


district_result_df.iloc[548,5] = 593537
district_result_df.iloc[548,6] = 510748


# In[33]:


district_result_df[(district_result_df['State'] == 'Uttar Pradesh') &(district_result_df['District'] == 'hamirpur')]


# In[34]:


district_result_df[(district_result_df['State'] == 'Chhattisgarh') &(district_result_df['District'] == 'bilaspur')]


# In[35]:


district_result_df.iloc[99,5] = 1351574
district_result_df.iloc[99,6] = 1312055


# In[36]:


district_result_df[(district_result_df['State'] == 'Chhattisgarh') &(district_result_df['District'] == 'bilaspur')]


# In[37]:


district_result_df[(district_result_df['State'] == 'Uttar Pradesh') &(district_result_df['District'] == 'pratapgarh')]


# In[38]:


district_result_df.iloc[571,5] = 1606085
district_result_df.iloc[571,6] = 1603056


# In[39]:


district_result_df[(district_result_df['State'] == 'Uttar Pradesh') &(district_result_df['District'] == 'pratapgarh')]


# In[40]:


district_result_df[(district_result_df['State'] == 'Maharashtra') &(district_result_df['District'] == 'aurangabad')]


# In[41]:


district_result_df.iloc[321,5] = 1924469
district_result_df.iloc[321,6] = 1776813


# In[42]:


district_result_df[(district_result_df['State'] == 'Maharashtra') &(district_result_df['District'] == 'aurangabad')]


# In[43]:


district_result_df


# In[44]:


# Calculating the Ratio of number of females vaccinated to number of males vaccinated 
# Also the ratio of population of females to population of male for every district
district_result_df['F_to_M_Vaccination_Ratio'] = district_result_df['Females_Vaccinated'] / district_result_df['Males_Vaccinated']
district_result_df['F_to_M_Population_Ratio'] = district_result_df['Female_Pop'] / district_result_df['Male_Pop']
district_result_df['Ratio_of_Ratios'] = district_result_df['F_to_M_Vaccination_Ratio'] / district_result_df['F_to_M_Population_Ratio']
district_result_df


# In[45]:


district_result_df.drop(['State','District','Males_Vaccinated','Females_Vaccinated','Male_Pop','Female_Pop'],axis=1,inplace = True)
district_result_df


# In[46]:


district_result_df.columns = ['districtid','vaccinationratio', 'populationratio', 'ratioofratios']
district_result_df


# In[47]:


#  Saving the result in district-vaccination-population-ratio.csv
district_result_df.to_csv('Outputs/district-vaccination-population-ratio.csv',index=False)


# ## Now Doing same thing for State Data

# In[48]:


# Creating a temporary dataframe to store the vaccination data for each state
newdf = pd.DataFrame()
newdf['State'] = df['State'].unique()
newdf


# In[49]:


# Adding null columns to newdf for vaccination data
newdf['Males_Vaccinated'] = np.nan
newdf['Females_Vaccinated'] = np.nan
newdf


# In[50]:


# Filling number of males/females vaccinated data for each state
# As vaccine_df contains data district wise so adding  number of males/females vaccinated of all the district of a state
for i in range(len(newdf)):
    tempdf = vaccine_df_copy[vaccine_df_copy['State'] == newdf.iloc[i,0]]
    sumdf = tempdf.sum(axis=0)
    newdf.iloc[i,1] = pd.to_numeric(sumdf.loc['14/08/2021.5'])
    newdf.iloc[i,2] = pd.to_numeric(sumdf.loc['14/08/2021.6'])
newdf


# In[51]:


# Separating state population data from complete census data
state_census = census_df[census_df['Level'] == 'STATE']
state_census


# In[52]:


newdf


# In[53]:


# Adding a null column to store state population data in future
newdf['Male_Pop'] = np.nan
newdf['Female_Pop'] = np.nan
newdf


# In[54]:


# Converting the state name's to upper case so that the names could match with state_census data
newdf['State'] = newdf['State'].apply(lambda x: x.upper())
newdf


# In[55]:


# Changing the names of states according to census data
newdf.replace('ANDAMAN AND NICOBAR ISLANDS', 'ANDAMAN & NICOBAR ISLANDS',inplace=True)
newdf.replace('DELHI', 'NCT OF DELHI',inplace=True)


# In[56]:


newdf


# In[57]:


# Filling that state population values from state_census dataframe
# Also printing the names of the states not present in state census data
for i in newdf.index:
    try:
        newdf.iloc[i,4] = int(state_census[state_census['Name'] == newdf.iloc[i,0]].iloc[0]['TOT_F'])
        newdf.iloc[i,3] = int(state_census[state_census['Name'] == newdf.iloc[i,0]].iloc[0]['TOT_M'])
    except:
        print(newdf.iloc[i,0])


# In[58]:


newdf


# In[59]:


# As state census data contains dadra & nagar haveli population and daman  & diu population seperately, adding both values
# to find the population of Union territory DADRA AND NAGAR HAVELI AND DAMAN AND DIU
newdf.iloc[7,3] = state_census[state_census['Name']=='DADRA & NAGAR HAVELI'].iloc[0]['TOT_M'] + state_census[state_census['Name']=='DAMAN & DIU'].iloc[0]['TOT_M']
newdf.iloc[7,4] = state_census[state_census['Name']=='DADRA & NAGAR HAVELI'].iloc[0]['TOT_F'] + state_census[state_census['Name']=='DAMAN & DIU'].iloc[0]['TOT_F']


# In[60]:


newdf


# In[61]:


# Dropping remaining states as their population state in not present in 2011 census data
newdf.dropna(inplace=True)


# In[62]:


newdf


# In[63]:


newdf.reset_index(drop=True,inplace=True)


# In[64]:


newdf


# In[65]:


state_result_df = newdf.copy()


# In[66]:


## Calculating the Ratio of number of females vaccinated to number of males vaccinated 
# Also the ratio of population of females to population of male for every state
state_result_df['F_to_M_Vaccination_Ratio'] = state_result_df['Females_Vaccinated'] / state_result_df['Males_Vaccinated']
state_result_df['F_to_M_Population_Ratio'] = state_result_df['Female_Pop'] / state_result_df['Male_Pop']
state_result_df['Ratio_of_Ratios'] = state_result_df['F_to_M_Vaccination_Ratio'] / state_result_df['F_to_M_Population_Ratio']
state_result_df


# In[67]:


state_result_df.drop(['Males_Vaccinated','Females_Vaccinated','Male_Pop','Female_Pop'],axis=1,inplace = True)
state_result_df


# In[68]:


state_result_df.columns = ['stateid','vaccinationratio', 'populationratio', 'ratioofratios']
state_result_df


# In[69]:


#  Saving the result in state-vaccination-population-ratio.csv
state_result_df.to_csv('Outputs/state-vaccination-population-ratio.csv',index=False)


# ## Now doing the same thing for India

# In[70]:


# Finding the number of males/females vaccinated in India till last data (14/08/2021)
males_vaccinated_india = vaccine_df_copy['14/08/2021.5'].sum()
females_vaccinated_india = vaccine_df_copy['14/08/2021.6'].sum()


# In[71]:


# Creating dataframe to store result
india_result_df = pd.DataFrame()


# In[72]:


# Adding a single row India
india_result_df['Country'] = ['India']
india_result_df


# In[73]:


# Adding vaccination data
india_result_df['Males_Vaccinated'] = males_vaccinated_india
india_result_df['Females_Vaccinated'] = females_vaccinated_india
india_result_df


# In[74]:


census_df


# In[75]:


# Finding male/female population in india from census data
males_population_india = census_df.iloc[0]['TOT_M']
females_population_india = census_df.iloc[0]['TOT_F']


# In[76]:


# Adding population of males/females of India to dataframe
india_result_df['Male_Pop'] = males_population_india
india_result_df['Female_Pop'] = females_population_india
india_result_df


# In[77]:


## Calculating the Ratio of number of females vaccinated to number of males vaccinated 
# Also the ratio of population of females to population of male for India
india_result_df['F_to_M_Vaccination_Ratio'] = india_result_df['Females_Vaccinated'] / india_result_df['Males_Vaccinated']
india_result_df['F_to_M_Population_Ratio'] = india_result_df['Female_Pop'] / india_result_df['Male_Pop']
india_result_df['Ratio_of_Ratios'] = india_result_df['F_to_M_Vaccination_Ratio'] / india_result_df['F_to_M_Population_Ratio']
india_result_df


# In[78]:


india_result_df.drop(['Males_Vaccinated','Females_Vaccinated','Male_Pop','Female_Pop'],axis=1,inplace = True)
india_result_df


# In[79]:


india_result_df.columns = ['countryid','vaccinationratio', 'populationratio', 'ratioofratios']
india_result_df


# In[80]:


#  Saving the result in india-vaccinated-dose-ratio.csv
india_result_df.to_csv('Outputs/india-vaccination-population-ratio.csv',index=False)

