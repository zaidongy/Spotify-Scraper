<img src="assets\spotify_logo.png" alt="Spotify Logo" width="50" height="50"> Spotify Web Scraper
=======================

Spotify Web Scraper crawls through the web interface of Spotify and extracts information for different artists

## Dependencies
```cmd

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
  [Chris Yang](https://chrisyang.io) (EIS Systems Analyst, Cedars-Sinai)
