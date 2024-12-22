# Rocksmith2014 Scrobbler
Scrobble to [last.fm](https://www.last.fm/) while playing Rocksmith 2014.

## Features
1. Scrobble to last.fm while playing Rocksmith 2014's "Learn a Song" game mode.
    * Other modes not tested.
2. Update now playing status on last.fm when starting a song.
3. Edits and replacements are supported.
    * Full tag matching.
    * Individual tag bulk matching with plain text.
    * Individual tag bulk matching with regular expressions.

## Requirements
Python3, [Rocksniffer](https://github.com/kokolihapihvi/RockSniffer), `pylast`, and `selenium` with Firefox or Chrome.

## Usage
1. Start the [Rocksniffer](https://github.com/kokolihapihvi/RockSniffer) application.  Don't open any Rocksniffer HTML files when starting the scrobbler.
2. Edit the `config.py` file with your last.fm information.  You will need to get an [API key](https://www.last.fm/api/account/create).
3. Run `python main.py`.