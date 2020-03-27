import pandas as pd
import lxml
from datetime import date

today = date.today()

#create dataframe of polling locations from LA County website
la = pd.read_html("https://locator.lavote.net/locations-list/vc?id=4085")[0]

#output dataframe to CSV and save it with today's date so we have a record of when/how polling locations changed
la = la.to_csv("la_county_pls_{0}.csv".format(today))
