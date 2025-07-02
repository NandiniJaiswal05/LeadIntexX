# app.py

import streamlit as st
from core.scraper import GoogleMapsScraper, YelpScraper
from core.deduplicator import Deduplicator
from core.enricher import LeadEnricher
from core.scorer import LeadScorer
import pandas as pd
import time

st.set_page_config(page_title="LeadGen Pro", layout="wide")
st.title("🚀 SaaSquatch+ Lead Generator (Enhanced)")

# Sidebar Input
with st.sidebar:
    st.header("🔍 Lead Search Config")
    query = st.text_input("Business Type", value="Marketing Agency")
    location = st.text_input("Location", value="New York, NY")
    sources = st.multiselect("Data Sources", ["Google Maps", "Yelp"], default=["Google Maps"])
    scrape_btn = st.button("🔎 Find Leads")

# Result placeholders
if scrape_btn:
    with st.spinner("Scraping leads, deduplicating, and enriching them..."):
        all_leads = []

        if "Google Maps" in sources:
            g_scraper = GoogleMapsScraper(query, location)
            all_leads += g_scraper.scrape()
            time.sleep(1)

        if "Yelp" in sources:
            y_scraper = YelpScraper(query, location)
            all_leads += y_scraper.scrape()
            time.sleep(1)

        # Deduplicate
        deduper = Deduplicator()
        leads_deduped = deduper.deduplicate(all_leads)

        # Enrich
        enricher = LeadEnricher()
        leads_enriched = enricher.enrich(leads_deduped)

        # Score
        scorer = LeadScorer()
        final_leads = scorer.score(leads_enriched)

        df = pd.DataFrame(final_leads)

        st.success(f"✅ {len(df)} leads processed successfully.")
        st.dataframe(df[["name", "phone", "email", "rating", "score", "category", "source"]])

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "leads.csv", "text/csv")

        with st.expander("📊 Full Data Table"):
            st.dataframe(df)
else:
    st.info("👈 Enter your lead query and click 'Find Leads' to begin.")
