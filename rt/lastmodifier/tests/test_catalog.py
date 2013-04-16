# -*- coding: utf-8 -*-

import zope.event

from zope.component import getMultiAdapter

from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID

from Products.Archetypes.interfaces import IObjectEditedEvent
from Products.Archetypes.event import ObjectEditedEvent

from rt.lastmodifier.testing import LAST_MODIFIER_INTEGRATION_TESTING

from base import BaseTestCase

class TestCatalogIntegration(BaseTestCase):

    layer = LAST_MODIFIER_INTEGRATION_TESTING

    def setUp(self):
        self.markRequestWithLayer()

    def test_first_modifier_is_creator(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        catalog = portal.portal_catalog
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        results = catalog(Modifier=TEST_USER_ID)
        self.assertTrue(len(results)==1)
        self.assertEqual(results[0].Title, 'Document 1')
        self.assertEqual(results[0].Modifier, TEST_USER_ID)

    def test_modifier_updated_on_edit(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        catalog = portal.portal_catalog
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        logout()
        login(portal, 'user1')
        portal.document1.edit(text='bar')
        event = ObjectEditedEvent(portal.document1)
        zope.event.notify(event)
        portal.document1.reindexObject()
        self.assertTrue(len(catalog(Modifier=TEST_USER_NAME))==0)
        self.assertTrue(len(catalog(Modifier='user1'))==1)
        results = catalog(Modifier='user1')
        self.assertEqual(results[0].Title, 'Document 1')
        self.assertEqual(results[0].Modifier, 'user1')

    def test_modifier_updated_on_workflow_change(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        catalog = portal.portal_catalog
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        logout()
        login(portal, 'user1')
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        results = catalog(Modifier='user1')
        self.assertEqual(results[0].Title, 'Document 1')
        self.assertEqual(results[0].Modifier, 'user1')
