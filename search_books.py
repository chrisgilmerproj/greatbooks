#! /usr/local/bin/python

import sys

import pyes

import settings


def main(search_terms, max_results):
    """
    This searches books
    """

    conn = pyes.ES(settings.ES_CLUSTER)

    q = pyes.TermsQuery("text", search_terms)
    results = conn.search(query=q)

    for num, r in enumerate(results['hits']['hits']):
        if num >= max_results:
            break
        source = r['_source']
        print '+' * 79
        for label in ['file', 'id', 'text']:
            print '%s:\t%s' % (label, source[label])
        print '-' * 79 + '\n'


if __name__ == "__main__":
    terms = ['something']
    max_results = 5
    if len(sys.argv) < 2:
        print 'Please supply a search word'
        sys.exit()
    if len(sys.argv) >= 2:
        terms = sys.argv[1].split()
    if len(sys.argv) == 3:
        max_results = int(sys.argv[2])
    main(terms, max_results)
