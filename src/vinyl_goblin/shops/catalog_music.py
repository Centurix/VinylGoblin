# Fetch releases from Catalog Music in Brisbane
# Basic web scraper with infinite scroll, there is no direct query
# 30 releases per scroll, roughly 1337 items
# Base URL: https://www.catalogmusic.store/s/shop?page=1&limit=1500&sort_by=name&sort_order=asc
from .shop import Shop, Record
import re
from decimal import Decimal, InvalidOperation
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import time


class CatalogMusic(Shop):
    def __init__(self):
        self._base_url = "https://www.catalogmusic.store"
        self._driver = None
        self.shop_name = "catalog_music"
        self.shop_title = "Catalog Music"
        self.releases_per_page = 30
    
    def __enter__(self):
        options = Options()
        options.headless = True
        options.add_argument("--headless")
        self._driver = webdriver.Firefox(options=options)
        self._driver.implicitly_wait(30)
        # Gather the infinite scroll here
        try:
            self._driver.get(f"{self._base_url}/s/shop?page=1&limit=1500&sort_by=name&sort_order=asc")
            # Get the total number of releases
            release_count_container = self._driver.find_element(By.CLASS_NAME, "filter")
            release_count = release_count_container.find_element(By.TAG_NAME, "p")
            regular_count = re.sub('[^0-9]', '', release_count.text)
            for i in range(1, 100):
                self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
                rc = len(self._driver.find_elements(By.CLASS_NAME, "mosaic-product-group"))
                if rc == int(regular_count):
                    break

            self._releases = []

            soup = BeautifulSoup(self._driver.page_source, "html.parser")
            releases = soup.find_all(name="div", class_="mosaic-product-group")
            for release in releases:
                release_title = release.find(name="p", class_="w-product-title").text.lower()
                release_title = release_title.replace("\t", "").replace("\n", "").replace("\r", "")
                regular_price = release.find(name="p", class_="product-price__wrapper")
                regular_price = re.sub('[^0-9,.]', '', regular_price.text)
                regular_price = Decimal(regular_price)

                self._releases.append(Record(
                    release=release_title,
                    regular_price=regular_price,
                    sale_price=regular_price
                    ))
        except (TimeoutError, InvalidOperation, WebDriverException):
            pass


        return self

    def __exit__(self, *args):
        self._driver.close()

    def fetch_items_by_artist_and_album(self, artist: str, album: str) -> list[Record]:
        # Find this data in the already scraped shop
        found_releases = []

        for release in self._releases:
            if artist.lower() in release.release and album.lower() in release.release:
                found_releases.append(release)

        return found_releases
