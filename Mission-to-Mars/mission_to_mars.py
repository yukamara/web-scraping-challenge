#!/usr/bin/env python
# coding: utf-8

# # Step 1 - Scraping

# In[1]:


# Import Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time
import pprint


# ## *1. Scraping NASA Mars News - API*

# In[2]:


# Initialize PyMongo to work with MongoDBs
#conn = 'mongodb://localhost:27017'
#client = pymongo.MongoClient(conn)

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# URL of page to be scraped
url = 'https://redplanetscience.com/'
browser.visit(url)
time.sleep(2)
html = browser.html

# Retrieve  page witht the request module
#response = requests.get(url)

# Create BeautifulSoup object, parse with 'lxml'
soup = bs(html, 'html.parser')


# In[4]:


# Retrieve the dives for all the titles and paragraphs
results = soup.find_all('div', class_='list_text')

# Loop over the results to get the article titles and paragraph texts
for result in results:
    
    # Scrape the article date
    news_date = result.find('div', class_='list_date').text
    # Scrape the article title
    news_title = result.find('div', class_='content_title').text
    
    # Scrape the article paragraph
    news_p = result.find('div', class_='article_teaser_body').text
    
    # Print all the data
    print('-------------------------------')
    print(news_date)
    print(news_title)
    print(news_p)
    
    # Dictionary to be inserted into MongoDB
    news = {
        'news_title': news_title,
        'news_p': news_p,
        'news_date': news_date,
    }


# ## *2. Scraping the Featured Image - Splinter*

# In[5]:


# URL of page to be scraped
url= 'https://spaceimages-mars.com/'
browser.visit(url)


# In[6]:


# html Object
html = browser.html

# Parse with beautiful soup
soup = bs(html, 'html.parser')

# retrieve image url
image_url = soup.find_all('img')[1]['src']
featured_image_url = url + image_url

# Print image url
print(f'featured_image_url = {featured_image_url}')


# ## *3. Scraping Mars Facts - Pandas*

# In[7]:


# Mars Facts web page url 
url = 'https://galaxyfacts-mars.com/'


# In[8]:


# List all table on page
tables = pd.read_html(url)
tables


# In[9]:


# Slice off table of interest
df = tables[0]
df


# In[10]:


#make the first row the table header

#grab the first row for the header
new_header = df.iloc[0]

#take the data less the header row
df = df[0:] 

#set the header row as the df header
df.columns = new_header

df


# In[11]:


# Drop the row with index = 0
df = df.iloc[1:]
df


# In[12]:


# Rename first column and set it as the index
df = df.rename(columns={"Mars - Earth Comparison": "Description"})
df = df.set_index('Description')
df


# In[13]:


#Convert table to html
mars_facts = df.to_html()

# Clean up unwanted new lines
mars_facts.replace('\n', '')


# In[14]:


print(mars_facts)


# ## *4. Scraping Mars Hemisphers*

# In[15]:


# URL of page to be scraped
mars_url = 'https://marshemispheres.com/'
browser.visit(mars_url)


# In[16]:


# html Object
html = browser.html

# Parse with Beautiful Soup
mars_soup = bs(html, 'html.parser')


# In[17]:


# Mars hemispheres info
mars_hemispheres = mars_soup.find('div', class_='collapsible results')
hemisphere_info = mars_hemispheres.find_all('div', class_='item')

#create an empty list to store names & urls of the hemispheres 
image_urls = []

# Iterate through hemisphere info
for data in hemisphere_info:
    # Get image title
    hemisphere = data.find('div', class_="description")
    title = hemisphere.h3.text
    
    # Collect image link by browsing to hemisphere page
    hemisphere_image_link = hemisphere.a["href"]    
    browser.visit(mars_url + hemisphere_image_link)
    
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'html.parser')
    
    hemisphere_link = hemisphere_soup.find('div', class_='downloads')
    hemisphere_url = hemisphere_link.find('li').a['href']

    # Create Dictionary to store title and url info
    image_dict = {}
    image_dict['title'] = title
    image_dict['img_url'] =  (mars_url + hemisphere_url)
    
    image_urls.append(image_dict)

pprint.pprint(image_urls)


# In[18]:


browser.quit()


# In[ ]:




