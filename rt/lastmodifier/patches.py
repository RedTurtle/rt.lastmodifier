# -*- coding: utf-8 -*-

from zope.annotation.interfaces import IAnnotations
from persistent.dict import PersistentDict
from zope.component import getMultiAdapter


def notifyModified(self):
    # do all of the default stuff
    self._old_notifyModified()
    # now save the current userid as raw last modifier
    annotations = IAnnotations(self)
    annotations['rt.lastmodifier'] = PersistentDict()
    portal_state = getMultiAdapter((self,
                                    self.REQUEST),
                                   name=u'plone_portal_state')
    # BBB: what to do if the action is someway triggered by anonymous?
    if portal_state.anonymous():
        annotations['rt.lastmodifier']['lastmodifier'] = 'anonymous'
    else:
        annotations['rt.lastmodifier']['lastmodifier'] = portal_state.member().getId()
