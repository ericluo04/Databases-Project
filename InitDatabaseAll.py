# Lan Luo, CPSC 437, Database Project
# This file constructs a database from downloaded raw HTML files from the Yale Facebook for each college
# that compiles basic information on each Yale students (first name, last name, class year, college, address,
# country, major, and birthday) into a single relation.

# import HTML parser/processor
from bs4 import BeautifulSoup
# import to use for regex
import re
# import to use pandas as data frame tables
import pandas as pd
# import to use when shuffling/permuting each column in the pandas data frame
import numpy as np
# import to use when converting address to latitude, longitude coordinates
from geopy.geocoders import Nominatim
# import to wait when chunking to avoid time out
import time

# initialize final scraped data list variable
allfin = []

# loop through every college raw html file to get student information
for collegelist in ["Benjamin Franklin", "Berkeley", "Branford", "Davenport", "Ezra Stiles", "Grace Hopper", "Jonathan Edwards", "Morse", "Pauli Murray", "Pierson", "Saybrook", "Silliman", "Timothy Dwight", "Trumbull"]:
    # initialize variables
    collegeraw = None
    college = None
    # collegeraw for reading html file and then college as parsed cleanly
    collegeraw = open(collegelist + ".html").read()
    college = BeautifulSoup(collegeraw, 'html.parser')
    
    # split up each student into their own class
    classes = None
    classes = [student for student in college.find_all("div", class_="student_container")]
    
    # make each student into one string variable
    students = []
    for x in classes:
        students.append(str(x))
    # clean data by making it easier to split/extract information
    for i in range(len(students)):
        # remove extra html tags that won't be used to split the data
        students[i] = students[i].replace("</div>","")
        # replace html ampersand to &
        students[i] = students[i].replace("&amp;","&")
        # remove phone numbers (extraneous info - location information can be drawn from the home address)
        students[i] = re.sub('<br/>(\d{3} ?-)?\d{3}-\d{4} / ', "", students[i])
        # remove strange sequences of numbers (e.g. ending in YS), not address information so extraneous
        students[i] = re.sub('<br/>#? ?\d* YS', "", students[i])
        students[i] = re.sub('<br/>\d-\d{4} /', "", students[i])
        students[i] = re.sub('<br/>\d+ /', "", students[i])
        # if there's an american zip code, then add United States as a country to be consistent with students who have information for their foreign home country
        USzip = re.search('([A-Z]{2} \d{5}-?(\d{4})?)', students[i])
        if USzip:
            students[i] = students[i].replace(USzip.group(1), USzip.group(1) + "<br/>United States")    
    # split by line break to make creating a relation easier
    out = []
    for i in range(len(students)):
        out.append(students[i].split("<br/>"))
    
    # only include students with complete information 
    fin = []
    fin = [i for i in out if len(i) == 7]
    # duplicate variable to avoid python memory issue
    copy_fin = []
    copy_fin = fin[:] 
    
    # loop through each student
    for i in range(len(copy_fin)):
        # intialize column information
        yearsearch, emailsearch, lastsearch, firstsearch = None, None, None, None
        
        # extract year by matching with regex
        yearsearch = re.search('(\d{2})<div class="year_border">', copy_fin[i][0])
        if yearsearch:
            Year = "20" + yearsearch.group(1)
            
        # extract email by matching with regex
        emailsearch = re.search('href="mailto:(.*)">', copy_fin[i][0])
        if emailsearch:
            Email = emailsearch.group(1)
        
        # extract last name by matching with regex
        lastsearch = re.search('<h5 class="yalehead">(.*),', copy_fin[i][0])
        if lastsearch:
            LastName = lastsearch.group(1)

        # extract first name by matching with regex
        firstsearch = re.search('<h5 class="yalehead">.*, (.*) </h5>', copy_fin[i][0])
        if firstsearch:
            FirstName = firstsearch.group(1)
        
        # delete first value in list (long string with all the information extracted above)
        del copy_fin[i][0]
        # insert values for the information extracted above
        copy_fin[i].insert(0, collegelist)
        copy_fin[i].insert(0, Year)
        copy_fin[i].insert(0, Email)
        copy_fin[i].insert(0, LastName)
        copy_fin[i].insert(0, FirstName)
        # remove college tag at beginning of room sequence
        tagindex = (copy_fin[i][5]).find('-')
        copy_fin[i][5] = copy_fin[i][5][tagindex + 1:]
    
    # create variable to match room number appropriately (throws out rows with non-sensical rows)
    matchroomfin = []
    for i in range(len(copy_fin)):
        # if statement removes rows with an address for the room number value
        if len(copy_fin[i][5]) <= 6:
            # use regexes to match for appropriate room number types
            if re.search('[A-Z][0-9]{2}[A-Z]?', copy_fin[i][5]):
                matchroomfin.append(copy_fin[i])
            if re.search('\d{3}[A-Z]?', copy_fin[i][5]):
                matchroomfin.append(copy_fin[i])
    
    # create final scraped data list
    allfin.extend(matchroomfin)

