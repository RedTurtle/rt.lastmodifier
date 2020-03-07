# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces import ISiteSchema
from Products.CMFPlone.controlpanel.browser.site import SiteControlPanel as BaseSiteControlPanel


class SiteControlPanel(BaseSiteControlPanel):
    """
    Hide display_pub_date_in_byline field.
    Now we use the permissions
    """

    # form_fields = FormFields(ISiteSchema).omit('display_pub_date_in_byline')
    def updateFields(self):
        super(SiteControlPanel, self).updateFields()
        # nascondere il campo a mano
