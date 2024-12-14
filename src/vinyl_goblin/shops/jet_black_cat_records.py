# Fetch releases from Jet Black Cat Records in Brisbane
# Basic web scraper
# Base URL: https://jetblackcatmusic.com/search?q=pixies+doolittle
from .shop import Shop, Record
import re
from decimal import Decimal, InvalidOperation
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import ReadTimeoutError


class JetBlackCatRecords(Shop):
    def __init__(self):
        self._base_url = "https://jetblackcatmusic.com"
        self._driver = None
        self.shop_name = "jet_black_cat_records"
        self.shop_title = "Jet Black Cat Records"
    
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
            self._driver.get(f"{self._base_url}/search?q={artist}+{album}")

            releases = self._driver.find_elements(By.CLASS_NAME, "list-view-item")

            for release in releases:
                sold_outs = release.find_elements(By.CLASS_NAME, "list-view-item__sold-out")
                if len(sold_outs) == 0:
                    release_title = release.find_element(By.CLASS_NAME, "list-view-item__title").text
                    regular_price = release.find_element(By.CLASS_NAME, "product-price__price")
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
