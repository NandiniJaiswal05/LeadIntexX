# core/exporter.py

import pandas as pd
from typing import List, Dict
import os
import json
from fpdf import FPDF

class LeadExporter:
    """
    Export leads to various formats: CSV, Excel, JSON, and PDF.
    """

    def __init__(self, output_dir: str = "exports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def to_csv(self, leads: List[Dict], filename: str = "leads.csv") -> str:
        df = pd.DataFrame(leads)
        path = os.path.join(self.output_dir, filename)
        df.to_csv(path, index=False)
        return path

    def to_excel(self, leads: List[Dict], filename: str = "leads.xlsx") -> str:
        df = pd.DataFrame(leads)
        path = os.path.join(self.output_dir, filename)
        df.to_excel(path, index=False)
        return path

    def to_json(self, leads: List[Dict], filename: str = "leads.json") -> str:
        path = os.path.join(self.output_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(leads, f, ensure_ascii=False, indent=4)
        return path

    def to_pdf(self, leads: List[Dict], filename: str = "leads.pdf") -> str:
        path = os.path.join(self.output_dir, filename)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        for lead in leads:
            pdf.cell(200, 6, txt=f"Name: {lead.get('name', '')}", ln=True)
            pdf.cell(200, 6, txt=f"Phone: {lead.get('phone', '')} | Email: {lead.get('email', '')}", ln=True)
            pdf.cell(200, 6, txt=f"Website: {lead.get('website', '')}", ln=True)
            pdf.cell(200, 6, txt=f"Score: {lead.get('score', 0)} | Category: {lead.get('category', '')}", ln=True)
            pdf.cell(200, 6, txt="-" * 90, ln=True)

        pdf.output(path)
        return path
