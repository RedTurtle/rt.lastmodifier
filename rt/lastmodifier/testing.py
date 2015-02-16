# -*- coding: utf-8 -*-

from zope.configuration import xmlconfig

from plone.testing import z2

from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

class LastModifierLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import rt.lastmodifier
        xmlconfig.file('configure.zcml',
                       rt.lastmodifier,
                       context=configurationContext)
        z2.installProduct(app, 'rt.lastmodifier')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'rt.lastmodifier:default')
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        #quickInstallProduct(portal, 'rt.lastmodifier')
        setRoles(portal, TEST_USER_ID, ['Member', 'Manager'])
        acl_users = portal.acl_users
        acl_users.userFolderAddUser('user1', 'secret', ['Member'], [])
        member = portal.portal_membership.getMemberById('user1')
        member.setMemberProperties(mapping={"fullname": "User 1"})
        setRoles(portal, 'user1', ['Member', 'Contributor', 'Editor', 'Reviewer'])


LAST_MODIFIER_FIXTURE = LastModifierLayer()
LAST_MODIFIER_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(LAST_MODIFIER_FIXTURE, ),
                       name="LastModifier:Integration")
LAST_MODIFIER_FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(LAST_MODIFIER_FIXTURE, ),
                       name="LastModifier:Functional")

