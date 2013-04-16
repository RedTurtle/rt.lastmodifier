# -*- coding: utf-8 -*-

from pyquery import PyQuery

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

class TestViewlet(BaseTestCase):

    layer = LAST_MODIFIER_INTEGRATION_TESTING

    def setUp(self):
        self.markRequestWithLayer()
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/document1')

    def test_same_creator_and_modifier_1(self):
        portal = self.layer['portal']
        request = self.layer['request']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        self.assertFalse('documentModifier' in portal.document1())

    def test_same_creator_and_modifier_2(self):
        portal = self.layer['portal']
        request = self.layer['request']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        portal.portal_properties.site_properties.displayLastModifierInByline = True
        self.assertFalse('documentModifier' in portal.document1())

    def test_different_creator_and_modifier_1(self):
        portal = self.layer['portal']
        request = self.layer['request']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        logout()
        login(portal, 'user1')
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        self.assertFalse('documentModifier' in portal.document1())

    def test_different_creator_and_modifier_2(self):
        portal = self.layer['portal']
        request = self.layer['request']
        portal_url = 'http://nohost/%s' % portal.getId()
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        logout()
        login(portal, 'user1')
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        portal.portal_properties.site_properties.displayLastModifierInByline = True
        pq = PyQuery(portal.document1())
        self.assertEqual(len(pq(".documentModifier")), 1)
        self.assertEqual(pq(".documentModifier").text(), 'by User 1')
        self.assertEqual(pq(".documentModifier a").attr('href'),
                         'http://nohost/%s/author/user1' % portal.getId())
