import plotly.express as px
import plotly.graph_objects as go

def plot_category_breakdown(df, save_path=None):
    s = df.groupby("category")["amount"].sum().reset_index()
    fig = px.bar(s, x="category", y="amount", title="Spending by Category (sum of amounts)")
    if save_path:
        fig.write_html(save_path)
    return fig

def plot_monthly_trend(series, save_path=None):
    fig = px.line(series.reset_index(), x="date", y="monthly_amount", title="Monthly Transaction Volume")
    if save_path:
        fig.write_html(save_path)
    return fig

def plot_top_anomalies(df, save_path=None, n=25):
    top = df.sort_values("z_score", key=abs, ascending=False).head(n)
    fig = px.scatter(top, x="date", y="amount", color="anomaly_zscore", hover_data=["transaction_id","customer_name","category"])
    fig.update_layout(title=f"Top {n} Potential Anomalies (by z-score)")
    if save_path:
        fig.write_html(save_path)
    return fig
