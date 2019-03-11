# -*- coding: utf-8 -*-

from plone.app.controlpanel.security import ISecuritySchema
from plone.app.controlpanel.security import SecurityControlPanel as BaseSecurityControlPanel


class SecurityControlPanel(BaseSecurityControlPanel):
    """
    Hide allow_anon_views_about field.
    Now we use the permissions
    """

    # form_fields = FormFields(ISecuritySchema).omit('allow_anon_views_about')
    def updateFields(self):
        super(SiteControlPanel, self).updateFields()
        # nascondere il campo a mano
