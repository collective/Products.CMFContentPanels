from zope.interface import implements
from Globals import InitializeClass, DTMLFile
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Acquisition import Implicit, aq_base
from cgi import escape

from Products.CMFCore.utils import UniqueObject, getToolByName
from Products.CMFCore.permissions import ManagePortal, ModifyPortalContent

from Products.CMFCore.ActionInformation import ActionInformation
from Products.CMFCore.ActionsTool import ActionsTool
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.Expression import Expression
try:
    from Products.CMFPlone.migrations.migration_util import safeEditProperty
except ImportError:
    # Plone 4
    from plone.app.upgrade.utils import safeEditProperty

from Products.CMFContentPanels.interfaces import IContentPanelsTool

viewlet_registery = []
def registerViewlets(actions):
    for action in actions:
        viewlet_registery.append(action)

class ContentPanelsTool( UniqueObject, SimpleItem, PropertyManager, ActionsTool ):

    id = 'portal_contentpanels'
    meta_type = 'ContentPanels Tool'
    _actions = tuple()

    action_providers = ('portal_contentpanels',)
    security = ClassSecurityInfo()
    implements(IContentPanelsTool)
    
    manage_options = (ActionProviderBase.manage_options +
                #     ({ 'label' : 'Overview', 'action' : 'manage_overview' }
                #     , 
                #     ) + 
                     PropertyManager.manage_options +
                     ({ 'label' : 'Install All Viewlets', 'action' : 'manage_installAllViewlets' }, ) + 
                     SimpleItem.manage_options)

    def __init__(self):
        self._setProperty('defaultPortletWrapper', 'Default', 'string')
        self._setProperty('notitlePortletWrapper', 'No Title', 'string')
        self._setProperty('zopezenPortletWrapper', 'ZopeZen', 'string')
        self._setProperty('boxPortletWrapper', 'Default Box', 'string')
        self._setProperty('alertPortletWrapper', 'Alert', 'string')
        self._setProperty('dottedPortletWrapper', 'Dotted', 'string')
        self._setProperty('roundedPortletWrapper', 'Rounded', 'string')
        self._setProperty('templates', [], 'lines')

    def valid_property_id(self, id):
        if not id or id[:1]=='_' or (id[:3]=='aq_') \
           or hasattr(aq_base(self), id) or escape(id) != id:
            return 0
        return 1

    security.declarePublic('getPanelSkins')
    def getPanelSkins(self):
        return [ (i[1], i[0]) for i in list(self.propertyItems()) if i[0] not in  ['title', 'templates'] ]

    security.declarePublic('getTemplates')
    def getTemplates(self):
        raw_templates = self.getProperty('templates', [])
        portal = getToolByName(self, 'portal_url').getPortalObject()
        templates = []
        for t in raw_templates:
            id, path, title = t.split('|')
            templates.append({'id':id, 'title':title, 'path':path})
        return templates

    security.declarePublic('getTemplateById')
    def getTemplateById(self, id):
        if not id:
            return None
        raw_templates = self.getProperty('templates', [])
        portal = getToolByName(self, 'portal_url').getPortalObject()
        for t in raw_templates:
            _id, path, title = t.split('|')
            if id == _id:
                try:
                    obj = portal.unrestrictedTraverse(path)
                    return obj
                except AttributeError:
                    return None

    def getTemplateInfo(self, obj):
        url = getToolByName(self, 'portal_url').getRelativeContentURL(obj)
        raw_templates = self.getProperty('templates', [])
        for t in raw_templates:
            id, path, title = t.split('|')
            if path == url:
                return {'id':id, 'title':title}
        return None

    security.declareProtected(ManagePortal, 'setTemplate')
    def setTemplate(self, id, title, obj):
        raw_templates = list(self.getProperty('templates', []))
        url = getToolByName(self, 'portal_url').getRelativeContentURL(obj)
        filtered = []
        added = False
        for t in raw_templates:
            _id, path, _title = t.split('|')
            if path == url:
                filtered.append("%s|%s|%s" % (id, url, title))
                added = True
            elif _id == id:
                raise "Duplicated tempalte id!"
            else:
                filtered.append(t)
        if not added:
            filtered.append("%s|%s|%s" % (id, url, title))
        safeEditProperty(self, 'templates', filtered, 'lines')

    security.declareProtected(ManagePortal, 'removeFromTemplates')
    def removeFromTemplates(self, ids):
        raw_templates = self.getProperty('templates', [])
        filtered = []
        for t in raw_templates:
            id, path, title = t.split('|')
            if id not in ids:
                filtered.append(t)
        safeEditProperty(self, 'templates', filtered, 'lines')

    def installActions(self, actions=[]):
        for action in actions:
            if not self.getViewletAction(action[0]):
                self.addAction(action[0],action[1],action[2],
                           action[3],action[4],action[5],action[6])

    security.declareProtected(ManagePortal, 'manage_installAllViewlets')
    def manage_installAllViewlets(self, REQUEST = None):
        """reinstall all registered actions
        """
        self.installActions(viewlet_registery)
        if REQUEST:
            REQUEST.RESPONSE.redirect('manage_editActionsForm')

    security.declarePublic('getViewletAction')
    def getViewletAction(self, viewletId, actions_dict=None):
        """get a name of a viewlet"""
        if actions_dict is None:
            actions_dict = self.listFilteredActionsFor()

        for actions in actions_dict.values():
            for action in actions:
                if action['id'] == viewletId:
                    return action
        return None

    security.declarePublic('getViewletName')
    def getViewletName(self, viewletId, actions_dict=None):
        """get a name of a viewlet"""
        action = self.getViewletAction(viewletId, actions_dict)
        if action:
             return action['title']
        return None

    security.declarePublic('getViewletPath')
    def getViewletPath(self, viewletId, actions_dict=None):
        """get a name of a viewlet"""
        action = self.getViewletAction(viewletId, actions_dict)
        if action:
            return action['url']
        return None

InitializeClass( ContentPanelsTool )
