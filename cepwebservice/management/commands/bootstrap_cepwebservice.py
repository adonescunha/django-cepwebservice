#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-cepwebservice
# https://github.com/adonescunha/django-cepwebservice

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Adones Cunha adonescunha@gmail.com


import re
import os
import traceback
from django.db import connection, transaction
from django.core.management.base import BaseCommand
from django.conf import settings

from ...utils import download_seed, untar_seed_file

class Command(BaseCommand):

    def handle(self, *args, **options):
        sql_file = untar_seed_file(download_seed())
        cursor = connection.cursor()
        statements_regex = re.compile(r";[ \t]*$", re.M)

        try:
            for statement in statements_regex.split(sql_file.read().decode(settings.FILE_CHARSET)):
                statement = re.sub(ur"--.*([\n\Z]|$)", "", statement)

                if statement != '':
                    cursor.execute(statement + ';')
        except Exception, e:
            if not 'Query was empty' in str(e):
                traceback.print_exc()
                print 'Fail while bootstrapping cepwebservice app'
                transaction.rollback_unless_managed()
        else:
            transaction.commit_unless_managed()

        sql_file.close()
        os.remove(sql_file.name)
