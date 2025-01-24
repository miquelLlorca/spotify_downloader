from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import numpy as np

import argparse

def download_playlist(path, webpage):
    if(webpage=='notube'):
        download_with_notube(path)
    if(webpage=='y2mate'):
        download_with_y2mate(path)



def download_with_notube(path):
    print('holi')
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
    chrome_options.add_argument("--disable-web-security")       # Disable security checks
    chrome_options.add_argument("--disable-infobars")           # Suppress infobars (if applicable)
    # chrome_options.add_argument("--headless")                   # Optional: No GUI if headless mode is needed

    # Set up ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    df = pd.read_csv(path, encoding='ISO-8859-1', sep=';')

    if('downloaded' not in df.columns):
        df['downloaded'] = [False for i in range(len(df))]
        
    try:
        driver.get("https://notube.si/es/youtube-app-57")

        for i, row in df.iterrows():
            # 1. Look for the textbox
            textbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "video")))
            print(type(row['YouTube_URL']), row['downloaded'])
            if(type(row['YouTube_URL'])==str and not row['downloaded']):
                print(f'Downloading {row["name"]}')
                # 2. Write some data
                textbox.send_keys(row['YouTube_URL'])

                # 3. Click on convert button
                convert_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Convert']"))
                )
                convert_button.click()

                # 4. Wait for download button to appear and click it
                dowload_button = WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Download']"))
                )
                dowload_button.click()
                
                # 5. Sleep for a bit so downloads have time to finish
                time.sleep(2)
                df.at[i, 'downloaded'] = True
                df.to_csv(path, index=False, sep=';')
                print(f'Downloaded {i} - {row["YouTube_Title"]}')
                
                # 6. Click on next to continue donwloading
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
                )
                next_button.click()
                
    finally:
        df.to_csv(path, index=False, sep=';')
        driver.quit()


def download_with_y2mate(path):
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
    chrome_options.add_argument("--disable-web-security")       # Disable security checks
    chrome_options.add_argument("--disable-infobars")           # Suppress infobars (if applicable)
    # chrome_options.add_argument("--headless")                   # Optional: No GUI if headless mode is needed

    # Set up ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    df = pd.read_csv(path, encoding='ISO-8859-1', sep=';')

    if('downloaded' not in df.columns):
        df['downloaded'] = [False for i in range(len(df))]
        
    try:
        driver.get("https://y2mate.nu/en-efXo/")

        for i, row in df.iterrows():
            # 1. Look for the textbox
            textbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "video")))
            print(type(row['YouTube_URL']), row['downloaded'])
            if(type(row['YouTube_URL'])==str and not row['downloaded']):
                print(f'Downloading {row["name"]}')
                # 2. Write some data
                textbox.send_keys(row['YouTube_URL'])

                # 3. Click on convert button
                convert_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Convert']"))
                )
                convert_button.click()

                # 4. Wait for download button to appear and click it
                dowload_button = WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Download']"))
                )
                dowload_button.click()
                
                # 5. Sleep for a bit so downloads have time to finish
                time.sleep(2)
                df.at[i, 'downloaded'] = True
                df.to_csv(path, index=False, sep=';')
                print(f'Downloaded {i} - {row["YouTube_Title"]}')
                
                # 6. Click on next to continue donwloading
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
                )
                next_button.click()
                
    finally:
        df.to_csv(path, index=False, sep=';')
        driver.quit()


if(__name__=='__main__'):
    parser = argparse.ArgumentParser(description="Scraper script.")
    parser.add_argument("--path", type=str, required=True, help="Path to playlist")
    args = parser.parse_args()

    download_playlist(args.path)