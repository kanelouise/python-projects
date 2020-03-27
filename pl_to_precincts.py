import os
import datetime
import pandas as pd

HOME = os.getcwd()
from datetime import date
today = date.today()

os.chdir("output")
loc = pd.read_csv("locality.txt", dtype = str).rename(columns = {'id': 'locality_id'})
pre = pd.read_csv("precinct.txt", dtype = str).rename(columns = {'id': 'precinct_id'})
prePl = pd.read_csv("precinct_polling_location.txt", dtype = str)
pl = pd.read_csv("polling_location.txt", dtype = str).rename(columns = {'id': 'polling_location_id'})

#end goal = to join locality all the way to polling location without losing data 
locPre = pd.merge(loc, pre, on = 'locality_id', how = 'left')
#print to check that locality and precinct are being joined without losing data 
#print(locPre)
locPrePl = pd.merge(locPre, prePl, on = 'precinct_id', how = 'left')
#print to check that locality, precinct and pls  are being joined without losing data (i.e. precincts without pls are still showing up)
#print(locPrePl)
locPl = pd.merge(locPrePl, pl, on = 'polling_location_id', how = 'left')
print(locPl)

os.chdir(HOME)
locPl.to_csv("precincts_to_pl_{0}.csv".format(today), index = False)

