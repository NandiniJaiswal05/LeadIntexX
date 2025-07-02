# core/deduplicator.py

from typing import List, Dict
import pandas as pd
from fuzzywuzzy import fuzz

class Deduplicator:
    """
    Deduplicates lead entries by:
    1. Removing exact duplicates on name, phone, or website.
    2. Using fuzzy string matching on name + address for soft matching.
    """

    def __init__(self, threshold: int = 85):
        self.threshold = threshold

    def deduplicate(self, leads: List[Dict]) -> List[Dict]:
        if not leads:
            return []

        # Step 1: Drop exact duplicates
        df = pd.DataFrame(leads)
        df.drop_duplicates(subset=["name", "phone", "website"], inplace=True)

        # Step 2: Fuzzy matching on name + address
        unique = []
        for i, row in df.iterrows():
            is_duplicate = False
            for existing in unique:
                name_score = fuzz.token_sort_ratio(str(row['name']), str(existing['name']))
                addr_score = fuzz.token_sort_ratio(str(row.get('address', '')), str(existing.get('address', '')))
                if name_score > self.threshold and addr_score > self.threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique.append(row.to_dict())

        return unique
