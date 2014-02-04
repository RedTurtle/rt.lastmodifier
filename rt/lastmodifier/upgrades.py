# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from rt.lastmodifier import logger

default_profile = 'profile-rt.lastmodifier:default'


def to_1001(context):
    context.runImportStepFromProfile(default_profile, 'rolemap')
    cleanPortalProperties(context)
    logger.info('Upgraded to version 0.3')


def cleanPortalProperties(context):
    """
    """
    ptool = getToolByName(context, 'portal_properties')
    props = ptool.site_properties
    if props.hasProperty('displayLastModifierInByline'):
        logger.info('Removing unused portal_properties and set new roles')
        props.manage_delProperties(ids=['displayLastModifierInByline'])
