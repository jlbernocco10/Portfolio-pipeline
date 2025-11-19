# Efficient Frontier Modeling Tool

This project uses Pyomo and financial data from Yahoo Finance to build and visualize efficient frontiers.

## Structure
FOR COLLAB USE, YOU MUST USE
!pip install idaes-pse --pre
!idaes get-extensions --to ./bin
import os
os.environ['PATH'] += ':/content/bin'
AT THE TOP OF THE SCRIPT
- !git clone 'LINK'
- !pip install -r /content/Portfolio-pipeline/requirements.txt
- from portfolio_pipeline import BDM_Project

## Example
```python
BDM_Project(['AAPL', 'MSFT', 'NVDA'], '2021-01-01', '2023-01-01')
