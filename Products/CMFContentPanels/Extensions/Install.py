from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFContentPanels.config import PROJECTNAME, GLOBALS, NEW_VIEW_METHODS
from Products.CMFContentPanels.config import PLONE_VERSION
from Products.CMFContentPanels.ContentPanelsTool import ContentPanelsTool

from Products.StandardCacheManagers import RAMCacheManager

from Acquisition import aq_base
from cStringIO import StringIO
import string

from Acquisition import Implicit
import Persistence

def install_RSSCache(portal, out):
    if 'RSSCache' not in portal.objectIds():
        RAMCacheManager.manage_addRAMCacheManager(portal, 'RSSCache')

    portal.RSSCache.manage_editProps('RSSCache for getRSSResult', \
             settings={ 'threshold':1000,
                        'request_vars':['itemCount', 'rssUrl'],
                        'cleanup_interval':300,
                        'max_age':3600})
    out.write( "added and initalized RAMCache" )

def install_default_page(portal, out):
    site_props = getToolByName(portal, 'portal_properties').site_properties
    dpt = site_props.getProperty('default_page_types', None)
    if dpt is None:
        return
    if 'ContentPanels' not in dpt:
        site_props._setPropValue('default_page_types', list(dpt) + ['ContentPanels'])

def addViewMethods(portal, out):
    portal_types = getToolByName(portal, 'portal_types')

    for portal_type, view_methods in NEW_VIEW_METHODS.items():
        ti = portal_types.getTypeInfo(portal_type)
        real_new_methods = [method for method in view_methods if method not in ti.view_methods]
        if real_new_methods:
            ti.view_methods += tuple(real_new_methods)

def resetContentPanelsPermissions(portal, out):
    permissions = ['Access contents information', 'Modify portal content', 'View']
    portal_catalog = portal.portal_catalog
    brains = portal_catalog(portal_type="ContentPanels")
    for brain in brains:
        obj = brain.getObject()
        for perm in permissions:
            obj.manage_permission(perm, acquire=1)
        portal_catalog.catalog_object(obj, None)

def install(self, reinstall=False):
    
    out = StringIO()
    out.write( 'CMFContentPanels installation tool\n')
    
    portal = getToolByName(self, 'portal_url').getPortalObject()
    setup_tool = getToolByName(portal, 'portal_setup')
    if PLONE_VERSION >= 3:
        setup_tool.runAllImportStepsFromProfile(
                "profile-Products.CMFContentPanels:default",
                purge_old=False)
    else:
        factory_tool = getToolByName(self,'portal_factory')
        factory_types=[
            "ContentPanels",
            ] + factory_tool.getFactoryTypes().keys()
        factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=factory_types)
    
        installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
        install_subskin(self, out, GLOBALS)
    
        if not hasattr(portal, 'portal_contentpanels'):
            portal._setObject( 'portal_contentpanels', ContentPanelsTool() )
            out.write('Added ConentPanels Tool\n')

    p_cp=getToolByName(self, 'portal_contentpanels')
    p_cp.manage_installAllViewlets()

    install_RSSCache(portal, out)
    install_default_page(portal, out)

    addViewMethods(portal, out)

    return out.getvalue()
