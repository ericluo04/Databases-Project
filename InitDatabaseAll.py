# Lan Luo, CPSC 437, Database Project
# This file constructs a database from raw HTML files from the Yale Facebook
# that compiles basic information on Yale students such as name, grade, class,
# and home address into a relation.

# import HTML parser/processor
from bs4 import BeautifulSoup
# import to use for regex
import re
# import to use pandas as data frame tables
import pandas as pd


allfin = []

for collegelist in ["Benjamin Franklin", "Berkeley", "Branford", "Davenport", "Ezra Stiles", "Grace Hopper", "Jonathan Edwards", "Morse", "Pauli Murray", "Pierson", "Saybrook", "Silliman", "Timothy Dwight", "Trumbull"]:
    collegeraw = None
    college = None
    collegeraw = open(collegelist + ".html").read()
    college = BeautifulSoup(collegeraw, 'html.parser')
    
    classes = None
    classes = [student for student in college.find_all("div", class_="student_container")]

    students = []
    for x in classes:
        students.append(str(x))
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

    out = []
    for i in range(len(students)):
        out.append(students[i].split("<br/>"))
    
    fin = []
    fin = [i for i in out if len(i) == 7]
    copy_fin = []
    copy_fin = fin[:] 

    for i in range(len(copy_fin)):
        yearsearch = re.search('(\d{2})<div class="year_border">', copy_fin[i][0])
        if yearsearch:
            Year = "20" + yearsearch.group(1)

        emailsearch = re.search('href="mailto:([a-z]*.[a-z]*@yale.edu)', copy_fin[i][0])
        if emailsearch:
            Email = emailsearch.group(1)

        lastsearch = re.search('<h5 class="yalehead">([A-Z][a-z]*)', copy_fin[i][0])
        if lastsearch:
            LastName = lastsearch.group(1)

        firstsearch = re.search('<h5 class="yalehead">[A-Z][a-z]*, ([A-Z][a-z]*)', copy_fin[i][0])
        if firstsearch:
            FirstName = firstsearch.group(1)

        del copy_fin[i][0]
        copy_fin[i].insert(0, collegelist)
        copy_fin[i].insert(0, Year)
        copy_fin[i].insert(0, Email)
        copy_fin[i].insert(0, LastName)
        copy_fin[i].insert(0, FirstName)
        # remove college tag at beginning of room sequence
        tagindex = (copy_fin[i][5]).find('-')
        copy_fin[i][5] = copy_fin[i][5][tagindex + 1:]

    matchroomfin = []
    for i in range(len(copy_fin)):
        if len(copy_fin[i][5]) <= 6:
            if re.search('[A-Z][0-9]{2}[A-Z]?', copy_fin[i][5]):
                matchroomfin.append(copy_fin[i])
            if re.search('\d{3}[A-Z]?', copy_fin[i][5]):
                matchroomfin.append(copy_fin[i])

    allfin.extend(matchroomfin)

DFfin = pd.DataFrame(allfin)
DFfin.columns = ['First Name', 'Last Name', 'Email','Class Year', 'College','Room','Street','City_State_ZIP', 'Country','Major','Birthday']

DFfin.to_csv('studentdata.csv')

