# Stock Porfolio Allocation Modeling
*This project was designed for my Business Decision Modeling graduate class. THIS IS NOT FINANCIAL ADVICE, just simple data analyses with python.

This project uses Pyomo and financial data from Yahoo Finance to build and visualize efficient frontiers. All outputs are saved to a file in the local environment called 'BDM_Ouputs'. This model accounts for correlation and covariance of given stocks based on the date range provided. It then conducts a risk sweep and builds an Efficent Frontier to display risk and expected return. It also outputs weighted allocations for each stock.

## Table of Contents
- Structure
- Example
- Navigating Function Outputs
- Error Handeling

## Structure
- FOR GOOGLE COLAB USE, YOU MUST USE THIS AT THE TOP OF THE SCRIPT:
  
```python
#This ensures the proper solvers are loaded for the main function
!pip install idaes-pse --pre
!idaes get-extensions --to ./bin
import os
os.environ['PATH'] += ':/content/bin'
```
- For Cloning:
```python
!git clone 'PASTE-REPOSITORY-LINK-HERE'
```
```python
#This installs the necessary packages for the main function to run
!pip install -r /content/Portfolio-pipeline/requirements.txt
```
  
```python
#This adjusts the file to work in a google colab environment
import sys
sys.path.append('/content/Portfolio-pipeline')
from main import BDM_Project
```
## Example of a Diversified Portfolio for Testing
```python
BDM_Project([
    "AAPL",  # Apple - Technology
    "MSFT",  # Microsoft - Technology
    "NVDA",  # NVIDIA - Semiconductors
    "JNJ",   # Johnson & Johnson - Healthcare
    "PFE",   # Pfizer - Healthcare
    "JPM",   # JPMorgan Chase - Financials
    "GS",    # Goldman Sachs - Financials
    "AMZN",  # Amazon - Consumer Discretionary
    "TSLA",  # Tesla - Consumer Discretionary
    "PG",    # Procter & Gamble - Consumer Staples
    "KO",    # Coca-Cola - Consumer Staples
    "CAT",   # Caterpillar - Industrials
    "BA",    # Boeing - Industrials
    "XOM",   # ExxonMobil - Energy
    "NEE"    # NextEra Energy - Utilities
]
, '2021-01-01', '2023-01-01')
```
## Navigating Function Outputs
- All outputs will be stored here: '/content/BDM_Outputs'
- 3 recommendations for Stock Allocations will be generated: A High Risk, Conservative, and Balanced Portfolio. Found here: /content/BDM_Outputs/alloc_balanced.png, /content/BDM_Outputs/alloc_conservative.png, /content/BDM_Outputs/alloc_highrisk.png
- The Efficient Frontier (/content/BDM_Outputs/efficient_frontier.png) shows Risk vs Expected Return and is used to determien the portfolio options above. Also Available is an efficient frontier with the baseline of a 100% investment in the S&P 500.
- Other outputs are all the raw data used to calculate the outputs above and can be examined for a further deep dive into the individual stock data.

## Error Handeling
The most likely error to occur is with your ticker selection and date range. If your ticker does not have data for a given date range, it will not output. Other potential errors may result from infeasible solutions based on the stocks selected and the calculated risk. I reccomend using at least 5 tickers and starting with a recent date range (i.e. 1-5 years). Note: the "Example" above works and is a good starting point.
