# app.py – Main Streamlit Interface

import streamlit as st
from core.scraper import GoogleMapsScraper, YelpScraper
from core.deduplicator import Deduplicator
from core.enricher import LeadEnricher
from core.scorer import LeadScorer
from ui.dashboard import Dashboard
from utils.file_handler import FileHandler

st.set_page_config(page_title="LeadIntelX - Smart Lead Intelligence", layout="wide")
st.title("📊 LeadIntelX – AI-Powered Local Lead Intelligence")

# Upload business keyword and location input
st.sidebar.header("Search Settings")
business_type = st.sidebar.text_input("Business Type (e.g., dentist, plumber)", "dentist")
city = st.sidebar.text_input("City or Area", "San Francisco")
source = st.sidebar.selectbox("Data Source", ["Google Maps", "Yelp"])

if st.sidebar.button("🔍 Find Leads"):
    with st.spinner("Scraping leads from the web..."):
        if source == "Google Maps":
            scraper = GoogleMapsScraper(query=business_type, location=city)
        else:
            scraper = YelpScraper(query=business_type, location=city)

        raw_leads = scraper.scrape()
        deduplicated = Deduplicator().deduplicate(raw_leads)
        enriched = LeadEnricher().enrich(deduplicated)
        scored = LeadScorer().score(enriched)

        st.success(f"✅ {len(scored)} leads extracted, enriched, and scored.")
        Dashboard().render(scored)

        # Export options
        st.download_button("📥 Download CSV", FileHandler.to_csv(scored), "leads.csv")
