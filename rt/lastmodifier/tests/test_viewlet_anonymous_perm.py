# -*- coding: utf-8 -*-
from base import BaseTestCase
from DateTime import DateTime
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import TEST_USER_NAME
from pyquery import PyQuery
from rt.lastmodifier.testing import LAST_MODIFIER_INTEGRATION_TESTING
from rt.lastmodifier.permissions import DocumentByLineViewAuthor, DocumentByLineViewLastModifier,\
                                        DocumentByLineViewModifiedDate, DocumentByLineViewPublishedDate


class TestViewletAnonymousPermissions(BaseTestCase):
    """
    Same test of test_viewlet.py, but now we add the permissions also to
    anonymous user
    """

    layer = LAST_MODIFIER_INTEGRATION_TESTING

    def setUp(self):
        self.markRequestWithLayer()
        request = self.layer['request']
        portal = self.layer['portal']
        request.set('ACTUAL_URL', 'http://nohost/plone/document1')
        for perm in [DocumentByLineViewAuthor,
                     DocumentByLineViewPublishedDate,
                     DocumentByLineViewModifiedDate,
                     DocumentByLineViewLastModifier]:

            portal.manage_permission(perm, roles=["Anonymous",
                                                  "Member",
                                                  "Manager",
                                                  "Site Administrator"])

    def test_author(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        self.assertTrue('documentAuthor' in portal.document1())

    def test_author_anonymous(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        logout()
        self.assertTrue('documentAuthor' in portal.document1())

    def test_published_date(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.setEffectiveDate(DateTime())
        portal.document1.reindexObject()
        self.assertTrue('documentPublished' in portal.document1())

    def test_published_date_anonymous(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.setEffectiveDate(DateTime())
        portal.document1.reindexObject()
        logout()
        self.assertTrue('documentPublished' in portal.document1())

    def test_modified_date(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        self.assertTrue('documentModified' in portal.document1())

    def test_modified_date_anonymous(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        logout()
        self.assertTrue('documentModified' in portal.document1())

    def test_same_creator_and_modifier(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        self.assertFalse('documentModifier' in portal.document1())

    def test_same_creator_and_modifier_anonymous(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        logout()
        self.assertFalse('documentModifier' in portal.document1())

    def test_different_creator_and_modifier(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        logout()
        login(portal, 'user1')
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        pq = PyQuery(portal.document1())
        self.assertEqual(len(pq(".documentModifier")), 1)
        self.assertEqual(pq(".documentModifier").text(), 'by User 1')
        self.assertEqual(pq(".documentModifier a").attr('href'),
                         'http://nohost/%s/author/user1' % portal.getId())

    def test_different_creator_and_modifier_anonymous(self):
        """
        This test also fails because anonymous user can't access to object's history
        to get last modifier
        """
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        logout()
        login(portal, 'user1')
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        logout()
        pq = PyQuery(portal.document1())
        self.assertEqual(len(pq(".documentModifier")), 1)
