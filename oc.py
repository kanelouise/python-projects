import pandas as pd

#create dataframe of polling locations from Orange County website
oc = pd.read_html('https://ocvote.com/fileadmin/vc/vclist.html')[1]

#test to make sure the correct table was selected
#print(oc)

#output dataframe to csv
oc.to_csv("oc_pls_from_county_site_2020-02-28.csv", index=False)
