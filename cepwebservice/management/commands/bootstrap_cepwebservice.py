# -*- coding: utf-8 -*-

import re
import os
import tarfile
import traceback
from django.db import connection, transaction
from django.db.models import get_app#, get_models
from django.core.management.base import BaseCommand
from django.conf import settings
# from django.core.management.sql import custom_sql_for_model
# from django.core.management.color import no_style

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.file_name = 'cepwebservice.sql'
        self._untar_file()
        full_file_name = os.path.join(os.getcwd(), self.file_name)
        sql_file = open(full_file_name, 'U')
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
        os.remove(full_file_name)

        # models = get_models(app)
        # style = no_style()s

        # for model in models:
        #     custom_sql = custom_sql_for_model(model, no_style(), connection)
        #     print 'Instalando %s' % model._meta.verbose_name

        #     try:
        #         for sql in custom_sql:
        #             cursor.execute(sql)
        #     except Exception, e:
        #         traceback.print_exc()
        #         print 'Falha ao cadastrar %s' % model._meta.verbose_name
        #         transaction.rollback_unless_managed()
        #     else:
        #         transaction.commit_unless_managed()

    def _untar_file(self):
        app = get_app('cepwebservice')
        app_dir = os.path.normpath(os.path.join(os.path.dirname(app.__file__),
            'files'))
        tar = tarfile.open(os.path.join(app_dir, '%s.tar.bz2' % self.file_name))
        tar.extractall()
        tar.close()
