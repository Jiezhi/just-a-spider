#!/usr/bin/env python3
"""
Created on 5/21/16

@author: 'Jiezhi.G@gmail.com'

This code mainly parse & download free books from oreily(www.oreilly.com/programming/free/)

To get the latest code, please visit my github: https://github.com/Jiezhi/just-a-spider

Reference: 
"""
import os
import requests
from bs4 import BeautifulSoup
import threading
import re


def get_keyword(url):
    """
    Return catelog and book
    """
    # TODO error handler
    reg=r"http://www\.oreilly\.com/([a-z]+)/free/([^.]+)\.csp.*"
    m = re.match(reg,url)
    return m.groups()


def download_file(url):
    """
    Just download a small file by url
    This code snip come from http://stackoverflow.com/a/16696317/5425709
    :param url: The file url
    :return: The downloaded file name
    """
    local_filename = url.split('/')[-1]
    dir_name = 'oreilly' + os.path.sep + url.split('/')[-4]
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    local_filename = os.path.join(dir_name, local_filename)
    if os.path.exists(local_filename):
        print('file already downloaded: ', local_filename)
        return local_filename
    print('downloading ', url)
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


def get_free_book(content, file_format='pdf'):
    """
    Parse free book information from html content
    :param content: the content of what your get from oreily free book web page
    :param file_format epub mobi or pdf
    :return:
    """
    soup = BeautifulSoup(content, 'lxml')
    # books = soup.find_all('div', {'class': 'product-row cover-showcase'})
    # TODO handle error
    books = soup.find_all('a', {'data-toggle': 'popover'})
    print('Find %d book(s)...' % len(books))
    for book in books:
        href = book['href']
        if not href or 'player.oreilly.com' in href or not '.csp' in href:
            print("this page will be igored: ", href)
            continue
        try:
            catelog,book_name = get_keyword(href)
            book_url = 'http://www.oreilly.com/%s/free/files/%s.%s' % (catelog, book_name, file_format)
            t = threading.Thread(target=download_file,args=(book_url,))
            t.start()
        except Exception:
            print("Downloading from {} failed".format(href))


if __name__ == '__main__':
    free_oreilly = ['http://www.oreilly.com/programming/free/',
                    'http://www.oreilly.com/web-platform/free/',
                    'http://www.oreilly.com/security/free/',
                    'http://www.oreilly.com/business/free/',
                    'http://www.oreilly.com/data/free/',
                    'http://www.oreilly.com/iot/free/',
                    'http://www.oreilly.com/design/free/',
                    'http://www.oreilly.com/webops-perf/free/',
                    ]
    for free in free_oreilly:
        html = requests.get(free)
        get_free_book(html.content)
