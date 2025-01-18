#install modules
!pip install beautifulsoup4 requests selenium pandas

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_string = title.text.strip()
    except AttributeError:
        title_string = ""
    return title_string

def get_price(soup):
    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip()
    except AttributeError:
        try:
            price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip()
        except:
            price = ""
    return price

def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-small-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""
    return rating

def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""
    return review_count

def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'}).find("span").string.strip()
    except AttributeError:
        available = "Not Available"
    return available

if __name__ == '__main__':
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 
        'Accept-Language': 'en-US, en;q=0.5'
    }

    url = 'https://www.amazon.com/s?k=women+clothing'
    webpage = requests.get(url, headers=headers)

    soup = BeautifulSoup(webpage.content, "html.parser")

    # Find all links to product pages
    links = soup.find_all("a", attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    links_list = []

    # Extract the href attribute and store full URL
    for link in links:
        full_link = "https://www.amazon.com" + link.get('href')
        links_list.append(full_link)

    # Add product link to the dictionary
    d = {"title": [], "price": [], "rating": [], "reviews": [], "availability": [], "link": []}

    # Extract product details from each link
    for link in links_list:
        new_webpage = requests.get(link, headers=headers)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))
        d['link'].append(link)  # Store the product link

    # Create a DataFrame and clean up the data
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    
    # Save to CSV
    amazon_df.to_csv("amazon_wc.csv", header=True, index=False)

    print("Data saved to 'amazon_wc.csv'")

amazon_df
