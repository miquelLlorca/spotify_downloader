from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import numpy as np

import argparse
import data


def create_youtube_playlist(path):
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
    chrome_options.add_argument("--disable-web-security")       # Disable security checks
    chrome_options.add_argument("--disable-infobars")           # Suppress infobars (if applicable)
    # chrome_options.add_argument("--headless")                   # Optional: No GUI if headless mode is needed

    # Set up ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    df = data.read_as_df(path)
    youtube_titles = []
    youtube_urls = []

    try:
        # Open YouTube
        driver.get("https://www.youtube.com")
        time.sleep(5)

        for i, row in df.iterrows():
            query = str(row['name']) + ' ' + str(row['artist'])
            # Locate the search bar
            if(type(row['YouTube_Title'])!=str or row['YouTube_Title']==''):
                print(f' # Searching for: {query}')
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "search_query"))
                )
                search_box.clear()
                # Enter the song name and press Enter
                search_box.send_keys(query + Keys.RETURN)
                # Wait for results
                time.sleep(2)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//ytd-video-renderer"))
                )

                # Find the first organic result (skip ads)
                organic_results = driver.find_elements(By.XPATH, "//ytd-video-renderer[not(ancestor::ytd-ad-slot)]")
                youtube_url = None
                youtube_title = None

                for result in organic_results:
                    url = result.find_element(By.ID, "thumbnail").get_attribute("href")
                    # Check if URL is a video URL (not a playlist)
                    if url and "watch?v=" in url and "list=" not in url:
                        youtube_url = url
                        youtube_title = result.find_element(By.XPATH, ".//a[@id='video-title']").text
                        break  # stop at first valid video result
                
                print(f"    First organic result title: {youtube_title}")
                print(f"    First organic result URL: {youtube_url}")
            else: 
                youtube_title, youtube_url = row['YouTube_Title'], row['YouTube_URL']
                # print(' Already have the link.')
            print()
            youtube_titles.append(youtube_title)
            youtube_urls.append(youtube_url)

        # Saves the extracted data
        df['YouTube_Title'] = youtube_titles
        df['YouTube_URL'] = youtube_urls

        data.save_df(df, path)
    finally:
        driver.quit()

if(__name__=='__main__'):
    parser = argparse.ArgumentParser(description="Scraper script.")
    parser.add_argument("--path", type=str, required=True, help="Path to playlist")
    args = parser.parse_args()

    create_youtube_playlist(args.path)