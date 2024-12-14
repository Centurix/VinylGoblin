# Fetch releases from Stash Records in Brisbane
# Basic web scraper
# Base URL: https://www.stashrecords.com.au/pages/search-results-page?q=pixies%20bossanova&page=1&rb_stock_status=In%20Stock
from .shop import Shop, Record
import re
from decimal import Decimal, InvalidOperation
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException


class StashRecords(Shop):
    def __init__(self):
        self._base_url = "https://www.stashrecords.com.au"
        self._driver = None
        self.shop_name = "stash"
        self.shop_title = "Stash Records"
    
    def __enter__(self):
        options = Options()
        options.headless = True
        options.add_argument("--headless")
        self._driver = webdriver.Firefox(options=options)
        return self

    def __exit__(self, *args):
        self._driver.close()

    def fetch_items_by_artist_and_album(self, artist: str, album: str) -> list[Record]:
        # Go fetch a page
        try:
            self._driver.get(f"{self._base_url}/pages/search-results-page?q={artist}%20{album}&page=1&rb_stock_status=In%20Stock")

            releases = self._driver.find_elements(By.CLASS_NAME, "snize-product")
            found_releases = []

            for release in releases:
                # document.querySelector("#snize-product-7269948588068 > a > div > span > span.snize-title")
                release_title = release.find_element(By.CLASS_NAME, "snize-title").text
                regular_price = release.find_element(By.CLASS_NAME, "snize-price")
                regular_price = re.sub('[^0-9,.]', '', regular_price.text)
                regular_price = Decimal(regular_price)

                found_releases.append(Record(
                    release=release_title,
                    regular_price=regular_price,
                    sale_price=regular_price
                    ))
        except (TimeoutError, InvalidOperation, WebDriverException):
            pass

        return found_releases
