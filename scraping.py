from selenium import webdriver
from selenium.webdriver import Safari, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
import time
import listingwindow
from bs4 import BeautifulSoup
from urllib.parse import urljoin

driver = Chrome()
driver.minimize_window()
job_titles = []
job_links = []

job_listing_button_keywords = ["View","Apply","Jobs","Internships","Openings","See","Open","Roles","Join","Our","Team","Current","Browse","Now"]
google_search_link_keywords = ["careers","be","roles","recruiting","talent","university"]
actual_job_posting_keywords = ["Senior","Junior","Engineer","Time","Full","Manager","Intern","Designer","Product","Analyst"]
not_actual_job_posting_keywords = ["jobs","how","to","internships","course","roadmap","why","tips","opportunities","experience"]

def search_links(list_of_links,keyword):

    global driver
    
    for link in list_of_links:
        
        search_link(link.get(),str(link.get() + " " + keyword),driver,keyword)
        time.sleep(2.5)

    listingwindow.generate_pages(job_titles,job_links)

def open_link(link,job_name):
    
    global drivergit 
    
    try:
        
        driver.get(link)
        
    except:
        
        return

# searching of an individual link
def search_link(company,phrase,driver,keyword):

    driver.switch_to.new_window('tab') 
    driver.get('https://bing.com/')
    time.sleep(2)
    global job_titles, job_links, is_job_site
    search_text_area = driver.find_element(By.ID,'sb_form_q')
    search_text_area.clear()
    time.sleep(2)
    search_text_area.send_keys(phrase)
    time.sleep(2)
    search_text_area.send_keys(Keys.ENTER)
    time.sleep(2)
    
    page_source = driver.page_source
    page_url = driver.current_url
    
    soup = BeautifulSoup(page_source,'html.parser')

    links_all = soup.find_all('a')
    
    links_to_be_clicked = []

    for link in links_all:

        text = link.text.strip().lower()

        if (
            keyword.lower() in text or
            company.lower() in text or
            any(k in text for k in google_search_link_keywords)
        ):
            if 'video' not in text:
                links_to_be_clicked.append(link)

    links_to_be_clicked = links_to_be_clicked[:6]

    for link in links_to_be_clicked:

        search_within_link(link)

    job_titles.append("LISTINGS FOR " + phrase.upper())
    job_links.append("Not a link")
    

def is_valid_job(job_text):

    job_text = job_text.strip()

    if(len(job_text) > 45): return False
    
    words_list = job_text.split()

    if len(words_list) < 3: 
        return False

    for word in words_list:

        if (
            any(k in word for k in actual_job_posting_keywords)
            and not any(k in word.lower() for k in not_actual_job_posting_keywords)
        ):
            return True
    
    return False

    
def search_for_jobs(button):

    print("Searching For Jobs From: " + button.text)
    global driver

    try:

        button_href = button['href']

        if button_href.startswith('/'):

            button_href = 'https://bing.com/' + button_href

        driver.get(button_href)
        time.sleep(2)

        job_search_soup = BeautifulSoup(driver.page_source,'html.parser')

        potential_jobs = job_search_soup.find_all('a')

        for job in potential_jobs:

            if is_valid_job(job.text) and job['href']:
                    
                print("Job: " + job.text)
                
                job_titles.append(job.text)
                job_links.append(job['href'])
    except Exception:

        return

def search_within_link(link):


    link_href = link.get('href')
    global driver

    if link_href:

        if link_href.startswith('/'):
            link_href = 'https://bing.com/' + link_href

        driver.get(link_href)
        print("Clicking on Link: " + link.text)
        time.sleep(2)

        new_soup = BeautifulSoup(driver.page_source,'html.parser')

        buttons = new_soup.find_all('a')
        buttons_to_be_clicked = []

        for button in buttons:

           if any(k in button.text for k in job_listing_button_keywords):
                
                buttons_to_be_clicked.append(button)

        buttons_to_be_clicked = buttons_to_be_clicked[:4]
        for button in buttons_to_be_clicked:

            search_for_jobs(button)


