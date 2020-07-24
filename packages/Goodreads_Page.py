import re
import requests
from bs4 import BeautifulSoup

class Book:
  def __init__(self):
    self.title = None
    self.series = None
    self.author = None
    self.image = None
    self.rating = None
    self.review = None
    self.description = None

  def get_content(self, html):
    #TODO Finish Adding content
    contents = []
    soup = BeautifulSoup(html, features="lxml")
    col = soup.find("div", {"id": "topcol"})
    self.title = col.find("h1", {"id": "bookTitle"}).getText().strip()
    series = col.find("h2", {"id": "bookSeries"})
    if series:
        self.series = series.getText().strip()
    self.authors = col.find("span", {"itemprop": "author"}).getText().strip().replace('\n', '')
    self.image = soup.find("img", {"id": "coverImage"})["src"]
    self.rating = col.find("span", {"itemprop": "ratingValue"}).getText().strip()
    description = col.find("div", {"id": "description"})
    if len(description.findAll("span")) == 1:
        span = description.findAll("span")[0]
    else:
        span = description.findAll("span")[1]
    self.description = span.getText()

    return self

  def format_result(self):
      string = f"\U0001F4D6 <b>{self.title}</b> \n Author: {self.authors} \nRating: {self.rating} \n\nDescription:\n{self.description}\n\n"
      return string
