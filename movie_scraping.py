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

    try:
        title = soup.find('h1').get_text(strip=True)
    except:
        title = 'N/A'

    try:
        year = soup.find("span", class_="release-year").get_text(strip=True)
    except:
        year = 'N/A'

    try:
        imdb = soup.find("span", class_="imdb-score").get_text(strip=True)
    except:
        imdb = "N/A"

    try:
        details = soup.find_all("div", class_="title-detail-hero-details__item")
        duration = next((d.text.strip() for d in details if "min" in d.text), "N/A")
    except:
        duration = "N/A"

    try:
        for div in soup.find_all("div", class_="poster-detail-infos__value"):
            span = div.find("span")
            if span:
                text = span.get_text(strip=True)

                if "," in text and not any(char.isdigit() for char in text):
                    genres = text
                    break
    except:
        genres = "N/A"

    try:
        article = soup.find("article", class_="article-block")
        if article:
            synopsis_p = article.find("p")
            if synopsis_p:
                synopsis = synopsis_p.get_text(strip=True)
    except:
        synopsis = "N/A"

    try:
        actors = soup.find_all("div", class_="title-credits__actor")
        cast = ", ".join(actor.find('span', class_='title-credit-name').get_text(strip=True) for actor in actors if actor.find('span', class_='title-credit-name'))
    except:
        cast = "N/A"

    try:
        directors = soup.find_all("div", class_="poster-detail-infos")
        director = ", ".join(director.find('span', class_='title-credit-name').get_text(strip=True) for director in directors if director.find('span', class_='title-credit-name'))
    except:
        director = "N/A"

    try:
        providers = [p.get("alt") for p in soup.select("img.provider-icon")]
        providers = ", ".join(providers)
    except:
        providers = "N/A"

    data.append({
        "Title": title,
        "Year": year,
        "IMDb Rating": imdb,
        "Duration": duration,
        "Genres": genres,
        "Synopsis": synopsis,
        "Cast": cast,
        "Director": director,
        "Providers": providers,
        "Link": link
    })

    driver.quit()

    df = pd.DataFrame(data)
    df.to_csv("movies.csv", index=False)
    print(df.head())