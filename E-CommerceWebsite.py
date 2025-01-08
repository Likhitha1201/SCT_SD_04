"""
        @Author: Likhitha S
        @Date: 06-01-2025 16:30
        @Last Modified by: Likhitha S
        @Last Modified time: 07-01-2025 14:30
        @Title: Create a program that extracts product information, such as names, prices, and ratings from an online e-commerce website and stores the data in a structured format like csv

"""

import requests
from bs4 import BeautifulSoup
import csv

def scrape_ebay(url):
    
    """
            Description: 
                In this we are searching products from online website, if found we are adding it to our file like .csv extension .
            Parameters: 
                url- online website's location, Product- which we like to get/order and file_name- where we are going to save the products detailes. 
            return:
                It prints the message if sucessfully added or not.
    
    """
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    products = []

    for item in soup.select('.s-item'):
        name = item.select_one('.s-item__title')
        price = item.select_one('.s-item__price')
        rating = item.select_one('.b-starrating__star')

        if name and price:
            products.append({
                'Name': name.text.strip(),
                'Price': price.text.strip(),
                'Rating': rating.text.strip() if rating else "No Rating"
            })
    
    return products

def save_to_csv(products, filename):
    keys = products[0].keys() if products else ["Name", "Price", "Rating"]
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(products)

if __name__ == "__main__":
    url = "https://www.ebay.com/sch/i.html?_nkw=laptops"
    product_data = scrape_ebay(url)
    
    if product_data:
        save_to_csv(product_data, 'ebay_products.csv')
        print(f"Data saved to ebay_products.csv")
    else:
        print("No products found or scraping failed.")
