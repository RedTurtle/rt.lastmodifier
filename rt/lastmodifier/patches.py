# -*- coding: utf-8 -*-

from zope.annotation.interfaces import IAnnotations
from persistent.dict import PersistentDict
from plone import api


def notifyModified(self):
    # do all of the default stuff
    self._old_notifyModified()
    # now save the current userid as raw last modifier
    annotations = IAnnotations(self)
    annotations["rt.lastmodifier"] = PersistentDict()
    # BBB: what to do if the action is someway triggered by anonymous?
    if api.user.is_anonymous():
        annotations["rt.lastmodifier"]["lastmodifier"] = "anonymous"
    else:
        annotations["rt.lastmodifier"]["lastmodifier"] = api.user.get_current().getId()
