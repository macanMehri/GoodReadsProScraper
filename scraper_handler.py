import requests
from bs4 import BeautifulSoup
import models
from constants import ITEM_CLASS


class ScraperHandler:
    """A class to handle scraping better"""

    def __init__(self, base_url, search_url):
        self.base_url = base_url
        self.search_url = search_url

    @staticmethod
    def send_request(url) -> requests.Response:
        """Send a request to the base url"""
        return requests.get(url=url, timeout=20)

    @staticmethod
    def get_target_urls(soup, keyword_search_instance):
        """Returns the url of target website to scrape"""
        targets = soup.find_all('a', attrs={'class': ITEM_CLASS[keyword_search_instance.search_type]})
        for target in targets:
            yield target['href']

    def search(self, keyword_search_instance):
        """Search the website with an instance of keyword_search"""
        # Search each page
        for page_number in range(1, keyword_search_instance.page_count + 1):

            url = self.search_url.format(
                page_number=keyword_search_instance.keyword,
                search_title=keyword_search_instance.keyword,
                search_type=keyword_search_instance.search_type,
                tab=keyword_search_instance.search_tab
            )
            response = ScraperHandler.send_request(url=url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for url in ScraperHandler.get_target_urls(soup=soup, keyword_search_instance=keyword_search_instance):
                # Calculate target url
                target_url = self.base_url + url
                # Send request to target url
                target_response = ScraperHandler.send_request(url=target_url)
                target_soup = BeautifulSoup(target_response.text, 'html.parser')
                # If we are searching for books then:
                if keyword_search_instance.search_type == 'books':
                    author, _ = ScraperHandler.get_author_info(soup=target_soup)
                    print(author)
                    book, _ = ScraperHandler.get_book_info(soup=target_soup, url=target_url, author=author)
                    print(book)
                    genres = ScraperHandler.get_genres(soup=target_soup)
                    for genre in genres:
                        print(genre)
                        models.BookGenre.get_or_create(book=book, genre=genre)
                # If we are searching for groups then:
                elif keyword_search_instance.search_type == 'groups':
                    genre, _ = ScraperHandler.get_group_genre(soup=target_soup)
                    group, _ = ScraperHandler.get_group_info(soup=target_soup, genre=genre)
                    print(group)
                # Seperator
                print('-' * 50)

    @staticmethod
    def get_author_info(soup: BeautifulSoup):
        """Scrape authors info and creates and returns an author object"""
        name = soup.find('span', attrs={'class': 'ContributorLink__name'}).text
        number_of_books = soup.find('div', attrs={'class': 'PageSection'}
                                    ).find_next('span', attrs={'class': 'Text Text__body3 Text__subdued'}).text

        number_of_books_end = number_of_books.find('b') - 1
        # Remove number separator (,)
        number_of_books = number_of_books.replace(',', '')
        # Slice string and convert to int
        number_of_books = int(number_of_books[:number_of_books_end])

        number_of_followers = soup.find('div', attrs={'class': 'PageSection'}
                                        ).find_next('span', attrs={'class': 'u-dot-before'}).text

        return models.Author.get_or_create(
            name=name,
            books=number_of_books,
            followers=number_of_followers
        )

    @staticmethod
    def get_genres(soup: BeautifulSoup):
        """Scrape genres of each book"""
        genres = list()
        genres_boxes = soup.find_all('span', attrs={'class': 'BookPageMetadataSection__genreButton'})
        for genre in genres_boxes:
            genre_item, _ = models.Genre.get_or_create(title=genre.text)
            genres.append(genre_item)

        return genres

    @staticmethod
    def get_book_info(soup: BeautifulSoup, url: str, author: models.Author):
        """Scrape books information"""
        title = soup.find(name='h1', attrs={'data-testid': 'bookTitle'}).text
        rating = float(soup.find(name='div', attrs={'class': 'RatingStatistics__rating'}).text)

        return models.Book.get_or_create(
            url=url,
            title=title,
            author=author,
            rate=rating,
        )

    @staticmethod
    def get_group_genre(soup: BeautifulSoup):
        """Get genre of a group"""
        genre_box = soup.find(name='div', attrs={'class': 'infoBoxRowItem narrow'}).find_all('a')
        genre = genre_box[1].text
        return models.Genre.get_or_create(title=genre)

    @staticmethod
    def get_group_info(soup: BeautifulSoup, genre: models.Genre):
        """Scrape all information of groups"""
        title = soup.find('h1').text
        group_type = soup.find_all(name='div', attrs={'class': 'infoBoxRowItem'})
        group_type = group_type[2].text.strip()
        members = soup.find_all(name='div', attrs={'class': 'h2Container gradientHeaderContainer'})
        # Find members count in a string
        members = members[3].text.strip()
        # We need data inside the parentheses
        start_index = members.find('(') + 1
        members = members[start_index:-1]
        if not members.isnumeric():
            members = 0
        else:
            members = int(members)
        return models.Group.get_or_create(title=title, members=members, genre=genre, group_type=group_type)
