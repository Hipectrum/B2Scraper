import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

file_path = os.path.join(os.getcwd(), 'data.xlsx')

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "tr,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
}

base_URL = "https://books.toscrape.com/catalogue/page-{}.html"

first_response = requests.get(url=base_URL.format(1), headers=headers, timeout=20)
f_html = first_response.text

first_soup = BeautifulSoup(f_html, "html.parser")
page_count = first_soup.find('li', class_="current")
fixed_page_count = page_count.text.strip().replace('Page 1 of ', "")
max_page = int(fixed_page_count)


book_data = []
price_data = []
stock_data = []
rating = []


for page in range(1, max_page +1):
    URL = base_URL.format(page)
    second_response = requests.get(url=URL, headers=headers, timeout=20)
    s_html = second_response.text
    second_soup = BeautifulSoup(s_html, "html.parser")

    book_names = second_soup.find_all('h3')
    book_prices = second_soup.find_all('p', class_="price_color")
    stock_status = second_soup.find_all('p', class_="instock availability")
    star_rating = second_soup.find_all('p', class_="star-rating")

    for i in book_names:
        extended = i.find('a')
        if extended:
            fixed_book_names = extended['title']
            book_data.append(fixed_book_names)

    for j in book_prices:
        fixed_book_prices = j.text.strip().replace("Â", "")
        price_data.append(fixed_book_prices)

    for n in stock_status:
        stock_data.append(n.text.strip())

    for s in star_rating:
        fixed_stars = s.get('class')[1]

        if fixed_stars == "One":
            rating.append("⭐")

        elif fixed_stars == "Two":
            rating.append("⭐⭐")

        elif fixed_stars == "Three":
            rating.append("⭐⭐⭐")

        elif fixed_stars == "Four":
            rating.append("⭐⭐⭐⭐")

        elif fixed_stars == "Five":
            rating.append("⭐⭐⭐⭐⭐")

        else:
            rating.append("None")



df = pd.DataFrame({
    'Book Names': book_data,
    'Prices': price_data,
    'Rating': rating,
    'Stock Status': stock_data
})

with pd.ExcelWriter(file_path) as writer:
    df.to_excel(writer, index=False)


