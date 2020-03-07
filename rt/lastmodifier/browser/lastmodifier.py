# -*- coding: utf-8 -*-

import sys
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SecurityManagement import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from plone.app.layout.viewlets.content import ContentHistoryViewlet
from plone.memoize.view import memoize
from zope.component import queryMultiAdapter
from zope.interface import Interface
from zope.annotation.interfaces import IAnnotations
from zope.component import queryAdapter

try:
    from AccessControl.User import UnrestrictedUser
except ImportError:
    from AccessControl.User import Super as UnrestrictedUser


class UnrestrictedUser(UnrestrictedUser):
    """Unrestricted user that still has an id."""

    def getId(self):
        """Return the ID of the user."""
        return self.getUserName()


class LastModifierView(BrowserView):
    """Display info about last modifier"""

    @memoize
    def last_modifier(self):
        # Let's see if we have any last_modifier annotation
        raw_last_modifier = self._raw_last_modifier()
        if raw_last_modifier:
            return raw_last_modifier
        # If we are here: try with with history support if is available.
        history = queryMultiAdapter(
            (self.context, self.request),
            interface=Interface,
            name=u"contenthistory",
        )

        # Security is in the view definition. Here we act as an omnipotent user
        old_sm = getSecurityManager()
        tmp_user = UnrestrictedUser(
            old_sm.getUser().getId() or '', '', ['Manager'], ''
        )
        newSecurityManager(None, tmp_user)

        try:
            if not history and sys.version_info < (2, 6):
                # We didn't found any history... is this a Plone 3? Let's try with the old history viewlet
                # To be sure of that let's do it only if we are using Python 2.4
                # Please remove this abomination when Plone 3.3 compatibity will be dropped
                history = ContentHistoryViewlet(
                    self.context, self.request, None, manager=None
                )
                history.update()
            if history:
                full_history = history.fullHistory()
                if full_history:
                    return full_history[0].get('actorid') or full_history[
                        0
                    ].get('actor').get('username')
        finally:
            setSecurityManager(old_sm)

    def _raw_last_modifier(self):
        annotations = queryAdapter(self.context, IAnnotations)
        if not annotations:
            return None
        return annotations.get('rt.lastmodifier', {}).get('lastmodifier')


class LastModifierFolderView(LastModifierView):
    """Last modifier from folder: look last modifier from most recent content inside the folder"""

    @memoize
    def last_modifier(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(
            path='/'.join(self.context.getPhysicalPath()),
            sort_on='modified',
            sort_order='reverse',
            sort_limit=1,
        )
        if results:
            new_context = results[0].getObject()
            # BBB: dirty, but calling @@lastmodifier on new_context can return another Folder
            self.context = new_context
        return super(LastModifierFolderView, self).last_modifier()
