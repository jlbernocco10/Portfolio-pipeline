# Stock Porfolio Allocation Modeling
*this project was designed for my Business Decision Modeling graduate class.

This project uses Pyomo and financial data from Yahoo Finance to build and visualize efficient frontiers. All outputs are saved to a file in the local environment called 'BDM_Ouputs'. This model accounts for correlation and covariance of given stocks based on the date range provided. It then conducts a risk sweep and builds an Efficent Frontier to display risk and expected return. It also outputs weighted allocations for each stock.

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
## Example of a diversified Portfolio for testing
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
