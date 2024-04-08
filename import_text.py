"""
file: import_text.py
description: a file that uses the Yelp API to get reviews from Yelp website and
convert them to a text file
"""

import requests
from bs4 import BeautifulSoup

# Create URL list with 9 different restaurants
restaurant_list = ['mala-restaurant-boston',
                   'tora-japanese-restaurant-boston',
                   'pho-le-restaurant-boston',
                   'seoul-soulongtang-boston',
                   'kaju-tofu-house-allston-2',
                   'happy-lamb-hot-pot-boston-4',
                   'futago-udon-boston',
                   'peach-farm-boston',
                   'santouka-back-bay-boston-2'
                   ]
url_dict = {}

for restaurant in restaurant_list:
    url = f'https://www.yelp.com/biz/{restaurant}?sort_by=date_desc'
    url_dict[restaurant] = url

for restaurant, url in url_dict.items():
    # Send a GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find review elements (assuming they are contained in <div class="review">)
        review_divs = soup.find_all('span', class_='raw__09f24__T4Ezm', lang='en')

        # Create review list
        review_list = []

        for review_div in review_divs:
            # Extract and print the review text (assuming it's within <p> tags)
            review_text = review_div.text
            review_list.append(review_text)

        # Specify the file name
        file_name = f'{restaurant}.txt'

        # Open the file in write mode ('w') and write each review to the file
        with open(file_name, 'w', encoding='utf-8') as file:
            for review in review_list:
                file.write(review + "\n\n")
    else:
        print(f"Failed to retrieve the webpage, status code: {response.status_code}")
