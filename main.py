from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep, time
import sys
import pylast
import logging
import os
import re
from threading import Thread
sys.path.append(os.path.dirname(sys.executable))
from config import *

class RocksmithScrobbler:
  def __init__(self, network, logger):
    """Constructor"""
    self.logger = logger
    self.logger.info("Starting RocksmithScrobbler.")
    self.sniffer_thread = Thread(target = self.run_sniffer)
    self.sniffer_thread.daemon = True
    self.sniffer_thread.start()

    self.network = network
    try:
      self.driver = webdriver.Firefox()
    except:
      self.driver = webdriver.Chrome()
    self.artist = ""
    self.title = ""
    self.album = ""
    self.listening = False
    self.driver.get(f'file:///{os.path.join(REQUIRED_FIELDS["ROCKSNIFFER_PATH"], r"addons\current_song\current_song.html").replace("\\","/")}')
    self.logger.info("Fetching Rocksniffer HTML file...")
    WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "progress_bar_text")))

  def run_sniffer(self):
    os.system(f'"{os.path.join(REQUIRED_FIELDS["ROCKSNIFFER_PATH"], "RockSniffer.exe")}"')

  def run(self):
    """Start and loop the Scrobbler"""
    self.logger.info("Reading Rocksmith data and waiting to scrobble")
    while True:
      sleep(SLEEP_INTERVAL)
      try:
        self.scrobble_loop()
      except KeyboardInterrupt as e:
        self.logger.critical("KeyboardInterrupt received, closing driver...")
        self.driver.close()
        raise e


  def scrobble_loop(self):
    status = self.song_checkpoint(self.driver.find_element(By.CLASS_NAME, "progress_bar_text").text)
    if status == 1:
      # Start checkpoint
      if (not self.listening) or ((self.title, self.artist, self.album) != self.fetch_data()):
        # Only update now playing if we were not listening to a song before or if the song is different
        # The song could be different if the user hit the start checkpoint, but quit before reaching the end
        self.title, self.artist, self.album = self.fetch_data()
        self.scrobble_now_playing()
      else:
        self.logger.debug("Start checkpoint hit but not scrobbling")
      self.listening = True

    elif status == 2:
      # End checkpoint
      if self.listening and ((self.title, self.artist, self.album) == self.fetch_data()):
        # Only scrobble if the start checkpoint was reached and song data is the same
        # The song data might be different if the user hit the start checkpoint on a different song, quit, selected another song, fast forwarded to the end
        self.scrobble()
      else:
        self.logger.debug("End checkpoint hit but not scrobbling")
      self.listening = False


  def song_checkpoint(self, progress_text: str) -> int:
    """
    Detect if reached a checkpoint in the song
    Return 0 for none, 1 for start of song, 2 for end of song
    """
    if progress_text == "":
      self.logger.debug(f"Progress_text currently not present")
      return False
    current_time = progress_text.split("/")[0]
    total_time = progress_text.split("/")[1]

    current_seconds = int(current_time.split(":")[0]) * 60 + int(current_time.split(":")[1])
    total_seconds = int(total_time.split(":")[0]) * 60 + int(total_time.split(":")[1])
    self.logger.debug(f"Current time: {current_seconds} Total time: {total_seconds}")
    if (total_seconds - current_seconds) <= END_THRESHOLD:
      self.logger.debug("Ending checkpoint reached")
      return 2
    elif abs(current_seconds - START_THRESHOLD) <= 1:
      self.logger.debug("Starting checkpoint reached")
      return 1
    else:
      return 0


  def fetch_data(self) -> (str, str, str):
    """Fetch song data from the Rocksniffer HTML file"""
    artist = self.driver.find_element(By.CLASS_NAME, "artist_name").get_attribute("data-stroke")
    title = self.driver.find_element(By.CLASS_NAME, "song_name").get_attribute("data-stroke")
    album = self.driver.find_element(By.CLASS_NAME, "album_name").get_attribute("data-stroke")
    
    if album != "":
      album = album.split(" (")[0]
    title, artist, album = self.apply_edits(title, artist, album)

    return (title, artist, album)


  def apply_edits(self, title: str, artist: str, album: str) -> (str, str, str):
    """Apply edits to song information based on config.py"""

    # Specific song edits
    if (title, artist, album) in SPECIFIC_SONG_EDITS:
      return SPECIFIC_SONG_EDITS[(title, artist, album)]

    title_done, artist_done, album_done = False, False, False

    # Bulk plain text edits
    if title in BULK_TITLE_EDITS:
      title = BULK_TITLE_EDITS[title]
      title_done = True
    if artist in BULK_ARTIST_EDITS:
      artist = BULK_ARTIST_EDITS[artist]
      artist_done = True
    if album in BULK_ALBUM_EDITS:
      album = BULK_ALBUM_EDITS[album]
      album_done = True
    
    # Bulk regex edits
    if not title_done:
      for pattern in REGEX_BULK_TITLE_EDITS:
        modified = re.sub(pattern, REGEX_BULK_TITLE_EDITS[pattern], title)
        if title != modified:
          title = modified
          title_done = True
          break
    if not artist_done:
      for pattern in REGEX_BULK_ARTIST_EDITS:
        modified = re.sub(pattern, REGEX_BULK_ARTIST_EDITS[pattern], artist)
        if artist != modified:
          artist = modified
          artist_done = True
          break
    if not album_done:
      for pattern in REGEX_BULK_ALBUM_EDITS:
        modified = re.sub(pattern, REGEX_BULK_ALBUM_EDITS[pattern], album)
        if album != modified:
          album = modified
          album_done = True
          break

    return (title, artist, album)

  def clear_data(self):
    """Clear song data"""
    self.artist = ""
    self.title = ""
    self.album = ""
    self.listening = False


  def scrobble(self):
    """Submit a scrobble"""
    self.logger.info(f"Scrobbling: {self.title}, {self.artist}, {self.album}")
    if self.album and SCROBBLE_ALBUMS:
      self.network.scrobble(title=self.title, artist=self.artist, album=self.album, timestamp=int(time()))
    else:
      self.network.scrobble(artist=self.artist, title=self.title, timestamp=int(time()))
    self.clear_data()


  def scrobble_now_playing(self):
    """Update now playing"""
    self.logger.info(f"Updating now playing: {self.title}, {self.artist}, {self.album}")
    if self.album and SCROBBLE_ALBUMS:
      self.network.update_now_playing(title=self.title, artist=self.artist, album=self.album)
    else:
      self.network.update_now_playing(artist=self.artist, title=self.title)


if __name__ == "__main__":
  # Create logger
  logging.basicConfig(
    level = logging.INFO,
    format = "[%(levelname)s] %(message)s"
    )
  logger = logging.getLogger(__name__)

  # Ensure all required fields are present before continuing
  required_fields_present = True
  for key in REQUIRED_FIELDS:
    if not REQUIRED_FIELDS[key]:
      logger.error(f"Missing required field: {key}")
      required_fields_present = False
  if not required_fields_present:
    logger.critical("There are missing required fields.  Please edit config.py and fill out the required fields.")
    sys.exit()

  # Start Pylast
  # In order to perform a write operation you need to authenticate yourself
  password_hash = pylast.md5(REQUIRED_FIELDS["LAST_FM_PASSWORD"])
  network = pylast.LastFMNetwork(
      api_key = REQUIRED_FIELDS["LAST_FM_API_KEY"],
      api_secret = REQUIRED_FIELDS["LAST_FM_API_SECRET"],
      username = REQUIRED_FIELDS["LAST_FM_USERNAME"],
      password_hash = password_hash,
  )

  # Run scrobbler
  scrobbler = RocksmithScrobbler(network, logger)
  scrobbler.run()
