# Retreive configuration parameters
import configparser

config = configparser.ConfigParser()
config.sections()

config.read('config.ini')

apiURL = config['DEFAULT']['apiURL']
apiUser = config['DEFAULT']['apiUser']
apiPassword = config['DEFAULT']['apiPassword']
outputFormat = config['DEFAULT']['outputFormat']

# Set -or override config defaults- required API parameters
aqsClass = 'AQI POLLUTANTS'
bDate = '20170101'
eDate = '20170131'
stateCode = '49'
countyCode = '035'

# Make an API request
import requests

requestURL = apiURL + 'user=' + apiUser + '&pw=' + apiPassword + '&format=' + outputFormat + '&pc=' + aqsClass + '&bdate=' + bDate + '&edate=' + eDate + '&state=' + stateCode + '&county=' + countyCode
apiResp = requests.get(requestURL)


# Convert raw request into a Pandas data frame
import pandas as pd
import io

aqs_df = pd.read_csv(io.StringIO(apiResp.content.decode('utf-8')))
aqs_df.head(n=20)

