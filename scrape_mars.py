# Dependencies
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd
import pymongo
from selenium import webdriver
import time

def chrome_browser():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False) 

def scrape():
    browser = chrome_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #first_li = soup.find('li', class_='slide')
    # Get the title of news
    title = soup.find("div", class_="content_title").get_text()

    #Get the date of the news posted
    #title_d = first_li.find('div', calss_='list_date')
    #title_date = title_d.text
    

    # Get the paragraph description
    news_para = soup.find("div", class_="article_teaser_body").text
    
    

    # *************************************************************************************************
    # JPL mars Space Image.
    # *************************************************************************************************

    img_url = "https://spaceimages-mars.com/"
    browser.visit(img_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    image_url = soup.find('img', class_='thumbimg')['src']
    
    featured_image_url = f"{img_url}{image_url}"

    # *************************************************************************************************
    # Facts about mars
    # *************************************************************************************************
    
    panda_url = "https://galaxyfacts-mars.com"
    browser.visit(panda_url)
    time.sleep(1)

    html = browser.html

    tables = pd.read_html(html)

    facts_df = tables[0]
    facts_df = facts_df.iloc[1:]
    facts_df.set_index(0)

    facts_df.columns=['Mars-Earth Comparison','Mars','Earth']

    html_table = facts_df.to_html(index=False, header=True)

    # *************************************************************************************************
    # Scraping Mars Hemisphere Image
    # *************************************************************************************************

    hemi_url = "https://marshemispheres.com"
    browser.visit(hemi_url)
    html = browser.html
    hemi_soup = bs(html, 'html.parser')
    hemi = hemi_soup.find_all('div', class_='item')
    hemi_list = []

    for hemisphere in range(len(hemi)):
        hemi_link = browser.find_by_css('a.product-item h3')
        hemi_link[hemisphere].click()
        time.sleep(1)
        
        img_html = browser.html
        img_soup = bs(img_html, 'html.parser')
        
        img_title = img_soup.find('h2', class_='title').get_text()
        
        img_find_class = img_soup.find('div', class_="downloads")
        img_find_click = img_find_class.find('li')
        img_find = img_find_click.find('a')['href']
        
        img_url = f"{hemi_url}/{img_find}"
        
        hemi_list.append({"title":img_title,
                        "img_url":img_url})
        browser.back()
    
    browser.quit()

    # **************************************************************************************************
    # Storing the data into a single dictionary to return the values
    # **************************************************************************************************

    scraped_data = {
        "title_part": title,
        "news": news_para,
        "featured_image": featured_image_url,
        "mars_table": html_table,
        "hemisphere_images": hemi_list 
    }
    '''
    browser.quit()
    scraped_data={
        "title": title,
        "news_para": news_para,
    }'''

    return scraped_data
