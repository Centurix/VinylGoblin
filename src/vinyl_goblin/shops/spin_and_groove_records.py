# Fetch releases from Waxx Lyrical Records in Brisbane
# Basic web scraper
# Base URL: https://www.spinandgrooverecords.com.au/search?q=amy+winehouse+back+to+black&options%5Bprefix%5D=last&filter.v.availability=1
from .shop import Shop, Record
import re
from decimal import Decimal, InvalidOperation
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
from urllib3.exceptions import ReadTimeoutError


class SpinAndGrooveRecords(Shop):
    def __init__(self):
        self._base_url = "https://www.spinandgrooverecords.com.au"
        self._driver = None
        self.shop_name = "spin_and_groove_records"
        self.shop_title = "Spin and Groove Records"
    
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
            self._driver.get(f"{self._base_url}/search?q={artist}+{album}&options%5Bprefix%5D=last&filter.v.availability=1")

            soup = BeautifulSoup(self._driver.page_source, "html.parser")
            releases = soup.find_all(name="li", class_="grid__item")


            for release in releases:
                release_title = release.find(name="h3", class_="card__heading").text.replace("\n", "").strip()
                regular_price = release.find(name="span", class_="price-item--regular")
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
