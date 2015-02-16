# -*- coding: utf-8 -*-

import sys
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager, getSecurityManager
from AccessControl.User import UnrestrictedUser
from Products.CMFCore.utils import getToolByName
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
                # We didn't found any history... is this a Plone 3? Let's try with the old history viewlet
                # To be sure of that let's do it only if we are using Python 2.4
                # Please remove this abomination when Plone 3.3 compatibity will be dropped
                history = ContentHistoryViewlet(self.context, self.request, None, manager=None)
                history.update()
            if history:
                full_history = history.fullHistory()
                if full_history:
                    return full_history[0].get('actorid') or full_history[0].get('actor').get('username')
        finally:
            setSecurityManager(old_sm)


class LastModifierFolderView(LastModifierView):
    """Last modifier from folder: look last modifier from most recent content inside the folder""" 

    def last_modifier(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(path='/'.join(self.context.getPhysicalPath()),
                          sort_on='modified', sort_order='reverse', sort_limit=1)
        if results:
            new_context = results[0].getObject()
            # BBB: dirty, but calling @@lastmodifier on new_context can return another Folder 
            self.context = new_context
        return super(LastModifierFolderView, self).last_modifier()
