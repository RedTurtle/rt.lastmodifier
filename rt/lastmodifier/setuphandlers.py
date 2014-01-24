# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from rt.lastmodifier import logger


# form : http://maurits.vanrees.org/weblog/archive/2009/12/catalog
def addKeyToCatalog(portal):
    '''Takes portal_catalog and adds a key to it
    @param portal: context providing portal_catalog
    '''

    catalog = getToolByName(portal, 'portal_catalog')
    indexes = catalog.indexes()
    # Specify the indexes you want, with ('index_name', 'index_type')

    indexables = []

    WANTED_INDEXES = (('Modifier', 'FieldIndex'),)

    for name, meta_type in WANTED_INDEXES:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)
    if len(indexables) > 0:
        logger.info("Indexing new index: %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def setupVarious(context):
    if context.readDataFile('rt.lastmodifier_various.txt') is None:
        return
    portal = context.getSite()
    addKeyToCatalog(portal)
