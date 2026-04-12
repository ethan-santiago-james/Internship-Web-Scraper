# from selenium import webdriver
# from selenium.webdriver import Safari, Chrome
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# import re
# import random
# import time
# import listingwindow
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin

# driver = Chrome()

# job_titles = []
# job_links = []
# visited_links = set()

# job_listing_button_keywords = ["View","Apply","Jobs","Internships","Openings","See","Open","Roles","Join","Our","Team","Current","Browse","Now"]
# google_search_link_keywords = ["careers","be","roles","recruiting","talent","university"]
# actual_job_posting_keywords = ["Senior","Junior","Engineer","Time","Full","Manager","Intern","Designer","Product","Analyst"]
# not_actual_job_posting_keywords = ["jobs","how","to","internships","course","roadmap","why","tips","opportunities","experience"]

# def search_links(list_of_links,keyword):

#     global driver
    
#     for link in list_of_links:
        
#         search_link(link.get(),str(link.get() + " " + keyword),driver,keyword)
#         time.sleep(random.uniform(2,8))

#     listingwindow.generate_pages(job_titles,job_links)

# def open_link(link,job_name):
    
#     global driver
    
#     try:
        
#         driver.get(link)
        
#     except:
        
#         return

# # searching of an individual link
# def search_link(company,phrase,driver,keyword):

#     driver.get('https://bing.com/')
#     time.sleep(random.uniform(0.5,1.3))
#     global job_titles, job_links, is_job_site
#     search_text_area = driver.find_element(By.ID,'sb_form_q')
#     search_text_area.clear()
#     time.sleep(random.uniform(0.5,1.3))
#     for char in phrase:
#         search_text_area.send_keys(char)
#         time.sleep(random.uniform(0.05, 0.2))

#     search_text_area.send_keys(Keys.ENTER)
#     time.sleep(random.uniform(1,4))
    
#     page_source = driver.page_source
#     page_url = driver.current_url
    
#     soup = BeautifulSoup(page_source,'html.parser')

#     job_titles.append("LISTINGS FOR " + phrase.upper())
#     job_links.append("Not a link")

#     links_all = soup.find_all('a')
    
#     links_to_be_clicked = []

#     for link in links_all:

#         text = link.text.strip().lower()

#         if (
#             keyword.lower() in text or
#             company.lower() in text or
#             any(k in text for k in google_search_link_keywords)
#         ):
#             if 'video' not in text:
#                 links_to_be_clicked.append(link)

#     links_to_be_clicked = links_to_be_clicked[:6]

#     for link in links_to_be_clicked:

#         search_within_link(link)
#         driver.get(page_url)
#         search_for_jobs(link)

   
    

# def is_valid_job(job_text):

#     job_text = job_text.strip()

#     if(len(job_text) > 45): return False
    
#     words_list = job_text.split()

#     if len(words_list) < 3: 
#         return False

#     for word in words_list:

#         if (
#             any(k in word for k in actual_job_posting_keywords)
#             and not any(k in word.lower() for k in not_actual_job_posting_keywords)
#         ):
#             return True
    
#     return False

    
# def search_for_jobs(button):

#     print("Searching For Jobs From: " + button.text)
#     global driver

#     try:

#         button_href = button['href']

#         if button_href.startswith('/'):

#             button_href = 'https://bing.com/' + button_href

#         if button_href in visited_links:

#             return

#         driver.get(button_href)
#         visited_links.add(button_href)
#         time.sleep(random.uniform(1,4))

#         job_search_soup = BeautifulSoup(driver.page_source,'html.parser')

#         potential_jobs = job_search_soup.find_all('a')

#         for job in potential_jobs:

#             if is_valid_job(job.text) and job['href']:
                    
#                 print("Job: " + job.text)
                
#                 job_titles.append(job.text)
#                 job_links.append(job['href'])
#     except Exception:

#         return

# def search_within_link(link):


#     link_href = link.get('href')
#     global driver

#     if link_href:

