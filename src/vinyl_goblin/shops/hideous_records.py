# Fetch releases from Hideous Records in Brisbane
# Basic web scraper
# Base URL: https://www.hideousrecords.com.au/search?q=pixies+doolittle&options%5Bprefix%5D=last
from .shop import Shop, Record
import re
from decimal import Decimal, InvalidOperation
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup, Tag
from urllib3.exceptions import ReadTimeoutError


class HideousRecords(Shop):
    def __init__(self):
        self._base_url = "https://www.hideousrecords.com.au"
        self._driver = None
        self.shop_name = "hideous_records"
        self.shop_title = "Hideous Records"
    
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
        # Hideous records do not include the artist name in the releases, only the album name
        # so we artificially inject the artist name into the release
        found_releases: list[Record] = []
        try:

            self._driver.get(f"{self._base_url}/search?q={artist}+{album}&options%5Bprefix%5D=last")

            soup = BeautifulSoup(self._driver.page_source, "html.parser")
            release_container = soup.find(name="ul", class_="product-grid")
            if not isinstance(release_container, Tag):
                return found_releases

            releases = release_container.find_all(name="li", class_="grid__item")

            for release in releases:
                sold_out = release.find(name="span", class_="badge")
                if sold_out and sold_out.text == "Sold out":
                    continue

                release_container = release.find(name="h3", class_="card__heading")
                if not isinstance(release_container, Tag):
                    continue

                release_title_container = release_container.find(name="a")
                if not isinstance(release_title_container, Tag):
                    continue

                release_title = release_title_container.text.replace("\n", "").strip()

                regular_price = release.find(name="span", class_="price-item--regular")
                if regular_price:
                    regular_price = re.sub('[^0-9,.]', '', regular_price.text)
                    regular_price = Decimal(regular_price)

                    found_releases.append(Record(
                        release=f"{artist} - {release_title}",
                        regular_price=regular_price,
                        sale_price=regular_price
                        ))
        except (TimeoutError, InvalidOperation, WebDriverException, ReadTimeoutError):
            pass

        return found_releases
