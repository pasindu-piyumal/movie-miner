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

for _ in range(6):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

movies = driver.find_elements(By.CSS_SELECTOR, 'div.title-list-grid__item a')

links = []
for movie in movies:
    link = movie.get_attribute('href')
    if link:
        links.append(link)

print(f"Total movie links: {len(links)}")