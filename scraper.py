from pymongo import MongoClient
from bs4 import BeautifulSoup
from requests import get
from splinter import Browser
from time import sleep
from random import randint
import config

# MongoDB Configuration Setup
dbuser = config.DATABASE_CONFIG['dbuser']
dbuserpassword = config.DATABASE_CONFIG['dbuserpassword']
client = MongoClient(config.DATABASE_CONFIG['host'].format(dbuser, dbuserpassword))

# Connect to the 'artistlogo' Database and the 'logo' collection
db = client.artistlogo
logos = db.logo

# Set an initial artist seed, I've used my favorite artist Giuseppe Ottaviani
seed = "/artist/5B9q1NRokzWYB7nSgnlHyv"

# main will handling the loop and crawling logic
def main(startingArtist):
    artistLinks = [startingArtist]
    while(len(artistLinks) > 0):
        additionalLinks = scrapArtist(artistLinks.pop(-1)) #
        artistLinks = artistLinks + additionalLinks
        #print(artistLinks)
        
        #randomly sleep between 2-4 seconds to not abuse the server
        sleep(randint(2,4))

# ScrapArtist will handle logic to parse html and collect data for a particular artist
def scrapArtist(artistLink):
    response = get("https://open.spotify.com" + artistLink)
    nextLinksToCrawl = []

    html_soup = BeautifulSoup(response.text, 'html.parser')
    artist_container = html_soup.find_all('li')
    for el in artist_container:
        artistTag = el.find_all('a', attrs={'class':'cover artist'})
        for artist in artistTag:
            entry = {
                'artist': artist['alt'],
                'logo': artist.div['data-src']
            }
            duplicate = logos.find_one({'logo': artist.div['data-src']})
            if(duplicate == None):
                logos.insert_one(entry)
                print("Scraped {0}".format(artist['alt']))
            else:
                print("{0} already in the Database".format(artist['alt']))

            nextLinksToCrawl.append(artist['href'])
            sleep(1)
    return nextLinksToCrawl


# run the main loop
main(seed)
