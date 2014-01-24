# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from rt.lastmodifier import logger

default_profile = 'profile-rt.lastmodifier:default'


def to_1001(context):
    """
    """
    logger.info('Upgrading rt.lastmodifier to version 1001: removing unused portal_properties and set new roles')
    context.runImportStepFromProfile(default_profile, 'rolemap')
    cleanPortalProperties(context)
    logger.info('upgrade done')


def cleanPortalProperties(context):
    """
    """
    ptool = getToolByName(context, 'portal_properties')
    props = ptool.site_properties
    if props.hasProperty('displayLastModifierInByline'):
        props.manage_delProperties(ids=['displayLastModifierInByline'])
