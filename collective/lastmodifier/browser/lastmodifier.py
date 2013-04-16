# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.component import getMultiAdapter

from Products.Five.browser import BrowserView

class LastModifierView(BrowserView):
    
    def last_modifier(self):
        history = getMultiAdapter((self.context, self.request), interface=Interface, name=u"contenthistory")
        if history:
            full_history = history.fullHistory()
            if full_history:
                return full_history[0].get('actorid') or full_history[0].get('actor').get('username')
