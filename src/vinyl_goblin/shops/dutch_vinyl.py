# Fetch releases from Dutch Vinyl in Brisbane
# Basic web scraper
# Base URL: https://www.dutchvinyl.com.au/search?q=pixies+doolittle
# NOTE: This store doesn't show location of the vinyl, Brisbane or Melbourne
from .shop import Shop, Record
import re
from decimal import Decimal, InvalidOperation
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import ReadTimeoutError


class DutchVinyl(Shop):
    def __init__(self):
        self._base_url = "https://www.dutchvinyl.com.au"
        self._driver = None
        self.shop_name = "dutch_vinyl"
        self.shop_title = "Dutch Vinyl"
    
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

            releases = self._driver.find_elements(By.CLASS_NAME, "productgrid--item")

            for release in releases:
                sold_out = release.find_element(By.TAG_NAME, "a").text
                if sold_out != "Sold out":
                    release_title_container = release.find_element(By.CLASS_NAME, "productitem--title")
                    release_title = release_title_container.find_element(By.TAG_NAME, "a").text
                    regular_price_container = release.find_element(By.CLASS_NAME, "price__current")
                    regular_price = regular_price_container.find_element(By.TAG_NAME, "span")
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
