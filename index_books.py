#! /usr/local/bin/python

import os

import pyes

import settings


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
                text = ''.join(paragraph).strip().decode('utf-8')
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

    conn = pyes.ES(settings.ES_CLUSTER)

    # Delete any existing index
    try:
        conn.delete_index(settings.INDEX_NAME)
    except Exception:
        pass

    # Try to create the index
    try:
        conn.create_index(settings.INDEX_NAME)
    except Exception:
        pass

    # Parse each book
    book_path = os.path.abspath(os.path.join(os.getcwd(), settings.BOOK_FOLDER, settings.BOOK_TYPE))
    book_filename_list = os.listdir(book_path)
    for filename in book_filename_list:
        if filename[-len(settings.BOOK_TYPE):] == settings.BOOK_TYPE:
            paragraphs = parse_book_txt(os.path.join(book_path, filename))
            for data in paragraphs:
                conn.index(data, settings.INDEX_NAME, settings.TYPE_NAME)


if __name__ == "__main__":
    main()
