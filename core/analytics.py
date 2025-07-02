# core/analytics.py

from typing import List, Dict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class LeadAnalytics:
    """
    Generates visual insights from lead data.
    Output: histogram, category pie chart, score heatmap.
    """

    def __init__(self, output_dir: str = "charts"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        sns.set_theme(style="whitegrid")

    def score_distribution(self, leads: List[Dict]) -> str:
        df = pd.DataFrame(leads)
        plt.figure(figsize=(6, 4))
        sns.histplot(df["score"], bins=10, kde=True, color="steelblue")
        plt.title("Lead Score Distribution")
        plt.xlabel("Score")
        plt.ylabel("Frequency")
        path = os.path.join(self.output_dir, "score_distribution.png")
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        return path

    def category_pie(self, leads: List[Dict]) -> str:
        df = pd.DataFrame(leads)
        top_categories = df["category"].value_counts().head(8)
        plt.figure(figsize=(6, 6))
        top_categories.plot.pie(autopct="%1.1f%%", startangle=140, colors=sns.color_palette("pastel"))
        plt.ylabel("")
        plt.title("Top Lead Categories")
        path = os.path.join(self.output_dir, "category_pie.png")
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        return path

    def source_breakdown(self, leads: List[Dict]) -> str:
        df = pd.DataFrame(leads)
        plt.figure(figsize=(6, 4))
        sns.countplot(y="source", data=df, palette="muted")
        plt.title("Lead Source Breakdown")
        plt.xlabel("Count")
        path = os.path.join(self.output_dir, "source_breakdown.png")
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        return path
