import requests
from bs4 import BeautifulSoup
import models


class ScraperHandler:
    """A class to handle scraping better"""

    def __init__(self, base_url):
        self.base_url = base_url
        self.response = None
        self.soup = None

    def send_request(self) -> requests.Response:
        """Send a request to the base url"""
        self.response = requests.get(url=self.base_url, timeout=20)
        # If request sent successfully then create a soup object
        if self.status_code == 200:
            self.soup = BeautifulSoup(self.html_source_code, 'html.parser')
        return self.response

    @property
    def status_code(self) -> int:
        """Returns response status code"""
        return self.response.status_code

    @property
    def html_source_code(self) -> str:
        """Returns html source code of base url"""
        return self.response.text

    def get_target_urls(self):
        """Returns the url of target website to scrape"""
        targets = self.soup.find_all('a', attrs={'class': 'bookTitle'})
        for target in targets:
            yield target['href']

    def get_author_info(self):
        """Scrape authors info and creates and returns an author object"""
        name = self.soup.find('span', attrs={'class': 'ContributorLink__name'}).text
        number_of_books = self.soup.find('div', attrs={'class': 'PageSection'}
                                         ).find_next('span', attrs={'class': 'Text Text__body3 Text__subdued'}).text

        number_of_books_end = number_of_books.find('b') - 1
        # Remove number separator (,)
        number_of_books = number_of_books.replace(',', '')
        # Slice string and convert to int
        number_of_books = int(number_of_books[:number_of_books_end])

        number_of_followers = self.soup.find('div', attrs={'class': 'PageSection'}
                                             ).find_next('span', attrs={'class': 'u-dot-before'}).text

        return models.Author.get_or_create(
            name=name,
            books=number_of_books,
            followers=number_of_followers
        )

    def get_edition_info(self):
        """Scrape editions info and creates and returns an edition object"""
        # Get all editions information
        edition = self.soup.find('dl', attrs={'class': 'DescList'}).find_all('dd')

        print(
            f'edition_format: {edition[0].text} | edition_published_date: {edition[1].text} | '
            f'isbn: {edition[2].text} | language: {edition[3].text}'
        )
        """
        return models.Edition.get_or_create(
            edition_format=edition[0].text,
            edition_published_date=edition[1].text,
            isbn=edition[2].text,
            language=edition[3].text,
        )
"""

    def get_genres(self):
        """Scrape genres of each book"""
