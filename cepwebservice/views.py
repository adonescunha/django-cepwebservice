#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-cepwebservice
# https://github.com/adonescunha/django-cepwebservice

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Adones Cunha adonescunha@gmail.com


import re
from django.http import Http404, HttpResponse
from django.utils import simplejson as json

from .models import CEP


def service(request):
    cep = request.GET.get('q')

    if cep and re.match(r'^\d{5}\-\d{3}$', cep):
        try:
            result = CEP.objects.fetch_by_cep(cep)
        except CEP.DoesNotExist:
            raise Http404
    else:
        raise Http404

    return HttpResponse(json.dumps(result.to_json(), ensure_ascii=True),
        mimetype='text/javascript')
