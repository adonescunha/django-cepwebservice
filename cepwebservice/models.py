#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-cepwebservice
# https://github.com/adonescunha/django-cepwebservice

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Adones Cunha adonescunha@gmail.com


import urllib
import urllib2
from django.db import models
from django.utils import simplejson as json

from .constants import WEBSERVICE_URL


class Estado(models.Model):

    uf = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'estado'
        verbose_name_plural = 'estados'
        ordering = ('nome',)

    def __unicode__(self):
        return self.nome


class Cidade(models.Model):

    estado = models.ForeignKey(Estado)
    nome = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'cidade'
        verbose_name_plural = 'cidades'
        ordering = ('nome',)
        unique_together = ('estado', 'nome')

    def __unicode__(self):
        return '%s - %s' % (self.nome, self.estado.uf)


class Bairro(models.Model):

    cidade = models.ForeignKey(Cidade)
    nome = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'bairro'
        verbose_name_plural = 'bairros'
        ordering = ('nome',)
        unique_together = ('cidade', 'nome')

    def __unicode__(self):
        return '%s' % self.nome


class Logradouro(models.Model):

    bairro = models.ForeignKey(Bairro)
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'logradouro'
        verbose_name_plural = 'logradouros'
        ordering = ('nome',)
        unique_together = ('bairro', 'nome', 'tipo')

    def __unicode__(self):
        return '%s, %s' % (self.nome, self.tipo)


class CEPManager(models.Manager):
    def fetch_by_cep(self, cep):
        try:
            raise CEP.DoesNotExist
            return self.get(cep=cep)
        except CEP.DoesNotExist:
            return self._fetch_from_webservice(cep)

        raise CEP.DoesNotExist

    def _fetch_from_webservice(self, cep):
        query_string = urllib.urlencode({'cep': cep, 'formato': 'jsonp'})
        response = urllib2.urlopen('%s?%s' % (WEBSERVICE_URL, query_string))\
            .read()

        return self._build_cep_from_webservice_response(cep, response)

    def _build_cep_from_webservice_response(self, cep, response):
        cep_dict = json.loads(response)

        if cep_dict['resultado'] == '1':
            estado = Estado.objects.get(uf=cep_dict['uf'])
            cidade, _ = Cidade.objects.get_or_create(nome=cep_dict['cidade'],
                estado=estado)
            bairro, _ = Bairro.objects.get_or_create(nome=cep_dict['bairro'],
                cidade=cidade)
            logradouro, _ = Logradouro.objects.get_or_create(
                nome=cep_dict['logradouro'], tipo=cep_dict['tipo_logradouro'],
                    bairro=bairro)

            return self.get_or_create(cep=cep, logradouro=logradouro)[0]

        raise CEP.DoesNotExist


class CEP(models.Model):

    logradouro = models.ForeignKey(Logradouro)
    cep = models.CharField(max_length=9, unique=True)

    objects = CEPManager()

    class Meta:
        verbose_name = 'CEP'
        verbose_name_plural = 'CEPs'

    def __unicode__(self):
        return self.cep

    def to_json(self):
        return {
            'cep': self.cep,
            'logradouro': self.logradouro.nome,
            'tipo_logradouro': self.logradouro.tipo,
            'bairro': self.logradouro.bairro.nome,
            'cidade': self.logradouro.bairro.cidade.nome,
            'estado': self.logradouro.bairro.cidade.estado.nome,
            'uf': self.logradouro.bairro.cidade.estado.uf
        }
