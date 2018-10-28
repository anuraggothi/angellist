import requests
import lxml
from lxml.html import fromstring
from selenium import webdriver
from itertools import cycle
import traceback
import scrapy
from bs4 import BeautifulSoup
import urllib.request
import os
from selenium.webdriver.common.keys import Keys
import time
import xlsxwriter
import csv
from datetime import datetime
def seprateEquity(s):
    lst=s.split('·')
    return(lst[0].strip(),lst[1].strip())

def seprateSchedule(r):
    lst=r.split('·')
    if(len(lst)>=2):
        if('Remote' in lst[1]):
            lst[1]='yes'
    else:
        lst.append('no')
    return(lst[0].strip(),lst[1].strip())




main_url = "https://angel.co"
login_url="https://angel.co/login?utm_source=top_nav_home"
userurl = input("please enter an valid angel.co/jobs url:")
joburl= userurl
if joburl != "https://angel.co/jobs":
    jobtype = input("enter your desired job:")
    joburl = '''https://angel.co/jobs#find/f!%7B"keywords"%3A%5B"'''+jobtype+'''"%5D%7D'''

if not userurl:
    jobtype = input("enter your desired job:")
    joburl = '''https://angel.co/jobs#find/f!%7B"keywords"%3A%5B"'''+jobtype+'''"%5D%7D'''

#parsing url with filters below

#getlocation = input("EnterLocation:")
#location = '''"%5D%2C"locations"%3A%5B"'''+getlocation
#end = '''"%5D%7D'''
#if not getlocation:
#    location=""


#worktypelist = ['for fulltime press f ','for contract press c','for internship press i'+' for cofounder press cf']
#print(worktypelist)
#getworktype = input("enter job type using above give keyword:")
#getworktype = getworktype.lower()
#workdef = '''"%5D%2C"types"%3A%5B"'''
#if getworktype=="f":
#    getworktype = "full-time"

#elif getworktype=="c":
    #getworktype="contract"
#elif getworktype=="i":
#    getworktype="internship"
#elif getworktype=="cf":
#    getworktype="cofounder"
#else:
#    print("Not a valid keyword will show jobs for all job types")
#    getworktype=""
#    workdef=""
#work = workdef+getworktype
#fullurl = joburl+location+workdef+getworktype+end
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

driver.get(login_url)
#lucky_button = driver.find_element_by_css_selector("[name=btnI]")
#lucky_button.click()

# capture the screen
#driver.get_screenshot_as_file("capture2.png")
inputElement = driver.find_element_by_id("user_email")
inputElement.send_keys('anuraggothi10@gmail.com')

inputElement1 = driver.find_element_by_id("user_password")
inputElement1.send_keys('anurag@123')
inputElement1.send_keys(Keys.ENTER)


driver.get(joburl)
driver.get_screenshot_as_file("capture3.png")
driver.execute_script("window.scrollTo(0, 10800)")
time.sleep(5)
driver.execute_script("window.scrollTo(0, 10800)")
time.sleep(5)
#compname = driver.find_element_by_class_name("startup-link")


html = driver.page_source

soup = BeautifulSoup(html, "lxml")
#compdetail = soup.find_all(class_='startup-link')
#print(compdetail)
jobsList = []

for i in soup.find_all(class_="header-info"):
    compDix = {}
    x = i.find('a', attrs={'class': 'startup-link'})
    compDix['name'] = x.text
    compDix['link'] = x['href']
    e = i.find('div',attrs = {'class':"tag active"})
    compDix['active']= e.text.strip()
    f = i.find('div',attrs = {'class':"tag applicants"})
    compDix['applicants']= f.text.strip()
    g = i.find('div',attrs = {'class':"tag locations tiptip"})
    compDix['location']= g.text.strip()
    h = i.find('div',attrs = {'class':"tag employees"})
    compDix['employees']= h.text.strip()
    compDix['jobs']= []
    for job in i.find_all(class_='collapsed-listing-row'):
        jobDix={}
        j = job.find('div',attrs = {'class':"collapsed-title"})
        jobDix['title'] = j.text.strip()
        k = job.find('div',attrs = {'class':"collapsed-compensation"})
        jobDix['salary'],jobDix['equity']=seprateEquity(k.text.strip())
        l = job.find('div',attrs = {'class':"collapsed-tags"})
        jobDix['working schedule'],jobDix['remote']=seprateSchedule(l.text.strip())
        compDix['jobs'].append(jobDix)
    jobsList.append(compDix)
print (jobsList)

csv_file = open('angel.csv','a')
writer = csv.writer(csv_file)
writer.writerow(['Name','Link','Last Active',"No of applicants","location",'employees',"job title","salary","equity","working schedule","remote"])
for details in jobsList:
    for noj in details['jobs']:
        writer.writerow([details['name'].encode("utf-8"),details['link'].encode("utf-8"),details['active'].encode("utf-8"),details['applicants'].encode("utf-8"),details['location'].encode("utf-8"),details['employees'].encode("utf-8"),noj['title'].encode("utf-8"),noj['salary'].encode("utf-8"),noj['equity'].encode("utf-8"),noj['working schedule'].encode("utf-8"),noj['remote'].encode("utf-8")])

csv_file.close()
driver.close()
