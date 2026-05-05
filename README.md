# The Hidden Cost of Inflation on Your Portfolio
 
Can your investments actually beat inflation over time?
 
## Central Question
Does your stock portfolio actually grow your wealth — or does inflation silently eat your gains?
 
## Dataset
- Stock prices: SPY, GLD, XOM, TLT, VNQ (2019–2024) via yfinance
- CPI inflation data: Monthly from Federal Reserve (FRED)
## Project Progress
- [x] Data Collection — stock prices + CPI data
- [x] Data Cleaning — forward fill, frequency alignment
- [x] Feature Engineering — simple, log, monthly, real returns
- [x] EDA — distributions, correlations, rolling volatility
- [x] Deep Insights — cumulative returns, rolling correlation, t-test
- [x] Final Dashboard
## Key Findings
- SPY beat inflation with ~14% annualized real return
- TLT (bonds) lost -4% in real terms — destroyed wealth
- XOM (energy) was the best inflation hedge — not gold
- Gold disappointed as an inflation hedge despite its reputation
- None of the assets proved statistically significant real returns (p > 0.05)
## Tech Stack
Python | pandas | numpy | matplotlib | seaborn | scipy | yfinance
 
## How to Run
1. Install dependencies: `pip install pandas numpy matplotlib seaborn scipy yfinance`
2. Download CPI data from [FRED](https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL)
3. Open `inflation.ipynb` and run all cells