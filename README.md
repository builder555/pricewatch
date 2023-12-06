# pricewatch
A way to monitor an item on a website and get notified of the price changes

Add modules to `/readers` directory that can extract the price from a site. See `demo_store.py` as an example.

## Running

Clone the repo:

```bash
git clone https://github.com/builder555/pricewatch.git
cd pricewatch
```

## Docker

Put tokens in `.env` file.

e.g. for telegram notifier:

```.env
TELEGRAM_TOKEN=2223545336:AAAAAAAAAABBBBBBBBBCCCCCCCCCDDDDDDDD
TELEGRAM_CHAT_ID=555555555
```

Modify `items.json` as needed - add whichever items you want to monitor, follow the example provided in the file.

Run it using docker compose:

```bash
docker compose up -d
```

For development, you should use `compose-dev.yml`:

```bash
docker compose -f compose-dev.yml up -d --build
```

Open [http://localhost:8700/][http://localhost:8700/] (assuming you didn't override the port) to view the UI.

## Stand-alone

### Prerequisites

* python 3.10+
* pipenv

### Install

```bash
PIPENV_VENV_IN_PROJECT=true pipenv install
```

### Set up tokens

Any tokens (e.g. for telegram notifier) need to be placed in `.env` file in the `pricewatch` folder

e.g.:

```.env
TELEGRAM_TOKEN=2223545336:AAAAAAAAAABBBBBBBBBCCCCCCCCCDDDDDDDD
TELEGRAM_CHAT_ID=555555555
```

### Run

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
