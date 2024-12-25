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

`pip install -r requirements.txt`

If you are using the pre built binary, you just need Rocksniffer and Firefox or Chrome.

## Usage

### From Source (preferred)
1. Install the [Rocksniffer](https://github.com/kokolihapihvi/RockSniffer) application.  Don't open any Rocksniffer HTML files when starting the scrobbler.
2. Edit the `config.py` file with your last.fm information and location of the Rocksniffer folder.  You will need to get a last.fm [API key](https://www.last.fm/api/account/create).
3. Run `python main.py`.  The scrobbler will automatically start the Rocksniffer application.

### From Binary
1. Acquire the binary from the [releases](https://github.com/azusalad/Rocksmith2014-Scrobbler/releases) page.
2. Install the [Rocksniffer](https://github.com/kokolihapihvi/RockSniffer) application.  Don't open any Rocksniffer HTML files when starting the scrobbler.
3. Extract the zip file.  Edit the `config.py` file with your last.fm information and location of the Rocksniffer folder.  You will need to get a last.fm [API key](https://www.last.fm/api/account/create).
4. Run `.\RocksmithScrobbler.exe` from a terminal.  The scrobbler will automatically start the Rocksniffer application.

### Autostart with Steam

You can have the scrobbler run automatically when the game is launched by modifying the launch options on Steam.  The launch options would be something like:

```
"path\to\your\script.bat" %command%
```

Where the `.bat` file is a custom script containing something like:

```
start "python path\to\rocksmith\scrobbler\main.py"
%1
```

This batch file asynchronously starts the scrobbler, then starts the game with `%1`