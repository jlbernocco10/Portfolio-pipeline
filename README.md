# Stock Porfolio Allocation Modeling
*this project was designed for my Business Decision Modeling graduate class.

This project uses Pyomo and financial data from Yahoo Finance to build and visualize efficient frontiers. All outputs are saved to a file in the local environment called 'BDM_Ouputs'. This model accounts for correlationand covariance of given stocks based on the date range provided. It then conducts a risk sweep and builds and Efficent Frontier to display risk and expected return. It also outputs weighted allocations to each stock.

## Structure
- FOR COLLAB USE, YOU MUST USE AT THE TOP OF THE SCRIPT
  
```python
!pip install idaes-pse --pre
!idaes get-extensions --to ./bin
import os
os.environ['PATH'] += ':/content/bin'
```
- For Cloning:
```python
!git clone 'LINK'
```
```python
!pip install -r /content/Portfolio-pipeline/requirements.txt
```
  
```python
import sys
sys.path.append('/content/Portfolio-pipeline')
from main import BDM_Project
```
## Example
```python
BDM_Project(['AAPL', 'MSFT', 'NVDA'], '2021-01-01', '2023-01-01')
