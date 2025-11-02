"""
Generate an HTML report with interactive Plotly charts.
Run: python src/generate_report.py
"""
from src.data_preprocessing import load_transactions, add_features
from src.analysis import monthly_trends, summary_stats
from src.anomaly_detection import zscore_anomalies
from src.visualization import plot_category_breakdown, plot_monthly_trend, plot_top_anomalies
import os

def main():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "transactions.csv")
    reports_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    df = load_transactions(data_path)
    df = add_features(df)
    monthly = monthly_trends(df)
    anom = zscore_anomalies(df)
    # Create charts and save as interactive HTML files, then combine into one HTML
    cat_html = os.path.join(reports_dir, "cat_breakdown.html")
    plot_category_breakdown(df, save_path=cat_html)
    month_html = os.path.join(reports_dir, "monthly_trend.html")
    plot_monthly_trend(monthly, save_path=month_html)
    top_html = os.path.join(reports_dir, "top_anomalies.html")
    plot_top_anomalies(anom, save_path=top_html, n=50)
    # Combine simple
    combined = os.path.join(reports_dir, "insights_dashboard.html")
    with open(combined, "w", encoding="utf-8") as outf:
        outf.write("<html><head><title>Insights Dashboard</title></head><body>")
        outf.write("<h1>Financial Transaction Insights Dashboard</h1>")
        outf.write("<h2>Category Breakdown</h2>")
        with open(cat_html, "r", encoding="utf-8") as f:
            outf.write(f.read())
        outf.write("<h2>Monthly Trend</h2>")
        with open(month_html, "r", encoding="utf-8") as f:
            outf.write(f.read())
        outf.write("<h2>Top Anomalies</h2>")
        with open(top_html, "r", encoding="utf-8") as f:
            outf.write(f.read())
        outf.write("</body></html>")
    print(f"Report generated: {combined}")

if __name__ == '__main__':
    main()
