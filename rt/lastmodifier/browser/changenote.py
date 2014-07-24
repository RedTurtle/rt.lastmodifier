# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from plone.app.layout.viewlets.common import ViewletBase
from rt.lastmodifier import permissions


class ShowChangeNoteViewlet(ViewletBase):
    
    def changenote(self):
        """Get last saved change info"""
        context = self.context
        if not hasattr(context, 'getField'):
            return None
        field = context.getField('hidden_cmfeditions_version_comment')
        if field:
            return field.get(context)
        return None

    def can_change_change_note_show_state(self):
        sm = getSecurityManager()
        return sm.checkPermission(permissions.EditChangeNoteShowState,
                                  self.portal_state.portal())