# generate pandas data frame in line with ordering of scraped data list
DFfin = pd.DataFrame(allfin)
DFfin.columns = ['First Name', 'Last Name', 'Email', 'Class Year', 'College', 'Room', 'Street', 'City_State_ZIP', 'Country', 'Major', 'Birthday']

# drop last name to better anonymizedata
DFfin.drop(columns=['Last Name'])
# create new last name that's simply a duplicate of the first name
# this is great for anonymity since first names are hardly useful for uniquely identifying a person
DFfin['Last Name'] = DFfin['First Name']

# combine all address information into a single field
DFfin['Address'] = DFfin['Street'] + ", " + DFfin['City_State_ZIP'] + ", " + DFfin['Country']
# drop unnecessary columns
DFfin.drop(columns=['Street', 'City_State_ZIP', 'Email'])

# reorder data frame appropriately
DFfin = DFfin[['First Name', 'Last Name', 'Class Year', 'College', 'Address', 'Country', 'Major', 'Birthday', 'Room']]

DFfinv1 = DFfin.copy()
DFfinv2 = DFfin.copy()
# table with non-address info
DFfinv1 = DFfinv1.drop(columns=['Address', 'Country'])
# table with address info
DFfinv2 = DFfinv2.drop(columns=['First Name', 'Last Name', 'Class Year', 'College', 'Major', 'Birthday', 'Room'])
# permute/shuffle/randomize each column independently from the others
# perfectly anonymizes the data so that no single row gives any useful identifying information
DFfinv1 = DFfinv1.apply(np.random.permutation)
# this permutation does address information separately (since these need to be done together to preserve the location information)
DFfinv2 = DFfinv2.reindex(np.random.permutation(DFfinv2.index))

DFlast = DFfinv1.join(DFfinv2, how = "left")
DFlast = DFlast[['First Name', 'Last Name', 'Class Year', 'College', 'Major', 'Birthday', 'Room', 'Address', 'Country']]

# test for anonymity, indeed none of the information below matches my personal information
DFlast.loc[DFlast['First Name'] == 'Lan']

# # add field for address coordinates using geopy package
# geolocator = Nominatim(user_agent="school project")

# # manually create chunks to create coordinates, geocoder times out if the request is too long
# # create chunks without address
# DFchunks = []
# for i in range(176):
#     DFchunks.append( DFlast[i*25: (i+1)*25].copy() )
# # addresses added into chunks
# for i in range(len(DFchunks)):
#     print i
#     DFchunks[i]['LatLong'] = DFchunks[i]['Address'].apply(geolocator.geocode)
#     DFchunks[i]['LatLong'] = DFchunks[i]['LatLong'].apply(lambda x: (x.latitude, x.longitude) if x != None else None)
#     time.sleep(60)

# # append all the chunks together into one large relation
# DFfinish = DFchunks[0]
# for i in range(1, len(DFchunks)):
#     DFfinish.append(DFchunks[i])

DFlast.to_csv("studentdata.csv")