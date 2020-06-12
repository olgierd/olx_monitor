# OLX Monitor

This small script allows you to monitor OLX ads and notify you, whenever a new one gets posted in a specific category / matching your search criteria.

## Configuration

Paste the proper `url` into the source code.

`sleeptime` sets the amount of seconds between checks.

Currently only *Telegram* notifications are supported.

Put your Telegram API token into line 1 and chat ID into line 2 of `secrets.txt`.

## Usage

`./monitor.py`


## How does it work?

The script uses `requests` and `bs4` to fetch & parse raw HTML page and extract information about the latest ads. Whenever a new one is detected, a notification function is triggered.
