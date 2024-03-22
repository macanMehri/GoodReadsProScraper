from constants import SEARCH_URL, BASE_URL, DEFAULT_TAB, DEFAULT_PAGE_COUNTS, DEFAULT_TITLE
import scraper_handler
import local_settings
from database_manager import DatabaseManager
import models


# Connect to database
database_manager = DatabaseManager(
        database_name=local_settings.DATABASE['name'],
        user=local_settings.DATABASE['user'],
        password=local_settings.DATABASE['password'],
        host=local_settings.DATABASE['host'],
        port=local_settings.DATABASE['port'],
    )

if __name__ == '__main__':
    # Create tables
    database_manager.create_tables(models=[models.Author])
    # Inputs
    search_title = input('Please enter a search title: ') or DEFAULT_TITLE
    search_type = input('What are you searching for?(books, groups, quotes, people or listopia) ') or DEFAULT_TAB
    tab = search_type
    page_count = int(input('How many pages you want to scrape data from? ') or DEFAULT_PAGE_COUNTS)
    # Search each page
    for page_number in range(1, page_count+1):

        url = SEARCH_URL.format(page_number=page_number, search_title=search_title, search_type=search_type, tab=tab)

        main_scraper_handler = scraper_handler.ScraperHandler(base_url=url)
        main_scraper_handler.send_request()

        for url in main_scraper_handler.get_target_urls():
            target_url = BASE_URL + url
            target_scraper_handler = scraper_handler.ScraperHandler(base_url=target_url)
            target_scraper_handler.send_request()
            author, _ = target_scraper_handler.get_author_info()
            print(author)
            print('-' * 50)

    if database_manager.db:
        database_manager.close_connection()
