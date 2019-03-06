from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time


def init_browser():

    execute_path = {
        "executable_path": "C:/Users/Sam Lin/Desktop/UoA_BC/chromedriver"}
    return Browser('chrome', **execute_path, headless=False)


def scrape():
     browser = init_browser()
     mars_data = {}

     url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
     browser.visit(url)
     time.sleep(2)

     html = browser.html
     soup = bs(html,"html.parser")
     
     title = soup.find("div", class_="content_title").text
     content = soup.find("div", class_="article_teaser_body").text
     print(f"Title: {title}")
     print(f"Content: {content}")
     mars_data["News_Title"] = title
     mars_data["News_Paragraph"] = content

     base_url = "https://www.jpl.nasa.gov/"
     url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
     browser.visit(url2)
     time.sleep(2)

     browser.click_link_by_id("full_image")
     time.sleep(2)

     html_image = browser.html
     soup = bs(html_image, "html.parser")

     img_url = soup.find("img", class_="fancybox-image")["src"]
     featured_img_url = base_url + img_url
     print(featured_img_url)
     mars_data["Featured_Image"] = featured_img_url

     weather_url = "https://twitter.com/marswxreport?lang=en"
     browser.visit(weather_url)
     time.sleep(2)

     html_weather = browser.html
     soup = bs(html_weather, "html.parser")

     mars_weather = soup.find("p", class_="TweetTextSize").text
     mars_weather = mars_weather.partition('pic')
     print(mars_weather)
     mars_data["Weather"] = mars_weather

     fact_url = "https://space-facts.com/mars/"

     fact = pd.read_html(fact_url)
     mars_facts_df = fact[0]
     mars_facts_df.columns = ["Parameter", "Values"]
     mars_facts_df

     mars_html_table = mars_facts_df.to_html()
     mars_html_table = mars_html_table.replace("\n", "")
     mars_html_table
     mars_data["Table"] = mars_html_table

     hemisphere_image_urls = [
          {"title": "Valles Marineris Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
          {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
          {"title": "Schiaparelli Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
          {"title": "Syrtis Major Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
     ]
     mars_data["Hemisphere"] = hemisphere_image_urls

     return mars_data
