# -*- coding: utf-8 -*-

from DateTime import DateTime

from zope.component import getMultiAdapter
from zope.interface import Interface

from Products.CMFCore.utils import getToolByName

from plone.memoize.view import memoize
from plone.app.layout.viewlets.content import DocumentBylineViewlet as BaseDocumentBylineViewlet

class DocumentBylineViewlet(BaseDocumentBylineViewlet):

    def pub_date(self):
        """Taken from recent Plone versions, to let viewlet template working also on old Plone
        """
        # check if we are allowed to display publication date
        properties = getToolByName(self.context, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        if not site_properties.getProperty('displayPublicationDateInByline',
           False):
            return None
        
        # check if we have Effective Date set
        date = self.context.EffectiveDate()
        if not date or date == 'None':
            return None

        return DateTime(date)

    @memoize
    def last_modifier(self):
        # check if we are allowed to display the last modifier
        properties = getToolByName(self.context, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        if not site_properties.getProperty('displayLastModifierInByline',
           False):
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
