import re
import requests
from bs4 import BeautifulSoup

class SearchResult:
  def __init__(self, link=None, title=None, author=None, goodreads_author = None, rating=None, published=None, editions=None):
    self.link = link
    self.title = title
    self.author = author
    self.goodreads_author = goodreads_author
    self.rating = rating
    self.published = published #May not be available
    self.editions = editions

def search_in_goodreads(term):
  term = term.strip().replace(' ', '+')
  url = f'https://www.goodreads.com/search?utf8=%E2%9C%93&q={term}&search_type=books'
  return url

def download_page(url):
  res = requests.get(url)
  res.raise_for_status()
  return res.text

def get_results(html):
  search_results = []
  soup = BeautifulSoup(html, features="lxml")
  table_rows = soup.select('tr[itemtype="http://schema.org/Book"]')
  for i in table_rows:
    search_result = SearchResult()
    search_result.link = 'https://www.goodreads.com' + i.td.a['href']
    search_result.title = i.find("a", {"class": "bookTitle"}).span.getText()
    search_result.author = i.find("a", {"class": "authorName"}).span.getText()
    search_result.goodreads_author = "(Goodreads Author)" if bool(i.find("span", {"class": "greyText"}).span) else ""
    search_result.rating = (i.find("span", {"class": "minirating"}).getText()).strip()
    
    published = re.compile("(\d\d\d\d)")
    date = published.search(i.find("span", {"class": "greyText smallText uitext"}).getText())
    search_result.published = date.group() if date else ''
    
    search_result.editions = i.find("a", {"class": "greyText"}).getText()
    search_results.append(search_result)
  
  return search_results


def formatted_results(search_results, count):
  
  formatted = '\U0001F4DA <b>Results | Books</b>\n\n'
  i = 0
  exp = '(\d+)'
  regexp = re.compile(exp)
  while i < count:
    search_result = search_results[i]
    link = '/bk_' + regexp.search(search_result.link).group()
    string = f"\U0001F4D6 <b>{search_result.title}</b> \n <i>by {search_result.author}</i> {search_result.goodreads_author}\n{search_result.rating} — published {search_result.published} — {search_result.editions}\n{link}\n\n"
    formatted += string
    i+=1     
  return formatted

