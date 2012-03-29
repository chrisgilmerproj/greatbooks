#! /usr/local/bin/python

import random
import sys

import pyes

import settings

SYNTOPICON_01 = ['Angel', 'Animal', 'Aristocracy', 'Art', 'Astronomy',
    'Beauty', 'Being', 'Cause', 'Chance', 'Change', 'Citizen', 'Constitution',
    'Courage', 'Custom and Convention', 'Definition', 'Democracy', 'Desire',
    'Dialectic', 'Duty', 'Education', 'Element', 'Emotion', 'Eternity',
    'Evolution', 'Experience', 'Family', 'Fate', 'Form', 'God',
    'Good and Evil', 'Government', 'Habit', 'Happiness', 'History', 'Honor',
    'Hypothesis', 'Idea', 'Immortality', 'Induction', 'Infinity', 'Judgment',
    'Justice', 'Knowledge', 'Labor', 'Language', 'Law', 'Liberty',
    'Life and Death', 'Logic', 'Love']
SYNTOPICON_02 = ['Man', 'Mathematics', 'Matter', 'Mechanics', 'Medicine',
    'Memory and Imagination', 'Metaphysics', 'Mind', 'Monarchy', 'Nature',
    'Necessity and Contingency', 'Oligarchy', 'One and Many', 'Opinion',
    'Opposition', 'Philosophy', 'Physics', 'Pleasure and Pain', 'Poetry',
    'Principle', 'Progress', 'Prophecy', 'Prudence', 'Punishment', 'Quality',
    'Quantity', 'Reasoning', 'Relation', 'Religion', 'Revolution', 'Rhetoric',
    'Same and Other', 'Science', 'Sense', 'Sign and Symbol', 'Sin', 'Slavery',
    'Soul', 'Space', 'State', 'Temperance', 'Theology', 'Time', 'Truth',
    'Tyranny', 'Universal and Particular', 'Virtue and Vice', 'War and Peace',
    'Wealth', 'Will', 'Wisdom', 'World']
TERM_LIST = SYNTOPICON_01 + SYNTOPICON_02


def main(search_terms, max_results):
    """
    This searches books
    """
    print 'Searching documents for %s results of: %s' % (max_results, ' '.join(search_terms))

    conn = pyes.ES(settings.ES_CLUSTER)

    q = pyes.TermsQuery("text", search_terms)
    results = conn.search(query=q)

    for num, r in enumerate(results['hits']['hits']):
        if num >= max_results:
            break
        source = r['_source']
        print '+' * 79
        for label in ['file', 'title', 'author', 'paragraph_id', 'text']:
            print '%s:\t%s' % (label, source[label])
        print '-' * 79 + '\n'


if __name__ == "__main__":
    terms = [random.choice(TERM_LIST).lower()]
    max_results = 5
    if len(sys.argv) >= 2:
        terms = sys.argv[1].split()
    if len(sys.argv) == 3:
        max_results = int(sys.argv[2])
    main(terms, max_results)
