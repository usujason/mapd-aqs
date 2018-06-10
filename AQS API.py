
# coding: utf-8

# # Air Quality Index Analysis
# 
# 
# 
# ### Links
# [AQI Calculation](https://forum.airnowtech.org/t/the-aqi-equation/169)<br>
# [Calculating the Average](https://forum.airnowtech.org/t/daily-and-hourly-aqi-ozone/170)<br>
# [Online AQI Calculator](https://airnow.gov/index.cfm?action=airnow.calculator)<br>
# 
# ### Pollutants Used
# Ozone (44201)<br>
# PM2.5 (88101)<br>
# PM10 (81102)<br>
# CO (42101)<br>
# SO2 (42401)<br>
# NO2 (42602)<br>
# 
# 
# ### Average Calculation Parameters
# __Average Requirements__<br>
#  Ozone = 8-hour <br>
#  PM2.5 = 24-hour <br>
#  PM10 = 24-hour <br>
#  CO = 8-hour <br>
#  SO2 = 1-hour <br>
#  NO2 = 1-hour <br>
#  
# __Decimal truncation__<br>
#  Ozone = 3 places<br>
#  PM2.5 = 1 place<br>
#  PM10 = Integer<br>
#  CO = 1 place<br>
#  SO2 = integer<br>
#  NO2 = integer

# In[66]:


# Import libraries
import pandas as pd
import io
import requests
import bisect
import numpy as np


# In[67]:


# Import Config file defaults
from src import config

# Define Start and End Dates
config.bDate = '20170101'
config.eDate = '20170102'

# Define AQI Lower and Upper Bound Lookup Tables

#Ozone
ozone_breaks_lower = {(0.000, 0.054): 0, (0.055, 0.070): 51, (0.071, 0.085): 101, (0.086, 0.105): 151, (0.106, 0.200): 201, (0.405, 0.504): 301, (0.505, 0.604): 401}
ozone_breaks_upper = {(0.000, 0.054): 50, (0.055, 0.070): 100, (0.071, 0.085): 150, (0.086, 0.105): 200, (0.106, 0.200): 300, (0.405, 0.504): 400, (0.505, 0.604): 500}

#PM2.5


#PM10


#C02


#SO2


#NO2




# In[68]:


# Function to return lower and upper AQI ranges
def get_range(table, measurement):
    for key in table:
        if key[0] < measurement < key[1]:
            return table[key]


# In[69]:


# Running the query for an entire state exceeds API size limits so we need to query by county
# For the defined stateName, loop through counties and execute API call for each county
df = pd.DataFrame()

from src import county

for key in county.counties[config.stateName]:
    config.countyCode = county.counties[config.stateName][key]
    
    #Build API request URL
    requestURL = config.apiURL + 'user=' + config.apiUser + '&pw=' + config.apiPassword + '&format=' + config.outputFormat     + '&pc=' + config.aqsClass + '&bdate=' + config.bDate + '&edate=' + config.eDate + '&state=' + config.stateCode     + '&county=' + config.countyCode

    #print(requestURL)
    apiResp = requests.get(requestURL)

    #TODO: Add error handling if request does not return a 200 code

    aqs_df = pd.read_csv(io.StringIO(apiResp.content.decode('utf-8')))
    df = pd.concat([df,aqs_df])
               


# In[70]:


#Cleanup data frame

#Remove 'END OF FILE' entries
df = df[df['Latitude'] != 'END OF FILE']

#Remove all but 1-hour observations
df = df[df['Sample Duration'] == '1 HOUR']

#Sorting
df = df.sort_values(['County Code', 'Site Num', 'AQS Parameter Desc', 'Date Local', '24 Hour Local'])


# In[72]:


# Create a working Dataframe based on County, Site, and AQS Parameter Desc
# TODO: This needs to be dynamic to build for each county, site, and paramter
df_ = df.loc[(df['County Code'] == 3) & (df['Site Num'] == 3) & (df['AQS Parameter Desc'] == 'Ozone')]


# In[96]:


#Reverse the order of the data frame so Pandas rolling can use the "look back" window
#Use Pandas rolling to calculate 8 hour average
df_ = df_[::-1]
df_['8 Hour Avg'] = df_['Sample Measurement'].rolling(8, min_periods=8).mean()
df_['8 Hour Avg'] = df_['8 Hour Avg'].round(3)
df_ = df_[pd.notnull(df_['8 Hour Avg'])]


# In[99]:


# Calculate AQI for each measurment observation
for i, row in df_.iterrows():
   aqiAvg = row["8 Hour Avg"]
   
   if np.isnan(aqiAvg) == False:
       aqiLow = get_range(ozone_breaks_lower, aqiAvg)
       aqiHigh = get_range(ozone_breaks_upper, aqiAvg)
   
       breakRange = [key for key in ozone_breaks_lower.items() if key[1] == value][0][0]
   
       breakRangeLow = breakRange[0]
       breakRangeHigh = breakRange[1]
   
       rowAqi = (aqiHigh - aqiLow)/(breakRangeHigh - breakRangeLow)*(aqiAvg - breakRangeLow) + aqiLow
       rowAqi = int(rowAqi)
       
       df_.set_value(i,'AQI',rowAqi)    
       
       print (aqiAvg, aqiLow, aqiHigh, breakRangeLow, breakRangeHigh, rowAqi)



# In[102]:


# Create a combined dataframe which concats each of the processing dataframes (df_) for each loop through county/site/pollutant
dfCombined = pd.DataFrame()
dfCombined = pd.concat([dfCombined,df_])


# In[103]:


#Output for debugging/validation
df_.to_csv('AQI_Calc_Out.csv', sep=',')


# In[ ]:


#TODO: Create a daily summary Dataframe - AQI is defined as the single highest pollutant per day; we can also look at
#the highest measurement rate for each pollutant rather than a rolled up AQI measure. Although we may be able to 
#handle this in mapD

