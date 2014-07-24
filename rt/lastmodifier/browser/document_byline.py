# -*- coding: utf-8 -*-

from DateTime import DateTime
from zope.component import getMultiAdapter
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone.memoize.view import memoize
from plone.app.layout.viewlets.content import DocumentBylineViewlet as BaseDocumentBylineViewlet
from rt.lastmodifier.permissions import DocumentByLineViewAuthor, DocumentByLineViewLastModifier, \
                                        DocumentByLineViewModifiedDate, DocumentByLineViewPublishedDate, \
                                        DocumentByLineViewChangeNote
from rt.lastmodifier.browser.changenote import ShowChangeNoteViewlet
from AccessControl import getSecurityManager


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
        if self.can_see_author or self.can_see_last_modifier or\
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
