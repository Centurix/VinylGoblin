from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Record:
    release: str
    regular_price: Decimal
    sale_price: Decimal


class Shop:
    def __init__(self):
        self._base_url = ""
        self.shop_name = "UNKNOWN"
        self.shop_title = "UNKNOWN"
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass

    def fetch_items_by_artist_and_album(self, artist: str, album: str) -> list[Record]:
        raise NotImplementedError
