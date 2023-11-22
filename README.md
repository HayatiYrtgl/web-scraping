# Arabam Scraper

This Python script is designed for scraping second-hand car listings from the Arabam website. It utilizes BeautifulSoup and requests libraries for web scraping.

## Initialization

```python
from bs4 import BeautifulSoup
import requests as req

header = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,ar;q=0.5",
}


class ArabamScraper:
    def __init__(self):
        self.base_url = None
        self.brand = input("Enter the brand: ")
        self.model = input("Enter the model: ")
        self.min_pr = input("Enter the minimum price: ")
        self.max_pr = input("Enter the maximum price: ")
        self.min_year = input("Enter the minimum year: ")
        self.max_year = input("Enter the maximum year: ")
        self.url_list = []

    def requester(self, url):
        """This function requests the given URL and returns the content of the web page."""
        my_request = req.get(url, headers=header)
        if my_request.status_code == 200:
            print("Connected to", url)
            return my_request.content
        else:
            print(my_request.status_code, "failed")
            return False

    def url_modifier(self, page=1):
        """Modifies the base URL based on user input and page number."""
        self.base_url = f"https://www.arabam.com/ikinci-el?searchText={self.brand}+{self.model}&take=50&currency=TL&minPrice={self.min_pr}&maxPrice={self.max_pr}&minYear={self.min_year}&maxYear={self.max_year}&page={page}"

    def scrap_the_content(self, content):
        """This function scrapes the content of a page and appends the URL to the list of car URLs."""
        try:
            page_content = BeautifulSoup(content, "lxml")
            divs = page_content.findAll("div", attrs={"class": "inner-container"})
            for i in divs:
                try:
                    self.url_list.append("https://arabam.com" + i.find("a").get("href"))
                except:
                    pass
        except:
            pass

    def scrap_pages(self, page_numbers):
        """This function scrapes the given number of pages."""
        for number in range(1, page_numbers + 1):
            self.url_modifier(page=number)
            content = self.requester(self.base_url)
            self.scrap_the_content(content)
            print(number, len(self.url_list))

    def feature_extractor(self):
        """This function extracts features from the list of car URLs."""
        for link in self.url_list:
            content = self.requester(link)
            div_finder = BeautifulSoup(content, "lxml")
            div_list_header = div_finder.findAll("div", attrs={"class": "property-name"})
            div_list_value = div_finder.findAll("div", attrs={"class": "property-value"})
            for header, value in zip(div_list_header, div_list_value):
                print(header.text.strip().replace("\n", ""), value.text.strip().replace("\n", ""))
            print("\n-------------")


# Example Usage
c = ArabamScraper()
c.scrap_pages(4)
c.feature_extractor()
```

## Usage

1. Run the script.
2. Enter the requested information for the car search (brand, model, price range, and year range).
3. The script will connect to the Arabam website, scrape the specified number of pages, and extract features from the obtained car URLs.

## Note

- Use this script responsibly and ensure compliance with the terms of service of the website you are scraping.
