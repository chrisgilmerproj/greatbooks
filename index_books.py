#! /usr/local/bin/python

import glob
import os

import pyes

import settings


def parse_book_txt(book_filename):
    book_paragraphs = []
    book_text = False
    paragraph = []
    count = 0
    title = ''
    author = ''

    for line in open(book_filename, 'r'):
        # Find title and author
        if not title and 'Title:' in line:
            title = line.split(':')[1].strip()
        if not author and 'Author:' in line:
            author = line.split(':')[1].strip()

        # Find Start and End of text
        if 'START OF THE PROJECT GUTENBERG EBOOK' in line:
            book_text = True
            line = ''
        if 'END OF THE PROJECT GUTENBERG EBOOK' in line:
            book_text = False
        if book_text:
            if line.strip() == '':
                text = ''.join(paragraph).strip().decode('utf-8')
                if text.strip() != '':
                    data = {
                            'file': book_filename,
                            'title': title,
                            'author': author,
                            'paragraph_id': count,
                            'text': text,
                           }
                    book_paragraphs.append(data)
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
    book_path = os.path.join(os.getcwd(), settings.BOOK_FOLDER, 'volume_*', '*.%s' % settings.BOOK_TYPE)

    for filename in glob.glob(book_path):
        print filename
        if filename[-len(settings.BOOK_TYPE):] == settings.BOOK_TYPE:
            paragraphs = parse_book_txt(os.path.join(book_path, filename))
            for data in paragraphs:
                conn.index(data, settings.INDEX_NAME, settings.TYPE_NAME)


if __name__ == "__main__":
    main()
