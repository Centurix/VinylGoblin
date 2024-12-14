# Fetch releases from Monster Robot in Brisbane
# Basic web scraper
# Base URL: https://monsterrobot.party/?product_cat=&s=andy+c&post_type=product
from .shop import Shop, Record
import re
from decimal import Decimal, InvalidOperation
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException


class MonsterRobot(Shop):
    def __init__(self):
        self._base_url = "https://monsterrobot.party"
        self._driver = None
        self.shop_name = "monster_robot"
        self.shop_title = "Monster Robot"
    
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
            self._driver.get(f"{self._base_url}/?product_cat=&s={artist}+{album}&post_type=product")

            releases = self._driver.find_elements(By.CLASS_NAME, "product-small")
            found_releases = []

            for release in releases:
                # document.querySelector("#snize-product-7269948588068 > a > div > span > span.snize-title")
                release_title = release.find_element(By.CLASS_NAME, "woocommerce-LoopProduct-link").text
                regular_price = release.find_element(By.TAG_NAME, "bdi")
                # regular_price = release.find_element(By.CLASS_NAME, "woocommerce-Price-currencySymbol")
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
