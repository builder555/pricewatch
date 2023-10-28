# pricewatch
A way to monitor an item on a website and get notified of the price changes

Add modules to `/readers` directory that can extract the price from a site. See `demo_store.py` as an example.

## Prerequisites

* python 3.10+
* pipenv

## Install

```bash
git clone https://github.com/builder555/pricewatch.git
cd pricewatch
PIPENV_VENV_IN_PROJECT=true pipenv install
```

## Set up tokens

Any tokens (e.g. for telegram notifier) need to be placed in `.env` file in the `pricewatch` folder

e.g.:

```.env
TELEGRAM_TOKEN=2223545336:AAAAAAAAAABBBBBBBBBCCCCCCCCCDDDDDDDD
TELEGRAM_CHAT_ID=555555555
```

## Run

Usage (__NB__: the example URL may not work anymore):
```bash
$ PIPENV_VENV_IN_PROJECT=true pipenv shell 
$ python main.py 
```
You should see similar output:

```
[2023-10-22 08:04:21.745922] Checking HomeDepot screwdriver set...$29.97
Price has changed!
Demo notifier: 
Price has changed for HomeDepot screwdriver set from $9999 to $29.97. Check it out: https://www.homedepot.com/p/Husky-Screwdriver-Set-15-Piece-246340150/204663546

Send to test@example.com
-----
```

You can also set up a cronjob to run periodically:

```
0 */4 * * * cd /home/me/pricewatch && /usr/bin/pipenv run start >>log.txt 2>>error.txt
```
