# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from rt.lastmodifier import logger

default_profile = 'profile-rt.lastmodifier:default'


def cleanPortalProperties(context):
    """Removed unused portal properties"""
    ptool = getToolByName(context, 'portal_properties')
    props = ptool.site_properties
    if props.hasProperty('displayLastModifierInByline'):
        logger.info('Removing unused portal_properties and set new roles')
        props.manage_delProperties(ids=['displayLastModifierInByline'])

def to_1001(context):
    context.runImportStepFromProfile(default_profile, 'rolemap')
    cleanPortalProperties(context)
    logger.info('Upgraded to version 0.3')

def to_1010(context):
    context.runImportStepFromProfile(default_profile, 'rolemap')
    cleanPortalProperties(context)
    logger.info('Upgraded to version 0.3.1')

def to_1100(context):
    context.runAllImportStepsFromProfile('profile-rt.lastmodifier:to_1100')
    logger.info('Upgraded to version 0.4')
