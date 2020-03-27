
#after .format(State,  number of No location addresses, number total addresses)
text = "For {0}, {1} out of {2} addresses didn't return a polling location.".format("WV","31","299")

#if state had no incorrect addresses
correct = "\n There were no incorrect addresses,"

#pl names if the state expected different pl names than what was returned
#pl_names = "however, we had different pl names. For example, the state expected a polling location name to be: WHETSTONE TWP SOUTH and the API returned the pl name as: COLONEL CRAWFORD HIGH SCHOOL."

#if necesary for states that had incorrect addresses
#seventy = "\n {0} was expected to return: {1} but returned: {2}.\n {3} was expected to return: {4} but returned: {5}.\n Seven addresses were expected to return: {6} but returned: {7}.".format("3196 HATCH PARKWAY NORTH BAXLEY GA 31513", "no address", "3397 HATCH PARKWAY NORTH BAXLEY GA 31513", "1004 UPPER TY TY ROAD TY TY GA 31795", "163 INMAN ST  TY TY GA 31795","141 EAST ELMAN STREET TY TY GA 31795", "4417 WILLIAMSON ZEBULON RD  WILLIAMSON GA 30292", "65 PATTON STREET WILLIAMSON GA 30292")
one = "\nOne address was expected to return: {0} but returned: {1}.".format("The address entered was not found in our data","541 ORCHARD DR TWIN FALLS ID 83301")
two = "\nOne address was expected to return: {0} but returned: {1}.".format("ST. CHARLES/CITY HALL 75 N MAIN ST ST. CHARLES ID 83272","5PARIS/REAR TABERNACLE ANNEX 40 S FIELDING, PARIS ID 83261")
#ninety = "\n A spot-check of addresses with >=90% match revealed no issues." 

print(text, correct)