#! /usr/local/bin/python

import os

import epub
import pyes


ES_HOST = '127.0.0.1'
ES_PORT = '9200'
ES_CLUSTER = '%s:%s' % (ES_HOST, ES_PORT)
BOOK_FOLDER = 'books'
BOOK_TYPE = 'txt'
INDEX_NAME = "great_book_index"
TYPE_NAME = "book"


def parse_book_epub(book_filename):
    """ Return an ePub book object """
    book = epub.open(book_filename)
    print book.opf.metadata.__dict__
    return book


def parse_book_txt(book_filename):
    book_paragraphs = []
    book_text = False
    paragraph = []
    count = 0
    for line in open(book_filename, 'r'):
        if 'START OF THE PROJECT GUTENBERG EBOOK' in line:
            book_text = True
            line = ''
        if 'END OF THE PROJECT GUTENBERG EBOOK' in line:
            book_text = False
        if book_text:
            if line.strip() == '':
                text = ''.join(paragraph).strip()
                if text.strip() != '':
                    book_paragraphs.append({'file': book_filename, 'id': count, 'text': text})
                    count += 1
                paragraph = []
            else:
                paragraph.append(line)
    return book_paragraphs


def main():
    """
    This indexes books
    """

    conn = pyes.ES(ES_CLUSTER)

    # Try to create the index
    try:
        conn.create_index(INDEX_NAME)
    except Exception:
        pass

    # Parse each book
    book_path = os.path.abspath(os.path.join(os.getcwd(), BOOK_FOLDER, BOOK_TYPE))
    book_filename_list = os.listdir(book_path)
    for filename in book_filename_list:
        if filename[-len(BOOK_TYPE):] == BOOK_TYPE:
            paragraphs = parse_book_txt(os.path.join(book_path, filename))
            for data in paragraphs:
                conn.index(data, INDEX_NAME, TYPE_NAME)

    q = pyes.TermQuery("text", "him")
    results = conn.search(query=q)
    for r in results['hits']['hits']:
        print r

if __name__ == "__main__":
    main()
