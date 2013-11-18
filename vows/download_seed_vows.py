#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-cepwebservice
# https://github.com/adonescunha/django-cepwebservice

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Adones Cunha adonescunha@gmail.com


import urllib2
from pyvows import Vows, expect
from mock import Mock
from StringIO import StringIO

from cepwebservice.utils import download_seed
from cepwebservice.conf import CEPWEBSERVICE_SEED_URL


RESPONSE = 'RESPONSE'


def mock_urlopen(f):
    def wrapper(*args, **kwargs):
        response_buf = StringIO(RESPONSE)
        response_buf.seek(0)
        urllib2.urlopen = Mock(return_value=response_buf)

        return f(*args, **kwargs)
    return wrapper


@Vows.batch
class DownloadSeedVows(Vows.Context):

    def topic(self):
        return (CEPWEBSERVICE_SEED_URL, RESPONSE)

    @mock_urlopen
    def requests_provided_url(self, topic):
        seed_url, _ = topic
        download_seed()
        urllib2.urlopen.assert_called_with(seed_url)

    @mock_urlopen
    def returns_buffered_response(self, topic):
        _, expected = topic
        actual = download_seed()
        expect(actual.read()).to_equal(expected)

    @mock_urlopen
    def returns_io_buffer_positioned_at_zero(self, topic):
        expect(download_seed().tell()).to_equal(0)
