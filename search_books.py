#! /usr/local/bin/python

import sys

import pyes

import settings


def main(search_term):
    """
    This searches books
    """

    conn = pyes.ES(settings.ES_CLUSTER)

    # Try to create the index
    try:
        conn.create_index(settings.INDEX_NAME)
    except Exception:
        pass

    q = pyes.TermQuery("text", search_term)
    results = conn.search(query=q)
    for r in results['hits']['hits']:
        print '+++Start+++'
        print r['_source']['text'], '\n'
        print '---End---'

if __name__ == "__main__":
    if len(sys.argv) == 2:
        term = sys.argv[1]
        main(term)
    else:
        print 'Please supply a search word'
        sys.exit()
