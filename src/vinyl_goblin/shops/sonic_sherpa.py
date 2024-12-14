# Fetch releases from Sonic Sherpa in Brisbane
# Basic web scraper
# Base URL: https://www.sonicsherpa.com.au/store/index.php?route=product/search&search=pixies%20bossanova
from .shop import Shop, Record
import re
from decimal import Decimal, InvalidOperation
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import ReadTimeoutError


class SonicSherpa(Shop):
    def __init__(self):
        self._base_url = "https://www.sonicsherpa.com.au"
        self._driver = None
        self.shop_name = "sonic_sherpa"
        self.shop_title = "Sonic Sherpa"
    
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
            self._driver.get(f"{self._base_url}/store/index.php?route=product/search&search={artist}%20{album}")

            releases = self._driver.find_elements(By.CLASS_NAME, "product-layout")
            found_releases = []

            for release in releases:
                release_title_container = release.find_element(By.CLASS_NAME, "caption")
                release_title = release_title_container.find_element(By.TAG_NAME, "a").text
                release_title = release_title.replace("\n", " ")
                regular_price = release.find_element(By.CLASS_NAME, "price")
                regular_price = re.sub('[^0-9,.]', '', regular_price.text)
                regular_price = Decimal(regular_price)

                found_releases.append(Record(
                    release=release_title,
                    regular_price=regular_price,
                    sale_price=regular_price
                    ))
        except (TimeoutError, InvalidOperation, WebDriverException, ReadTimeoutError):
            pass

        return found_releases
