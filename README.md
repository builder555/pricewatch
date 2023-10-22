# pricewatch
A way to monitor an item on a website and get notified of the price changes

Add modules to `/readers` directory that can extract the price from a site. See `demo_store.py` as an example.

Usage:
```python
>>> from readers import demo_store
>>> demo_store.get_price('https://www.homedepot.com/p/Milwaukee-M12-12-Volt-Lithium-Ion-2-0-Ah-Compact-Battery-Pack-48-11-2420/203806660')
64.97
```
