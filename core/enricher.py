# core/enricher.py

import requests
from typing import List, Dict
from bs4 import BeautifulSoup
import re
import socket

class LeadEnricher:
    """
    Enriches lead data by:
    - Verifying website availability
    - Extracting contact email from homepage
    - Tagging with detected keywords (basic NLP)
    """

    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def enrich(self, leads: List[Dict]) -> List[Dict]:
        enriched_leads = []
        for lead in leads:
            website = lead.get("website")
            lead["reachable"] = False
            lead["email"] = None
            lead["tags"] = []

            if website:
                try:
                    if not website.startswith("http"):
                        website = "https://" + website
                    response = requests.get(website, timeout=self.timeout, headers={
                        "User-Agent": "Mozilla/5.0"
                    })

                    lead["reachable"] = response.status_code == 200
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Extract email
                    emails = re.findall(r"[\w\.-]+@[\w\.-]+", response.text)
                    lead["email"] = emails[0] if emails else None

                    # Extract tags based on meta content
                    meta = soup.find_all("meta")
                    keywords = []
                    for tag in meta:
                        if tag.get("name") in ["keywords", "description"] and tag.get("content"):
                            keywords += tag["content"].lower().split(",")

                    lead["tags"] = list(set([k.strip() for k in keywords if len(k.strip()) > 2]))

                except (requests.RequestException, socket.timeout):
                    lead["reachable"] = False

            enriched_leads.append(lead)

        return enriched_leads
