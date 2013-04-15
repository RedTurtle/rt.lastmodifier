# -*- coding: utf-8 -*-

#from Products.CMFEditions.interfaces import IVersioned
from zope.interface import Interface
from zope.component import getMultiAdapter

from plone.indexer import indexer

@indexer(Interface)
def last_modifier(object):
    history = getMultiAdapter((object, object.REQUEST), interface=Interface, name=u"contenthistory")
    if history:
        full_history = history.fullHistory()
        if full_history:
            last_entry = full_history[0]
            return last_entry.get('actor').get('username')
