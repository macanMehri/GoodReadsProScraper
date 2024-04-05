
# GoodReads Scraper

When you run this program it will ask you to type a title to search and scrape data for this title. It will ask you the number of pages you want to scrape and the type you like such as books or groups.

## Acknowledgements

 - [w3schools website](https://www.w3schools.com/)



## Authors

- [Macan Mehri](https://github.com/macanMehri)


## Deployment

To deploy this project run

```bash
  pip install -r requirements.txt
```
Rename sample_settings.py file to local_settings.py.
Put you database information in here
```bash
  DATABASE = {
    'name': '',
    'user': '',
    'password': '',
    'host': '',
    'port': 5432,
}
```


## Run Locally

Clone the project

```bash
  git clone https://github.com/macanMehri/BookScraper.git
```

Go to the project directory

```bash
  cd good_reads_scraper
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the program

```bash
  python main.py
```


## Features

- Ease of use
- User friendly
- Warm environment
- Scrape very fast
- Every time you scrape data, the information of your search such as datetime and title will store in database so you can see your search history
- Avoid storing duplicated data
