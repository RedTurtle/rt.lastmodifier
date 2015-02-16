# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.content import DocumentBylineViewlet as BaseDocumentBylineViewlet
from plone.memoize.view import memoize
from rt.lastmodifier.browser.changenote import ShowChangeNoteViewlet
from rt.lastmodifier.permissions import DocumentByLineViewAuthor
from rt.lastmodifier.permissions import DocumentByLineViewChangeNote
from rt.lastmodifier.permissions import DocumentByLineViewLastModifier
from rt.lastmodifier.permissions import DocumentByLineViewModifiedDate
from rt.lastmodifier.permissions import DocumentByLineViewPublishedDate
from zope.component import getMultiAdapter
from zope.interface import Interface


class DocumentBylineViewlet(BaseDocumentBylineViewlet, ShowChangeNoteViewlet):

    def update(self):
        super(DocumentBylineViewlet, self).update()
        sm = getSecurityManager()
        self.can_see_author = sm.checkPermission(DocumentByLineViewAuthor, self.portal_state.portal())
        self.can_see_last_modifier = sm.checkPermission(DocumentByLineViewLastModifier, self.portal_state.portal())
        self.can_see_published = sm.checkPermission(DocumentByLineViewPublishedDate, self.portal_state.portal())
        self.can_see_modified = sm.checkPermission(DocumentByLineViewModifiedDate, self.portal_state.portal())
        self.can_see_change_note = sm.checkPermission(DocumentByLineViewChangeNote, self.portal_state.portal())

    @memoize
    def show(self):
        if self.can_see_author or self.can_see_last_modifier or \
           self.can_see_modified or self.can_see_published:
            return True
        return False

    def pub_date(self):
        """Taken from recent Plone versions, to let viewlet template working also on old Plone
        """
        # check if we are allowed to display publication date
        if not self.can_see_published:
            return None
        # check if we have Effective Date set
        date = self.context.EffectiveDate()
        if not date or date == 'None':
            return None

        return DateTime(date)

    @memoize
    def last_modifier(self):
        # check if we are allowed to display the last modifier
        if not self.can_see_last_modifier:
            return None
        view_last_modifier = getMultiAdapter((self.context, self.request),
                                             interface=Interface, name=u"lastmodifier")
        if view_last_modifier:
            return view_last_modifier.last_modifier()

    def modifier(self):
        membership = getToolByName(self.context, 'portal_membership')
        return membership.getMemberInfo(self.last_modifier() or '')

    def modifiername(self):
        modifier = self.modifier()
        return modifier and modifier['fullname'] or self.last_modifier()

    def modification_date(self):
        return self.context.ModificationDate()


class DocumentBylineFolderViewlet(DocumentBylineViewlet):
    """When on folders, last modifier and last modification date must be taken from
    last modified content inside the folder
    """

    def modification_date(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(sort_on='modified', sort_order='reverse', sort_limit=1)
        if results:
            return results[0].modified
        return super(DocumentBylineFolderViewlet, self).modification_date()
