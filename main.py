#imports all modules needed for the webscraper 
import os
import time
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

class MAL(webdriver.Chrome):
    def __init__(self, collapse = False):
        #sets a path for the chrome webdriver to be found
        self.collapse = collapse 

        self.top_50_URL = []
        self.producer_dict = {}
        self.genres_dict = {}
        self.licensors_dict = {}
        self.studio_dict = {}
        self.number_of_episodes_dict = {}

        os.environ['PATH'] += r"/usr/local/bin"
        options = Options()
        options.add_argument('--headless')
        super(MAL, self).__init__()
    
    def __exit__(self, *args):
        if self.collapse == True:
            return super().__exit__(*args)
            
    def load_main_page(self):
        #uses the Chrome web driver
        self.get("https://myanimelist.net")
        self.maximize_window()

    def load_and_accept_cookies(self):
        try:
            WebDriverWait(
                self, const.DELAY).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@class = "qc-cmp2-summary-buttons"]')
                )
            )
        except TimeoutException as e:
            print(e)
        cookie_container = self.find_element(By.XPATH, '//*[@class = "qc-cmp2-summary-buttons"]')
        buttons = cookie_container.find_elements(By.TAG_NAME, 'button')
        for button in buttons:
            if button.get_attribute('innerHTML') == 'AGREE':
                button.click()
            else:
                continue

    def accept_policy_button(self):
        try:
            WebDriverWait(
                self, const.DELAY).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@class = "button-wrapper"]')
                )
            )
        except TimeoutException as e:
            print(e)
        Ok_container = self.find_element(By.XPATH, '//*[@class = "button-wrapper"]')
        ok_buttons = Ok_container.find_elements(By.TAG_NAME, 'button')
        time.sleep(2)
        for button in ok_buttons:
            if button.get_attribute('innerHTML') == 'OK':
                button.click()
            else:
                continue
    
    def load_top_anime(self):
        try:
            WebDriverWait(
                self, const.DELAY).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@class = "x-wider"]')
                )
            )
        except TimeoutException as e:
            print(e)
        anime = self.find_element(By.XPATH, '//*[@class = "x-wider"]')
        mal_headers = anime.find_elements(By.TAG_NAME, 'a')
        for anime in mal_headers:
            if anime.get_attribute('innerHTML') == 'Top Anime':
                top_anime_URL = anime.get_attribute('href')
            else:
                continue
        self.get(top_anime_URL)

    def get_top_50_links(self):
        ranking_table = self.find_element(By.CLASS_NAME, 'top-ranking-table')
        top_50_list =  ranking_table.find_elements(By.CLASS_NAME, 'ranking-list')
        for animes in top_50_list:
            link_tag = animes.find_element(By.CLASS_NAME, 'hoverinfo_trigger')
            self.top_50_URL.append(link_tag.get_attribute('href'))

    def scrap_all_data_for_top_50_animes(self):
        for url in self.top_50_URL:  
            with requests.get(url) as response:
                html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            #self.get_producers(url,soup)
            #self.get_licensors(url,soup)
            #self.get_studio(url,soup)
            self.get_genres(url,soup)
            #self.get_number_of_episodes(url,soup)

    def get_producers(self,url,soup):
        all_dark_text = soup.find_all('span', {'class':'dark_text'})
        for d_text in all_dark_text:
            if d_text.text == 'Producers:':
                prod_tag = d_text
            else:
                continue
        prod_sibs = prod_tag.find_next_siblings('a')
        producers = []
        for sib in prod_sibs:
            producers.append(sib.text)
        self.producer_dict[url] = producers

    def get_genres(self,url,soup):
        try:
            all_dark_text = soup.find_all('span', {'class':'dark_text'})
            for d_text in all_dark_text:
                if d_text.text == 'Genres:':
                    genre_tag = d_text
                else:
                    continue
            genre_sibs = genre_tag.find_next_siblings('a')
            genre = []
            for sib in genre_sibs:
                genre.append(sib.text)
            self.genres_dict[url] = genre
        except:
            all_dark_text = soup.find_all('span', {'class':'dark_text'})
            for d_text in all_dark_text:
                if d_text.text == 'Genre:':
                    genre_tag = d_text
                else:
                    continue
            genre_sib = genre_tag.find_next_sibling('a')
            genre = []
            genre.append(genre_sib.text)
            self.genres_dict[url] = genre

    def get_licensors(self,url,soup):
        all_dark_text = soup.find_all('span', {'class':'dark_text'})
        for d_text in all_dark_text:
            if d_text.text == 'Licensors:':
                licensors_tag = d_text
            else:
                continue
        licensors_sibs = licensors_tag.find_next_siblings('a')
        licensors = []
        for sib in licensors_sibs:
            if sib.text == "add some":
                sib.text == "None"
                licensors.append(sib.text)
                continue 
            licensors.append(sib.text)
        self.licensors_dict[url] = licensors

    def get_studio(self,url,soup):
        all_dark_text = soup.find_all('span', {'class':'dark_text'})
        for d_text in all_dark_text:
            if d_text.text == 'Studios:':
                studio_tag = d_text
            else:
                continue
        studio_sibs = studio_tag.find_next_siblings('a')
        studios = []
        for sib in studio_sibs:
            studios.append(sib.text)
        self.producer_dict[url] = studios

    def get_number_of_episodes(self,url,soup):
        all_dark_text = soup.find_all('span', {'class':'dark_text'})
        for d_text in all_dark_text:
            if d_text.text == 'Episodes:':
                no_episode_tag = d_text
            else:
                continue
            