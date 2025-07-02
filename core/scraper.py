# core/scraper.py

import requests
from typing import List, Dict
import os
from bs4 import BeautifulSoup
import time

class GoogleMapsScraper:
    """
    Scrapes business leads from Google Maps using SerpAPI.
    """

    def __init__(self, query: str, location: str):
        self.query = query
        self.location = location
        self.api_key = os.getenv("SERPAPI_KEY")
        self.base_url = "https://serpapi.com/search.json"

    def scrape(self) -> List[Dict]:
        params = {
            "engine": "google_maps",
            "q": self.query,
            "location": self.location,
            "api_key": self.api_key,
            "type": "search",
            "hl": "en",
        }

        response = requests.get(self.base_url, params=params)
        if response.status_code != 200:
            raise Exception(f"Google Maps API error: {response.status_code}")

        results = response.json().get("local_results", [])
        leads = []

        for r in results:
            lead = {
                "name": r.get("title"),
                "address": r.get("address"),
                "phone": r.get("phone"),
                "rating": r.get("rating"),
                "reviews": r.get("reviews"),
                "category": r.get("type"),
                "website": r.get("website"),
                "source": "Google Maps"
            }
            leads.append(lead)

        return leads


class YelpScraper:
    """
    Scrapes business leads from Yelp public listings (fallback web scraping).
    """

    def __init__(self, query: str, location: str):
        self.query = query.replace(" ", "%20")
        self.location = location.replace(" ", "%20")
        self.base_url = f"https://www.yelp.com/search?find_desc={self.query}&find_loc={self.location}"

    def scrape(self) -> List[Dict]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }

        response = requests.get(self.base_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Yelp scraping error: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        business_cards = soup.find_all('div', {'class': 'container__09f24__21w3G'})

        leads = []
        for card in business_cards:
            try:
                name_tag = card.find('a', {'class': 'css-19v1rkv'})
                if not name_tag:
                    continue
                name = name_tag.text.strip()

                rating_tag = card.find('span', {'class': 'display--inline__09f24__EhyFv border-color--default__09f24__NPAKY'})
                rating = rating_tag['aria-label'].split(' ')[0] if rating_tag else None

                category_tag = card.find('span', {'class': 'css-1yy09vp'})
                category = category_tag.text.strip() if category_tag else "Unknown"

                leads.append({
                    "name": name,
                    "address": "",
                    "phone": "",
                    "rating": rating,
                    "reviews": None,
                    "category": category,
                    "website": None,
                    "source": "Yelp (scraped)"
                })

                time.sleep(1)

            except Exception as e:
                continue

        return leads
