
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

# In[1]:


# Import libraries
import pandas as pd
import io
import requests
import bisect
import numpy as np
import time


# In[2]:


# Import Config file defaults
from src import config

# Define Start and End Dates
config.bDate = '20170101'
config.eDate = '20170131'

# Define AQI Lower and Upper Bound Lookup Tables

#Ozone
ozone_breaks_lower = {(0.000, 0.054): 0, (0.055, 0.070): 51, (0.071, 0.085): 101, (0.086, 0.105): 151, (0.106, 0.200): 201, (0.405, 0.504): 301, (0.505, 0.604): 401}
ozone_breaks_upper = {(0.000, 0.054): 50, (0.055, 0.070): 100, (0.071, 0.085): 150, (0.086, 0.105): 200, (0.106, 0.200): 300, (0.405, 0.504): 400, (0.505, 0.604): 500}

#PM2.5
pm25_breaks_lower = {(0.0, 12.0): 0, (12.1, 35.4): 51, (35.5, 55.4): 101, (55.5, 150.4): 151, (150.5, 250.4): 201, (250.5, 350.4): 301, (350.5, 500.4): 401}
pm25_breaks_upper = {(0.0, 12.0): 50, (12.1, 35.4): 100, (35.5, 55.4): 150, (55.5, 150.4): 200, (150.5, 250.4): 300, (250.5, 350.4): 400, (350.5, 500.4): 500}


#PM10
pm10_breaks_lower = {(0.0, 54): 0, (55, 154): 51, (155, 254): 101, (255, 354): 151, (355, 424): 201, (425, 504): 301, (505, 604): 401}
pm10_breaks_upper = {(0.0, 54): 50, (55, 154): 100, (155, 254): 150, (255, 354): 200, (355, 424): 300, (425, 504): 400, (505, 604): 500}


#C0
co_breaks_lower = {(0.0, 4.4): 0, (4.5, 9.4): 51, (9.5, 12.4): 101, (12.5, 15.4): 151, (15.5, 30.4): 201, (30.5, 40.4): 301, (40.5, 50.4): 401}
co_breaks_upper = {(0.0, 4.4): 50, (4.5, 9.4): 100, (9.5, 12.4): 150, (12.5, 15.4): 200, (15.5, 30.4): 300, (30.5, 40.4): 400, (40.5, 50.4): 500}


#SO2
so2_breaks_lower = {(0.0, 35): 0, (36, 75): 51, (76, 185): 101, (186, 304): 151, (305, 604): 201, (605, 804): 301, (805, 1004): 401}
so2_breaks_upper = {(0.0, 35): 50, (36, 75): 100, (76, 185): 150, (186, 304): 200, (305, 604): 300, (605, 804): 400, (805, 1004): 500}


#NO2
no2_breaks_lower = {(0.0, 53): 0, (54, 100): 51, (101, 360): 101, (361, 649): 151, (650, 1249): 201, (1250, 1649): 301, (1650, 2049): 401}
no2_breaks_upper = {(0.0, 53): 50, (54, 100): 100, (101, 360): 150, (361, 649): 200, (650, 1249): 300, (1250, 1649): 400, (1650, 2049): 500}




# In[3]:


# Function to return lower and upper AQI ranges
def get_range(table, measurement):
    for key in table:
        if key[0] <= measurement <= key[1]:
            return table[key]


# In[4]:


start = time.time()
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
    
end = time.time()
print("Process Time: ", end - start)                   


# In[5]:


#Cleanup data frame

#Remove 'END OF FILE' entries
df = df[df['Latitude'] != 'END OF FILE']

#Remove all but 1-hour observations
df = df[df['Sample Duration'] == '1 HOUR']

#Force codes to int
df['County Code'] = df['County Code'].astype(int)
df['Site Num'] = df['Site Num'].astype(int)

#Sorting
df = df.sort_values(['County Code', 'Site Num', 'Parameter Code', 'Date Local', '24 Hour Local'])


# In[6]:


#AQI Calculation Function
def calc_aqi(df,county,site,param_code,param_rnd,avg_unit,breaks_lower,breaks_upper):
    df_activePollutant = df.loc[(df['County Code'] == activeCounties[i]) & (df['Site Num'] == activeSites[j]) & (df['Parameter Code'] == param_code)]
    
    #Reverse the order of the data frame so Pandas rolling can use the "look back" window
    #Use Pandas rolling to calculate 8 hour average
    df_activePollutant = df_activePollutant[::-1]
    df_activePollutant['Rolling Avg'] = df_activePollutant['Sample Measurement'].rolling(avg_unit, min_periods=avg_unit).mean()
    df_activePollutant['Rolling Avg'] = df_activePollutant['Rolling Avg'].round(param_rnd)
    
    df_activePollutant = df_activePollutant[pd.notnull(df_activePollutant['Rolling Avg'])]
    
    # Calculate AQI for each measurment observation in the current processing data frame
    for k, row in df_activePollutant.iterrows():
        aqiAvg = row["Rolling Avg"]
        
        if np.isnan(aqiAvg) == False:
            aqiLow = get_range(breaks_lower, aqiAvg)
            aqiHigh = get_range(breaks_upper, aqiAvg)
            
            if aqiLow is not None:
                breakRange = [key for key in breaks_lower.items() if key[1] == aqiLow][0][0]
   
                breakRangeLow = breakRange[0]
                breakRangeHigh = breakRange[1]
   
                rowAqi = (aqiHigh - aqiLow)/(breakRangeHigh - breakRangeLow)*(aqiAvg - breakRangeLow) + aqiLow
                rowAqi = int(rowAqi)
       
                df_activePollutant.set_value(k,'AQI',rowAqi)   
                
                #print(aqiAvg, aqiLow, rowAqi) 
                  
    return df_activePollutant


