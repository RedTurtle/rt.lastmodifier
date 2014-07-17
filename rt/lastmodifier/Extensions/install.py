# -*- coding: utf-8 -*-

try:
    import plone.app.querystring
    QS = True
except ImportError:
    QS = False

from rt.lastmodifier import logger
from zExceptions import BadRequest


def _removeProperty(portal):
    try:
        portal.portal_properties.site_properties.manage_delProperties(['displayLastModifierInByline'])
        logger.info("Removed property displayLastModifierInByline")
    except BadRequest:
        pass

def install(portal):
    # keep this until we want to support Plone < 4.2
    setup_tool = portal.portal_setup
    setup_tool.runAllImportStepsFromProfile('profile-rt.lastmodifier:default')
    if QS:
        setup_tool.runAllImportStepsFromProfile('profile-rt.lastmodifier:new-collection')
    logger.info("Installed")

def uninstall(portal, reinstall=False):
    if not reinstall:
        # Don't want to delete stuff on reinstall
        setup_tool = portal.portal_setup
        setup_tool.runAllImportStepsFromProfile('profile-rt.lastmodifier:uninstall')
        if QS:
            setup_tool.runAllImportStepsFromProfile('profile-rt.lastmodifier:new-collection-uninstall')
        _removeProperty(portal)
        logger.info("Uninstalled")
