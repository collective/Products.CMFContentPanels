from Products.CMFCore.utils import getToolByName

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig

class CMFContentPanels(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    USER_NAME = 'johndoe'
    USER_PASSWORD = 'secret'
    MEMBER_NAME = 'janedoe'
    MEMBER_PASSWORD = 'secret'
    USER_WITH_FULLNAME_NAME = 'freddie'
    USER_WITH_FULLNAME_FULLNAME = 'Freddie Mercury'
    USER_WITH_FULLNAME_PASSWORD = 'secret'
    MANAGER_USER_NAME = 'manager'
    MANAGER_USER_PASSWORD = 'secret'

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.CMFContentPanels
        xmlconfig.file('configure.zcml',
                       Products.CMFContentPanels,
                       context=configurationContext)
        with z2.zopeApp() as app:
                z2.installProduct(app, 'Products.CMFContentPanels')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'Products.CMFContentPanels:default')
        # Creates some users
        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser(
            self.USER_NAME,
            self.USER_PASSWORD,
            [],
            [],
        )
        acl_users.userFolderAddUser(
            self.MEMBER_NAME,
            self.MEMBER_PASSWORD,
            ['Member'],
            [],
        )
        acl_users.userFolderAddUser(
            self.USER_WITH_FULLNAME_NAME,
            self.USER_WITH_FULLNAME_PASSWORD,
            ['Member'],
            [],
        )
        mtool = getToolByName(portal, 'portal_membership', None)
        mtool.addMember(self.USER_WITH_FULLNAME_NAME, self.USER_WITH_FULLNAME_NAME, ['Member'], [])
        mtool.getMemberById(self.USER_WITH_FULLNAME_NAME).setMemberProperties({"fullname":
                                                                               self.USER_WITH_FULLNAME_FULLNAME})

        acl_users.userFolderAddUser(
            self.MANAGER_USER_NAME,
            self.MANAGER_USER_PASSWORD,
            ['Manager'],
            [],
        )

CMFCONTENTPANELS_FIXTURE = CMFContentPanels()
CMFCONTENTPANELS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CMFCONTENTPANELS_FIXTURE,),
    name="CMFContentPanels:Integration")
CMFCONTENTPANELS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CMFCONTENTPANELS_FIXTURE,),
    name="CMFContentPanels:Functional")

