from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import pylast
import webbrowser

from config import *

class RocksmithScrobbler:
  def __init__(self, network):
    print("Starting RocksmithScrobbler")
    self.network = network
    self.driver = webdriver.Firefox()
    self.artist = ""
    self.title = ""
    self.album = ""
    self.driver.get(CURRENT_SONG_HTML)
    print("Fetched Rocksniffer HTML file")
    sleep(10)  # TODO: Replace this with a WebDriverWait

  def run(self):
    self.scrobble_loop()
  
  def scrobble_loop(self):
    if self.end_of_song(self.driver.find_element(By.CLASS_NAME, "progress_bar_text").text):
      self.artist = self.driver.find_element(By.CLASS_NAME, "artist_name").get_attribute("data-stroke")
      self.title = self.driver.find_element(By.CLASS_NAME, "song_name").get_attribute("data-stroke")
      self.album = self.driver.find_element(By.CLASS_NAME, "album_name").get_attribute("data-stroke")
      self.scrobble()
    sleep(SLEEP_INTERVAL)

  def end_of_song(self, progress_text: str) -> bool:
    current_time = progress.split("/")[0]
    total_time = progress.split("/")[1]

    current_seconds = int(current_time.split(":")[0]) * 60 + int(current_time.split(":")[1])
    total_seconds = int(total_time.split(":")[0]) * 60 + int(total_time.split(":")[1])
    print(f"Current time: {current_seconds} Total time: {total_seconds}")
    return (total_seconds - current_seconds) <= END_THRESHOLD

  def clear_data(self):
    self.artist = ""
    self.title = ""
    self.album = ""

  def scrobble(self):
    # TODO: Scrobble to last.fm
    print(f"Scrobbling: {self.artist}, {self.album}, {self.title}")
    self.clear_data()
    sleep(SCROBBLE_TIMEOUT)


if __name__ == "__main__":
  # Start Pylast
  # In order to perform a write operation you need to authenticate yourself
  password_hash = pylast.md5(LAST_FM_PASSWORD)
  network = pylast.LastFMNetwork(
      api_key=LAST_FM_API_KEY,
      api_secret=LAST_FM_API_SECRET,
      username=LAST_FM_USERNAME,
      password_hash=password_hash,
  )

  scrobbler = RocksmithScrobbler(network)
  scrobbler.run()
