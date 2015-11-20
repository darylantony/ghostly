# -*- coding: utf-8 -*-
"""
    module.name
    ~~~~~~~~~~~~~~~
    Preamble...
"""
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.remote.command import Command

from ghostly import Ghostly


class GhostlyDjangoTestCase(StaticLiveServerTestCase):
    """
    Django TestCase that allows you to define your Ghostly tests pragmatically.

    This class is mostly a light weight wrapper around Ghostly.
    """
    driver = 'Chrome'

    def setUp(self):
        super(GhostlyDjangoTestCase, self).setUp()
        self.ghostly = Ghostly(self.driver)

    def tearDown(self):
        super(GhostlyDjangoTestCase, self).tearDown()
        self.ghostly.end()

    def assertGetUrl(self, url):
        """
        HTTP GET url and assert it's response code is in assert_statuses.

        :param url: The URL to retrieve, if relative the test servers URL is
                    prepended.
        :type url: str
        :param assert_statuses: A list of acceptable status codes.
        :type assert_statuses: list
        """
        if url.startswith('/'):
            # Append the server URL to the url
            url = self.live_server_url + url

        self.ghostly.driver.get(url)

    def assertBrowserSubmit(self, selector, contents):
        self.ghostly.submit(selector, contents)

    def assertBrowserHasValue(self, selector, value):
        self.ghostly.assert_value(selector, value)
