# -*- coding: utf-8 -*-

import sys
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager, getSecurityManager
from AccessControl.User import UnrestrictedUser
from Products.Five.browser import BrowserView
from plone.app.layout.viewlets.content import ContentHistoryViewlet
from zope.component import queryMultiAdapter
from zope.interface import Interface


class UnrestrictedUser(UnrestrictedUser):
    """Unrestricted user that still has an id."""

    def getId(self):
        """Return the ID of the user."""
        return self.getUserName()


class LastModifierView(BrowserView):
    """Display info about last modifier""" 

    def last_modifier(self):
        history = queryMultiAdapter((self.context, self.request), interface=Interface, name=u"contenthistory")

        # Security is in the iew definition. Here we act as an omnipotent user
        old_sm = getSecurityManager()
        tmp_user = UnrestrictedUser(old_sm.getUser().getId() or '', '', ['Manager'], '')
        newSecurityManager(None, tmp_user)
        
        try:
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
        finally:
            setSecurityManager(old_sm)

