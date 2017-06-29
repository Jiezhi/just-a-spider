#!/usr/bin/env python
"""
Created on 22/06/2017

@author: 'Jiezhi.G@gmail.com'

Reference:
"""
from bs4 import BeautifulSoup as bs
import csv


def get_book(path):
    with open(path, 'r') as f, open('result/pack_book.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        soup = bs(f, 'html.parser')
        books = soup.find_all('div', {'class': 'product-line unseen'})
        # print(titles)
        for book in books:
            print('----------------------------')
            title = book['title']
            nid = book['nid']

            paper_book = book.find('div', {'type': 'book'})
            if paper_book:
                isbn = paper_book['isbn']
                paper_nid = paper_book['nid']
                source_file = 'https://www.packtpub.com/code_download/%s' % paper_nid
            else:
                isbn = ''
                paper_nid = ''
                source_file = ''
            pdf_path = 'https://www.packtpub.com/ebook_download/%s/pdf' % nid
            mobi_path = 'https://www.packtpub.com/ebook_download/%s/mobi' % nid
            epub_path = 'https://www.packtpub.com/ebook_download/%s/epub' % nid
            print(title, nid, isbn)
            csvwriter.writerow([title, nid, paper_nid, isbn, pdf_path, mobi_path, epub_path, source_file])


if __name__ == '__main__':
    get_book('~/tmp/packt.html')
