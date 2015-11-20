# -*- coding: utf-8 -*-
"""
    ghostly.tests.django.test_testcase
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for :py:class:`.GhostlyDjangoTestCase`
"""
from __future__ import absolute_import, print_function, unicode_literals

import unittest

from django.core.urlresolvers import reverse
from django.utils import six
from selenium.webdriver import ActionChains

from ghostly.django.testcase import GhostlyDjangoTestCase


class GhostlyDjangoTestCaseTestCase(GhostlyDjangoTestCase):
    #driver = 'Chrome'

    def test_h1(self):
        self.goto(reverse('test1'))
        self.ghostly.assert_text('Test1', 'h1')

    def test_svg(self):
        self.goto(reverse('test1'))

        # Check the circle exists
        circle = self.ghostly.driver.find_element_by_xpath('//*[@id="refresh"]/*[name()="circle"]')
        self.assertEqual(circle.get_attribute('cx'), six.text_type('50'))

        # Click the link around the red circle
        self.ghostly.xpath_click('//*[@id="refresh"]')

        # Test the click happened
        self.assertCurrentUrl('/test1/?title=Success')
        self.assertSelectorEqual('h1', 'Success')

        # h2 is not yet visible
        self.assertXpathEqual('//h2', '')

        # Click the link around the blue circle
        self.ghostly.xpath_click('//*[@id="popup"]')

        # Now check that Hello World is visible
        self.assertXpathEqual('//h2', 'Hello World')
