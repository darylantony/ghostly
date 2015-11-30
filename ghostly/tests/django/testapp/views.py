# -*- coding: utf-8 -*-
"""
    module.name
    ~~~~~~~~~~~~~~~
    Preamble...
"""
from __future__ import absolute_import, print_function, unicode_literals

from django.views.generic import TemplateView


class ParameterisedTitleView(TemplateView):

    def get_context_data(self, **kwargs):
        kwargs.update(
            title=self.request.GET.get('title', 'Test1'),
            delay=int(self.request.GET.get('delay', 1)) * 1000
        )
        return super(ParameterisedTitleView, self).get_context_data(**kwargs)
