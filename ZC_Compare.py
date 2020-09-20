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
import re
import math
import operator
import functools
from pathlib import Path
from PIL import Image
from io import BytesIO

logging.basicConfig(filename='myProgramLog.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s-%(message)s')
# logging.disable(logging.CRITICAL)

# Check if URL provided in sys arguments, otherwise look at clipboard.
if len(sys.argv) == 2:
    # ['ZC_Compare.py','Zillow URL']
    zillowURL = sys.argv[1]
else:
    zillowURL = pyperclip.paste()

logging.info(f'The zillowURL is {zillowURL}')
# Add later to check if string provided in sys argv or clipboard is a zillow url, otherwise ask for

# Open Zillow site and capture the zip code and store photo images in an image object
req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

resZillow = requests.get(zillowURL, headers=req_headers)
if resZillow.raise_for_status() is not None:  # Check if Response object succesful and quit if not.
    print(f'Failed to create request object from url {zillowURL}')
    sys.exit()

soupZillow = bs4.BeautifulSoup(resZillow.text, 'html.parser')

addressZillow = soupZillow.find('div', class_='ds-price-change-address-row')

# Use a Regex to extract the zipcode from addressZillow.text
zipRegex = re.compile(r'\d\d\d\d\d')  # Define Regex object for finding 5 digit zipcodes
zipMo = zipRegex.findall(addressZillow.text)  # Finds all matches, multiple possible if address has >5 numbers
zipcode = zipMo[-1]  # Extracts the zipcode as the last matched object in list.

logging.info(f'The zipcode from Zillow is {zipcode}')


# Download home images from Zillow
soupZillowPicElement = soupZillow.find_all('picture', class_='media-stream-photo')  # All elements with phrase picture
# Note this above parse does not capture all Zillow images. Troubleshoot later
logging.info(f'Found {len(soupZillowPicElement)} pictures on Zillow')

zilPilImage = []  # List to hold pillow objects of Zillow Images
for step in soupZillowPicElement:
    zilImageURL = str(step).split('src=')[1].split('"')[1]  # Str for URL to .jpg image
    zilResponse = requests.get(zilImageURL)  # Download image from URL
    zilPilImage.append(Image.open(BytesIO(zilResponse.content)))  # Add PIL object to list

# TODO: Navigate to Craiglist and perform rental search based on zipcode from Zillow site

# Note need to update to work on different craiglist websties based on zipcode
base_IE_CL_URL = 'https://inlandempire.craigslist.org'  # Will change pending on CL specific area site.
CLSearchURL = f'{base_IE_CL_URL}/search/apa?query={zipcode}&availabilityMode=0&sale_date=all+dates'  # Initial CL search URL

resultFile = open('resultFile.txt', 'w')
resultFile.write(f'Zillow URL of rental listing is:{zillowURL}\n')

def search(CLpageURL):
    resCLSearch = requests.get(CLpageURL, headers=req_headers)
    if resCLSearch.raise_for_status() is not None:  # Check if Response object succesful and quit if not.
        print(f'Failed to create request object from url {CLpageURL}')
        sys.exit()

    soupCL = bs4.BeautifulSoup(resCLSearch.text, 'html.parser')
    return soupCL

while True:
    soupCLSearch = search(CLSearchURL)
    soupCLlinks = soupCLSearch.find_all('a', class_='result-image gallery')
    logging.info(f'found {len(soupCLlinks)} links on the Craiglist page {CLSearchURL}')

    for links in soupCLlinks:  # Loop through each listing on each search page
        res = requests.get(links.attrs['href'])  # Open up info on listing
        if res.raise_for_status() is not None:  # Check if Response object succesful and quit if not.
            print(f'Failed to create request object from url {res}')
            continue  # If unable to pull request, skip to next iteration

        logging.info(f"URL is {links.attrs['href']}")
        soupPage = bs4.BeautifulSoup(res.text, 'html.parser')
        picElements = soupPage.find_all('a', class_='thumb')

        listingCLPictures = []  # Reset list to store Pillow objects of pictures on CL listing
        for elements in picElements:
            imageRes = requests.get(elements.attrs['href'])
            listingCLPictures.append(Image.open(BytesIO(imageRes.content)))  # Add PIL object to list

        clResize = []  # Reset list to hold resized craiglist images resized.  Picture size need to match for comparison
        for pic in listingCLPictures:
            for x in range(len(zilPilImage)):
                clResize.append(pic.resize(zilPilImage[x].size))

        for imageElem in clResize:  # Comparing images on craiglist page to zillow
            clH = imageElem.histogram()
            for zPic in zilPilImage:
                zH = zPic.histogram()
                rms = math.sqrt(functools.reduce(operator.add, map(lambda a, b: (a - b)**2, clH, zH)) / len(clH))
                logging.info(f'rms is {rms}')
                if rms < 500:
                    resultFile.write(str(rms) + '\n')
                    resultFile.write(links.attrs['href'] + '\n\n')
                    break  # If match found break look
        resultFile.write('\n')

    # Grab the next button url link.
    soupNextButton = soupCLSearch.find('a', class_='button next')  # Find tag 'a' with class next button
    if soupNextButton is None:
        logging.info(f'No next button on craiglist URL {CLSearchURL}')
        break  # Stop looping when no next button link is found
    CLSearchURL = base_IE_CL_URL + soupNextButton.attrs['href']  # combine link with base CL url for next button link
    logging.info(f'Next button URL is {CLSearchURL}')

resultFile.close()
print('End of Code')
