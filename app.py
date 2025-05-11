import streamlit as st
import pandas as pd
import datetime
import altair as alt

st.set_page_config(layout="wide")

# Mock Data
cash_flow_data = pd.DataFrame({
    'date': pd.date_range(start='2025-05-01', end='2025-05-31'),
    'inflow': [300 if i % 5 != 0 else 0 for i in range(31)],
    'outflow': [200 if i % 7 == 0 else 0 for i in range(31)]
})
cash_flow_data['net'] = cash_flow_data['inflow'] - cash_flow_data['outflow']
cash_flow_data['cumulative_cash'] = cash_flow_data['net'].cumsum()

transactions = pd.DataFrame({
    'date': ['2025-05-10', '2025-05-15', '2025-05-18', '2025-05-25'],
    'description': ['Rent', 'Utilities', 'Insurance', 'Credit Card'],
    'amount': [-1200, -180, -150, -300],
    'defer': [False, True, True, False]
})

net_worth_data = pd.DataFrame({
    'year': ['2021', '2022', '2023', '2024', '2025'],
    'Cash': [500, 1000, 1200, 1500, 1700],
    'Investments': [1000, 1200, 1400, 1600, 2000],
    'Real Estate': [300, 600, 900, 1200, 1600],
    'Other': [200, 250, 300, 350, 400]
})

# Layout
st.title("🏛️ Financial Telemetry Dashboard")

col1, col2 = st.columns([2, 1])

# 1. Cumulative Cash Flow Line Chart + Transactions
with col1:
    st.subheader("🔢 Cumulative Cash Flow")
    line_chart = alt.Chart(cash_flow_data).mark_line(point=True).encode(
        x='date:T',
        y='cumulative_cash:Q',
        tooltip=['date:T', 'cumulative_cash']
    ).properties(height=250)
    st.altair_chart(line_chart, use_container_width=True)

    st.subheader("🚨 High-Impact Transactions")
    st.dataframe(transactions, use_container_width=True)

# 2. Cash Buffer Gauge
with col2:
    st.subheader("⛽ Cash Buffer")
    buffer_days = 25  # Static example
    st.metric("Days of Buffer", f"{buffer_days} days")

    trend_data = pd.DataFrame({
        'Day': range(1, 11),
        'Buffer': [25 - i//2 for i in range(10)]
    })
    trend_chart = alt.Chart(trend_data).mark_line().encode(
        x='Day',
        y='Buffer'
    )
    st.altair_chart(trend_chart, use_container_width=True)

# 3. Net Worth
st.subheader("📊 Net Worth Breakdown")
net_worth_melted = net_worth_data.melt('year', var_name='Asset', value_name='Value')
area_chart = alt.Chart(net_worth_melted).mark_area(opacity=0.7).encode(
    x='year:O',
    y='Value:Q',
    color='Asset:N'
).properties(height=300)
st.altair_chart(area_chart, use_container_width=True)

# 4. Variance Analysis
st.subheader("📊 Variance vs Forecast")
forecast_data = pd.DataFrame({
    'Category': ['Income', 'Rent', 'Utilities', 'Insurance'],
    'Forecast': [5000, -1200, -150, -100],
    'Actual': [4800, -1200, -180, -150]
})
forecast_data['Variance'] = forecast_data['Actual'] - forecast_data['Forecast']

bar_chart = alt.Chart(forecast_data).transform_fold(
    ['Forecast', 'Actual'],
    as_=['Type', 'Amount']
).mark_bar().encode(
    x='Category:N',
    y='Amount:Q',
    color='Type:N',
    column='Type:N'
)
st.altair_chart(bar_chart, use_container_width=True)

st.caption("Built for financial clarity and rapid decision-making.")
