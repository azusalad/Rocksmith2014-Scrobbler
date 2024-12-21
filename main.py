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
    self.driver.get(REQUIRED_FIELDS["CURRENT_SONG_HTML"])
    self.logger.info("Fetching Rocksniffer HTML file...")
    WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "progress_bar_text")))

  def run(self):
    self.logger.info("Reading Rocksmith data and waiting to scrobble")
    while True:
      try:
        self.scrobble_loop()
      except KeyboardInterrupt as e:
        self.logger.critical("KeyboardInterrupt received, closing driver...")
        self.driver.close()
        raise e
  
  def scrobble_loop(self):
    if self.end_of_song(self.driver.find_element(By.CLASS_NAME, "progress_bar_text").text):
      self.artist = self.driver.find_element(By.CLASS_NAME, "artist_name").get_attribute("data-stroke")
      self.title = self.driver.find_element(By.CLASS_NAME, "song_name").get_attribute("data-stroke")
      self.album = self.driver.find_element(By.CLASS_NAME, "album_name").get_attribute("data-stroke")
      if self.album != "":
        self.album = self.album.split(" (")[0]

      if self.artist in ARTIST_EDITS:
        self.artist = ARTIST_EDITS[self.artist]
      if self.title in TITLE_EDITS:
        self.title = TITLE_EDITS[self.title]
      if self.album in ALBUM_EDITS:
        self.album = ALBUM_EDITS[self.album]

      self.scrobble()
    sleep(SLEEP_INTERVAL)

  def end_of_song(self, progress_text: str) -> bool:
    if progress_text == "":
      self.logger.debug(f"Progress_text currently not present")
      return False
    current_time = progress_text.split("/")[0]
    total_time = progress_text.split("/")[1]

    current_seconds = int(current_time.split(":")[0]) * 60 + int(current_time.split(":")[1])
    total_seconds = int(total_time.split(":")[0]) * 60 + int(total_time.split(":")[1])
    self.logger.debug(f"Current time: {current_seconds} Total time: {total_seconds}")
    return (total_seconds - current_seconds) <= END_THRESHOLD

  def clear_data(self):
    self.artist = ""
    self.title = ""
    self.album = ""

  def scrobble(self):
    self.logger.info(f"Scrobbling: {self.title}, {self.artist}, {self.album}")
    if self.album:
      self.network.scrobble(title=self.title, artist=self.artist, album=self.album, timestamp=int(time()))
    else:
      self.network.scrobble(artist=self.artist, title=self.title, timestamp=int(time()))
    self.clear_data()
    sleep(SCROBBLE_TIMEOUT)


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
