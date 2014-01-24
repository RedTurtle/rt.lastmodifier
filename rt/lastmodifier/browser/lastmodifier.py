# -*- coding: utf-8 -*-

import sys

from zope.interface import Interface
from zope.component import queryMultiAdapter

from Products.Five.browser import BrowserView

from plone.app.layout.viewlets.content import ContentHistoryViewlet


class LastModifierView(BrowserView):

    def last_modifier(self):
        history = queryMultiAdapter((self.context, self.request), interface=Interface, name=u"contenthistory")
        if not history and sys.version_info < (2, 6):
            # we didn't found any history, is Plone 3? Let's try with the old histrory viewlet
            # to be sure, let's do it only if we are using Python 2.4
            # Please remove this abomination when Plone 3.3 compatibity will be dropped
            history = ContentHistoryViewlet(self.context, self.request, None, manager=None)
            history.update()
        if history:
            full_history = history.fullHistory()
            if full_history:
                return full_history[0].get('actorid') or full_history[0].get('actor').get('username')
