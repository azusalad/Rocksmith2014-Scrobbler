from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep, time
import pylast
import logging

from config import *

class RocksmithScrobbler:
  def __init__(self, network, logger):
    """Constructor"""
    self.logger = logger
    self.logger.info("Starting RocksmithScrobbler.  Please ensure that Rocksniffer is already running.")

    self.network = network
    try:
      self.driver = webdriver.Firefox()
    except:
      self.driver = webdriver.Chrome()
    self.artist = ""
    self.title = ""
    self.album = ""
    self.listening = False
    self.driver.get(REQUIRED_FIELDS["CURRENT_SONG_HTML"])
    self.logger.info("Fetching Rocksniffer HTML file...")
    WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "progress_bar_text")))


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

    if artist in ARTIST_EDITS:
      artist = ARTIST_EDITS[artist]
    if title in TITLE_EDITS:
      title = TITLE_EDITS[title]
    if album in ALBUM_EDITS:
      album = ALBUM_EDITS[album]
    
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
    if self.album:
      self.network.scrobble(title=self.title, artist=self.artist, album=self.album, timestamp=int(time()))
    else:
      self.network.scrobble(artist=self.artist, title=self.title, timestamp=int(time()))
    self.clear_data()


  def scrobble_now_playing(self):
    """Update now playing"""
    self.logger.info(f"Updating now playing: {self.title}, {self.artist}, {self.album}")
    if self.album:
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
    exit()

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
