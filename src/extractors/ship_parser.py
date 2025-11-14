thonpython
import logging
import requests
from bs4 import BeautifulSoup
from .utils_format import clean_text

class ShipParser:
    BASE_URL = "https://www.cruisemapper.com/ships/ACL-American-Jazz-1558"

    def fetch_and_parse(self, filters=None):
        logging.info("Fetching ship page...")
        try:
            res = requests.get(self.BASE_URL, timeout=12)
            res.raise_for_status()
        except Exception as e:
            logging.error(f"Failed to fetch ship page: {e}")
            return []

        soup = BeautifulSoup(res.text, "html.parser")
        data = self.parse_ship_page(soup)

        if filters:
            data = self.apply_filters([data], filters)
        else:
            data = [data]

        return data

    def parse_ship_page(self, soup):
        """Minimal real extraction with fallbacks."""
        def get(selector):
            el = soup.select_one(selector)
            return clean_text(el.get_text()) if el else "N/A"

        return {
            "imo_number": get(".shipinfo .imo"),
            "mmsi_number": get(".shipinfo .mmsi"),
            "ship_name": get("h1"),
            "year_build": get(".shipinfo .year-built"),
            "passengers": get(".shipinfo .passengers"),
            "ship_url": self.BASE_URL,
            "cover_image": (soup.select_one(".ship-main-photo img")["src"]
                            if soup.select_one(".ship-main-photo img") else "N/A"),
            "flag_state": get(".shipinfo .flag"),
            "builder": get(".shipinfo .builder"),
            "class": get(".shipinfo .class"),
            "building_cost": get(".shipinfo .building-cost"),
            "speed": get(".shipinfo .speed"),
            "length_loa": get(".shipinfo .length"),
            "beam_width": get(".shipinfo .beam"),
            "gross_tonnage": get(".shipinfo .gt"),
            "crew": get(".shipinfo .crew"),
            "decks": get(".shipinfo .decks"),
            "cabins": get(".shipinfo .cabins"),
            "sister_ships": get(".shipinfo .sister-ships"),
            "christened_by": get(".shipinfo .christened-by"),
            "owner": get(".shipinfo .owner"),
            "operator": get(".shipinfo .operator"),
        }

    def apply_filters(self, data_list, filters):
        filtered = data_list
        for key, value in filters.items():
            filtered = [d for d in filtered if d.get(key) == value]
        return filtered