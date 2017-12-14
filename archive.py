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


def prune_empty_values(dict_):
    new_dict = {}
    for key, val in dict_.items():
        if isinstance(val, dict):
            new_val = prune_empty_values(val)
            if new_val:
                new_dict[key] = new_val
        elif val:
            new_dict[key] = val
    return new_dict


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
    links = presentation.get('links')

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
    if isinstance(links, dict):
        links = prune_empty_values(links)
    if links:
        output.write('<p class="links">')
        n_sections = 0
        for link_section in ('venue', 'arxiv', 'author'):
            if link_section not in links:
                continue
            link_types = links[link_section]
            if n_sections >= 1:
                output.write(' | ')
            output.write(link_section)
            output.write(': ')
            n_types = 0
            for link_type in ('toc', 'meta', 'pdf', 'web'):
                if link_type not in link_types:
                    continue
                link_url = link_types[link_type]
                if n_types >= 1:
                    output.write(' ')
                output.write(link(link_type, link_url))
                n_types += 1
            n_sections += 1
        if 'info' in links:
            info_links = links['info']
            if info_links:
                if n_sections >= 1:
                    output.write(' | ')
                output.write('info: ')
                n_infos = 0
                for key, url in info_links.items():
                    if n_infos >= 1:
                        output.write(' ')
                    output.write(link(key, url))
                    n_infos += 1
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
