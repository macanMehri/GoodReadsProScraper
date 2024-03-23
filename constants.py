# Urls
BASE_URL = 'https://www.goodreads.com/'
SEARCH_URL = BASE_URL + 'search?page={page_number}&q={search_title}&search_type={search_type}&tab={tab}'
# Default values
DEFAULT_TAB = 'books'
DEFAULT_PAGE_COUNTS = 5
DEFAULT_TITLE = 'book'

ITEM_CLASS = {
    'books': 'bookTitle',
    'groups': 'groupName',
    'quotes': 'authorOrTitle',
    'people': '',
    'lists': 'listTitle'
}
