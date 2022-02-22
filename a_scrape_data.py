from bs4 import BeautifulSoup
from collections import defaultdict
import numpy as np
import os
import pandas as pd
import re
import requests
import utils

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# letter for saving file names
letter_prepend = os.path.basename(__file__).split('_')[0]
print(letter_prepend)

def create_soup_object(url):
    '''
    input: url
    output: soup object of url text
    '''
    response = requests.get(url)
    if response.status_code == 200:
        page = response.text
    soup = BeautifulSoup(page, 'html5lib')
    return soup

def get_price_indices(soup_obj):
    '''
    input: beautiful soup object
    output: the price indices on the expatistan website
    '''
    price_index = []
    for row in soup_obj.find_all('td', class_ ='price-index'):
        item = row.text
        price_index.append(item)
    return price_index

def get_links(soup_obj):
    '''
    output: a list of all the links on the expatistan website
    '''
    links = []
    for line in soup_obj.find_all('td', class_='city-name'):
        links.append(line.find('a')['href'])
    return links

def get_city_name(soup_obj):
    '''
    finds the city name from the expatistan website
    '''
    city = soup_obj.find('span', class_='city-2').text
    return city

def get_item_names(soup_obj):
    '''
    finds all the item names used in the cost of living index on the expatistan website
    returns a list of items
    '''
    items = []
    for row in soup_obj.find_all('td', class_='item-name'):
        item = row.find('a').text
        items.append(item)
    return items

def get_item_prices(soup_obj):
    '''
    returns a list of prices from scraped from the expatistan website
    '''
    prices = []
    price_regex = re.compile(r'\(?\$?([0-9,.]*)|([-])')
    for row in soup_obj.find_all('td', class_='price city-1'):
        row=row.text.strip()
        mo = price_regex.search(row)
        if mo:
            prices.append(mo.group(1))

    if len(prices) == 104:
        prices1 = prices[1::2]
    else:
        prices1 = prices
    return prices1

@utils.time_this_function(__file__)
def main():
    '''
    Scrape Expatistan website for cities, price indicies, items, and item prices
    '''
    url = 'https://www.expatistan.com/cost-of-living/index'
    response = requests.get(url)
    if response != 200:
        assert 'Unable to access Expatistan website!!'

    page = response.text

    soup = BeautifulSoup(page,"html5lib")

    cities_dict = defaultdict(list) 
    soup = create_soup_object(url)
    links = get_links(soup)
    price_indicies = get_price_indices(soup)
    for i, url in enumerate(links):
        url=url+'?currency=USD'
        print(i, url)
        soup = create_soup_object(url)
        city = get_city_name(soup)
        items = get_item_names(soup)
        prices = get_item_prices(soup)

        cities_dict['CITY'].append(city)

        for item, price in zip(items, prices):
            cities_dict[item].append(price)

    # this is already a list, don't need to append
    cities_dict['PRICE_INDEX'] = price_indicies

    cities_df = pd.DataFrame(cities_dict)
    pi = cities_df['PRICE_INDEX']
    cities_df.drop(labels = ['PRICE_INDEX'], axis = 1, inplace = True) 
    cities_df.insert(0, 'PRICE_INDEX', pi) # move "PRICE_INDEX" column to front
    cities_df.set_index(['CITY'], inplace = True)

    if not os.path.exists(f'{root_dir}/csvs'):
        os.makedirs(f'{root_dir}/csvs')

    cities_df.to_csv(f'{root_dir}/csvs/{letter_prepend}_cities_df.csv')

if __name__ == '__main__':
    main()