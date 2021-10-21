<img src="assets\spotify_logo.png" alt="Spotify Logo" width="25" height="25"> Spotify Web Scraper
=======================

Spotify Web Scraper crawls through the Spotify web interface and extracts artist logo information.

## Technology Stack
 - [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) - Parse HTML code
 - [PyMongo](https://api.mongodb.com/python/current/#) - Python MongoDB Driver
 - [Selenium](https://pypi.org/project/selenium/) - Browser Automation Tool

## Dependencies
Install Dependencies with [pip](https://pypi.org/project/pip/)

```
pip install beautifulsoup4
pip install pymongo
pip install selenium
```

Alternatively you can install the requirement.txt
```
pip install -r requirement.txt
```

## Configuration Setup
The scraper will look for **config.py** file at the root with the following parameters to connect to your database

```python
# config.py

DATABASE_CONFIG = {
    'host': 'mongodb://{0}:{1}@MONGODB_HOST/DB_COLLECTION_NAME',
    'dbuser': '', # Database user
    'dbuserpassword': '', # Database password
}
```

## Selenium Chrome Webdriver
Since Spotify webpages are generated dynamically, we need a headless browser to generate the webpages dynamically from the source. I have chosen the Chrome WebDriver which works great in this instance.

Download and save the <a href="http://chromedriver.chromium.org/downloads">Chrome WebDriver</a> at the root level.

## Author
  [Chris Yang](https://chrisyang.io) (ServiceNow Architect, GlideFast)
