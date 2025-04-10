import json
import requests
from bs4 import BeautifulSoup

# Function to create connection with URL
def connect_to_source(url_: str) -> BeautifulSoup:
    response = requests.get(url_)
    return BeautifulSoup(response.text, 'lxml')

# Function to save data to a json file
def save_to_json_file(path: str, data: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)

if __name__ == "__main__":
    URL = "https://quotes.toscrape.com/"
    current_url = URL
    quotes_data = []
    authors_data = []
    added_authors = []
    while True:
        source = connect_to_source(current_url)
        quotes = source.select("div", attrs={"class": "col-md-8"})[0].find_all("div", attrs={"class": "quote"})
        for entry in quotes:
            # Creating list of quotes
            quote_dict = {}
            tags = entry.find_all("a", attrs={"class": "tag"})
            tag_list = []
            for tag in tags:
                tag_list.append(tag.text)
            quote_dict["tags"] = tag_list
            author = entry.find("small", attrs={"class": "author"})
            quote_dict["author"] = author.text
            quote = entry.find("span", attrs={"class": "text"}).text
            quote_dict["quote"] = quote
            quotes_data.append(quote_dict)
            # Creating list of authors
            author_url = f"{URL}{author.find_next_sibling('a')['href']}"
            if author_url in added_authors:
                continue
            added_authors.append(author_url)
            author_source = connect_to_source(author_url)
            author_details = author_source.select("div", attrs={"class": "author-details"})[0]
            author_dict = {}
            author_dict["full_name"] = author_details.find("h3", attrs={"class": "author-title"}).text
            author_dict["born_date"] = author_details.find("span", attrs={"class": "author-born-date"}).text
            author_dict["born_location"] = author_details.find("span", attrs={"class": "author-born-location"}).text
            author_dict["description"] = author_details.find("div", attrs={"class": "author-description"}).text.strip()
            authors_data.append(author_dict)
        next_page = source.find('li', class_='next')
        # print(next_page)
        if not next_page:
            break
        current_url = f"{URL}{next_page.find('a')['href']}"
    save_to_json_file("quotes.json", quotes_data)
    save_to_json_file("authors.json", authors_data)
