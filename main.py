import argparse
import sys
import requests
from requests.exceptions import HTTPError
from selenium import webdriver
from selenium.webdriver.common.by import By

from utils.urlchecker import checkUrl
from pprint import pprint


def main():

    parser = argparse.ArgumentParser(
        description="Check for broken links from a website.")
    parser.add_argument(
        "--link", help="Enter the URL of the website you want to check.", type=str, required=True)

    args = parser.parse_args()
    url = args.link

    if not url or not checkUrl(url):
        print("URL is either not configured for anchor tag or it is empty")
        sys.exit(0)

    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    driver.get(url)

    links = driver.find_elements(By.TAG_NAME, "a")

    for link in links:
        href = link.get_attribute("href")
        if href is None or not href:
            print("URL is either not configured for anchor tag or it is empty")
            continue

        try:
            huc = requests.get(href)
            huc.raise_for_status()

        except HTTPError as err:
            pprint(f'Error in following url: {href} -> {err}')
            continue
        except Exception as err:
            pprint(f'Skipping this URL: {href}')
            continue

        pprint(f'URL perfectly fine: {href}')

    driver.close()


main()
