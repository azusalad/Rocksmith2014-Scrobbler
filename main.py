from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import *

class RocksmithScrobbler:
  def __init__(self):
    self.driver = webdriver.Firefox()
    self.artist = ""
    self.title = ""
    self.album = ""

    driver.get(CURRENT_SONG_HTML)
