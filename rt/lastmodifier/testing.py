# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import rt.lastmodifier


class RtLastmodifierLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=rt.lastmodifier)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'rt.lastmodifier:default')


RT_LASTMODIFIER_FIXTURE = RtLastmodifierLayer()


RT_LASTMODIFIER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RT_LASTMODIFIER_FIXTURE,),
    name='RtLastmodifierLayer:IntegrationTesting',
)


RT_LASTMODIFIER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RT_LASTMODIFIER_FIXTURE,),
    name='RtLastmodifierLayer:FunctionalTesting',
)


RT_LASTMODIFIER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        RT_LASTMODIFIER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='RtLastmodifierLayer:AcceptanceTesting',
)
