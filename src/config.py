# API Configuration Defaults
# API Reference https://aqs.epa.gov/aqsweb/documents/ramltohtml.html

# API Connection
apiURL = 'https://aqs.epa.gov/api/rawData?'
apiUser = ''
apiPassword = ''
outputFormat = 'DMCSV'

# Basic Query Parameters
aqsClass = 'AQI POLLUTANTS'
stateName = 'utah'
stateCode = '49'

# Pollutants Supported
aqi_pollutants = {
    "pollutant":{
        "Carbon Monoxide":"42101",
        "Sulfur dioxide":"42401",
        "Nitrogen dioxide (NO2)":"42602",
        "Ozone":"44201",
        "PM10 Total 0-10um STP":"81102",
        "PM2.5 - Local Conditions":"88101",
        "Acceptable PM2.5 AQI & Speciation Mass":"88502"
    }
}
