from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFContentPanels.config import PROJECTNAME, GLOBALS, STYLESHEETS, JAVASCRIPTS, NEW_VIEW_METHODS, ACTION_ICONS
from Products.CMFContentPanels.ContentPanelsTool import ContentPanelsTool

from Products.ExternalMethod import ExternalMethod
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

def install_actions(self, out):
    ai = getToolByName(self, 'portal_actionicons')
    for category, config in ACTION_ICONS.items():
        for icon_id, info in config.items():
            if ai.queryActionIcon(category, icon_id, None) is None:
                ai.addActionIcon(category, icon_id,
                                 info[0], info[1])
                print >> out, ('Installed action icon '
                               'for %s.' % info[1])
            else:
                print >> out, ('Action Icon for %s '
                               'was already Installed.'
                               % info[1])

def install_portal_css(portal, out):
    portal_css = getToolByName(portal, 'portal_css')
    for stylesheet in STYLESHEETS:
        try:
            portal_css.unregisterResource(stylesheet['id'])
        except:
            pass
        defaulttitle = '%s %s' % (PROJECTNAME, stylesheet['id'])
        defaults = {'id': '',
            'expression': None,
            'media': 'all',
            'title': defaulttitle,
            'enabled': True}
        defaults.update(stylesheet)
        portal_css.manage_addStylesheet(**defaults)

def install_portal_js(portal, out):
    portal_js = getToolByName(portal, 'portal_javascripts')
    for js in JAVASCRIPTS:
        try:
            portal_js.unregisterResource(js['id'])
        except:
            pass
        defaults = {'id': '',
            'enabled': True}
        defaults.update(js)
        portal_js.manage_addScript(**defaults)

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
    portal = getToolByName(self, 'portal_url').getPortalObject()

    out = StringIO()
    out.write( 'CMFContentPanels installation tool\n')

    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    install_subskin(self, out, GLOBALS)

    if not hasattr(portal, 'portal_contentpanels'):
        portal._setObject( 'portal_contentpanels', ContentPanelsTool() )
        out.write('Added ConentPanels Tool\n')

    p_cp=getToolByName(self, 'portal_contentpanels')
    p_cp.manage_installAllViewlets()

    install_RSSCache(portal, out)
    install_default_page(portal, out)
    install_portal_css(portal, out)
    install_portal_js(portal, out)

    factory_tool = getToolByName(self,'portal_factory')
    factory_types=[
        "ContentPanels",
        ] + factory_tool.getFactoryTypes().keys()
    factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=factory_types)

    # contentpanels don't need any workflow
    # it is more like some template
    # if not reinstall:
    #    wftool = getToolByName(portal, 'portal_workflow')
    #    wftool.setChainForPortalTypes(('ContentPanels',), '')

    addViewMethods(portal, out)
    install_actions(portal, out)

    # resetContentPanelsPermissions(portal, out)

    return out.getvalue()
