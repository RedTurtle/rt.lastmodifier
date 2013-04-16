# -*- coding: utf-8 -*-

from zExceptions import BadRequest

from collective.lastmodifier import logger

def _removeProperty(portal):
    try:
        portal.portal_properties.site_properties.manage_delProperties(['displayLastModifierInByline'])
        logger.info("Removed property displayLastModifierInByline")
    except BadRequest:
        pass

def uninstall(portal, reinstall=False):
    if not reinstall:
        # Don't want to delete stuff on reinstall
        setup_tool = portal.portal_setup
        setup_tool.runAllImportStepsFromProfile('profile-collective.lastmodifier:uninstall')
        _removeProperty(portal)
        logger.info("Uninstalled")
