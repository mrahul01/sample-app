import streamlit as st

# --- App Configuration ---
st.set_page_config(
    page_title="Interest Calculator",
    page_icon="💰",
    layout="centered"
)

# --- Title and Description ---
st.title("💰 Simple & Compound Interest Calculator")
st.markdown(
    """
    This app helps you calculate the future value of an investment or loan 
    using both simple and compound interest.
    """
)
st.write("---")

# --- User Inputs Sidebar ---
with st.sidebar:
    st.header("Input Parameters")
    principal = st.slider(
        "Initial Principal ($)",
        min_value=100.0,
        max_value=100000.0,
        value=1000.0,
        step=100.0
    )
    rate = st.slider(
        "Annual Interest Rate (%)",
        min_value=0.1,
        max_value=20.0,
        value=5.0,
        step=0.1
    )
    time = st.slider(
        "Time in Years",
        min_value=1,
        max_value=50,
        value=10,
        step=1
    )

    # For compound interest only
    compounding_frequency = st.selectbox(
        "Compounding Frequency",
        ("Annually", "Semi-annually", "Quarterly", "Monthly", "Daily")
    )

# --- Calculation Logic ---

# Simple Interest
simple_interest = principal * (rate / 100) * time
simple_future_value = principal + simple_interest

# Compound Interest
if compounding_frequency == "Annually":
    n = 1
elif compounding_frequency == "Semi-annually":
    n = 2
elif compounding_frequency == "Quarterly":
    n = 4
elif compounding_frequency == "Monthly":
    n = 12
else:  # Daily
    n = 365

compound_future_value = principal * (1 + (rate / 100) / n) ** (n * time)
compound_interest_earned = compound_future_value - principal

# --- Display Results ---
st.header("Calculation Results")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Simple Interest")
    st.info(f"**Final Amount:** ${simple_future_value:,.2f}")
    st.info(f"**Total Interest:** ${simple_interest:,.2f}")

with col2:
    st.subheader("Compound Interest")
    st.success(f"**Final Amount:** ${compound_future_value:,.2f}")
    st.success(f"**Total Interest:** ${compound_interest_earned:,.2f}")

st.write("---")

# --- Formula Explanations ---
st.subheader("Formulas Used")
st.markdown(
    """
    * **Simple Interest:** $A = P(1 + rt)$
    * **Compound Interest:** $A = P(1 + r/n)^{nt}$

    Where:
    * $A$ = final amount
    * $P$ = principal amount
    * $r$ = annual nominal interest rate
    * $t$ = time in years
    * $n$ = number of times interest is compounded per year
    """
)

st.write("---")

# --- Line Plot for Comparison ---
import numpy as np
import pandas as pd
import plotly.express as px

st.subheader("Simple vs. Compound Interest Growth")

# Create data for plotting
years = np.arange(1, time + 1)
simple_data = [principal + principal * (rate / 100) * y for y in years]
compound_data = [principal * (1 + (rate / 100) / n) ** (n * y) for y in years]

df = pd.DataFrame({
    'Year': years,
    'Simple Interest': simple_data,
    'Compound Interest': compound_data
})

df_melted = df.melt('Year', var_name='Type', value_name='Value')

fig = px.line(
    df_melted,
    x='Year',
    y='Value',
    color='Type',
    labels={
        "Value": "Amount ($)",
        "Type": "Interest Type"
    },
    title="Comparison Over Time"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Amount ($)",
    legend_title="Interest Type"
)

st.plotly_chart(fig, use_container_width=True)


