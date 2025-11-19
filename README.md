# Efficient Frontier Modeling Tool

This project uses Pyomo and financial data from Yahoo Finance to build and visualize efficient frontiers.

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
