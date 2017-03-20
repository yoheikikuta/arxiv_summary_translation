#!/usr/bin/env python
# -*- coding: utf-8 -*_

# This module refers https://github.com/lukasschwab/arxiv.py

import feedparser
import datetime


def get_date(baseday=None, beforeNdays=1):
    '''
    Get the date for collecting arXiv buld data
    input :
        baseday - reference day like '20160417'
        beforeNdays - the days we go back 
    output :
        datetime of {reference, previous} days
    '''
    
    if not baseday:
        today = datetime.date.today()
    else:
        today = datetime.datetime.strptime(baseday, '%Y%m%d').date()
    
    #Get the weekday
    today_weekday = today.weekday()
    
    #Weekend processing (NOT consider public holidays)
    if today_weekday == 0 and beforeNdays < 3:
        previousday = today + datetime.timedelta(days=-3)
    else:
        previousday = today + datetime.timedelta(days=-beforeNdays)
    
    t_str = today.strftime('%Y%m%d')
    p_str = previousday.strftime('%Y%m%d')
    
    return t_str, p_str


def _prune_result(result):
    '''
    Remove unused information from the returned json result
    input :
        result - returned json result
    output :
        pruned result
    '''
    prune_keys = [
            'updated_parsed'
            , 'published_parsed'
            , 'arxiv_primary_category'
            , 'summary_detail'
            , 'author_detail'
            , 'links'
            , 'guidislink'
            , 'title_detail'
            , 'tags'
            , 'id'
            ]
    for key in prune_keys:
        try:
            del result[key]
        except KeyError:
            pass


def _shape_result(result):
    '''
    input :
        result - returned json result
    output :
        shaped data
    '''
    # Useful to have for download automation
    result['pdf_url'] = None
    for link in result['links']:
        if 'title' in link and link['title'] == 'pdf':
            result['pdf_url'] = link['href']

    result['affiliation'] = result.pop('arxiv_affiliation', 'None')
    result['arxiv_url'] = result.pop('link')
    result['title'] = result['title'].rstrip('\n')
    result['summary'] = result['summary'].rstrip('\n')
    result['authors'] = [d['name'] for d in result['authors']]

    if 'arxiv_comment' in result:
        result['arxiv_comment'] = result['arxiv_comment'].rstrip('\n')
    else:
        result['arxiv_comment'] = None
    if 'arxiv_journal_ref' in result:
        result['journal_reference'] = result.pop('arxiv_journal_ref')
    else:
        result['journal_reference'] = None
    if 'arxiv_doi' in result:
        result['doi'] = result.pop('arxiv_doi')
    else:
        result['doi'] = None


def execute_query(query, prune=True, start=0, max_results=10):
    '''
    input :
        query, whether prune or not
    output :
        bulk of arXiv information
    '''
    root_url = 'http://export.arxiv.org/api/'

    results = feedparser.parse(
        root_url + 'query?search_query=' + query
        + '&start=' + str(start) + '&max_results=' + str(max_results)
    )

    if results['status'] != 200:
        # TODO: better error reporting
        raise Exception("HTTP Error " + str(results['status']) + " in query")
    else:
        results = results['entries']

    for result in results:
        # Renamings and modifications
        _shape_result(result)
        if prune:
            _prune_result(result)

    # Assert if the result is None
    assert len(results) > 0, "NO arXiv result returns. Check the dates."
    return results
