#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-cepwebservice
# https://github.com/adonescunha/django-cepwebservice

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Adones Cunha adonescunha@gmail.com


import os
from pyvows import Vows, expect

from cepwebservice.utils import untar_seed_file


EXTRACTED_FILE_NAME = 'cepwebservice.sql'

@Vows.batch
class UntarSeedFileVows(Vows.Context):

    def teardown(self):
        if os.path.exists(EXTRACTED_FILE_NAME):
            os.remove(EXTRACTED_FILE_NAME)

    def topic(self):
        seed_file = open(os.path.join(os.getcwd(),
                'files/cepwebservice.sql.tar.bz2'))
        return (seed_file, untar_seed_file(seed_file))

    def saves_extracted_file_on_current_working_directory(self, topic):
        expect(os.path.exists(EXTRACTED_FILE_NAME)).to_be_true()

    def returns_extracted_file(self, topic):
        _, extracted_file = topic
        expect(os.path.basename(extracted_file.name))\
                .to_equal(EXTRACTED_FILE_NAME)
