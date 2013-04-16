# -*- coding: utf-8 -*-

#from Products.CMFEditions.interfaces import IVersioned
from zope.interface import Interface
from zope.component import getMultiAdapter

from plone.indexer import indexer

@indexer(Interface)
def last_modifier(object):
    view_last_modifier = getMultiAdapter((object, object.REQUEST), interface=Interface, name=u"lastmodifier")
    if view_last_modifier:
        return view_last_modifier.last_modifier()