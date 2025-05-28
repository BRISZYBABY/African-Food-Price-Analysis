import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.set_page_config(
    page_title="African Food Trend Analysis",
    layout="wide"
)

st.title("Welcome to African Food Trend Analysis")

# Load the datasets once
@st.cache_data
def load_data():
    df = pd.read_csv('Bri1.csv')
    df2 = pd.read_csv('NewBri.csv')
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df2.drop('Unnamed: 0', axis=1, inplace=True)
    # Convert year and month to numeric safely
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['month'] = pd.to_numeric(df['month'], errors='coerce')
    return df, df2

df, df2 = load_data()

st.markdown("Explore and analyze price trends for various produce items across different countries and market types.")

# Sidebar Navigation
analysis_options = ["Data Preview", "Price Trends by Produce", "Comparison by Market Type", "Comparison by Country", "Average Price by Country","Average Price by Item", "Price Trend by Country", "Price Trend by Item"]
choice = st.sidebar.selectbox("Choose Analysis Type", analysis_options)

if choice == "Data Preview":
    st.dataframe(df.sample(100))

elif choice == "Price Trends by Produce":
    produce_list = df2['produce'].unique()
    selected_produce = st.multiselect("Select produce", options=produce_list)

    if selected_produce:
        average_prices_comparison = df2[df2['produce'].isin(selected_produce)]
        average_prices_comparison = average_prices_comparison.groupby(['year', 'produce'])['price'].mean().reset_index()

        cols = st.columns(len(selected_produce))
        for idx, produce in enumerate(selected_produce):
            with cols[idx]:
                fig, ax = plt.subplots()
                subset = average_prices_comparison[average_prices_comparison['produce'] == produce]
                ax.plot(subset['year'], subset['price'], marker='o')
                ax.set_xlabel('Year')
                ax.set_ylabel('Average Price')
                ax.set_title(f'Price Trend Over Time - {produce}')
                st.pyplot(fig)

elif choice == "Comparison by Market Type":
    market_types = df2['market_type'].unique().tolist()
    selected_market_type = st.multiselect("Choose Market Type", market_types, default=market_types[:1])
    produce_list = df2['produce'].unique()
    selected_produce = st.selectbox("Select Produce", options=produce_list)

    if selected_market_type and selected_produce:
        apc = df2[(df2['market_type'].isin(selected_market_type)) & (df2['produce'] == selected_produce)]
        apc = apc.groupby(['market_type', 'year'])['price'].mean().reset_index()

        cols = st.columns(len(selected_market_type))
        price_min = apc['price'].min()
        price_max = apc['price'].max()
        for idx, mt in enumerate(selected_market_type):
            with cols[idx]:
                fig, ax = plt.subplots()
                subset = apc[apc['market_type'] == mt]
                ax.plot(subset['year'], subset['price'], marker='o')
                ax.set_ylim(price_min, price_max)
                ax.set_xlabel('Year')
                ax.set_ylabel('Average Price')
                ax.set_title(f'Price Trend Over Time for {selected_produce} - {mt}')
                st.pyplot(fig)

elif choice == "Comparison by Country":
    produce_list = df2['produce'].unique()
    selected_produce = st.selectbox("Select Produce", options=produce_list)

    if selected_produce:
        apc = df2[df2['produce'] == selected_produce]
        countries = apc['country'].unique().tolist()
        selected_country = st.multiselect("Choose Country", countries, default=countries[:2])

        if selected_country:
            apc = apc[apc['country'].isin(selected_country)]
            apc = apc.groupby(['country', 'year'])['price'].mean().reset_index()

            cols = st.columns(len(selected_country))
            for idx, con in enumerate(selected_country):
                with cols[idx]:
                    fig, ax = plt.subplots()
                    subset = apc[apc['country'] == con]
                    ax.plot(subset['year'], subset['price'], marker='o')
                    ax.set_xlabel('Year')
                    ax.set_ylabel('Average Price')
                    ax.set_title(f'Price Trend Over Time in {con} for {selected_produce}')
                    st.pyplot(fig)

elif choice == "Average Price by Country":
    avg_country = df2.groupby('country')['price'].mean().sort_values(ascending=False).reset_index()
    st.subheader("Average Price by Country")
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(data=avg_country, x='price', y='country', palette='viridis', ax=ax)
    ax.set_xlabel("Average Price")
    ax.set_ylabel("Country")
    st.pyplot(fig)

elif choice == "Average Price by Item":
    avg_item = df2.groupby('produce')['price'].mean().sort_values(ascending=False).reset_index()
    st.subheader("Average Price by Item (Produce)")
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(data=avg_item, x='price', y='produce', palette='magma', ax=ax)
    ax.set_xlabel("Average Price")
    ax.set_ylabel("Produce")
    st.pyplot(fig)

