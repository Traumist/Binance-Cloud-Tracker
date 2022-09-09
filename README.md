# Binance-Cloud-Tracker
Looks for bullish flips on cloud on Binance USD pairs on either day or weekly timeframes.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required dependencies.

```bash
pip install python-binance
```




## Usage

Edit cloudtracker.py with your api key and api secret. 
Change line 119 to reflect desired timeframe (week or day).

Run file and it will alert you to pairs with bullish TK cross nearing or above cloud.
