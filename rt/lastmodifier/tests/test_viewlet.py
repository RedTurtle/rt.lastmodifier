# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from DateTime import DateTime
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from Products.CMFCore.utils import getToolByName
from pyquery import PyQuery
from rt.lastmodifier.interfaces import ILastModifierInertContent
from rt.lastmodifier.testing import RT_LASTMODIFIER_INTEGRATION_TESTING
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from plone import api

import unittest


class TestViewlet(unittest.TestCase):
    """Test that viewlet renders correctly."""

    layer = RT_LASTMODIFIER_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer['request']
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request.set('ACTUAL_URL', 'http://nohost/plone/document1')
        acl_users = getToolByName(self.portal, 'acl_users')

        acl_users.userFolderAddUser('user1', 'secret', ['Member'], [])

    def test_author(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(
            type_name='Document', id='document1', title="Document 1"
        )
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        self.assertTrue('documentAuthor' in portal.document1())

    def test_author_anonymous(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(
            type_name='Document', id='document1', title="Document 1"
        )
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        logout()
        self.assertFalse('documentAuthor' in portal.document1())

    def test_published_date(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(
            type_name='Document', id='document1', title="Document 1"
        )
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.setEffectiveDate(DateTime())
        portal.document1.reindexObject()
        self.assertTrue('documentPublished' in portal.document1())

    def test_published_date_anonymous(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(
            type_name='Document', id='document1', title="Document 1"
        )
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.setEffectiveDate(DateTime())
        portal.document1.reindexObject()
        logout()
        self.assertFalse('documentPublished' in portal.document1())

    def test_modified_date(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(
            type_name='Document', id='document1', title="Document 1"
        )
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        self.assertTrue('documentModified' in portal.document1())

    def test_modified_date_anonymous(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(
            type_name='Document', id='document1', title="Document 1"
        )
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        logout()
        self.assertFalse('documentModified' in portal.document1())

    def test_same_creator_and_modifier(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(
            type_name='Document', id='document1', title="Document 1"
        )
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        self.assertFalse('documentModifier' in portal.document1())

    def test_same_creator_and_modifier_anonymous(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(
            type_name='Document', id='document1', title="Document 1"
        )
        portal.portal_workflow.doActionFor(portal.document1, 'publish')
        portal.document1.reindexObject()
        logout()
        self.assertFalse('documentModifier' in portal.document1())

    # def test_different_creator_and_modifier(self):
    #     portal = self.layer['portal']
    #     login(portal, TEST_USER_NAME)
    #     portal.invokeFactory(
    #         type_name='Document', id='document1', title="Document 1"
    #     )
    #     logout()
    #     login(portal, 'user1')
    #     portal.portal_workflow.doActionFor(portal.document1, 'publish')
    #     portal.document1.reindexObject()
    #     pq = PyQuery(portal.document1())
    #     self.assertEqual(len(pq(".documentModifier")), 1)
    #     self.assertEqual(pq(".documentModifier").text(), 'by User 1')
    #     self.assertEqual(
    #         pq(".documentModifier a").attr('href'),
    #         'http://nohost/%s/author/user1' % portal.getId(),
    #     )

    # def test_different_creator_and_modifier_anonymous(self):
    #     portal = self.layer['portal']
    #     login(portal, TEST_USER_NAME)
    #     portal.invokeFactory(
    #         type_name='Document', id='document1', title="Document 1"
    #     )
    #     logout()
    #     login(portal, 'user1')
    #     portal.portal_workflow.doActionFor(portal.document1, 'publish')
    #     portal.document1.reindexObject()
    #     logout()
    #     self.assertFalse('documentModifier' in portal.document1())

    # def test_changenote(self):
    #     portal = self.layer['portal']
    #     login(portal, TEST_USER_NAME)
    #     portal.invokeFactory(
    #         type_name='Document', id='document1', title="Document 1"
    #     )
    #     # simulate the change
    #     portal.portal_archivist.prepare(portal.document1)
    #     # we need to manually simulate what JavaScript trick will do
    #     portal.document1.getField('hidden_cmfeditions_version_comment').set(
    #         portal.document1, 'Done something evil'
    #     )
    #     self.assertTrue(
    #         '<em class="documentModifierChanges"> Done something evil </em>'
    #         in portal.document1()
    #     )

    def test_calling_manage_viewlets(self):
        # Prevent regression introduced in version 0.4
        portal = self.layer['portal']
        request = self.layer['request']
        login(portal, TEST_USER_NAME)
        view = getMultiAdapter((portal, request), name='manage-viewlets')
        self.assertTrue('plone.belowcontenttitle.documentbyline' in view())

    # def test_byline_on_folder(self):
    #     portal = self.layer['portal']
    #     plone_utils = getToolByName(portal, 'plone_utils')
    #     login(portal, TEST_USER_NAME)
    #     portal.invokeFactory(
    #         type_name='Folder', id='folder', title="The Main Folder"
    #     )
    #     portal.folder.invokeFactory(
    #         type_name='Document',
    #         id='doc1',
    #         title="Document 1",
    #         text="Lorem Ipsum",
    #     )
    #     logout()
    #     login(portal, 'user1')
    #     with api.env.adopt_roles(['Contributor', 'Editor']):
    #         portal.folder.invokeFactory(
    #             type_name='Document',
    #             id='doc2',
    #             title="Document 2",
    #             text="Dolor Sit Amet",
    #         )
    #         folder_mod_date = portal.folder.modified()
    #         # Simulate that document has been created later that folder
    #         portal.folder.doc2.setModificationDate(folder_mod_date + 1)
    #         portal.folder.doc2.reindexObject(idxs=['modified', 'Modifier'])
    #     doc_mod_date = portal.folder.doc2.modified()
    #     pq = PyQuery(portal.folder())
    #     date_str = plone_utils.toLocalizedTime(doc_mod_date, long_format=1)
    #     self.assertTrue(
    #         "last modified %s" % date_str in pq('.documentModified').text()
    #     )
    #     self.assertTrue('by User 1' in pq('.documentModified').text())

    # def test_raw_lastmodifier(self):
    #     # By default folder do not have any versioning support
    #     portal = self.layer['portal']
    #     login(portal, TEST_USER_NAME)
    #     portal.invokeFactory(
    #         type_name='Folder', id='folder', title="The Main Folder"
    #     )
    #     logout()
    #     login(portal, 'user1')
    #     portal.folder.edit(description="Dolor Sit Amet")
    #     pq = PyQuery(portal.folder())
    #     self.assertTrue('by User 1' in pq('.documentModified').text())

    # def test_byline_on_site_root(self):
    #     # Do not display anything
    #     portal = self.layer['portal']
    #     login(portal, TEST_USER_NAME)
    #     pq = PyQuery(portal())
    #     self.assertFalse('last modified' in pq('.documentModified').text())

    # def test_disable_byline(self):
    #     portal = self.layer['portal']
    #     login(portal, TEST_USER_NAME)
    #     portal.invokeFactory(
    #         type_name='Document', id='doc', title="A document"
    #     )
    #     self.assertTrue('documentByLine' in portal.doc())
    #     alsoProvides(portal.doc, ILastModifierInertContent)
    #     self.assertFalse('documentByLine' in portal.doc())
