# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.component import queryMultiAdapter

from plone.indexer import indexer

@indexer(Interface)
def last_modifier(object):
    view_last_modifier = queryMultiAdapter((object, object.REQUEST), interface=Interface, name=u"lastmodifier")
    if view_last_modifier:
        return view_last_modifier.last_modifier()