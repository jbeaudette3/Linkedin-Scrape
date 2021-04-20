#!/usr/bin/env python
# coding: utf-8


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
 
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time as time
import random
import pprint
pp = pprint.PrettyPrinter(indent=4)
 
pd.set_option("display.max_rows", None)
pd.set_option('display.max_colwidth', None)
 
###################### function definitions ######################
 
def keywords(l):
  """
  Accepts list of strings to use in keywords.
  Separated by spaces

  Ex: keywords(l = ['helpdesk', 'IT'])
  """
  _ = 'keywords='
  list1 = l.split()
  if len(list1) == 1:
    return _ + list1[0]
  else:
    return _ + '%20'.join(list1)
 
 
def daysToSeconds(days = 1):
  """
  Input number of days to backdate search
  Returns number of seconds
  Integers only, please

  Ex:
  daysToSeconds(days = 5)
  daysToSeconds(5)
  """
  return 'f_TPR=r' + str(int(days) * 24 * 60 * 60)
 
 
def expLevel(level = '3'):
  """
  Accepts list of numbers as strings or single number (as string).

  Ex:
  expLevel(level = ['2', '3'])
  expLevel('6')

  1 = Internship  
  2 = Entry Level  
  3 = Associate  
  4 = Mid-Senior  
  5 = Director  
  6 = Executive  
  """
  _ = 'f_E='
  level = level.split()
  if(len(level) == 1):
    return _ + level[0]
  else:
    for i in range(len(level)):
      return _ + '%2C'.join(level)
 
 
def jobType(jobT = 'F'):
  """
  Accepts list of strings.
  F = Full-Time
  C = Contract
  P = Part-Time
  T = Temporary
  O = Other

  Ex:
  jobType(jobT = ['O', 'F'])
  jobType('O')
  """
  _ = 'f_JT='
  jobT = jobT.upper().split()
  if(len(jobT) == 1):
    return _ + jobT[0]
  else:
    for i in range(len(jobT)):
      return _ + '%2C'.join(jobT)
 
 
def salary(s = 1):
  """
  Listed as minimum, always greater than number listed
  One number only, please

  Ex: salary(4)
  - 1 = $40k  
  - 2 = $60k  
  - 3 = $80k  
  - 4 = $100k  
  - 5 = $120k  
  - 6 = $140k  
  - 7 = $160k  
  - 8 = $180k  
  - 9 = $200k  
  """
  return 'f_SB2=' + str(s)


def scrape(lP, aP):
  """
  Takes length of allPosts, and allPosts.
  Uses Requests, Beautiful Soup to scrape from Linkedin
  Appends data to arrays
  """
  for i in range(lP):
  # company name
    companyList.append(aP.find_all('div', {'class':'result-card__contents job-result-card__contents'})[i].find('a',{'class':'result-card__subtitle-link job-result-card__subtitle-link'}).string)
  # job website
    jobWebsiteList.append(aP.find_all('a', {'class':'result-card__full-card-link'})[i]['href'])       # get website
    jobWebsiteListC.append(jobWebsiteList[i][:jobWebsiteList[i].find('?')])                                 # clean website
  # title
    titleList.append(aP.find_all('a', {'class':'result-card__full-card-link'})[i].find('span', {'class':'screen-reader-text'}).string)
  # company website
    companyWebsiteList.append(aP.find_all('div', {'class':'result-card__contents job-result-card__contents'})[i].find('a', {'class':'result-card__subtitle-link job-result-card__subtitle-link'})['href'])      # get website
    companyWebsiteListC.append(companyWebsiteList[i][:companyWebsiteList[i].find('?')])                                                                                                                               # clean website
  # location
    locationList.append(aP.find_all('div', {'class':'result-card__contents job-result-card__contents'})[i].find('span',{'class':'job-result-card__location'}).string)
  # snippet
    descriptionList.append(aP.find_all('div', {'class':'result-card__contents job-result-card__contents'})[i].find('p',{'class':'job-result-card__snippet'}).string)
  # post date
    try:
      dateList.append(aP.find_all('time',{'class':'job-result-card__listdate'})[i]['datetime'])
    except:
      dateList.append(None)


url = 'https://www.linkedin.com/jobs/search/?'
 
