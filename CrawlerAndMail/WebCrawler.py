# Import required packages
import requests
from bs4 import BeautifulSoup
import time
from CrawlerAndMail import ConfigReader


# Create stand variable for later putting the date in the email's Subject
date = ""


# Create Crawler class
class Crawler:

    # Returns the ceawled page after logging into it
    def get_soup(self):
        with requests.session() as s:
            login_data = {"username": ConfigReader.elternportal_email,
                          "password": ConfigReader.elternportal_password}

            time.sleep(0.5)
            r = s.get(ConfigReader.url)
            r = s.post(ConfigReader.post_url, data=login_data)
            r = s.get(ConfigReader.end_url)
            soup = BeautifulSoup(r.text, "html.parser")

        return soup

    # Returns the main_table from get_soup
    def get_entire_table(self):
        umbruch = 0
        soup = f.get_soup()
        fin = []

        for line in soup.find("div", attrs={"class": "main_center"}):
            # Add a Space in the table for ascetics
            if "KW" in str(line) and umbruch == 1:
                fin.append('<table class="table" style="min-width: 75%;"><tbody><tr class=""><td width="100%" '
                           'colspan="6" align="center" valign="top"><br></td></tr></tbody></table>')

            # Set date in the Stand variable
            if "Stand" in str(line):
                global date
                date = line.text

            umbruch = 1
            fin.append(str(line))

        # Pop the useless stuff like the date and the rest contained in the main table
        fin.pop()
        fin.pop()
        vaulue = "\n".join(fin)

        return vaulue

    # Returns the content of the tables to compare them later in the main file
    def get_table_content(self):
        soup = f.get_soup()
        return soup.find_all("table", attrs={"class": "table"})


f = Crawler()