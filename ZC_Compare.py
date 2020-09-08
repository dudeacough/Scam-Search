#! python3
# ZC_Compare.py
# Program will compare a rental listing on Zillow with craiglist rental listings.  Duplicates on craiglist will be
# provided as an output

# TODO: Add Library Imports
import pyperclip
import sys
import os
import requests
import bs4
import logging
from pathlib import Path

logging.basicConfig(filename='myProgramLog.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s-%(message)s')
# logging.disable(logging.CRITICAL)

# Check if URL provided in sys arguments, otherwise look at clipboard.
if len(sys.argv) == 2:
    # ['ZC_Compare.py','Zillow URL']
    zillowURL = sys.argv[1]
else:
    zillowURL = pyperclip.paste()

# Add later to check if string provided in sys argv or clipboard is a zillow url, otherwise ask for

# TODO: Open Zillow site and capture the zip code and store photo images in an image object
req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

resZillow = requests.get('zillowURL', headers=req_headers)
if resZillow.raise_for_status() is not None:  # Check if Response object succesful and quit if not.
    print(f'Failed to create request object from url {zillowURL}')
    sys.exit()

soupZillow = bs4.BeautifulSoup(resZillow.text, 'html.parser')

addressZillow = soupZillow.find('div', class_='ds-price-change-address-row')
# TODO: Use a Regex to extract the zipcode from addressZillow.text



# TODO: Navigate to Craiglist and perform rental search based on zipcode from Zillow site

# TODO: Cycle through each search results pulled up.  Navigate to next page if necessary

# TODO: At each Craiglist listing, download images and compare them to the Zillow images.
# if greater than a certain % similiar, then output the CL URL to a file

