# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from base import BaseTestCase
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import logout
from pyquery import PyQuery
from rt.lastmodifier.testing import LAST_MODIFIER_INTEGRATION_TESTING
from zope.component import getMultiAdapter


class TestViewlet(BaseTestCase):

    layer = LAST_MODIFIER_INTEGRATION_TESTING

    def setUp(self):
        self.markRequestWithLayer()
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/document1')

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
        self.assertFalse('documentAuthor' in portal.document1())

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
        self.assertFalse('documentPublished' in portal.document1())

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
        self.assertFalse('documentModified' in portal.document1())

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
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        logout()
        login(portal, 'user1')
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        logout()
        self.assertFalse('documentModifier' in portal.document1())

    def test_changenote(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Document', id='document1', title="Document 1", text="foo")
        # simulate the change
        portal.portal_archivist.prepare(portal.document1)
        # we need to manually simulate what JavaScript trick will do
        portal.document1.getField('hidden_cmfeditions_version_comment').set(portal.document1,
                                                                            'Done something evil')
        self.assertTrue('<em class="documentModifierChanges"> Done something evil </em>' in portal.document1())

    def test_calling_manage_viewlets(self):
        # Prevent regression introduced in version 0.4
        portal = self.layer['portal']
        request = self.layer['request']
        login(portal, TEST_USER_NAME)
        view = getMultiAdapter((portal, request), name='manage-viewlets')
        self.assertTrue('plone.belowcontenttitle.documentbyline' in view())

    def test_byline_on_folder(self):
        portal = self.layer['portal']
        plone_utils = getToolByName(portal, 'plone_utils')
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='Folder', id='folder', title="The Main Folder")
        portal.folder.invokeFactory(type_name='Document', id='doc1', title="Document 1",
                                    text="Lorem Ipsum")
        logout()
        login(portal, 'user1')
        portal.folder.invokeFactory(type_name='Document', id='doc2', title="Document 2",
                                    text="Dolor Sit Amet")
        folder_mod_date = portal.folder.modified()
        # Simulate that document has been created later that folder
        portal.folder.doc2.setModificationDate(folder_mod_date + 1)
        portal.folder.doc2.reindexObject(idxs=['modified', 'Modifier'])
        doc_mod_date = portal.folder.doc2.modified()
        pq = PyQuery(portal.folder())
        date_str = plone_utils.toLocalizedTime(doc_mod_date, long_format=1)
        self.assertTrue("last modified %s" % date_str in pq('.documentModified').text())
        self.assertTrue('by User 1' in pq('.documentModified').text())
