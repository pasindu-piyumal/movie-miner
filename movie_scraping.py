from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get('https://www.justwatch.com/us/movies')
time.sleep(5)

last_height = driver.execute_script("return document.body.scrollHeight")

for _ in range(1):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    driver.execute_script("window.scrollBy(0, -500);")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, 500);")

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break

    last_height = new_height

movies = driver.find_elements(By.CSS_SELECTOR, 'div.title-list-grid__item a')

links = []
for movie in movies:
    link = movie.get_attribute('href')
    if link:
        links.append(link)

print(f"Total movie links: {len(links)}")

data = []

total = min(len(links), 1)

for i, link in enumerate(links[:total]):
    print(f"\nScrapping {i+1}: {link}")
    driver.get(link)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')