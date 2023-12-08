## Website price readers

Usage:
```python
>>> from readers import demo_store
>>> demo_store.get_price('https://www.homedepot.com/p/Milwaukee-M12-12-Volt-Lithium-Ion-2-0-Ah-Compact-Battery-Pack-48-11-2420/203806660')
64.97
```

To add your own, add a file to this directory, in which you:
* implement a function with this definition: `def get_price(url: str) -> float`
* add variable `SITE='www.yourstore.com'` with the base url of the website for this reader
