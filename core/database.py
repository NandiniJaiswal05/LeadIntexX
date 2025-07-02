# core/database.py

import os
from typing import List, Dict
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class LeadDatabase:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["leadgenpro"]
        self.collection = self.db["leads"]

    def insert_leads(self, leads: List[Dict], query: str, location: str) -> None:
        for lead in leads:
            lead["query"] = query
            lead["location"] = location
        self.collection.insert_many(leads)

    def get_leads_by_query(self, query: str, location: str) -> List[Dict]:
        return list(self.collection.find({"query": query, "location": location}))

    def get_all_leads(self) -> List[Dict]:
        return list(self.collection.find())

    def clear_all(self):
        self.collection.delete_many({})
