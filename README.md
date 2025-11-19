# Efficient Frontier Modeling Tool

This project uses Pyomo and financial data from Yahoo Finance to build and visualize efficient frontiers.

## Structure
** FOR COLLAB USE, YOU MUST USE
!pip install idaes-pse --pre
!idaes get-extensions --to ./bin
import os
os.environ['PATH'] += ':/content/bin'

AT THE TOP OF THE SCRIPT***

- `main.py`: Entry point for running the model
- `SRC/`: Contains core logic and functions

## How to Use
1. Install dependencies: `pip install -r requirements.txt`
2. Run `main.py` with your chosen tickers and date range

## Example
```python
BDM_Project(['AAPL', 'MSFT', 'NVDA'], '2021-01-01', '2023-01-01')
