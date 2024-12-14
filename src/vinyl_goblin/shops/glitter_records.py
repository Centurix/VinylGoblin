# Fetch releases from Glitter Records in Brisbane
# Basic web scraper
# Base URL: https://glitterrecords.com.au/search?q=the+beatles+revolver&options%5Bprefix%5D=last
from .shop import Shop, Record
import re
from decimal import Decimal, InvalidOperation
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import ReadTimeoutError


class GlitterRecords(Shop):
    def __init__(self):
        self._base_url = "https://glitterrecords.com.au"
        self._driver = None
        self.shop_name = "glitter_records"
        self.shop_title = "Glitter Records"
    
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
        found_releases: list[Record] = []
        try:
            self._driver.get(f"{self._base_url}/search?q={artist}+{album}&options%5Bprefix%5D=last")

            releases = self._driver.find_elements(By.CLASS_NAME, "grid__item")

            for release in releases:
                # document.querySelector("#snize-product-7269948588068 > a > div > span > span.snize-title")
                release_title = release.accessible_name
                # release_title = release.find_element(By.CLASS_NAME, "full-unstyled-link").text
                regular_price = release.find_element(By.CLASS_NAME, "price-item--regular")
                regular_price = re.sub('[^0-9,.]', '', regular_price.text)
                regular_price = Decimal(regular_price)

                found_releases.append(Record(
                    release=release_title,
                    regular_price=regular_price,
                    sale_price=regular_price
                    ))
        except (ValueError, TimeoutError, InvalidOperation, WebDriverException, ReadTimeoutError):
            pass

        return found_releases
