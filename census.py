"""
census.py --- Script that displays demographic information by county along with coverage information by county.
Programmer: kane klipka
Last Updated: 2/9/22
Last Updated by: kk
Notes: Before running for the first time, users must request a Census API key and save it in credentials/config.py as CENSUS_KEY
This script is currently using 2010 data from the Summary File 1 dataset. Should be updated when that dataset is available for 2020.
"""

import pandas as pd
import requests
from pandas.io.json import json_normalize
import datetime
import pygsheets
import sys
sys.path.insert(1, 'credentials')
import config

CENSUS_KEY =  config.CENSUS_KEY

client = pygsheets.authorize(service_file='credentials/coverage-demographics-76483a670ccc.json')
print("-----------------Authorized--------------------")
sheet = client.open('coverage_demographics')
print("-----------------SheetOpened--------------------")

today = datetime.date.today()
FILE = str("coverage/county_coverage.csv")

#total population
total = "P005001"
#white
white = "P005003"
#hispanic
hispanic =  "P005010"
#Black or African American alone or combined
black = "P005004"
#American Indian or Alaskan native alone or combined
amind_alnat = "P005005"
#Asian alone or combined
asian = "P005006"
#Native Hawaiian or other Pacific Islander alone or combined
nahi_pi = "P005007"
#other
other = "P005008"

#call Census API at the county level, retrieving population racial demographics information from the Race + Hispanic table listed below
CENSUS_URL = f"https://api.census.gov/data/2010/dec/sf1?get={total},{white},{hispanic},{black},{amind_alnat},{asian},{nahi_pi},{other}&for=COUNTY&key={CENSUS_KEY}"
#2010 Decennial Census information

CENSUS_URL = f"https://api.census.gov/data/2010/dec/sf1?get={total},{white},{hispanic},{black},{amind_alnat},{asian},{nahi_pi},{other}&for=COUNTY&key={CENSUS_KEY}"
#2010 Decennial Census information

def query_api():
    call = requests.get(CENSUS_URL)
    pre_data = call.json()
    return pre_data

census_data = pd.DataFrame(columns=['total','white','latinx','black','native','asian','pac_isl','other','state','county'], data=query_api())
census_data = census_data[1:]
census_data['fips'] = census_data['state'].str.cat(census_data['county'])
census_data['fips'] = census_data['fips'].astype(str)

id_map = {'white_per':'white', 'latinx_per': 'latinx', 'black_per':'black','native_per':'native','asian_per':'asian','pac_isl_per': 'pac_isl', 'other_per': 'other'}

for percent,identity in id_map.items():
    census_data[percent] = census_data[identity].astype(float)/census_data['total'].astype(float)*100

census_data = census_data[['total','white','white_per','latinx','latinx_per','black','black_per','native','native_per','asian','asian_per','pac_isl','pac_isl_per','other','other_per','fips']]

#read in census fips information and turn into DF.
#this is a cross walk between the census demographic information and VIP's coverage info
fips_url = 'https://www2.census.gov/geo/docs/reference/codes/files/national_county.txt'
cen_fips = pd.read_csv(fips_url,names=('state','state_fips','county_fips','county','NA'), dtype=str)
cen_fips['county'] = cen_fips['county'].str.upper()

#add each string that needs to be erased from cen_fips to this list
cen_fips_empty = ['COUNTY',' CITY AND BOROUGH', ' BOROUGH', 'CENSUS AREA','MUNICIPALITY', "'", "PARISH" ]
#add each string set that needs to be transformed from one thing to another here. e.g. 'ST.' should be 'ST' and is in the dictionary as 'ST.': 'ST'
cen_fips_replace= {'ST.': 'ST','STE.': 'STE', "DE ": "DE", "LA CROSSE ": "LACROSSE", "BALTIMORE": "BALTIMORE COUNTY", "BALTIMORE COUNTY CITY": "BALTIMORE CITY"}

for string in cen_fips_empty:
    cen_fips['county'] = cen_fips['county'].apply(lambda x: str(x).replace(string, ''))

for string, replace in cen_fips_replace.items():
    cen_fips['county'] = cen_fips['county'].apply(lambda x: str(x).replace(string, replace))

#general clean up of cen_fips after transformations have taken place
cen_fips['county'] = cen_fips['county'].apply(lambda x: str(x).strip())
cen_fips['fips'] = ""
cen_fips['fips'] = cen_fips['state_fips'].str.cat(cen_fips['county_fips']).astype(str)
cen_fips = cen_fips.sort_values(['state','county'], ascending=[True, True])

#if you need to debug census/fips codes that aren't matching, uncomment following line and see where they stop matching
# cen_fips.to_csv("cen_fips.csv", index = False)


#read in and clean coverage report
coverage = pd.read_csv(FILE, dtype=str)
#add each string that needs to be erased from coverage report to this list
cov_empty = ['CITY OF ',' CITY AND BOROUGH', ' BOROUGH', 'MUNICIPALITY OF']
#add each string set that needs to be transformed from one thing to another here. e.g. 'ST.' should be 'ST' and is in the dictionary as 'ST.': 'ST'
cov_replace= {"&": "AND",'SAINT': 'ST', 'JODAVIESS': 'JO DAVIESS', "DE ": "DE"}

for string in cov_empty:
    coverage['county'] = coverage['county'].apply(lambda x: str(x).replace(string, ''))

for string, replace in cov_replace.items():
    coverage['county'] = coverage['county'].apply(lambda x: str(x).replace(string, replace))
coverage = coverage.sort_values(['state','county'], ascending =[True, True])

#merge cen_fips onto coverage - can print uncomment this to debug as necesary 
cov_fips = pd.merge(coverage.loc[:,['state','county','TOTAL_count','SUCCESS_percent','TOTAL_PL_COVERAGE_percent']], cen_fips.loc[:, ['state', 'county','fips']], on = ['state', 'county'], how = 'left')
# cov_fips.to_csv(r"coverage/cov_fips_{0}.csv".format(today), index = False)

#merge demographic info onto cov_fips
cov_demo = pd.merge(cov_fips.loc[:,['state','county','TOTAL_PL_COVERAGE_percent','TOTAL_count','SUCCESS_percent','fips']], census_data.loc[:, ['total','white','white_per','latinx','latinx_per','black','black_per','native','native_per','asian','asian_per','pac_isl','pac_isl_per','other','other_per','fips']], on = 'fips', how = 'left')

#spit out report to csv
cov_demo.to_csv(r"coverage/cov_demo_{0}.csv".format(today), index = False)
print("Check folder for a new report")

#access worksheet
wks = sheet[0]
print("-----------------First Sheet Accessed----------")
#set data
wks.set_dataframe(cov_demo,(1,1))
print("-----------------Data Updated------------------")
