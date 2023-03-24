import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time

PROMISED_DOWN = 150
PROMISED_UP = 10
TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")
chrome_driver_path = "/Users/hadikassamali/Development/chromedriver"
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"


class InternetSpeedTwitterBot:
  def __init__(self, chrome_driver_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    service = ChromeService(executable_path=chrome_driver_path)
    self.driver = webdriver.Chrome(service=service, options=chrome_options, desired_capabilities=caps)
    self.down = 0
    self.up = 0

  def get_internet_speed(self, url):
    self.driver.get(url)
    time.sleep(3)
    start_button = self.driver.find_element(By.CSS_SELECTOR, ".start-text")
    start_button.click()
    time.sleep(60)
    dismiss_button = self.driver.find_element(By.LINK_TEXT, 'Back to test results')
    dismiss_button.click()
    time.sleep(3)
    self.down = float(self.driver.find_element(By.CSS_SELECTOR, 'span[class="result-data-large number result-data-value download-speed"]').text)
    self.up = float(self.driver.find_element(By.CSS_SELECTOR, 'span[class="result-data-large number result-data-value upload-speed"]').text)

  def tweet_at_provider(self, url):
    tweet = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up\n" \
            f"when I pay for {PROMISED_DOWN}down/{PROMISED_UP}/up"
    tweet_area_xpath = '//div[@data-contents]'
    tweet_btn_xpath = '//div[@data-testid="tweetButtonInline"]'

    self.driver.get(url)
    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "text")))
    log_in = self.driver.find_element(By.NAME, 'text')
    log_in.send_keys(TWITTER_EMAIL)
    log_in.send_keys(Keys.ENTER)

    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "password")))
    password = self.driver.find_element(By.NAME, "password")
    password.send_keys(TWITTER_PASSWORD)
    password.send_keys(Keys.ENTER)

    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, tweet_area_xpath)))
    tweet_area = self.driver.find_element(By.XPATH, tweet_area_xpath)
    tweet_area.send_keys(tweet)

    tweet_btn = self.driver.find_element(By.XPATH, tweet_btn_xpath)
    tweet_btn.click()



twitter_bot = InternetSpeedTwitterBot(chrome_driver_path)
twitter_bot.get_internet_speed("https://www.speedtest.net/")
time.sleep(5)
twitter_bot.tweet_at_provider("https://twitter.com/i/flow/login")