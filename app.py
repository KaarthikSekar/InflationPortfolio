import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Inflation vs Portfolio", layout="wide")

# ── Load Data ─────────────────────────────────────────────
@st.cache_data
def load_data():
    prices = pd.read_csv('stock_prices.csv', parse_dates=['Date'], index_col='Date')
    cpi = pd.read_csv('cpi_data.csv', parse_dates=['observation_date'], index_col='observation_date')
    cpi.columns = ['CPI']
    cpi = cpi['2019-01-01':'2024-12-31']

    # Forward fill
    full_idx = pd.date_range(prices.index.min(), prices.index.max(), freq='D')
    prices = prices.reindex(full_idx).ffill()
    cpi_daily = cpi.reindex(prices.index, method='ffill')

    # Returns
    simple_returns = prices.pct_change().dropna()
    monthly_prices = prices.resample('MS').first()
    monthly_returns = monthly_prices.pct_change().dropna()

    # Real returns
    cpi_monthly = cpi.resample('MS').first()
    inflation_rate = cpi_monthly.pct_change().dropna()
    inflation_rate.columns = ['inflation']
    combined = monthly_returns.join(inflation_rate, how='inner')

    for col in ['SPY', 'GLD', 'XOM', 'TLT', 'VNQ']:
        combined[f'{col}_real'] = (1 + combined[col]) / (1 + combined['inflation']) - 1

    rolling_vol = simple_returns.rolling(90).std() * np.sqrt(252)

    return prices, simple_returns, monthly_returns, combined, rolling_vol

prices, simple_returns, monthly_returns, combined, rolling_vol = load_data()

# ── Header ────────────────────────────────────────────────
st.title("📈 The Hidden Cost of Inflation on Your Portfolio")
st.markdown("Analyzing 5 assets from **2019 to 2024** — does your portfolio actually beat inflation?")
st.divider()

# ── Sidebar ───────────────────────────────────────────────
st.sidebar.title("⚙️ Settings")
selected = st.sidebar.multiselect("Select Assets", ['SPY', 'GLD', 'XOM', 'TLT', 'VNQ'],
                                   default=['SPY', 'GLD', 'XOM', 'TLT', 'VNQ'])

st.sidebar.markdown("---")
st.sidebar.markdown("**Asset Guide**")
st.sidebar.markdown("SPY = S&P 500")
st.sidebar.markdown("GLD = Gold")
st.sidebar.markdown("XOM = Energy")
st.sidebar.markdown("TLT = Long Bonds")
st.sidebar.markdown("VNQ = Real Estate")

# ── KPI Row ───────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
ann_real = combined[['SPY_real','GLD_real','XOM_real','TLT_real','VNQ_real']].mean() * 12 * 100
k1.metric("SPY Real Return", f"{ann_real['SPY_real']:.1f}%")
k2.metric("GLD Real Return", f"{ann_real['GLD_real']:.1f}%")
k3.metric("XOM Real Return", f"{ann_real['XOM_real']:.1f}%")
k4.metric("TLT Real Return", f"{ann_real['TLT_real']:.1f}%")
k5.metric("VNQ Real Return", f"{ann_real['VNQ_real']:.1f}%")
st.divider()

# ── Section 1: Cumulative Returns ─────────────────────────
st.subheader("📊 Cumulative Returns")

nominal_cum = (1 + monthly_returns[selected]).cumprod() * 100
real_cols = [f'{c}_real' for c in selected]
real_cum = (1 + combined[real_cols]).cumprod() * 100

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(7, 4))
    nominal_cum.plot(ax=ax)
    ax.set_title('Nominal Returns (Base=100)')
    ax.set_ylabel('Portfolio Value')
    st.pyplot(fig)
    plt.close()

with col2:
    fig, ax = plt.subplots(figsize=(7, 4))
    real_cum.plot(ax=ax)
    ax.set_title('Real Returns (Base=100)')
    ax.set_ylabel('Real Portfolio Value')
    st.pyplot(fig)
    plt.close()

st.divider()

# ── Section 2: Inflation Rate ─────────────────────────────
st.subheader("💸 Monthly Inflation Rate")

fig, ax = plt.subplots(figsize=(13, 4))
combined['inflation'].plot(ax=ax, color='salmon')
ax.axhline(0, color='black', lw=0.8, linestyle='--')
ax.set_title('Monthly Inflation Rate (CPI)')
st.pyplot(fig)
plt.close()

st.divider()

# ── Section 3: Rolling Correlation ────────────────────────
st.subheader("🔗 Rolling Correlation vs Inflation")

fig, ax = plt.subplots(figsize=(13, 4))
for col in selected:
    combined[col].rolling(12).corr(combined['inflation']).plot(ax=ax, label=col)
ax.axhline(0, color='black', lw=0.8, linestyle='--')
ax.set_title('12-Month Rolling Correlation: Asset Returns vs Inflation')
ax.legend()
st.pyplot(fig)
plt.close()

st.divider()

# ── Section 4: Rolling Volatility ─────────────────────────
st.subheader("📉 Rolling 90-Day Volatility")

fig, ax = plt.subplots(figsize=(13, 4))
rolling_vol[selected].plot(ax=ax)
ax.axvspan('2020-02-01', '2020-04-01', color='red', alpha=0.15, label='COVID Crash')
ax.set_title('Rolling 90-Day Annualized Volatility')
ax.legend()
st.pyplot(fig)
plt.close()

st.divider()

# ── Section 5: Annualized Real Returns ────────────────────
st.subheader("🏆 Annualized Real Returns")

fig, ax = plt.subplots(figsize=(8, 4))
ann_real_selected = combined[[f'{c}_real' for c in selected]].mean() * 12 * 100
ann_real_selected.index = selected
colors = ['green' if v > 0 else 'red' for v in ann_real_selected]
ann_real_selected.plot(kind='bar', ax=ax, color=colors, edgecolor='white')
ax.axhline(0, color='black', lw=0.8)
ax.set_title('Annualized Real Return (%)')
ax.tick_params(axis='x', rotation=0)
st.pyplot(fig)
plt.close()