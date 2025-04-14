import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("cleaned_retail_sales_data.csv", parse_dates=["Date Purchase"])

# Page config
st.set_page_config(page_title="🛒 Retail Sales Dashboard", layout="wide")

# CSS Styling for Dark Mode
st.markdown("""
    <style>
    body {
        background-color: #1e1e2f;
        color: #f5f5f5;
    }
    .main, .block-container {
        background-color: #1e1e2f !important;
        color: #f5f5f5 !important;
    }
    h1, h2, h3, .stMarkdown {
        color: #f5f5f5;
    }
    .card {
        background-color: #2a2a40;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.5);
        margin-bottom: 1rem;
        color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center;'>🛍️ Retail Sales Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# KPIs
total_revenue = df['Purchase Amount (USD)'].sum()
avg_transaction = df['Purchase Amount (USD)'].mean()
top_item = df['Item Purchased'].value_counts().idxmax()

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='card'><h3>Total Revenue</h3><h2 style='color:#22d3ee;'>${total_revenue:,.2f}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='card'><h3>Avg Purchase</h3><h2 style='color:#a3e635;'>${avg_transaction:,.2f}</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='card'><h3>Top Item</h3><h2 style='color:#f472b6;'>{top_item}</h2></div>", unsafe_allow_html=True)

# Section A
st.subheader("📊 Sales Analysis")

sales_per_item = df['Item Purchased'].value_counts().reset_index()
sales_per_item.columns = ['Item', 'Count']
fig_item = px.bar(sales_per_item.head(10), x='Item', y='Count', text='Count',
                  color_discrete_sequence=["#38bdf8"], title="Top 10 Best-Selling Items")
fig_item.update_traces(textposition='outside')
fig_item.update_layout(xaxis_tickangle=-45, template='plotly_dark')

avg_purchase_item = df.groupby("Item Purchased")["Purchase Amount (USD)"].mean().reset_index().sort_values(by="Purchase Amount (USD)", ascending=False).head(10)
fig_avg = px.bar(avg_purchase_item, x='Item Purchased', y='Purchase Amount (USD)', text='Purchase Amount (USD)',
                 color_discrete_sequence=["#e879f9"], title="Top 10 Items with Highest Avg Purchase Value")
fig_avg.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
fig_avg.update_layout(xaxis_tickangle=-45, template='plotly_dark')

st.plotly_chart(fig_item, use_container_width=True)
st.plotly_chart(fig_avg, use_container_width=True)

# Section B
st.subheader("📈 Time-Based Analysis")
daily_sales = df.groupby("Date Purchase")["Purchase Amount (USD)"].sum().reset_index()
fig_trend = px.line(daily_sales, x="Date Purchase", y="Purchase Amount (USD)", title="Sales Trend Over Time",
                    markers=True, color_discrete_sequence=["#4ade80"])
fig_trend.update_layout(template='plotly_dark')
st.plotly_chart(fig_trend, use_container_width=True)

peak_day = df['Date Purchase'].value_counts().idxmax()
peak_sales = df[df['Date Purchase'] == peak_day]['Purchase Amount (USD)'].sum()
st.markdown(f"📌 **Peak Day:** `{peak_day.date()}` – **${peak_sales:,.2f}**", unsafe_allow_html=True)

# Section C
st.subheader("💳 Payment Method Analysis")
payment_count = df['Payment Method'].value_counts().reset_index()
payment_count.columns = ['Payment Method', 'Count']
fig_payment = px.pie(payment_count, values='Count', names='Payment Method',
                     title="Payment Method Distribution", hole=0.4,
                     color_discrete_sequence=px.colors.sequential.Tealgrn)
fig_payment.update_layout(template='plotly_dark')
st.plotly_chart(fig_payment, use_container_width=True)

# Section D
st.subheader("🌟 Review Rating Analysis")
avg_rating = df['Review Rating'].mean()
top_rating_item = df.groupby("Item Purchased")["Review Rating"].mean().sort_values(ascending=False).head(1)
low_rating_item = df.groupby("Item Purchased")["Review Rating"].mean().sort_values().head(1)

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown(f"<div class='card'><h3>Average Rating</h3><h2 style='color:#eab308;'>{avg_rating:.2f} ⭐</h2></div>", unsafe_allow_html=True)
with col5:
    st.markdown(f"<div class='card'><h3>Top Rated Item</h3><h2 style='color:#10b981;'>{top_rating_item.index[0]} ({top_rating_item.iloc[0]:.1f})</h2></div>", unsafe_allow_html=True)
with col6:
    st.markdown(f"<div class='card'><h3>Lowest Rated Item</h3><h2 style='color:#ef4444;'>{low_rating_item.index[0]} ({low_rating_item.iloc[0]:.1f})</h2></div>", unsafe_allow_html=True)

fig_corr = px.scatter(df, x="Purchase Amount (USD)", y="Review Rating",
                      title="Correlation: Purchase Amount vs Rating",
                      trendline="ols", color_discrete_sequence=["#7c3aed"])
fig_corr.update_layout(template='plotly_dark')
st.plotly_chart(fig_corr, use_container_width=True)

# Section E
st.subheader("👥 Customer Segmentation")
cust_purchase_count = df.groupby("Customer Reference ID").size().sort_values(ascending=False).reset_index(name="Transaction Count")
cust_total_spent = df.groupby("Customer Reference ID")["Purchase Amount (USD)"].sum().sort_values(ascending=False).reset_index(name="Total Spent")

top_10 = pd.merge(cust_purchase_count, cust_total_spent, on="Customer Reference ID").head(10)
fig_top10 = px.bar(top_10, x="Customer Reference ID", y="Total Spent", text="Total Spent",
                   title="Top 10 Customers by Spending", color_discrete_sequence=["#8b5cf6"])
fig_top10.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
fig_top10.update_layout(template='plotly_dark')
st.plotly_chart(fig_top10, use_container_width=True)
