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


def get_keyword(text, start, end):
    """
    Just get target keyword
    :param text:
    :param start:
    :param end:
    :return:
    """
    # TODO error handler
    return text.split(end)[0].split(start)[1]


def download_file(url):
    """
    Just download a small file by url
    This code snip come from http://stackoverflow.com/a/16696317/5425709
    :param url: The file url
    :return: The downloaded file name
    """
    local_filename = url.split('/')[-1]
    local_filename = os.path.join('oreilly', local_filename)
    if os.path.exists(local_filename):
        print('file already downloaded: ', local_filename)
        return local_filename
    print('downloading %s ---> %s' % (url, local_filename))
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


def get_free_book(html):
    """
    Parse free book information from html content
    :param html: the content of what your get from oreily free book web page
    :return:
    """
    soup = BeautifulSoup(html, 'lxml')
    # books = soup.find_all('div', {'class': 'product-row cover-showcase'})
    # TODO handle error
    books = soup.find_all('a', {'data-toggle': 'popover'})
    print('Find %d book(s)...', len(books))
    for book in books:
        book_name = get_keyword(book['href'], 'free/', '.csp')
        book_url = 'http://www.oreilly.com/programming/free/files/%s.pdf' % book_name
        print(book_url)
        download_file(book_url)


if __name__ == '__main__':
    free_oreilly = 'http://www.oreilly.com/programming/free/'
    html = requests.get(free_oreilly)
    get_free_book(html)
