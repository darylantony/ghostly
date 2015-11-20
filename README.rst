Ghostly
=======

Lightweight API around Selenium Webdriver for end to end testing with Django.

Usage
-----

GhostlyDjangoTestCase
`````````````````````

``GhostlyDjangoTestCase`` inherits StaticLiveServerTestCase_ and thus fires up
a WSGI server that handles requests.

Given you have a named URL ``home`` with a ``<h1>Hello World</h1>`` visible in
the source, you can do the following;

.. code-block:: python

    class MyTestCase(GhostlyDjangoTestCase):

        def test_homepage(self):
            self.goto(reverse('home'))

            # Assert that an element is equal to something
            self.assertSelectorEqual('h1', 'Hello World')

            # Assert the current url, relative or absolute
            self.assertCurrentUrl('/home')


Working with SVG
~~~~~~~~~~~~~~~~

To traverse SVG with Selenium web driver you must use xpath.

.. code-block:: python

    class MyTestCase(GhostlyDjangoTestCase):

        def test_homepage(self):
            self.goto(reverse('home'))

            # Click on an element, or example, in an SVG.
            self.ghostly.xpath_click('//*[@id="refresh"]')

            # Assert that an Xpath is equal to something
            self.assertXpathEqual('//h2', 'Hello World')


License
=======

This software is licensed under the `MIT License`. See the ``LICENSE``
file in the top distribution directory for the full license text.


Author
======

- Brenton Cleeland <brenton@commoncode.com>
- Alex Hayes <alex@commoncode.com>

.. _StaticLiveServerTestCase: https://docs.djangoproject.com/en/1.8/ref/contrib/staticfiles/#django.contrib.staticfiles.testing.StaticLiveServerTestCase
