import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the Streamlit page configuration
st.set_page_config(
    layout="wide",
    page_title="Booking.com Hotel Data Analysis"
)

# Load the hotel data
hotels_df = pd.read_csv("hotels_data.csv")

# Convert the 'price' column to numeric, handling errors
hotels_df['price'] = pd.to_numeric(
    hotels_df['price'].str.replace('EGP', '').str.replace(',', '').str.strip(),
    errors='coerce'
)

# Convert the 'rating' column to numeric, handling errors
hotels_df['rating'] = pd.to_numeric(
    hotels_df['rating'].str.extract('(\d+\.\d+)')[0],
    errors='coerce'
)

# Drop rows with NaN values in 'price' or 'rating'
hotels_df = hotels_df.dropna(subset=['price', 'rating'])

st.title("Booking.com Hotel Data Analysis")
st.sidebar.header("Filters")

# Sidebar filters
min_price, max_price = st.sidebar.slider(
    "Price Range (EGP)", 
    min_value=0.0, 
    max_value=float(hotels_df['price'].max() or 0), 
    value=(0.0, float(hotels_df['price'].max() or 0))
)

min_rating, max_rating = st.sidebar.slider(
    "Rating Range", 
    min_value=0.0, 
    max_value=10.0, 
    value=(0.0, 10.0)
)

selected_locations = st.sidebar.multiselect(
    "Select Locations", 
    options=hotels_df['location'].unique(), 
    default=hotels_df['location'].unique()
)

# Apply filters
filtered_df = hotels_df[
    (hotels_df['price'] >= min_price) &
    (hotels_df['price'] <= max_price) &
    (hotels_df['rating'] >= min_rating) &
    (hotels_df['rating'] <= max_rating) &
    (hotels_df['location'].isin(selected_locations))
]

# Display filtered data
st.subheader("Filtered Hotels Data")
st.dataframe(filtered_df)

# Analysis 1: Top-rated hotels
st.subheader("Top-Rated Hotels")
top_rated = filtered_df.sort_values(by="rating", ascending=False).head(10)
fig_top_rated = px.bar(
    top_rated, 
    x="name", 
    y="rating", 
    title="Top-Rated Hotels",
    labels={"name": "Hotel Name", "rating": "Rating"},
    text="rating"
)
fig_top_rated.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_top_rated)

# Analysis 2: Price distribution
st.subheader("Price Distribution")
fig_price_dist = px.histogram(
    filtered_df,
    x="price",
    nbins=10,
    title="Price Distribution of Hotels",
    labels={"price": "Price (EGP)"}
)
st.plotly_chart(fig_price_dist)

# Analysis 3: Rating vs. Price
st.subheader("Rating vs. Price Analysis")
fig_rating_vs_price = px.scatter(
    filtered_df,
    x="rating",
    y="price",
    size="price",
    color="name",
    hover_name="name",
    title="Rating vs. Price Analysis",
    labels={"rating": "Hotel Rating", "price": "Price (EGP)"}
)
st.plotly_chart(fig_rating_vs_price)

# Analysis 4: Average price by hotel
st.subheader("Average Price by Hotel")
avg_price_by_hotel = filtered_df.groupby("name")["price"].mean().reset_index()
fig_avg_price = px.bar(
    avg_price_by_hotel,
    x="name",
    y="price",
    title="Average Price by Hotel",
    labels={"name": "Hotel Name", "price": "Average Price (EGP)"},
    text="price"
)
fig_avg_price.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_avg_price)

# Analysis 5: Top-rated budget hotels
st.subheader("Top-Rated Budget Hotels")
budget_hotels = filtered_df[filtered_df['price'] < filtered_df['price'].mean()]
top_budget_rated = budget_hotels.sort_values(by="rating", ascending=False).head(10)
fig_budget_rated = px.bar(
    top_budget_rated, 
    x="name", 
    y="rating", 
    title="Top-Rated Budget Hotels",
    labels={"name": "Hotel Name", "rating": "Rating"},
    text="rating"
)
fig_budget_rated.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_budget_rated)

# Seaborn/Matplotlib Analysis 1: Line chart for ratings
st.subheader("Line Chart: Hotel Ratings")
fig1, ax1 = plt.subplots(figsize=(15, 5))
sns.lineplot(data=filtered_df, x='name', y='rating', ax=ax1)
ax1.set_title('Top Hotels Positive Reviews', fontsize=20)
ax1.set_xlabel('Hotel Name', fontsize=12)
ax1.set_ylabel('Rating', fontsize=12)
plt.xticks(rotation=45)
st.pyplot(fig1)

# Seaborn/Matplotlib Analysis 2: Line chart for prices
st.subheader("Line Chart: Price vs. Value")
fig2, ax2 = plt.subplots(figsize=(15, 5))
sns.lineplot(data=filtered_df, x='name', y='price', ax=ax2)
ax2.set_title('Price vs. Value', fontsize=20)
ax2.set_xlabel('Hotel Name', fontsize=12)
ax2.set_ylabel('Price (EGP)', fontsize=12)
plt.xticks(rotation=45)
st.pyplot(fig2)

# Analysis 6: Bar chart for hotel ratings in Hurghada
st.subheader("Hotel Ratings in Hurghada")
fig_price = px.bar(
    filtered_df.sort_values(by='rating', ascending=False),  # Sort by rating
    x='name', 
    y='rating', 
    title='Hotel Ratings in Hurghada',
    labels={'name': 'Hotel Name', 'rating': 'Rating (Score)'},
    text='name'
)
# Update layout for better aesthetics
fig_price.update_layout(
    xaxis={'categoryorder': 'total ascending'},
    xaxis_tickangle=-45,
    xaxis_title='Hotel Name',
    yaxis_title='Rating (Score)',
    title_x=0.5
)
st.plotly_chart(fig_price)

st.success("Analysis Complete!")
