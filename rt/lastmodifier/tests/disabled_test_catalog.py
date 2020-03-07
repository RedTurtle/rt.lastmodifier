# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from rt.lastmodifier.testing import RT_LASTMODIFIER_INTEGRATION_TESTING
from rt.lastmodifier.tests.base import BaseTestCase
from zope.lifecycleevent import ObjectModifiedEvent
from plone.dexterity.events import EditFinishedEvent
from transaction import commit

import zope.event


class TestCatalogIntegration(BaseTestCase):

    layer = RT_LASTMODIFIER_INTEGRATION_TESTING

    def setUp(self):
        self.markRequestWithLayer()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        acl_users = api.portal.get_tool(name='acl_users')
        acl_users.userFolderAddUser('user1', 'secret', ['Member'], [])

    def test_first_modifier_is_creator(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        catalog = portal.portal_catalog
        portal.invokeFactory(
            type_name='Document',
            id='document1',
            title="Document 1",
            text="foo",
        )
        results = catalog(Modifier=TEST_USER_ID)
        self.assertTrue(len(results) == 1)
        self.assertEqual(results[0].Title, 'Document 1')
        self.assertEqual(results[0].Modifier, TEST_USER_ID)

    def test_modifier_updated_on_edit(self):
        portal = self.layer['portal']
        login(portal, 'user1')
        catalog = portal.portal_catalog
        with api.env.adopt_roles(['Contributor']):
            portal.invokeFactory(
                type_name='Document',
                id='document1',
                title="Document 1",
                text="foo",
            )
        logout()
        login(portal, TEST_USER_NAME)
        portal.document1.description = 'bar'
        event = ObjectModifiedEvent(portal.document1)
        zope.event.notify(event)
        portal.document1.reindexObject()
        commit()
        import pdb

        pdb.set_trace()
        self.assertTrue(len(catalog(Modifier=TEST_USER_NAME)) == 0)
        self.assertTrue(len(catalog(Modifier='user1')) == 1)
        results = catalog(Modifier='user1')
        self.assertEqual(results[0].Title, 'Document 1')
        self.assertEqual(results[0].Modifier, 'user1')

    def test_modifier_updated_on_workflow_change(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        catalog = portal.portal_catalog
        portal.invokeFactory(
            type_name='Document',
            id='document1',
            title="Document 1",
            text="foo",
        )
        logout()
        login(portal, 'user1')
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        results = catalog(Modifier='user1')
        self.assertEqual(results[0].Title, 'Document 1')
        self.assertEqual(results[0].Modifier, 'user1')
