# Fetch releases from Relove Oxley in Brisbane
# Basic web scraper
# Base URL: https://shop.reloveoxley.com/search?q=pixies+bossanova&options%5Bprefix%5D=last
from .shop import Shop, Record
import re
from decimal import Decimal, InvalidOperation
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
from urllib3.exceptions import ReadTimeoutError


class ReloveOxley(Shop):
    def __init__(self):
        self._base_url = "https://shop.reloveoxley.com"
        self._driver = None
        self.shop_name = "relove_oxley"
        self.shop_title = "Relove Oxley"
    
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
            self._driver.get(f"{self._base_url}/search?q={artist}+{album}&options%5Bprefix%5D=last")

            soup = BeautifulSoup(self._driver.page_source, "html.parser")
            releases = soup.find_all(name="li", class_="grid__item")
            found_releases = []

            for release in releases:
                release_title_container = release.find(name="h3", class_="card__heading")
                release_title = release_title_container.find(name="a").text
                release_title = release_title.replace("\n", " ").strip()
                regular_price = release.find(name="span", class_="price-item--regular")
                regular_price = re.sub('[^0-9,.]', '', regular_price.text)
                regular_price = Decimal(regular_price)

                found_releases.append(Record(
                    release=release_title,
                    regular_price=regular_price,
                    sale_price=regular_price
                    ))
        except (AttributeError, TimeoutError, InvalidOperation, WebDriverException, ReadTimeoutError):
            pass

        return found_releases
