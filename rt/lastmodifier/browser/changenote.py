# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from plone.app.layout.viewlets.common import ViewletBase
from rt.lastmodifier import permissions


class ShowChangeNoteViewlet(ViewletBase):
    
    def changenote(self):
        """Get last saved change info"""
        field = self.context.getField('hidden_cmfeditions_version_comment')
        if field:
            return field.get(self.context)
        return None

    def can_change_change_note_show_state(self):
        sm = getSecurityManager()
        return sm.checkPermission(permissions.EditChangeNoteShowState,
                                  self.portal_state.portal())
