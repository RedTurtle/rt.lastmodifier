# -*- coding: utf-8 -*-

from plone.app.controlpanel.site import ISiteSchema
from plone.app.controlpanel.site import SiteControlPanel as BaseSiteControlPanel
from zope.formlib.form import FormFields


class SiteControlPanel(BaseSiteControlPanel):
    """
    Hide display_pub_date_in_byline field.
    Now we use the permissions
    """

    form_fields = FormFields(ISiteSchema).omit('display_pub_date_in_byline')
