"""Turns an archive of papers in YAML format into a web page for Jekyll

    $ python3 archive.py archive.yaml > archive.md

"""

# Copyright (c) 2017 AIRG Authors.  This is free software released under
# the MIT License.  See `LICENSE.md` for details.


from datetime import datetime
import sys

import yaml


# Functions


def span(content, class_=None):
    class_attr = ''
    if isinstance(class_, str):
        class_attr = ' class="{}"'.format(class_)
    return '<span{}>{}</span>'.format(class_attr, content)


def link(content, url):
    return '<a href="{}">{}</a>'.format(url, content)


# Script


# Load the YAML archive
papers_filename = sys.argv[1]
with open(papers_filename, 'rt') as papers_file:
    papers_yaml = yaml.load(papers_file)

# Use just the presentations
presentations = papers_yaml['presentations']

# Sort all papers by date, descending.  Leave ties in existing order.
presentations.sort(key=lambda p: p['when'], reverse=True)

# Open output
output = sys.stdout

# Write YAML header needed to tell Jekyll to render this page
output.write(
"""
---
copyright_year: {:%Y}
title: Archive
---

"""
.lstrip().format(datetime.now()))

# Output front matter
output.write(
"""
AIRG Archive
============


"""
.lstrip())

# List all presentations by year marked up as HTML
output.write('<dl class="archive">\n')
prev_year = None
for presentation in presentations:
    # Unpack the presentation dictionary
    pres_when = presentation['when']
    pres_who = presentation['who']
    paper_title = presentation['title']
    paper_authors = presentation['authors']
    pub_venue = presentation.get('venue')
    pub_number = presentation.get('number')
    pub_series = presentation.get('series')
    pub_year = presentation.get('year')
    link_venu_meta = presentation.get('metalink')
    link_venu_pdf = presentation.get('pdflink')
    link_auth_meta = presentation.get('author_metalink')
    link_auth_pdf = presentation.get('author_pdflink')

    # Start a new year if necessary
    curr_year = pres_when.year
    if curr_year != prev_year:
        # Close previous year
        if prev_year is not None:
            output.write('</ul>\n</dd>\n')
        output.write('<dt class="year">{}</dt>\n<dd>\n<ul>\n'
                     .format(curr_year))
    prev_year = curr_year

    # Start the paper list item
    output.write('<li class="paper">\n')

    # Date and presenter
    output.write('<p class="presentation">{:%m/%d}, {}</p>\n'
                 .format(pres_when, pres_who))

    # Title, authors
    output.write('<p class="title">{}</p>\n'.format(paper_title))
    output.write('<p class="authors">{}</p>\n'.format(paper_authors))

    # Publication information
    if pub_venue or pub_year:
        output.write('<p class="publication">')
        if pub_venue:
            output.write(span(pub_venue, 'venue'))
            if pub_number:
                output.write(' ')
                output.write(span(pub_number, 'number'))
            if pub_series:
                output.write(', ')
                output.write(span(pub_series, 'series'))
        if pub_year:
            if pub_venue:
                output.write(', ')
            output.write(span(pub_year, 'year'))
        output.write('</p>\n')

    # Links
    has_venu_link = link_venu_meta or link_venu_pdf
    has_auth_link = link_auth_meta or link_auth_pdf
    if has_venu_link or has_auth_link:
        output.write('<p class="links">')
        if has_venu_link:
            output.write('venue: ')
            if link_venu_meta:
                output.write(link('meta', link_venu_meta))
            if link_venu_meta and link_venu_pdf:
                output.write(' ')
            if link_venu_pdf:
                output.write(link('pdf', link_venu_pdf))
        if has_venu_link and has_auth_link:
            output.write(' | ')
        if has_auth_link:
            output.write('author: ')
            if link_auth_meta:
                output.write(link('meta', link_auth_meta))
            if link_auth_meta and link_auth_pdf:
                output.write(' ')
            if link_auth_pdf:
                output.write(link('pdf', link_auth_pdf))
        output.write('</p>\n')

    # End the paper list item
    output.write('</li>\n')

# Close year if there were any years
if presentations:
    output.write('</ul>\n</dd>\n')
# Close list of presentations
output.write('</dl>\n\n')

# Output end matter
output.write('Generated from the [archive data]({}).\n'
             .format(papers_filename))
