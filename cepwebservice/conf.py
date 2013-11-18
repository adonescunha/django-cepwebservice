#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-cepwebservice
# https://github.com/adonescunha/django-cepwebservice

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Adones Cunha adonescunha@gmail.com


from django.conf import settings

from .constants import DEFAULT_SEED_URL

CEPWEBSERVICE_SEED_URL = getattr(settings, 'CEPWEBSERVICE_SEED_URL',
        DEFAULT_SEED_URL)
