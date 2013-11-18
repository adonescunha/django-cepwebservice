#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-cepwebservice
# https://github.com/adonescunha/django-cepwebservice

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Adones Cunha adonescunha@gmail.com


from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('cepwebservice.views',
    url(r'^$', 'service', name='cepwebservice_service')
)