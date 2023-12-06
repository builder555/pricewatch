## Website price readers

Usage:
```python
>>> from readers import demo_store
>>> demo_store.get_price('https://www.homedepot.com/p/Milwaukee-M12-12-Volt-Lithium-Ion-2-0-Ah-Compact-Battery-Pack-48-11-2420/203806660')
64.97
```

In order to use the notifier in the main code, it needs to be imported in main.py and used in notify() function

```python
async def notify(msg: str):
    await my_notifier.notify(msg)
```