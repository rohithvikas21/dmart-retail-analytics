import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page layout to wide and modern
st.set_page_config(page_title="DMart Retail Analytics Dashboard", layout="wide")

# Title Header
st.title("🛒 DMart Enterprise Retail Sales Analytics Dashboard")
st.markdown("Interactive Master's Level Data Analytics Portfolio Piece | Explorer Environment")
st.markdown("---")

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_excel("Dataset/DMart_Sales_Data_50000_Records.xlsx")
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    return df

df = load_data()

# SIDEBAR FILTERS
st.sidebar.header("🎯 Strategic Filters")
selected_city = st.sidebar.multiselect("Select Cities:", options=df['City'].unique(), default=df['City'].unique()[:3])
selected_category = st.sidebar.multiselect("Select Categories:", options=df['Category'].unique(), default=df['Category'].unique()[:4])

# Filter Data Based on User Input
filtered_df = df[(df['City'].isin(selected_city)) & (df['Category'].isin(selected_category))]

# TOP ROW: KEY PERFORMANCE INDICATORS (KPIs)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💰 Total Revenue", f"₹{filtered_df['Total Sales'].sum():,.2f}")
with col2:
    st.metric("📈 Net Profit", f"₹{filtered_df['Profit'].sum():,.2f}")
with col3:
    st.metric("📦 Total Quantity Sold", f"{filtered_df['Quantity'].sum():,}")
with col4:
    st.metric("🏙️ Active Cities Selected", f"{len(selected_city)}")

st.markdown("---")

# MIDDLE ROW: TWO LIVE CHARTS SIDE-BY-SIDE
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("🏙️ Revenue Performance by Selected Cities")
    city_sales = filtered_df.groupby('City')['Total Sales'].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.barplot(x=city_sales.values, y=city_sales.index, palette="Blues_r", ax=ax)
    ax.set_xlabel("Total Revenue (in ₹)")
    plt.tight_layout()
    st.pyplot(fig)

with chart_col2:
    st.subheader("💳 Profit Distribution by Payment Mode")
    payment_profit = filtered_df.groupby('Payment Mode')['Profit'].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.pie(payment_profit.values, labels=payment_profit.index, autopct='%1.1f%%', colors=['#00539C', '#EEA47F', '#D4A373', '#E63946'])
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

# BOTTOM ROW: VIEW THE RAW FILTERED TRANSACTION DATA
st.subheader("📋 Filtered Transational Data View (Live Slice)")
st.dataframe(filtered_df.head(100), use_container_width=True)