#! /usr/local/bin/python

import sys

import pyes

import settings


def main(search_term):
    """
    This searches books
    """

    conn = pyes.ES(settings.ES_CLUSTER)

    q = pyes.TermQuery("text", search_term)
    results = conn.search(query=q)
    for r in results['hits']['hits']:
        source = r['_source']
        print '+' * 79
        for label in ['file', 'id', 'text']:
            print '%s:\t%s' % (label, source[label])
        print '-' * 79 + '\n'


if __name__ == "__main__":
    if len(sys.argv) == 2:
        term = sys.argv[1]
        main(term)
    else:
        print 'Please supply a search word'
        sys.exit()
