import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set a wide layout for the dashboard
st.set_page_config(layout="wide")

# Use st.cache_data to load the data once and cache it.
# This prevents reloading the data every time a user interacts with a widget.
@st.cache_data
def load_data():
    # Load a public dataset. Replace this with your own data source (e.g., CSV, API)
    df = px.data.gapminder()
    return df

df = load_data()

# --- Sidebar for user input ---
with st.sidebar:
    st.header("Dashboard Filters")
    
    # Year slider
    year_to_filter = st.slider('Select Year', 
                               min_value=int(df['year'].min()), 
                               max_value=int(df['year'].max()), 
                               value=int(df['year'].max()))
    
    # Country multi-select
    all_countries = df['country'].unique()
    selected_countries = st.multiselect(
        'Select Countries',
        all_countries,
        default=['United States', 'China', 'India', 'Germany']
    )
    
    # Continent radio buttons
    continent_options = ['All'] + list(df['continent'].unique())
    selected_continent = st.radio('Filter by Continent', continent_options)

# Filter the data based on user input
filtered_df = df[df['year'] == year_to_filter]
if selected_continent != 'All':
    filtered_df = filtered_df[filtered_df['continent'] == selected_continent]
filtered_df = filtered_df[filtered_df['country'].isin(selected_countries)]


# --- Main dashboard layout ---
st.title('Interactive Global Data Dashboard')

# --- Display key metrics ---
st.header("Key Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    total_population = filtered_df['pop'].sum()
    st.metric(label="Total Population", value=f"{total_population:,.0f}")
with col2:
    avg_life_exp = filtered_df['lifeExp'].mean()
    st.metric(label="Average Life Expectancy", value=f"{avg_life_exp:.2f}")
with col3:
    avg_gdp_per_cap = filtered_df['gdpPercap'].mean()
    st.metric(label="Average GDP per Capita", value=f"${avg_gdp_per_cap:,.0f}")

st.markdown("---")


# --- Display charts and data ---
st.header("Data Visualizations")

# 1. Bubble chart
st.subheader("Population, Life Expectancy, and GDP per Capita")
fig_bubble = px.scatter(
    filtered_df, 
    x="gdpPercap", 
    y="lifeExp", 
    size="pop", 
    color="continent",
    hover_name="country",
    log_x=True, 
    size_max=60,
    title=f"Global Data for {year_to_filter}"
)
st.plotly_chart(fig_bubble, use_container_width=True)

# 2. Bar chart
st.subheader("Life Expectancy by Country")
fig_bar = px.bar(
    filtered_df,
    x="country",
    y="lifeExp",
    color="continent",
    title=f"Life Expectancy per Country in {year_to_filter}"
)
st.plotly_chart(fig_bar, use_container_width=True)

# 3. Data table
st.subheader("Raw Data Table")
st.dataframe(filtered_df, use_container_width=True)



