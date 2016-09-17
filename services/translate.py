#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line example for Translate.

Command-line application that translates some text.
"""
from __future__ import print_function
from googleapiclient.discovery import build
import os

LANGUAGES = ['de', 'fr', 'es', 'it']


class TranslateEngine:

    def __init__(self):
        dev_key = os.environ['GOOGLE_DEV_KEY']
        self.service = build('translate', 'v2', developerKey=dev_key)

    def translate(self, sentence_list, language):
        return self.service.translations().list(source='en', target=language, q=sentence_list).execute()

    def translate_all(self, sentence_list):
        translation_dict = {}

        for lang in LANGUAGES:
            translation_dict['lang'] = self.translate(sentence_list,lang)

        return translation_dict