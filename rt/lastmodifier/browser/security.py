# -*- coding: utf-8 -*-

from plone.app.controlpanel.security import ISecuritySchema
from plone.app.controlpanel.security import SecurityControlPanel as BaseSecurityControlPanel
from zope.formlib.form import FormFields


class SecurityControlPanel(BaseSecurityControlPanel):
    """
    Hide allow_anon_views_about field.
    Now we use the permissions
    """

    form_fields = FormFields(ISecuritySchema).omit('allow_anon_views_about')
