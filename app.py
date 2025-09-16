import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import os

def create_dummy_orders_csv():
    """Creates a dummy orders.csv file if it doesn't exist."""
    if os.path.exists('orders.csv'):
        return

    dummy_content = [
        ['order_id', 'product', 'quantity', 'price', 'date'],
        ['101', 'Widget A', '2', '10.50', '2024-01-15'],
        ['102', 'Widget B', '5', '8.00', '2024-01-20'],
        ['103', 'Widget C', '1', '25.75', '2024-02-01'],
        ['104', 'Widget A', '3', '10.50', '2024-02-10'],
        ['105', 'Widget B', '2', '8.00', '2024-02-15'],
        ['106', 'Widget A', '4', '10.50', '2024-03-05'],
        ['107', 'Widget C', '2', '25.75', '2024-03-20'],
        ['108', 'Widget A', '1', '10.50', '2024-04-10'],
        ['109', 'Widget B', '3', '8.00', '2024-04-25']
    ]

    with open('orders.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(dummy_content)

def load_and_transform_data(filename):
    """Loads and transforms data from the CSV file."""
    df = pd.read_csv(filename)
    df['price'] = pd.to_numeric(df['price'])
    df['quantity'] = pd.to_numeric(df['quantity'])
    df['total_sale'] = df['price'] * df['quantity']
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%Y-%m')
    
    return df

# --- Main App Logic ---
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("Simple Sales Dashboard")
st.markdown("This app visualizes sales data from a dummy `orders.csv` file.")

# Create the dummy file to ensure the app runs independently
create_dummy_orders_csv()

# Load and transform the data
df = load_and_transform_data('orders.csv')

# --- Fact Table Aggregations ---
product_sales_df = df.groupby('product')['total_sale'].sum().reset_index()
product_sales_df = product_sales_df.rename(columns={'total_sale': 'Total Sales'})
monthly_sales_df = df.groupby('month')['total_sale'].sum().reset_index()
monthly_sales_df = monthly_sales_df.rename(columns={'total_sale': 'Total Sales'})

# --- Display Data and Visualizations ---
st.header("Aggregated Data")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Product Sales")
    st.dataframe(product_sales_df.set_index('product'))

with col2:
    st.subheader("Monthly Sales")
    st.dataframe(monthly_sales_df.set_index('month'))

st.header("Visualizations")

# Product Sales Bar Chart
fig_product, ax_product = plt.subplots()
ax_product.bar(product_sales_df['product'], product_sales_df['Total Sales'], color='skyblue')
ax_product.set_xlabel('Product')
ax_product.set_ylabel('Total Sales')
ax_product.set_title('Total Sales by Product')
st.pyplot(fig_product)

# Monthly Sales Line Chart
fig_monthly, ax_monthly = plt.subplots()
ax_monthly.plot(monthly_sales_df['month'], monthly_sales_df['Total Sales'], marker='o', linestyle='-', color='lightcoral')
ax_monthly.set_xlabel('Month')
ax_monthly.set_ylabel('Total Sales')
ax_monthly.set_title('Total Sales by Month')
ax_monthly.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig_monthly)
