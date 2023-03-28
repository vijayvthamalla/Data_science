# Import necessary modules

import requests                     # to process http requests
import re                           # using regular expressions for working with text
import pandas as pd                 # to work with dataframes
from bs4 import BeautifulSoup       # to work with http pages and extract relevant information

page = requests.get("https://www.nps.gov/index.htm")  # get the main index page using requests module
soup = BeautifulSoup(page.content, 'html.parser')     # create the Beautifulsoup object and parse the html page

text_loc = soup.find("a", text="FIND A PARK")         # to find the links we need a nearby string and find it in soup object
# print(text_loc.parent.parent.prettify())

event_pages = text_loc.parent.find_next_siblings("div")  # links were stored in li tag under div tag so finding div using next siblings as it is sibling to div tag
list_items = event_pages[0].findAll('li')           # now as we were just li tags, we can extract all li tags using findAll

links = [item.findChild('a')['href'] for item in list_items] # using list comprehension to store all state links that are stored in href of 'a' tag under li tag
# following is the for loop to understand the above list comprehension
# for item in list_items[0]:
#     link = item.findChild('a')
#     links.append(link['href'])

head_link = "https://www.nps.gov"  # creating the head link to concatenate with state links

state_links = [head_link+link for link in links] # list comprehension to concatenate head link with state links and form a full link,
# we can skip this and perform the concatenation in the below for loop directly so we can save some time and space complexity
# following is the for loop to perform the above list comprehension
# for link in links:
#     state_links.append(head_link+link)

all_records = []  # creating an empty list to store all records of parks and create a pandas dataframe from it

# now for all the state links we have to extract park links and extract the required parameters from park page
for state_link in state_links:
    page1 = requests.get(state_link) # going to each state page and extracting html page of it
    soup1 = BeautifulSoup(page1.content, 'html.parser') # creating a beautifulsoup object for the state page and parse html content of it
    # print(soup1.prettify) # we can print soup object by uncommenting this line

    parks = soup1.findAll("h3") # finding all h3 tags as all parks links and names were stored in h3 tags
    park_links = [re.search('/\w+/',str(park.findChild('a'))).group(0) for park in parks if 'href' in str(park.findChild('a'))] # list comprehension to
    # store the park links from 'a' tags under h3 and below is the for loop to understand above list comprehension
    # for park in parks:
    #     park_link = park.findChild('a')
    #     if 'href' in str(park_link):
    #         park_links.append(re.search('/\w+/',str(park_link)).group(0))
    
    park_full_links = [head_link+park_link+"index.htm" for park_link in park_links] # list comprehension to store full links for each park,
    # we can avoid this list comprehension and do the concatenation in requests below
    
    for park in park_full_links:
        page2 = requests.get(park) # going to each park page and getting html content from it
        soup2 = BeautifulSoup(page2.content, 'html.parser') # creating a beautifulsoup object of each park object and parse html contents of it
        # print(soup2.prettify) # we can print soup object by uncommenting this line

        text_loc = soup2.find("h4", text="Mailing Address:") # we are finding 'h4' tags for extracting Mailing address info
        # print(text_loc.parent.parent.prettify())

        park_details = soup2.find_all(class_=["Hero-designation","tel"]) # category is stored in "Hero-designation" class and phone number in "tel" class
        # getting the park name using either "Hero-title  -long" or "Hero-title" tag from park's page
        if soup2.find(class_="Hero-title -long") is None:
            name = soup2.find(class_="Hero-title ").contents[0]
        else:
            name = soup2.find(class_="Hero-title -long").contents[0]

        try:
            category = park_details[0].contents[0]
        except:
            pass
        # getting the description from park's page as it is the first paragraph in each page
        description = soup2.p.contents[0]
        # street address can be extracted by using either "street-address" class or "adr" class
        try:
            if soup2.find(class_="street-address") is None:
                street_details = soup2.find(class_='adr')
                line_1 = (street_details.contents[0]+str(street_details.contents[1].contents[0])).strip('\n')
                line_2,line_3 = None,None
            else:
                street_details = soup2.find(class_='street-address')
                line_1 = street_details.contents[0].strip('\n')
                try:
                    line_2 = street_details.contents[2].strip('\n')
                except:
                    line_2 = None
                try:
                    line_3 = street_details.contents[4].strip('\n')
                except:
                    line_3 = None
        except:
            line_1 = None
            line_2 = None
            line_3 = None
        # city name is stored in "addressLocality" itemprop and can be extracted using soup.find
        try:
            city = soup2.find(itemprop="addressLocality").contents[0]
        except:
            city = None
        # state name is stored in "addressRegion" itemprop and can be extracted using soup.find
        try:
            state = soup2.find(itemprop="addressRegion").contents[0]
        except:
            state = soup2.find(class_="Hero-location").contents[0]
        # zip_code can be extracted from "postalCode" itemprop and extra spaces are stripped off using strip()
        try:
            zip_code = soup2.find(itemprop="postalCode").contents[0].strip()
        except:
            zip_code = None
        # phone number is extracted from "tel" class and stripped of new line chars using strip('\n')
        try:
            phone = park_details[1].contents[0].strip('\n')
        except:
            phone = None
        # print([name,category,description,line_1,line_2,line_3,city,state,zip_code,phone])
        all_records.append([name,category,description,line_1,line_2,line_3,city,state,zip_code,phone]) # adding all parameters to the list in order

column_names = ['Name', 'Category', 'Description', 'Street Address Line 1', 'Line 2', 'Line 3', 'City',
                'State', 'Zip Code', 'Phone Number']
# creating the pandas dataframe from all_records list and column_names list
df = pd.DataFrame(all_records, columns=column_names)
# few park trails are existing in multiple states so we can remove the duplicate park information using drop_duplicates()
df = df.drop_duplicates()
# we need to reset index as we dropped duplicates
df = df.reset_index(drop=True)
# print(df)
# pd.set_option('display.max_columns', None)
# print(df)
# we can save pandas dataframe into csv file using to_csv() and removing indexes using index as False
df.to_csv("data.csv",index=False)