from selenium.webdriver.common.by import By
from selenium import webdriver
from tqdm import tqdm
import pandas as pd
import time

if __name__ == "__main__":
    driver = webdriver.Chrome()

    df = pd.read_csv("movie_urls.csv")
    movie_urls = df.url.to_list()

    movie_data = [] 
    for movie_url in tqdm(movie_urls):
            
        try:
            driver.get(movie_url)
            time.sleep(1)

            title = driver.find_element(By.CSS_SELECTOR, 'h1').text.strip()
            try:
                summary_element = driver.find_element(By.CLASS_NAME, 'c-productDetails_summary')
        
                # Click the 'Read More' button if it exists
                try:
                    read_more_button = summary_element.find_element(By.CLASS_NAME, 'c-productDetails_readMore')
                    read_more_button.click()
                    time.sleep(1)  # Allow time for the summary to expand
                except:
                    pass
        
                summary = summary_element.find_element(By.CLASS_NAME, 'c-productDetails_description').text.strip()
            except:
                summary = "No summary available"

           
            try:
                genres_elements = driver.find_elements(By.CSS_SELECTOR, ".c-genreList_item .c-globalButton_label")
                genres = list(set([genre.text for genre in genres_elements if genre.text]))
            except:
                genres = " "

            movie_data.append({
                "title": title,
                "url": movie_url,
                "summary": summary,
                "genres": genres
            })

            df = pd.DataFrame(data=movie_data, columns=movie_data[0].keys())
            df.to_csv("movie_details.csv", index=False)
        
        except:
            time.sleep(1)
