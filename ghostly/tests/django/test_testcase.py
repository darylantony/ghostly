# -*- coding: utf-8 -*-
"""
    ghostly.tests.django.test_testcase
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for :py:class:`.GhostlyDjangoTestCase`
"""
from __future__ import absolute_import, print_function, unicode_literals

import unittest

from django.core.urlresolvers import reverse

from ghostly.django.testcase import GhostlyDjangoTestCase


class GhostlyDjangoTestCaseTestCase(GhostlyDjangoTestCase):

    def test_test1(self):
        self.assertGetUrl(reverse('test1'))
