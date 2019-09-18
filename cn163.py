#!/usr/bin/env python3
"""
Created on 5/8/16

@author: 'Jiezhi.G@gmail.com'


To get the latest code, please visit my github: https://github.com/Jiezhi/just-a-spider

Reference: 
"""
import requests
from bs4 import BeautifulSoup
import csv
import time
import os.path


def get_content_from_url(url):
    split_url = url.split('/')
    number = split_url[len(split_url) - 2]
    print(url, number)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    title = soup.title.get_text().split('|')[0].strip()
    file_title = os.path.join('result', number + title.split('/')[0].strip() + '.csv')
    print('parsing %s' % title)

    # if the result file exists then continue
    if os.path.exists(file_title):
        print('%s already parsed' % file_title)
    else:
        with open(file_title, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            for link in soup.find('div', {'id': 'entry'}).findAll('a'):
                item_name = link.get_text().strip()
                item_value = link.get('href').strip()
                # exclude irrelevant url
                if item_value.startswith('http://cn163.net'):
                    continue
                csvwriter.writerow([item_name, item_value])
    try:
        next_url = soup.find('a', {'rel': 'next'}).get('href').strip()
    except AttributeError:
        print('it seems no more url to get')
        exit(0)
    time.sleep(5)
    # get_content_from_url(next_url)


if __name__ == '__main__':
    # TODO get list from this page: http://cn163.net/archives/
    first_url = 'http://cn163.net/archives/58/'
    first_url = 'http://cn163.net/archives/1316/'
    get_content_from_url(first_url)
