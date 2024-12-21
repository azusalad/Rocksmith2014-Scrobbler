from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

from config import *

class RocksmithScrobbler:
  def __init__(self):
    self.driver = webdriver.Firefox()
    self.artist = ""
    self.title = ""
    self.album = ""
    driver.get(CURRENT_SONG_HTML)
    sleep(10)  # TODO: Replace this with a WebDriverWait

  def run(self):
    # TODO: Add scrobbler connection here
    self.scrobble_loop()
  
  def scrobble_loop(self):
    if self.end_of_song(driver.find_element(By.CLASS_NAME, "progress_bar_text").text):
      self.artist = driver.find_element(By.CLASS_NAME, "artist_name").get_attribute("data-stroke")
      self.title = driver.find_element(By.CLASS_NAME, "song_name").get_attribute("data-stroke")
      self.album = driver.find_element(By.CLASS_NAME, "album_name").get_attribute("data-stroke")
      self.scrobble()
    sleep(SLEEP_INTERVAL)

  def end_of_song(self, progress_text: str) -> bool:
    current_time = progress.split("/")[0]
    total_time = progress.split("/")[1]

    current_seconds = int(current_time.split(":")[0]) * 60 + int(current_time.split(":")[1])
    total_seconds = int(total_time.split(":")[0]) * 60 + int(total_time.split(":")[1])
    return (total_seconds - current_seconds) <= END_THRESHOLD

  def clear_data(self):
    self.artist = ""
    self.title = ""
    self.album = ""

  def scrobble(self):
    # TODO: Scrobble to last.fm
    self.clear_data()
    sleep(SCROBBLE_TIMEOUT)
    pass


if __name__ == "__main__":
  scrobbler = RocksmithScrobbler()
  scrobbler.run()
