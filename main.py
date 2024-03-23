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
    database_manager.create_tables(models=[models.Author, models.Keyword, models.SearchByKeyword, models.Book,
                                           models.Genre, models.BookGenre])

    # Inputs
    search_title = input('Please enter a search title: ') or DEFAULT_TITLE
    keyword, _ = models.Keyword.get_or_create(keyword=search_title)
    search_type = input('What are you searching for?(books, groups, quotes, people or listopia) ') or DEFAULT_TAB
    tab = search_type
    page_count = int(input('How many pages you want to scrape data from? ') or DEFAULT_PAGE_COUNTS)
    search_keyword_item, _ = models.SearchByKeyword.get_or_create(
        keyword=keyword,
        search_type=search_type,
        search_tab=tab,
        page_count=page_count,
    )
    main_scraper_handler = scraper_handler.ScraperHandler(base_url=BASE_URL, search_url=SEARCH_URL)
    main_scraper_handler.search(keyword_search_instance=search_keyword_item)

    if database_manager.db:
        database_manager.close_connection()
