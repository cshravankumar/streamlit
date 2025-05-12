import streamlit as st
import pandas as pd
import datetime
import altair as alt

st.set_page_config(layout="wide")

# Mock Data for Demonstration
cash_on_hand = 2200
upcoming_payments = pd.DataFrame({
    'Due Date': ['2025-05-15', '2025-05-21', '2025-05-25'],
    'Description': ['Amex Statement', 'Visa Rent Payment', 'Capital One Auto'],
    'Amount': [350, 1200, 450],
    'Status': ['Pending', 'Pending', 'Pending']
})

credit_card_txns = pd.DataFrame({
    'Date': pd.date_range(start='2025-05-01', periods=10),
    'Merchant': ['Amazon', 'Starbucks', 'Groceries', 'Gas', 'Apple', 'Dining', 'Subscription', 'Uber', 'Coffee', 'Shopping'],
    'Amount': [-80, -6, -150, -40, -10, -60, -20, -25, -8, -100],
    'Category': ['Shopping', 'Dining', 'Groceries', 'Gas', 'Tech', 'Dining', 'Utilities', 'Transport', 'Dining', 'Shopping']
})

# Compute burn rate
rolling_burn = credit_card_txns.copy()
rolling_burn['Rolling 7D Spend'] = rolling_burn['Amount'].rolling(window=7).sum()

# Compute discretionary spend
discretionary_categories = ['Dining', 'Shopping', 'Entertainment', 'Coffee']
credit_card_txns['Discretionary'] = credit_card_txns['Category'].isin(discretionary_categories)

# Header
st.title("\U0001F4B0 Cashflow Telemetry Dashboard")

# Top Panel
st.subheader("\U0001F4C8 Snapshot")
col1, col2, col3 = st.columns(3)
col1.metric("Cash on Hand", f"${cash_on_hand:,.0f}")
col2.metric("Next Payment Due", "Visa - $1200", "May 21")
col3.metric("Runway Estimate", "16 days", "based on avg burn")

# Main Visual - Cashflow Forecast
st.subheader("\U0001F4C6 Cashflow Projection")
dates = pd.date_range(start='2025-05-01', periods=20)
cash_projection = pd.DataFrame({
    'Date': dates,
    'Projected Cash': cash_on_hand + pd.Series([-100 * i for i in range(20)])
})
line_chart = alt.Chart(cash_projection).mark_line(point=True).encode(
    x='Date:T',
    y='Projected Cash:Q',
    tooltip=['Date:T', 'Projected Cash']
).properties(height=250)
st.altair_chart(line_chart, use_container_width=True)

# Upcoming Payments
st.subheader("\u26a0\ufe0f Upcoming Payment Schedule")
st.dataframe(upcoming_payments, use_container_width=True)

# Discretionary Spend
st.subheader("\U0001F7E1 Discretionary Spending Tracker")
filtered_txns = credit_card_txns[credit_card_txns['Discretionary']]
st.dataframe(filtered_txns[['Date', 'Merchant', 'Amount', 'Category']], use_container_width=True)

# Burn Rate
st.subheader("\U0001F525 Rolling Spend Analysis")
burn_chart = alt.Chart(rolling_burn).mark_line().encode(
    x='Date:T',
    y='Rolling 7D Spend:Q'
)
st.altair_chart(burn_chart, use_container_width=True)

st.caption("Stay sharp. Watch your cash. Make informed calls.")
