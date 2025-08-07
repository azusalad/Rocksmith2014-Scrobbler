# ---------------------------------------
# Required fields
# ---------------------------------------
REQUIRED_FIELDS = {
  # Path to the Rocksniffer directory.
  # Keep the r before the quotes since literal string.
  # Example below:
  # "ROCKSNIFFER_PATH": r"C:\Path\To\RockSniffer.0.5.0",
  "ROCKSNIFFER_PATH": r"",

  # ---------------------------------------
  # last.fm information
  # ---------------------------------------

  "LAST_FM_USERNAME": "",
  "LAST_FM_PASSWORD": "",
  # You have to have your own unique two values for API_KEY and API_SECRET
  # Obtain yours from https://www.last.fm/api/account/create for Last.fm
  "LAST_FM_API_KEY": "",
  "LAST_FM_API_SECRET": "",
}

# ---------------------------------------
# Replacement/Edits
# ---------------------------------------
# Match all tags with plain text before replacing
SPECIFIC_SONG_EDITS = {
  # (original title, original artist, original album): (modified title, modified artist, modified album)
  # Album can be omitted on both sides: (original title, original artist): (modified title, modified artist)
  # Example below
  ('Don\'t Say "Lazy"', "Houkago Tea Time", 'Don\'t Say "Lazy"'): ('Don\'t Say "Lazy" (From "K-On!")', "Sakurakou K-ON Bu", 'Don\'t Say "Lazy" (From "K-On!)'),
}

# Match individual tags with plain text
BULK_ARTIST_EDITS = {
  # original artist: modified artist
  # Example below
  "Rosé (ft. Bruno Mars)": "Rosé",
}
BULK_TITLE_EDITS = {}
BULK_ALBUM_EDITS = {}

# Match individual tags with regular expressions
REGEX_BULK_ARTIST_EDITS = {
  # find: replace
  # Example below
  r"(.+) \(ft\..+": r"\1",
}
REGEX_BULK_TITLE_EDITS = {}
REGEX_BULK_ALBUM_EDITS = {}

# Whether to scrobble albums or not
# Consider setting this to False if you play a lot of CDLC.
SCROBBLE_ALBUMS = False

# ---------------------------------------
# Probably don't want to change the values below
# ---------------------------------------
# Submit scrobble when this many seconds away from the end of the song
END_THRESHOLD = 2
# Submit now playing when this many seconds away from the start of the song
START_THRESHOLD = 15
# Interval time in seconds between checking song duration
SLEEP_INTERVAL = 1
