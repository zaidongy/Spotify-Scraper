from pymongo import MongoClient
from bs4 import BeautifulSoup
from splinter import Browser
from time import sleep
from random import randint
from selenium import webdriver
import config
import re

# MongoDB Configuration Setup
dbuser = config.DATABASE_CONFIG['dbuser']
dbuserpassword = config.DATABASE_CONFIG['dbuserpassword']
client = MongoClient(config.DATABASE_CONFIG['host'].format(dbuser, dbuserpassword))

# Connect to the 'artistlogo' Database and the 'logo' collection
db = client.artistlogo
logos = db.logo

# Setup Selenium Chrome Driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe', chrome_options=chrome_options)


# Set an initial artist seed, I've used my favorite artist Giuseppe Ottaviani
seed = "/artist/478tAnskSff0wa0XxnpwmW"

# main will handling the loop and crawling logic
def main(startingArtist):
    artistLinks = [startingArtist]
    alreadySearched = [startingArtist]
    while(len(artistLinks) > 0):
        currentArtist = artistLinks.pop(0)
        additionalLinks = scrapArtist(currentArtist)
        alreadySearched.append(currentArtist)
        for link in additionalLinks:
            if link not in alreadySearched:
                artistLinks.append(link)
        # artistLinks = list(set(artistLinks + additionalLinks))
        #print(artistLinks)
        
        #randomly sleep between 2-4 seconds to not abuse the server
        sleep(randint(1,2))

# ScrapArtist will handle logic to parse html and collect data for a particular artist
def scrapArtist(artistLink):
    driver.get("https://open.spotify.com" + artistLink + "/related")

    # Scroll down to generate all content
    SCROLL_PAUSE_TIME = 0.5
    SCROLL_LENGTH = 200
    page_height = int(driver.execute_script("return document.body.scrollHeight"))
    scrollPosition = 0
    while scrollPosition < page_height:
        scrollPosition = scrollPosition + SCROLL_LENGTH
        driver.execute_script("window.scrollTo(0, " + str(scrollPosition) + ");")
        sleep(SCROLL_PAUSE_TIME)

    
    response = driver.find_element_by_class_name('related-artists').get_attribute('innerHTML')

    # print(response)
    # sleep(50)
    nextLinksToCrawl = []

    html_soup = BeautifulSoup(response, 'html.parser')
    artist_container = html_soup.find_all('div', attrs={'class': 'media-object mo-artist'})
    for el in artist_container:
        rawStyle = el.find('div', {'class': 'cover-art-image cover-art-image-loaded'})['style']
        artistLogo = re.findall('"([^"]*)"', rawStyle)[0]
        artistName = el.find('a', {'class': 'mo-info-name'})['title']
        artistLink = el.find('a', {'class': 'mo-info-name'})['href']

        print(artistName, artistLogo, artistLink)
        # sleep(1)

        duplicate = logos.find_one({'logo': artistLogo})
        if(duplicate == None):
            entry = {
                'artist': artistName,
                'logo': artistLogo,
                'link': artistLink
            }
            logos.insert_one(entry)
            print("Scraped {0}".format(artistName))
        else:
            print("{0} already in the Database".format(artistName))

        nextLinksToCrawl.append(artistLink)
    return nextLinksToCrawl


# run the main loop
main(seed)
driver.quit()
