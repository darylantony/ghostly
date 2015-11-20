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
    driver = 'PhantomJS'

    def setUp(self):
        super(GhostlyDjangoTestCase, self).setUp()
        self.ghostly = Ghostly(self.driver)

    def tearDown(self):
        super(GhostlyDjangoTestCase, self).tearDown()
        self.ghostly.end()

    def goto(self, url):
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

    def assertCurrentUrl(self, expected):
        """
        Assert the current URL is equal to expected.

        :param expected: Expected URL, if relative the test servers URL is
                         prepended.
        """
        if expected.startswith('/'):
            # Append the server URL to the url
            expected = self.live_server_url + expected

        self.assertEqual(self.ghostly.driver.current_url, expected)

    def assertBrowserSubmit(self, selector, contents):
        self.ghostly.submit(selector, contents)

    def assertBrowserHasValue(self, selector, value):
        self.ghostly.assert_value(selector, value)

    def assertXpathEqual(self, xpath, expected):
        element = self.ghostly.driver.find_element_by_xpath(xpath)

        self.assertEqual(
            element.text,
            expected,
            "Expected xpath '%s' to be equal to '%s' not '%s'." % (
                xpath,
                expected,
                element.text))

    def assertSelectorEqual(self, selector, expected):
        element = self.ghostly._get_element(selector)

        self.assertEqual(
            element.text,
            expected,
            "Expected selector '%s' to be equal to '%s' not '%s'." % (
                selector,
                expected,
                element.text))