elif choice == "Price Trend by Country":
    countries = df2['country'].unique().tolist()
    selected_countries = st.multiselect("Select Country", options=countries, default=countries[:2])

    if selected_countries:
        country_data = df2[df2['country'].isin(selected_countries)]
        avg_trend = country_data.groupby(['year', 'country'])['price'].mean().reset_index()
        st.subheader("Price Trend by Country")
        fig, ax = plt.subplots(figsize=(12,6))
        sns.lineplot(data=avg_trend, x='year', y='price', hue='country', marker='o', ax=ax)
        ax.set_ylabel("Average Price")
        ax.set_title("Yearly Price Trend by Country")
        st.pyplot(fig)

elif choice == "Price Trend by Item":
    items = df2['produce'].unique().tolist()
    selected_items = st.multiselect("Select Produce", options=items, default=items[:2])

    if selected_items:
        item_data = df2[df2['produce'].isin(selected_items)]
        avg_trend = item_data.groupby(['year', 'produce'])['price'].mean().reset_index()
        st.subheader("Price Trend by Produce Item")
        fig, ax = plt.subplots(figsize=(12,6))
        sns.lineplot(data=avg_trend, x='year', y='price', hue='produce', marker='o', ax=ax)
        ax.set_ylabel("Average Price")
        ax.set_title("Yearly Price Trend by Item")
        st.pyplot(fig)

    post_2010 = df[df['year'] > 2010]

    st.subheader("Comparison of Average Prices by Market Type")
    market_avg = post_2010.groupby('market_type')['price'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=market_avg, x='market_type', y='price', palette="Set2", ax=ax)
    ax.set_xlabel("Market Type")
    ax.set_ylabel("Average Price")
    st.pyplot(fig)

    st.subheader("Total Monthly Price Over the Years")
    Total_Monthly_Price = post_2010.groupby(['year', 'month'])['price'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12,6))
    sns.lineplot(data=Total_Monthly_Price, x='month', y='price', hue='year', marker='o', ax=ax)
    ax.set_title('Total Monthly Price Over the Years')
    ax.set_xlabel('Month')
    ax.set_ylabel('Price')
    st.pyplot(fig)

    # Highest and Lowest Average Prices by Country
    average_prices = post_2010.groupby(['country'])['price'].mean().reset_index()
    highest_avg_prices = average_prices.nlargest(10, 'price')
    lowest_avg_prices = average_prices.nsmallest(10, 'price')

    st.subheader("Top 10 Countries with Highest Average Food Prices")
    st.bar_chart(data=highest_avg_prices.set_index('country')['price'])

    st.subheader("Top 10 Countries with Lowest Average Food Prices")
    st.bar_chart(data=lowest_avg_prices.set_index('country')['price'])

    # T-tests between market types
    retail_prices = post_2010[post_2010['market_type'] == 'Retail']['price']
    wholesale_prices = post_2010[post_2010['market_type'] == 'Wholesale']['price']
    producer_prices = post_2010[post_2010['market_type'] == 'Producer']['price']

    p_val_rw = stats.ttest_ind(retail_prices, wholesale_prices, nan_policy='omit').pvalue
    p_val_rp = stats.ttest_ind(retail_prices, producer_prices, nan_policy='omit').pvalue
    p_val_wp = stats.ttest_ind(wholesale_prices, producer_prices, nan_policy='omit').pvalue

    st.subheader("Price Differences Between Market Types (T-Test p-values)")
    st.write(f"Retail vs Wholesale: p-value = {p_val_rw:.4f}")
    st.write(f"Retail vs Producer: p-value = {p_val_rp:.4f}")
    st.write(f"Wholesale vs Producer: p-value = {p_val_wp:.4f}")

    lowest_mean_price = min(
        [("Retail", retail_prices.mean()), ("Wholesale", wholesale_prices.mean()), ("Producer", producer_prices.mean())],
        key=lambda x: x[1]
    )
    st.write(f"Market type offering the lowest average price: **{lowest_mean_price[0]}** with mean price {lowest_mean_price[1]:.2f}")

    # Elasticity example plot
    st.subheader("Impact of Price Changes on Quantity Demanded")

    def elastic_demand(price):
        return 10 - 2 * price

    def inelastic_demand(price):
        return 6 - price

    prices = np.arange(0, 11)
    quantity_elastic = elastic_demand(prices)
    quantity_inelastic = inelastic_demand(prices)

    fig, ax = plt.subplots()
    ax.plot(prices, quantity_elastic, label="Elastic Demand", marker='o')
    ax.plot(prices, quantity_inelastic, label="Inelastic Demand", marker='o')
    ax.set_xlabel("Price")
    ax.set_ylabel("Quantity Demanded")
    ax.set_title("Impact of Price Changes on Quantity Demanded")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)