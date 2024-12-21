# Rocksmith2014 Scrobbler
Scrobble to last.fm while playing Rocksmith 2014.

## Requirements
Python3, [Rocksniffer](https://github.com/kokolihapihvi/RockSniffer), `pylast`, and `selenium` with Firefox or Chrome.

## Usage
1. Start the [Rocksniffer](https://github.com/kokolihapihvi/RockSniffer) application.  Don't open any Rocksniffer HTML files when starting the scrobbler.
2. Edit the `config.py` file with your last.fm information.  You will need to get an [API key](https://www.last.fm/api/account/create).
3. Run `python main.py`.