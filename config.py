# ---------------------------------------
# Required fields
# ---------------------------------------
REQUIRED_FIELDS = {
  # Path to the Rocksniffer current_song html file
  # Example: file:///C:/RockSniffer.0.5.0/addons/current_song/current_song.html
  "CURRENT_SONG_HTML": "",

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
# The key is the exact text you want to find
# The value is the exact text you want to replace it with
# Example:
#   "Rosé (ft. Bruno Mars)": "Rosé",
ARTIST_EDITS = {
  # Example: "Rosé (ft. Bruno Mars)": "Rosé",
}
TITLE_EDITS = {}
ALBUM_EDITS = {}

# ---------------------------------------
# Probably don't want to change the values below
# ---------------------------------------

# Submit scrobble when this many seconds away from the end of the song
END_THRESHOLD = 2
# Submit now playing when this many seconds away from the start of the song
START_THRESHOLD = 15
# Interval time in seconds between checking song duration
SLEEP_INTERVAL = 1
