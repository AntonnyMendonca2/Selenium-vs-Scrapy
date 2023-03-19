from cmath import log
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import csv

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler("logs/scrapping.log"),
                              logging.StreamHandler()])


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def advance_page():
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main_content"]/div[1]/div[2]/div/div[1]/div/div[9]/div/div/div[1]/span[2]/a'))).click()
    except Exception as e:
        logging.error(e)
    

def scrap():
    try:
        driver.get("https://www.metacritic.com/browse/games/score/metascore/all/all/filtered")
    except Exception as e:
        logging.error("'\033[91m' não foi possível fazer a requisição no site, confira se o mesmo ainda está no ar ou se o link foi alterado'\033[0m'")
    pages = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main_content"]/div[1]/div[2]/div/div[1]/div/div[9]/div/div/div[2]/ul/li[10]/a')))
    try:
        for i in range(int(pages.text)):
            # logging.warning(f"Avançado para a página: '\033[92m' {i} '\033[0m'")
            div = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'clamp-summary-wrap')))
            try:
                for item in range(len(div)):
                    title = WebDriverWait(div[item], 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.clamp-list .clamp-summary-wrap h3'))).text
                    plataform = WebDriverWait(div[item], 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'data'))).text
                    release_date = WebDriverWait(div[item], 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="clamp-details"]/span')))
                    release_date = [str(x.text) for x in release_date][item]
                    rating = WebDriverWait(div[item], 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.metascore_w'))).text
                    description = WebDriverWait(div[item], 5).until(EC.presence_of_element_located((By.CLASS_NAME, "summary"))).text
                    pd.DataFrame([title, plataform, release_date, rating, description]).T.to_csv('scrap.csv', mode='a', index=False, header=False)
                    logging.warning(f"página: '\033[92m' {i+1} '\033[0m' jogo: '\033[92m'{title}'\033[0m'") 
            except Exception as e:
                logging.error("'\033[91m' não foi possível iterar entre a página encontrada '\033[0m'")
            advance_page()
    except Exception as e:
        logging.error("'\033[91' não foi possível avançar a página '\033[0m'")

if __name__ == "__main__":
    scrap()