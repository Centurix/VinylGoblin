# Fetch releases from Rocking Horse Records in Brisbane
# Basic web scraper
# Base URL: https://rockinghorse.net/search?q=pixies+bossanova&filter.v.availability=1&filter.p.product_type=Vinyl+LPs
import requests
from bs4 import BeautifulSoup
from .shop import Shop, Record
import re
from decimal import Decimal


class RockingHorseRecords(Shop):
    def __init__(self):
        self._base_url = "https://rockinghorse.net"
        self.shop_name = "rocking_horse"
        self.shop_title = "Rocking Horse Records"

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass

    def fetch_items_by_artist_and_album(self, artist: str, album: str) -> list[Record]:
        # Go fetch a page
        found_releases: list[Record] = []
        response = requests.get(f"{self._base_url}/search?q={artist}+{album}&filter.v.availability=1&filter.p.product_type=Vinyl+LPs")
        soup = BeautifulSoup(response.text, "html.parser")
        releases = soup.find_all(name="li", class_="grid__item")
        # Find the img tag and grab the alt
        for release in releases:
            release_title = release.find(name="img").attrs.get("alt")
            regular_price = release.find(name="span", class_="price-item--regular")
            regular_price = re.sub('[^0-9,.]', '', regular_price.text)
            regular_price = Decimal(regular_price)

            sale_price = release.find(name="span", class_="price-item--sale")
            sale_price = re.sub('[^0-9,.]', '', sale_price.text)
            sale_price = Decimal(sale_price)
            found_releases.append(Record(
                release=release_title,
                regular_price=regular_price,
                sale_price=sale_price
                ))
        return found_releases
