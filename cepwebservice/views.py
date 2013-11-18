# -*- coding: utf-8 -*-

import re
from django.http import Http404, HttpResponse
from django.utils import simplejson as json
from cepwebservice.models import CEP

def service(request):
    import time
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
