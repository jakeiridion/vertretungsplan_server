import requests
from bs4 import BeautifulSoup
import time
from CrawlerAndMail import ConfigReader


class Crawler:
    def __init__(self):
        self.soup = None

    def fetch_soup(self):
        with requests.session() as s:
            login_data = {"username": ConfigReader.elternportal_email,
                          "password": ConfigReader.elternportal_password}

            time.sleep(0.5)
            r = s.get(ConfigReader.url)
            r = s.post(ConfigReader.post_url, data=login_data)
            r = s.get(ConfigReader.end_url)
            soup = BeautifulSoup(r.text, "html.parser")
            self.soup = soup
        return soup

    # this method will be called first in the main file so it is the only one
    # that needs to actually crawl the website with fetch_soup().
    # the rest of the methods can just use the self.soup variable for information.
    def fetch_table_content(self):
        soup = self.fetch_soup()
        table_content = soup.find_all("table", attrs={"class": "table"})
        return table_content

    def fetch_table(self):
        soup = self.soup
        table = soup.find("div", attrs={"class": "main_center"})
        return table

    def turn_table_to_list(self):
        table_list = []
        for line in self.fetch_table():
            table_list.append(str(line))
        return table_list

    def pop_warning_messages(self):
        table = self.turn_table_to_list()
        table.pop()
        table.pop()
        return table

    def insert_gap(self):
        # kw = Kalender Woche
        # I use it to see when i need to place a gap so the mail doesn't look so crowded
        # this however is only for aesthetic reasons.
        kw_counter = 0
        list_counter = 0
        gap = str('<table class="table" style="min-width: 75%;"><tbody><tr class=""><td width="100%" '
                  'colspan="6" align="center" valign="top"><br></td></tr></tbody></table>')

        table = self.pop_warning_messages()
        for line in table:
            if "KW" in line and kw_counter == 1:
                table.insert(list_counter, gap)
                break

            elif "KW" in line and kw_counter == 0:
                kw_counter = 1

            list_counter = list_counter + 1
        return table

    def fetch_finished_table(self):
        table_str = "\n".join(self.insert_gap())
        return table_str

    def fetch_date(self):
        soup = self.soup
        date = soup.find("div", attrs={"class": "list full_width"}).text
        return date


crawler = Crawler()