companyList = []
titleList = []
locationList = []
dateList = []
descriptionList = []
companyWebsiteList = []
companyWebsiteListC = []
jobWebsiteList = []
jobWebsiteListC = []


################## PROMPTS ##################

print();print();
print('Please enter your keywords, separated with spaces. 5 max:')
listA = input()

print() 
print('How many pages to search? 20 max:')
p = int(input())
 
print()
print('How many days to backdate search? 180 max:')
d = input()
 
print()
print('Experience Level? Please separate values with spaces.')
print('1 = Internship')
print('2 = Entry Level')
print('3 = Associate')
print('4 = Mid-Senior')
print('5 = Director')
print('6 = Executive')
level = input()

print() 
print('Job Type? Please separate values with spaces:')
print('F = Full-Time')
print('C = Contract')
print('P = Part-Time')
print('T = Temporary')
print('O = Other')
jT = input()
 
print()
print('Minimum Salary?')
print('1 = $40k')
print('2 = $60k')
print('3 = $80k')
print('4 = $100k')
print('5 = $120k')
print('6 = $140k')
print('7 = $160k')
print('8 = $180k')
print('9 = $200k')
s = input()
 
# sort
# sort by most recent - DD
# sort by most relevent - R
so = '&sortBy=R'
 
l = 'location=Chicago%2C%20Illinois%2C%20United%20States'
 
url2 = (url
        + keywords(listA)
        + '&'
        + daysToSeconds(d)
        + '&'
        + expLevel(level)
        + '&'
        + jobType(jT)
        + '&'
        + salary(s)
        + '&'
        + l
        + '&'
        + so
)

# DEBUGGING #
# print()
# print(keywords(listA))
# print(daysToSeconds(d))
# print(jobType(jT))
# print(salary(s))
# print()
# print(url2)
 
######################################################################
######################################################################
##########  END FUNCTION DEFINITION, BEGIN ACTUAL SCRAPING  ##########
 
print('---------------------')
print(' Parameters Accepted ')
for j in range(p):
  print(f'Downloading page {(j+1):.0f} of {p:.0f}')
  o = 25 * j
  url3 = url2 + '&start=' + str(o)
 
  response = requests.get(url3)
  soup = BeautifulSoup(response.text, 'lxml')
 
  allPosts = soup.find_all('ul', {'class':'jobs-search__results-list'})[0]
  lenPosts = len(allPosts.find_all('a', {'class':'result-card__full-card-link'}))
 
  if (lenPosts > 0):
    scrape(lenPosts, allPosts)
 
  if (p > 1 and j != p-1):
    time.sleep(random.uniform(15, 20))           # Remember kids, don't spam.
 
# Now that everything is scraped into arrays:
 
data = {'company': companyList,
        'title': titleList,
        'location': locationList,
        'date': dateList,
        'description': descriptionList,
        'companyWebsiteC': companyWebsiteListC,
        'jobWebsiteC': jobWebsiteListC}
 
df = pd.DataFrame(data)
 
print('---------------------')
print('Keywords Searched:');print();
print(listA)
print()
print(f'Results found: {len(df)}')
print()
print('---------------------')
print()
 
print('Most Common Job Titles')
print(df.groupby(['title']).size().sort_values(ascending=False).head(15))
print()
print('Most Common Locations')
print(df.groupby(['location']).size().sort_values(ascending=False).head(15))
print()
print('Companies Posting the Most')
print(df.groupby(['company']).size().sort_values(ascending=False).head(20))
print()
print('Companies Posting the Least')
print(df.groupby(['company']).size().sort_values(ascending=True).head(20))
print()
print('-------------------- Chicago or IL --------------------')
try: df.loc[df['location'].str.contains('Chicago') | df['location'].str.contains('IL')].head(20)
except: pass
print()
print('Companies located in Chicago:')
try: print(df.loc[df['location'] == 'Chicago, IL']['company'].unique())
except: pass
print()
print('-------------------- Chicago, IL --------------------')
try: df.loc[df['location'] == 'Chicago, IL']
except: pass
print('-------------------- Remote --------------------')
try: df.loc[df['title'].str.contains('Remote')].head(20)
except: pass
 
########## AT THE END, PRINT FINAL DATAFRAME AND SAVE RESULTS ##########
df

cwd = os.getcwd()
df.to_csv((cwd + '/job_list.csv'), index = False)

