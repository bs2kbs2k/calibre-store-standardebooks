# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

store_version = 1  # Needed for dynamic plugin loading

__license__ = 'GPL 3'
__copyright__ = ''
__docformat__ = 'restructuredtext en'

from contextlib import closing

from calibre import (browser, guess_extension)
from calibre.utils.xml_parse import safe_xml_fromstring
from calibre.utils.opensearch.query import Query

from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.gui2.store.opensearch_store import OpenSearchOPDSStore
from calibre.gui2.store.search_result import SearchResult


SEARCH_URL =  'https://standardebooks.org/ebooks/opensearch'

def open_search(url, query, max_results=10, timeout=60):
    url_template = 'https://standardebooks.org/opds/all?query={searchTerms}'
    oquery = Query(url_template)

    # set up initial values
    oquery.searchTerms = query
    oquery.count = max_results
    url = oquery.url()

    counter = max_results
    br = browser()
    with closing(br.open(url, timeout=timeout)) as f:
        doc = safe_xml_fromstring(f.read())
        for data in doc.xpath('//*[local-name() = "entry"]'):
            if counter <= 0:
                break

            counter -= 1

            s = SearchResult()

            s.detail_item = ''.join(data.xpath('./*[local-name() = "id"]/text()')).strip()

            for link in data.xpath('./*[local-name() = "link"]'):
                rel = link.get('rel')
                href = link.get('href')
                type = link.get('type')

                if rel and href and type:
                    if 'http://opds-spec.org/thumbnail' in rel:
                        s.cover_url = 'https://standardebooks.org' + href
                    elif 'http://opds-spec.org/image/thumbnail' in rel:
                        s.cover_url = 'https://standardebooks.org' + href
                    elif 'http://opds-spec.org/acquisition' in rel:
                        if type:
                            ext = href.split('.')[1]
                            if ext:
                                ext = ext[:].upper().strip()
                                s.downloads[ext] = 'https://standardebooks.org' + href
            s.formats = ', '.join(s.downloads.keys()).strip()

            s.title = ' '.join(data.xpath('./*[local-name() = "title"]//text()')).strip()
            s.author = ', '.join(data.xpath('./*[local-name() = "author"]//*[local-name() = "name"]//text()')).strip()

            yield s


def search(query, max_results=10, timeout=60):
    for result in open_search(SEARCH_URL, query, max_results=max_results, timeout=timeout):
        yield result


class StandardEbooksStore(BasicStoreConfig, OpenSearchOPDSStore):

    open_search_url = SEARCH_URL
    web_url = 'https://standardebooks.org/ebooks'

    # https://standardebooks.org/opds

    def search(self, query, max_results=10, timeout=60):
        for s in search(query, max_results, timeout):
            s.price = '$0.00'
            s.drm = SearchResult.DRM_UNLOCKED
            yield s


if __name__ == '__main__':
    import sys
    for s in search(' '.join(sys.argv[1:])):
        print(s)