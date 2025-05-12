import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# --- Mock Data Setup ---
today = datetime.today()
dates = pd.date_range(start=today, periods=30)
incomes = pd.DataFrame({
    'Date': [today + timedelta(days=5), today + timedelta(days=12)],
    'Amount': [1500, 1200],
    'Type': ['Income', 'Income']
})

expenses = pd.DataFrame({
    'Date': [today + timedelta(days=6), today + timedelta(days=15), today + timedelta(days=20), today + timedelta(days=25)],
    'Amount': [-1200, -1000, -500, -300],
    'Type': ['Expense']*4
})

transactions = pd.concat([incomes, expenses])
transactions = transactions.sort_values(by='Date')

cash_start = 3200
transactions['Cumulative Cash'] = cash_start + transactions['Amount'].cumsum()

# --- Top Metrics ---
st.title("\U0001F4B8 Modern Cashflow Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Cash on Hand", "$3,200")
col2.metric("Days Until Cash Out", "16")
col3.metric("Payments Due", "3")

# --- Projected Cash Flow Chart ---
st.subheader("Projected Cash Balance")
df_plot = pd.merge(pd.DataFrame({'Date': dates}), transactions, on='Date', how='left').fillna(0)
df_plot['Cumulative Cash'] = cash_start + df_plot['Amount'].cumsum()
df_plot['Inflow'] = df_plot['Amount'].apply(lambda x: x if x > 0 else 0)
df_plot['Outflow'] = df_plot['Amount'].apply(lambda x: x if x < 0 else 0)

line = alt.Chart(df_plot).mark_line(color="#2c7be5", point=True).encode(
    x='Date:T',
    y='Cumulative Cash:Q',
    tooltip=['Date:T', 'Cumulative Cash']
)

bars = alt.Chart(df_plot).mark_bar().encode(
    x='Date:T',
    y=alt.Y('Inflow:Q', title=''),
    color=alt.value('#4caf50'),
    tooltip=['Date:T', 'Inflow']
)

bars2 = alt.Chart(df_plot).mark_bar().encode(
    x='Date:T',
    y='Outflow:Q',
    color=alt.value('#f44336'),
    tooltip=['Date:T', 'Outflow']
)

chart = (line + bars + bars2).properties(height=300)
st.altair_chart(chart, use_container_width=True)

# --- Alerts ---
st.subheader("\u26a0\ufe0f Alerts")
if df_plot['Cumulative Cash'].min() < 0:
    st.error("Insufficient funds projected. Consider deferring or cutting expenses.")

# --- Recent Transactions ---
st.subheader("Recent Transactions")
recent_txns = transactions.copy()
recent_txns['Date'] = recent_txns['Date'].dt.strftime('%b %d')
recent_txns['Amount'] = recent_txns['Amount'].apply(lambda x: f"${abs(x):,.0f}" if x < 0 else f"+${x:,.0f}")
recent_txns['Category'] = recent_txns['Type'].apply(lambda x: "Discretionary" if x == 'Expense' else "Income")
st.dataframe(recent_txns[['Date', 'Type', 'Amount', 'Category']], use_container_width=True)

st.caption("Built for clarity, speed, and financial control.")
