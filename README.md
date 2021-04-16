# WFMarketPriceGaps
Simple Python script to check price gaps between sets and individual items on warframe.market

## Usage
Run the script using `py wfmarket.py`

Requires Python 3 (I think, haven't tested with Python 2)

## Known issues
### It's slow
Can't do much about this, the request rate is limited on purpose to comply with warframe.market ToS
### It returns false data for sets with duplicates of the same item (eg. Dual Kamas Prime)
Warframe market API has no info about duplicates when checking set data (as far as i know). Once I learn about a simple way to check for this data, I will fix this
