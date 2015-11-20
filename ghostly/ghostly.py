#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Surely we can do
basic acceptance testing
with just 7 commands
(& 5 asserts)

Browser Commands: get, click, fill, submit, wait, switch_to, navigate
Asserts: assert_text, assert_element, assert_value, assert_title, assert_url
"""

import random
import string
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from .errors import DriverDoesNotExistError, GhostlyTestFailed


def milli_now():
    return int(time.time() * 1000)


class Ghostly:
    """
    Lightweight wrapper and helper utilities around Selenium webdriver.
    """

    def __init__(self, driver, maximise_window=True):
        """
        :param driver: String name of driver, it's expected that it's an attribute
                       on webdriver. IE. 'Chrome' or 'Firefox' are valid.
        """

        try:
            self.driver = getattr(webdriver, driver)()
            """:type : webdriver.Chrome"""
        except AttributeError as e:
            raise DriverDoesNotExistError("Driver '%s' does not exist." % driver)

        if maximise_window:
            self.driver.maximize_window()

    def end(self):
        self.driver.quit()

    def _get_element(self, selector, parent=None, wait=10):
        """
        Returns a single element using a stripped down version of the jQuery lookup
        functions. Options are:
            - #element_id
            - .element_class
            - element_name
            - Link Text
        """

        # using our own wait-for-element logic
        wait = wait * 1000
        start = milli_now()

        # disable the driver/selenium wait time so that we can use our own logic
        self.driver.implicitly_wait(0)

        element = None
        while milli_now() < start + wait:
            if not parent:
                parent = self.driver

            try:
                if selector.startswith('#'):
                    elements = parent.find_elements_by_id(selector.replace('#', ''))
                elif selector.startswith('.'):
                    elements = parent.find_elements_by_class_name(selector.replace('.', ''))
                else:
                    funcs = [
                        parent.find_elements_by_tag_name,
                        parent.find_elements_by_name,
                        parent.find_elements_by_id,
                        parent.find_elements_by_css_selector,
                        parent.find_elements_by_link_text
                    ]

                    for f in funcs:
                        try:
                            elements = f(selector)
                            if elements:
                                break
                        except NoSuchElementException:
                            pass

                if elements:
                    for element in elements:
                        # ignore hidden form elements
                        if element.tag_name.lower() == 'input' and element.get_attribute('type') == 'hidden':
                            continue
                        return element

            except NoSuchElementException:
                pass

        raise NoSuchElementException('Could not find element matching {}'.format(selector))

    def get(self, url):
        """
        Load the provided URL in the web driver
        """
        return self.driver.get(url)

    def click(self, selector):
        """
        Click on an element that's currently visible on the page.

        The element can be selected with a range of selectors:
            - .class_name
            - #element_id
            - element
            - "Link Text"
        """
        element = self._get_element(selector)
        element.click()

    def xpath_click(self, xpath, wait=0.1):
        """
        Click an element selected using xpath.

        :param xpath: Xpath to the element to be clicked.
        :param wait:
        :return:
        """
        element = self.driver.find_element_by_xpath('//*[@id="refresh"]')

        ActionChains(self.driver)\
            .move_to_element(element)\
            .click()\
            .perform()

        if wait:
            self.wait(wait)

    def submit(self, selector, *contents):
        """
        Fill out and submit a form
        """
        form = self.fill(selector, *contents)
        return form.submit()

    def fill(self, selector, *contents):
        """
        Fill out a form without submitting it.

        Provide a list where the first item is the selector to use to find the form and
        all following items are <selector>: <value> pairs to be used to complete the form.

        Use the `submit` function if you also want to submit the form.
        """
        r = ''.join(random.choice(string.letters + string.digits) for _ in range(12))
        form = self._get_element(selector)
        for c in contents:
            for k, v in c.items():
                v = v.replace('<random>', r)
                element = self._get_element(k, parent=form)
                element.send_keys(v)
        return form

    def wait(self, seconds):
        """
        Wait for a specified number of seconds
        """
        if type(seconds) == str:
            seconds = int(seconds)
        time.sleep(seconds)

    def switch_to(self, selector):
        """
        Switch to a new frame (useful for navigating between iFrames)
        """
        self.driver.switch_to.frame(selector)

    def navigate(self, navigation):
        """
        Possible navigation methods:
            - forward
            - back
        """
        if navigation not in ['forward', 'back']:
            raise AttributeError("An invalid option was given to the navigation command")
        f = getattr(self.driver, navigation)
        f()

    def assert_text(self, text, selector='body'):
        """
        Assert that a piece of text exists on the currently displayed page.
        """
        self.wait(1)
        element = self._get_element(selector)

        if text not in element.text:
            raise GhostlyTestFailed("{} not in {}".format(text, element.text))

    def assert_element(self, selector):
        """
        Ensure that at least one element exists that matches the selector
        """
        self.wait(1)
        element = self._get_element(selector)
        if not element:
            raise GhostlyTestFailed("no element matched {}".format(selector))

    def assert_value(self, selector, value):
        """
        Assert that the value of a form element is the provided value

        - assert_value:
          - "input"
          - "Hello World"
        """
        self.wait(1)
        element = self._get_element(selector)
        if element.get_attribute('value') != value:
            raise GhostlyTestFailed("{} != {}".format(element.get_attribute('value'), value))

    def assert_title(self, value):
        self.wait(1)
        if self.driver.title != value:
            raise GhostlyTestFailed("title is {} not {}".format(self.driver.title, value))

    def assert_url(self, url):
        self.wait(1)
        if self.driver.current_url != url:
            raise GhostlyTestFailed("url is {} not {}".format(self.driver.current_url, url))

