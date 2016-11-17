import re
import json
import os

import requests
import requests.exceptions
from bs4 import BeautifulSoup

from .exceptions import DMException, SearchException, RequestException


class DMZJ:
    """The basic object of Comic and Chapter."""

    def get_content(self, url, decode=True, *args, **kw):
        """Gets html from url using requests."""

        try:
            resp = requests.get(url, *args, **kw)
            if resp.status_code == 200:
                # resp.text is text encoding with UTF-8, resp.content is binary.
                return resp.text if decode else resp.content
            else:
                raise RequestException("Page >" + url + "> not found.")
        except requests.exceptions.RequestException as e:
            raise RequestException("Page >" + url + "> not found.")

    def get_key(self, key, html):
        """Gets value from key-value sets in html."""

        expression = key + ".+"
        text = re.findall(expression, html)
        if text:
            value = re.findall(r"""['"].+['"]""", text[0])[0]
            return value.strip('"').strip('\'')
        else:
            raise SearchException("<" + key + "> not found.")

    def create_directory(self, path=None):
        """Create a directory if it doesn't exist."""

        directory = os.path.join(
            os.path.abspath(path if path else '.'), self.name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory


class Comic(DMZJ):
    """Represents a comic.
    
    Example:
        comic = Comic("comic_content_url_from_dmzj")
        comic.download()  # Download all chapter in this comic.
        # Or given a path.
        comic.download("/your_directory_to_save/")"""

    def __init__(self, url):
        self.id, self.name, self.url = self.get_detail(url)

    def get_detail(self, url):
        """Gets detail from html."""

        html = self.get_content(url)
        id = self.get_key("g_comic_id", html)
        name = self.get_key("g_comic_name", html)
        url = self.get_key("g_comic_url", html)
        return id, name, url

    def generate_url(self):
        """Generates comic url in domain manhua.dmzj.com."""

        return "http://manhua.dmzj.com/" + self.url

    def download(self, path=None):
        """Downloads all chapter in this comic."""

        self.chapter_urls = self.get_chapter_url()
        self.saved_path = self.create_directory(path)

        for url in self.chapter_urls:
            try:
                chapter = Chapter(url)
                chapter.download(self.saved_path)
            except DMException as e:
                print(e)
                continue

    def get_chapter_url(self):
        """Gets all chapter urls in html."""

        html = self.get_content(self.generate_url())
        soup = BeautifulSoup(html, "html.parser")

        divs = soup.findAll("div", {"class": "cartoon_online_border"})
        if not divs:
            raise SearchException("Tag <div> not found in page.")
        lis = []
        for div in divs:
            lis += div.findAll("li")
        if lis:
            return ["http://manhua.dmzj.com" + li.a["href"] for li in lis]
        raise SearchException("Tag <li> not found in tag <div>.")


class Chapter(DMZJ):
    """Represents a chapter of comic.

    Example:
        chap = Chapter("chapter_url_from_dmzj")
        chap.download()
        # Or given a path
        chap.download("/your_directory_to_save/")"""

    def __init__(self, url):
        self.comic_id, self.id, self.name = self.get_detail(url)

    def get_detail(self, url):
        """Gets detail from html."""

        html = self.get_content(url)
        comic_id = self.get_key("g_comic_id", html)
        id = self.get_key("g_chapter_id", html)
        name = self.get_key("g_chapter_name", html)
        return comic_id, id, name

    def generate_url(self):
        """Generates chapter url in domain m.dmzj.com."""

        return ("http://m.dmzj.com/view/"
                + self.comic_id + '/'
                + self.id + ".html")

    def download(self, path=None):
        """Downloads all pictures in this chapter."""

        self.picture_urls = self.get_picture_url()
        self.saved_path = self.create_directory(path)
        headers = {
            "User-Agent": "Mozilla/5.0 (Window NT 6.2; WOW64; rv:48.0)"
                          + " Gecko/2010010 Firefox/48.0",
            "Referer": "http://manhua.dmzj.com/grandblue/28907.shtml",
        }

        for i in range(len(self.picture_urls)):
            try:
                picture = self.get_content(self.picture_urls[i], False, headers=headers)
                with open(os.path.join(self.saved_path, str(i) + ".jpg"), "wb") as f:
                    f.write(picture)
            except RequestException as e:
                print(e)
                continue

    def get_picture_url(self):
        """Gets all picture urls in this chapter."""

        html = self.get_content(self.generate_url())
        text = re.findall("mReader\.initData.+", html)
        if text:
            text = text[0].split('{')[1].split('}')[0]
            return json.loads('{' + text + '}')["page_url"]
        else:
            raise SearchException("<mReader.initData> not found.")
