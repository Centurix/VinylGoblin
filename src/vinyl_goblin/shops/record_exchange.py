# Fetch releases from Record Exchange in Brisbane
# Basic web scraper
# Base URL: https://www.recordexchange.com.au/search?type=product&q=pixies*+trompe*+le*+monde*
from .shop import Shop, Record
import re
from decimal import Decimal, InvalidOperation
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException


class RecordExchange(Shop):
    def __init__(self):
        self._base_url = "https://www.recordexchange.com.au"
        self._driver = None
        self.shop_name = "record_exchange"
        self.shop_title = "Record Exchange"
    
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
            self._driver.get(f"{self._base_url}/search?type=product&q={artist}*+{album}*")

            releases = self._driver.find_elements(By.CLASS_NAME, "productitem--info")
            found_releases = []

            for release in releases:
                release_title = release.find_element(By.TAG_NAME, "a").text
                regular_price_container = release.find_element(By.CLASS_NAME, "price__current")
                regular_price = regular_price_container.find_element(By.TAG_NAME, "span")
                regular_price = re.sub('[^0-9,.]', '', regular_price.text)
                regular_price = Decimal(regular_price)

                found_releases.append(Record(
                    release=release_title,
                    regular_price=regular_price,
                    sale_price=regular_price
                    ))
        except (TimeoutError, InvalidOperation, StaleElementReferenceException, NoSuchElementException):
            pass

        return found_releases
