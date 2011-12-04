import unittest2 as unittest
from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, setRoles, login
from Products.CMFContentPanels.testing import CMFCONTENTPANELS_INTEGRATION_TESTING


class ContentPanelTest(unittest.TestCase):

    layer = CMFCONTENTPANELS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory(id='doc1',
                                  title='Document 1',
                                  type_name='Document')
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.document_brain = self.catalog.searchResults(
            portal_type = 'Document')[0]

    def test_factory(self):
        contentpanels1_id = self.portal.invokeFactory(id='cp1',
                                                  title='Content Panel 1',
                                                  type_name='ContentPanels')
        self.assertEqual(contentpanels1_id, 'cp1')
        self.assertIn('cp1', self.portal.objectIds())
        self.assertEqual(self.portal[contentpanels1_id].portal_type, 'ContentPanels')





def test_suite():
        return unittest.defaultTestLoader.loadTestsFromName(__name__)
