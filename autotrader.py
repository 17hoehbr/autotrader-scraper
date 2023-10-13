import undetected_chromedriver as uc
import re
import csv
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


driver = uc.Chrome()

# navigate to the Autotrader website
driver.get("https://www.autotrader.com/cars-for-sale/all-cars/buick/lucerne/blacklick-oh?searchRadius=100&zip=43004&isNewSearch=true&marketExtension=include&showAccelerateBanner=false&sortBy=relevance&numRecords=100&requestId=2281868035")

# Wait for the results container to load
results = driver.find_element(By.CSS_SELECTOR, '[data-qaid="cntnr-listings"]')

# Find all the listings on the page
listings = results.find_elements(By.CSS_SELECTOR, '[data-cmp="inventoryListing"]')

# Set up the CSV writer
header = ['URL', 'Year', 'Trim', 'Miles', 'Price']
filename = 'autotrader.csv'

data = []

data.append(header)

for l in listings:
    url = l.find_element('tag name', 'a').get_attribute('href')
    title = l.find_element('tag name', 'h3').text
    price = l.find_element('class name', 'first-price').text.replace(',','')
    miles = l.find_element('class name', 'display-inline').text
    # remove all non-numerical characters
    miles = re.sub(r"\D", "", miles)
    year = re.search(r"\b\d{4}\b", title).group()
    trim = title.split()[-1]
    data.append([url, year, trim, miles, price])

#if os.path.exists('autotrader.csv'):
#    with open('autotrader.csv', newline='') as csvfile:
#        reader = csv.reader(csvfile)
#        for row in reader:
#            if row in data:
#                data.remove(row)

with open('lucerne.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)

# close the browser
driver.quit()
