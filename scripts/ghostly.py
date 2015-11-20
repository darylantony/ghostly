#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Surely we can do
basic acceptance testing
with just 7 commands
(& 5 asserts)

Browser Commands: load, click, fill, submit, wait, switch_to, navigate
Asserts: assert_text, assert_element, assert_value, assert_title, assert_url
"""

import sys
import time

import click
import yaml
from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException
from ghostly import Ghostly, GhostlyTestFailed


def run_test(test, browser, verbose):
    # we create a new Ghostly instance for each tests, keeps things nice and
    # isolated / ensures there is a clear cache
    g = Ghostly(browser)
    try:
        for step in test['test']:
            # print step
            for f, v in step.items():
                func = getattr(g, f)
                if type(v) == list:
                    func(*v)
                else:
                    func(v)
    # explicitly catch the possible error states and fail the test with an appropriate message
    except NoSuchElementException as e:
        fail(test['name'], "couldn't find element", e, verbose)
        passed = False
    except WebDriverException as e:
        fail(test['name'], "webdriver failed", e, verbose)
        passed = False
    except GhostlyTestFailed as e:
        fail(test['name'], e.message, e, verbose)
        passed = False
    else:
        click.echo(click.style("✔", fg='green') + " " + test['name'])
        passed = True
    finally:
        g.end()

    return passed


def fail(name, reason, exception=None, verbose=False):
    click.echo(click.style("✘", fg='red') + " {} ({})".format(name, reason))
    if verbose:
        click.echo(exception)


@click.command()
@click.argument('ghostly_files', type=click.File('rb'), nargs=-1)
@click.option('--driver', default='Chrome', help='Selenium webdriver browser to use [Chrome, Firefox, Ie etc...]')
@click.option('--verbose', is_flag=True)
def run_ghostly(ghostly_files, browser, verbose):
    start = time.time()
    tests = []
    passed = []
    failed = []

    for f in ghostly_files:
        test_yaml = yaml.load(f.read())
        tests.extend(test_yaml)

    plural = len(tests) != 1 and "s" or ""
    click.echo('Running {} test{}...'.format(len(tests), plural))
    for test in tests:
        if run_test(test, browser, verbose):
            passed.append(test)
        else:
            failed.append(test)

    stop = time.time()

    taken = float(stop - start)
    click.echo("Ran {} test{} in {:.2f}s".format(len(tests), plural, taken))

    if failed:
        sys.exit(1)


if __name__ == '__main__':
    run_ghostly()
