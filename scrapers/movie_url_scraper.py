from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pandas as pd
import time


def main():

    base_url = "https://www.metacritic.com/browse/movie/all/all/all-time/new"
    driver = webdriver.Chrome()
    driver.get(base_url)
    movie_urls = []
    time.sleep(1)

    for idx in tqdm(range(1083)):
        page_no = idx + 1
        page_url = f"{base_url}?page={page_no}"
        driver.get(page_url)

        movie_cards = driver.find_elements(By.CLASS_NAME, 'c-finderProductCard')
        
        for card in movie_cards:
            anchor_tag = card.find_element(By.CLASS_NAME, 'c-finderProductCard_container')
            movie_url = anchor_tag.get_attribute('href')
            rows = card.find_elements(By.CLASS_NAME, 'c-finderProductCard_info')
        
            for row in rows:
                title_tag = row.find_element(By.CLASS_NAME, 'c-finderProductCard_titleHeading')
                title = title_tag.text
            
                movie_urls.append({"title": title,"url": movie_url})

    df = pd.DataFrame(data=movie_urls, columns=movie_urls[0].keys())

    df.to_csv("movie_urls.csv", index= False)
    driver.quit()

if __name__ == "__main__":
    main()