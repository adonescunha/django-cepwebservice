#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-cepwebservice
# https://github.com/adonescunha/django-cepwebservice

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Adones Cunha adonescunha@gmail.com


import os
import urllib2
import tarfile
from cStringIO import StringIO

from .conf import CEPWEBSERVICE_SEED_URL


def download_seed():
    response = urllib2.urlopen(CEPWEBSERVICE_SEED_URL)
    buf =  StringIO()
    buf.write(response.read())
    buf.seek(0)

    return buf

def untar_seed_file(seed_file):
    tar = tarfile.open(fileobj=seed_file)
    tar.extractall()
    tar.close()
    file_name = os.path.join(os.getcwd(), 'cepwebservice.sql')

    return open(file_name, 'U')
