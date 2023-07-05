# scrape-youtube-channel-videos-url.py
#_*_coding: utf-8_*_

import sys, unittest, time, datetime
import urllib.request, urllib.error, urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException

def getUrls(url):
	# url = sys.argv[1]
	# url = input("Enter the Youtube channel URL: ")
	channelId = url.split('/')[4]
	outputDirectory = "output/"
	driver = webdriver.Firefox()
	#driver = webdriver.Edge()
	# driver = webdriver.Chrome()
	driver.get(url)
	time.sleep(5)
	dt=datetime.datetime.now().strftime("%Y%m%d%H%M")
	height = driver.execute_script("return document.documentElement.scrollHeight")
	lastHeight = 0

	### If you don't have the Youtube cookie pop-up window issue, you can comment the following codes.
	consent_button_xpath = "//button[@aria-label='Reject all']"
	consent = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, consent_button_xpath)))
	consent = driver.find_element_by_xpath(consent_button_xpath)
	consent.click()
	###

	while True:
		if lastHeight == height:
			break
		lastHeight = height
		driver.execute_script("window.scrollTo(0, " + str(height) + ");")
		time.sleep(2)
		height = driver.execute_script("return document.documentElement.scrollHeight")

	userData = driver.find_elements_by_xpath('//*[@id="video-title"]')
	for i in userData:
		print(i.get_attribute('href'))
		link = (i.get_attribute('href'))
		f = open(outputDirectory + channelId+'-'+dt+'.txt', 'a+')
		f.write(link + '\n')
	f.close
	driver.quit()