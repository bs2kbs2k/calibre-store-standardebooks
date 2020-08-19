# -*- coding: utf-8 ts=4 sw=4 sts=4 et -*-
from __future__ import (absolute_import, print_function, unicode_literals)

__license__   = 'GPL 3'
__copyright__ = '2020, bs2k <bs2k@naver.com>'
__docformat__ = 'restructuredtext en'

from calibre.customize import StoreBase

class StandardEbooksStore(StoreBase):
    name            = 'Standard Ebooks'
    version         = (0, 1, 1)
    description     = 'Free and liberated ebooks, carefully produced for the true book lover.'
    author          = 'bs2k <bs2k@naver.com>'
    actual_plugin   = 'calibre_plugins.bs2k_store_standardebooks.standardebooks:StandardEbooksStore'
    formats         = ['EPUB', 'EPUB3', 'KEPUB', 'KINDLE']
    drm_free_only = True