#         if link_href.startswith('/'):
#             link_href = 'https://bing.com/' + link_href

#         if link_href in visited_links:
#             return
#         driver.get(link_href)
#         visited_links.add(link_href)
#         print("Clicking on Link: " + link.text)
#         time.sleep(2)

#         new_soup = BeautifulSoup(driver.page_source,'html.parser')

#         buttons = new_soup.find_all('a')
#         buttons_to_be_clicked = []

#         for button in buttons:

#            if any(k in button.text for k in job_listing_button_keywords):
                
#                 buttons_to_be_clicked.append(button)

#         buttons_to_be_clicked = buttons_to_be_clicked[:4]
#         for button in buttons_to_be_clicked:

#             search_for_jobs(button)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import random
import listingwindow

from urllib.parse import urlparse, urlunparse

def normalize_url(url):
    parsed = urlparse(url)

    # remove query + fragment
    clean = parsed._replace(query="", fragment="")

    # remove trailing slash
    return urlunparse(clean).rstrip("/")

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

visited = set()
job_titles = []
job_links = []

CAREER_PATHS = [
    "/careers",
    "/jobs",
    "/join-us",
    "/work-with-us",
    "/careers/jobs"
]

KEYWORDS = ["engineer", "developer", "manager", "analyst", "designer", "intern"]
JOB_BUTTON_KEYWORDS = [
    "view", "open", "positions", "jobs", "roles",
    "opportunities", "join", "team", "see", "all"
]


def human_delay():
    time.sleep(random.uniform(3, 7))


def get_base_url(company):
    company = company.lower().replace(" ", "")
    return f"https://{company}.com"


def search_links(list_of_links):

     global driver
    
     for link in list_of_links:
        
         job_titles.append("Listings For " + str(link.get()))
         job_links.append("Not a link")
         scrape_company(link.get())
         time.sleep(random.uniform(2,8))
         

     listingwindow.generate_pages(job_titles,job_links)

def find_careers_page(base_url):
    for path in CAREER_PATHS:
        url = base_url + path
        try:
            driver.get(url)
            human_delay()

            if "career" in driver.title.lower() or "job" in driver.page_source.lower():
                return url
        except:
            continue

    return None

def find_job_pages(url):
    new_pages = []

    driver.get(url)
    human_delay()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = soup.find_all("a")

    for link in links:
        text = link.text.strip().lower()

        if any(k in text for k in JOB_BUTTON_KEYWORDS):
            href = link.get("href")

            if href:
                if href.startswith("/"):
                    href = url.rstrip("/") + href

                if href not in visited:
                    print(f"Adding job button to list: {text} -> {href}")
                    new_pages.append(href)

    return new_pages

def extract_jobs_from_soup(soup, base_url):
    links = soup.find_all("a")

    for link in links:
        text = link.text.strip().lower()

        if any(k in text for k in KEYWORDS) and len(text) < 60:
            href = link.get("href")

            if href:
                if href.startswith("/"):
                    href = base_url.rstrip("/") + href

                if href not in job_links and text not in job_titles:
                    job_titles.append(text)
                    job_links.append(href)

                    print(f"Job found: {text}")

def crawl_for_jobs(start_url, depth=2):
    queue = [(start_url, 0)]

    while queue:
        current_url, level = queue.pop(0)

        if current_url in visited or level > depth:
            continue

        normalized = normalize_url(current_url)

        if normalized in visited:
            return

        visited.add(normalized)

        print(f"Visiting: {current_url}")

        driver.get(current_url)
        human_delay()

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract jobs on this page
        extract_jobs_from_soup(soup, current_url)

        # Find deeper job-related pages
        next_pages = find_job_pages(current_url)

        for page in next_pages:
            queue.append((page, level + 1))


def scrape_company(company):
    print(f"\n--- {company} ---")

    base = get_base_url(company)
    careers_page = find_careers_page(base)

    if not careers_page:
        print("No careers page found")
        return

    print(f"Careers page: {careers_page}")

    crawl_for_jobs(careers_page)



