# Introduction

This project is for educational purposes only to help learn to use
[elasticsearch](http://www.elasticsearch.org) and the python package
[pyes](https://github.com/aparo/pyes).  In this project I attempt
to index [The Great Books of the Western World](http://en.wikipedia.org/wiki/Great_Books_of_the_Western_World)
to make them searchable.  I own a copy of these books myself and thought
bringing them into the digital age would be a lot of fun.  Only some of these
books are currently in the project and I'm using [Project Gutenberg](http://www.gutenberg.org/)
for my source material.  Please support all of these good projects.


## Installation

Install Dependencies:

    $ brew install elasticsearch
    $ pip install pyes

Index your books:

    $ ./index_books.py

Search your books:

    $ ./search_books.py