# In[7]:


start = time.time()
# Loop through County -> Site -> Parameter Code

# Create a combined dataframe which concats each of the processing dataframes (df_activePollutant) for each loop through county/site/pollutant
dfCombined = pd.DataFrame()

# Get a list of County Codes based on current dataset
activeCounties = df['County Code'].unique()
    
# Loop through each unique county code, create a processing df, process AQI calculations    
i = 0
while i < len(activeCounties):
    #print("Processing Active County", activeCounties[i])
    
    
    # Return a data frame for the active county being processed
    df_activeCounty = df.loc[(df['County Code'] == activeCounties[i])]
    
    # From the active county, get an array of sites to process
    activeSites = df_activeCounty['Site Num'].unique()
    
    # Loop through each site, within the active county
    j = 0
    
    while j < len(activeSites):
        #print("Processing Active Site", activeSites[j])
        
        # Call calc_aqi for each pollutant
        # PARAMS: 
        # primary data frame (df)
        # active processing county
        # active processing site
        # Pollutant Code
        # Number of decimal places for pollutant code
        # Number of hours needed for rolling average
        # Pollutant lower breakpoint dictionary
        # Pollutant uppder breakpoint dictionary
        
        #Ozone 44201
        #print("NOW PROCESSING OZONE")
        df_activePollutant = calc_aqi(df,activeCounties[i],activeSites[j],44201,3,8,ozone_breaks_lower,ozone_breaks_upper)
        dfCombined = pd.concat([dfCombined,df_activePollutant]) 
        
        #print("NOW PROCESSING PM2.5")
        #PM2.5 88101
        df_activePollutant = calc_aqi(df,activeCounties[i],activeSites[j],88101,1,24,pm25_breaks_lower,pm25_breaks_upper)
        dfCombined = pd.concat([dfCombined,df_activePollutant])  
        
        #print("NOW PROCESSING PM10")
        #PM10 81102
        df_activePollutant = calc_aqi(df,activeCounties[i],activeSites[j],81102,1,24,pm10_breaks_lower,pm10_breaks_upper)
        dfCombined = pd.concat([dfCombined,df_activePollutant])    
        
        #print("NOW PROCESSING CO")
        #CO 42101
        df_activePollutant = calc_aqi(df,activeCounties[i],activeSites[j],42101,1,8,co_breaks_lower,co_breaks_upper)
        dfCombined = pd.concat([dfCombined,df_activePollutant])  
        
        #print("NOW PROCESSING SO2")
        #SO2 42401
        df_activePollutant = calc_aqi(df,activeCounties[i],activeSites[j],42401,1,1,so2_breaks_lower,so2_breaks_upper)
        dfCombined = pd.concat([dfCombined,df_activePollutant]) 
        
        #print("NOW PROCESSING NO2")
        #NO2 42602
        df_activePollutant = calc_aqi(df,activeCounties[i],activeSites[j],42602,1,1,so2_breaks_lower,so2_breaks_upper)
        dfCombined = pd.concat([dfCombined,df_activePollutant])          
        
        j += 1
    
    
    
    #print("\n")
    i += 1
    
dfCombined.to_csv('processed.csv', sep=',') 
end = time.time()
print("Records Processed: ", dfCombined.shape[0])
print("Process Time: ", end - start)   


# In[8]:


# Create a daily summary
dfDaily = dfCombined.groupby(['County Code', 'Site Num', 'Latitude','Longitude', 'AQS Parameter Desc', 'Date Local'], sort=False)['AQI'].max().reset_index()

aqi_desc = {(0, 50): "Good", (51, 100): "Moderate", (101, 150): "Unhealthy for Sensitive Groups", (151, 200): "Unhealthy", (201, 300): "Very Unhealthy", (301, 500): "Hazardous"}
aqi_color = {(0, 50): "Green", (51, 100): "Yellow", (101, 150): "Orange", (151, 200): "Red", (201, 300): "Purple", (301, 500): "Maroon"}

for l, row in dfDaily.iterrows():
    aqi = row["AQI"]
    aqiDesc = get_range(aqi_desc, aqi)
    aqiColor = get_range(aqi_color, aqi)    
    dfDaily.set_value(l,'AQI Description',aqiDesc)   
    dfDaily.set_value(l,'AQI Color',aqiColor)  


dfDaily.to_csv('daily.csv', sep=',') 

