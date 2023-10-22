# pricewatch
A way to monitor an item on a website and get notified of the price changes

Add modules to `/readers` directory that can extract the price from a site. See `demo_store.py` as an example.


Usage (__NB__: the example URL may not work anymore):
```shell
$ python main.py 
[2023-10-22 08:04:21.745922] Checking HomeDepot screwdriver set...$29.97
Price has changed!
Demo notifier: 
Price has changed for HomeDepot screwdriver set from $9999 to $29.97. Check it out: https://www.homedepot.com/p/Husky-Screwdriver-Set-15-Piece-246340150/204663546

Send to test@example.com
-----
```
