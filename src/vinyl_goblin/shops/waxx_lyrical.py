# Fetch releases from Waxx Lyrical Records in Brisbane
# Basic web scraper
# Base URL: https://www.waxxlyrical.com/search-results?q=pixies+doolittle
from .shop import Shop, Record
import re
from decimal import Decimal, InvalidOperation
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from bs4 import BeautifulSoup


class WaxxLyricalRecords(Shop):
    def __init__(self):
        self._base_url = "https://www.waxxlyrical.com"
        self._driver = None
        self.shop_name = "waxx_lyrical_records"
        self.shop_title = "Waxx Lyrical Records"
    
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
            self._driver.get(f"{self._base_url}/search-results?q={artist}+{album}")

            soup = BeautifulSoup(self._driver.page_source, "html.parser")
            releases = soup.find_all(name="li", attrs={"data-hook": "grid-layout-item"})

            found_releases = []

            for release in releases:
                sold_out = release.find(name="button").text
                if sold_out != "Out of Stock":
                    release_title = release.find(name="a", attrs={"data-hook": "item-title"}).text
                    regular_price = release.find(name="span", attrs={"data-hook": "item-price"})
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
