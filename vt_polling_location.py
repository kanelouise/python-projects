
import pandas as pd

#This creates a file for checking the polling location accuracy
#we need locality to get the name of each county
l = pd.read_csv("vt_all/locality.txt")
l = l[['name', 'id']]
l = l.rename(columns={"id" : "2018_locality_id"})
#print(l)


#Precinct has the precinct_id, which we need to link. Also locality_id on this so
#we can link the locality name for each precinct, then link on locality_id
pre = pd.read_csv("vt_all/precinct.txt")
pre = pre[['name', 'locality_id', 'id', 'polling_location_ids']]
pre = pre.rename(columns={"name" : "2018_precinct_name", "id" : "2018_precinct_id", "locality_id" : "2018_locality_id", "polling_location_ids" : '2018_polling_location_id'})
lpre = l.merge(pre, on='2018_locality_id')
#print(lpre)


#finally, we read in polling_location so that we have all the above data for each pl
pl = pd.read_csv("vt_all/polling_location.txt")
#print(pl.columns)

pl = pl[['id', 'name', 'address_line']]
pl = pl.rename(columns={"id" : "2018_polling_location_id", 
	"name" : "2018_name",
	"address_line" : "2018_address_line",
	})

lprepl = lpre.merge(pl, on="2018_polling_location_id")
print(lprepl)
lprepl.to_csv("vt_polling_locations_2018.csv", index=False)

print('vt_polling_locations_2018.csv created')
#we can end here and have a file of just the 2018 polling locations and 
#can manually add the 2020 information sent from VT (which might be better since Burnlington is separated anyway)



#hypothetical code to add VT's 2020 data instead of only the 2018 data from VIP
#vtpl = pd.read_xls("../vt_all/polling_location.txt")
#vtpl = vtpl[['Town or City', '2020 Town Meeting Polling Place', 'Address of Town Meeting Polling Place']]
#vtpl = vtpl.rename(columns={"Town or City" : "name",
#"Address of Town Meeting Polling Place" : "2020_address"})
#lpreplvtpl = lprepl.merge(vtpl, on= "name")
#stuck here, would like some help with the regex and writing file
# here's my attempt
#vtpl = pd.read_excel()