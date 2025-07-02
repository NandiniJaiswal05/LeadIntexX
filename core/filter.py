# core/filter.py

from typing import List, Dict

class LeadFilter:
    """
    Filters a list of leads based on score, email availability, and category match.
    """

    def __init__(self):
        pass

    def apply_filters(
        self,
        leads: List[Dict],
        min_score: int = 0,
        email_required: bool = False,
        categories: List[str] = None
    ) -> List[Dict]:

        filtered = []
        for lead in leads:
            if lead.get("score", 0) < min_score:
                continue
            if email_required and not lead.get("email"):
                continue
            if categories and lead.get("category") not in categories:
                continue
            filtered.append(lead)

        return filtered
