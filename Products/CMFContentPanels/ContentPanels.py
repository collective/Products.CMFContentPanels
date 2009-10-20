##############################################################################
#
# Copyright (c) 2002 ZopeChina Corporation (http://www.zopechina.com). All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################

"""Implement the content panels content type."""
import pprint
from zope.interface import implements
from copy import deepcopy
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base, aq_parent, aq_inner
from Products.CMFCore import permissions
from Products.CMFContentPanels import MessageFactory as _

try:
    from Products.CMFPlone.migrations import v3_0
    del v3_0
    HAS_PLONE_3 = True
except ImportError:
    HAS_PLONE_3 = False

try:
    from Products.LinguaPlone.public import registerType, BaseContent
    from Products.LinguaPlone.public import BaseSchema, Schema
    from Products.LinguaPlone.public import StringField
    from Products.LinguaPlone.public import ReadOnlyStorage
    from Products.LinguaPlone.public import TextAreaWidget, SelectionWidget
except ImportError:
    from Products.Archetypes.public import registerType, BaseContent
    from Products.Archetypes.public import BaseSchema, Schema
    from Products.Archetypes.public import StringField
    from Products.Archetypes.public import ReadOnlyStorage
    from Products.Archetypes.public import TextAreaWidget, SelectionWidget

from Products.CMFContentPanels.interfaces import IContentPanels
from config import VOC_PAGE_LAYOUT, VOC_PORTLET_POS, PROJECTNAME

ContentPanelsSchema = BaseSchema.copy() + Schema((

    StringField(
        name='description',
        default='',
        searchable=True,
        accessor='Description',
        widget=TextAreaWidget(
            label_msgid='label_description',
            description_msgid='help_description',
            i18n_domain='plone',
        ),
    ),

    StringField(
        name='panelsConfig',
        edit_accessor='getPanelsConfig',
        widget=TextAreaWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),

    StringField(
        name='pageLayoutMode',
        default='tile',
        vocabulary=VOC_PAGE_LAYOUT,
        widget=SelectionWidget(
            label=_(u'label_page_layout_mode', u'Page layout mode'), #            label_msgid='label_page_layout_mode',
            description=_(u"help_page_layout_mode", u"You can choose 'tile mode' or 'tab mode'. With"
                         u"'tile mode', all pages are shown directly as rows. "
                         u"It is useful for you to make very complex composite "
                         u"page. With 'tab mode', you can switch pages using "
                         u"the top-right tab links."),  #           description_msgid="help_page_layout_mode",
            
        ),
    ),

    StringField(
        name='portletsPos',
        vocabulary=VOC_PORTLET_POS,
        edit_accessor='getPortletsPos',
        storage=ReadOnlyStorage(),
        widget=SelectionWidget(
            label=_(u"label_portlet_pos", u'Set to left/right column'), #         label_msgid=u'label_portlet_pos',
            description=_(u"help_portlet_pos", u"You can set this contentpanels as the left or "
                               u"right column of the template."), #           description_msgid="help_portlet_pos",
            i18n_domain='contentpanels',
        ),
    ),

    StringField(
        name='customCSS',
        widget=TextAreaWidget(
            label=_(u"label_custom_css", u'Custom CSS'), #             label_msgid='label_custom_css',
            description=_(u"help_custom_css", u"You can define custom CSS for this contentpanels "
                               u"here. Leave it blank if you don't know about CSS."), #            description_msgid='help_custom_css',
            i18n_domain='contentpanels',
        ),
    ),

))


class ContentPanels(BaseContent):
    """ContentPanels is a portlet content to build composite page."""

    schema = ContentPanelsSchema

    __implements__ = (getattr(BaseContent,'__implements__',()),)
    implements(IContentPanels)
    security = ClassSecurityInfo()
    archetype_name            = 'ContentPanels'
    meta_type                 = 'CMF Content Panels'
    portal_type               = 'ContentPanels'
    allowed_content_types     = []
    filter_content_types      = 0
    global_allow              = 1
    allow_discussion          = 0
    content_icon              = 'contentpanels_icon.gif'
    immediate_view            = 'contentpanels_edit_form'
    default_view              = 'contentpanels_view'
    suppl_views               = ()

    typeDescription           = "ContentPanels is a portlet content to build composite page."
    typeDescMsgId             = 'description_edit_contentpanels'

    _at_rename_after_creation = True

    actions = (
        { 'id': 'view',
          'name': 'View',
          'action': 'string:${object_url}/contentpanels_view',
          'permissions': (permissions.View,),
        },
        { 'id': 'layout',
          'name': 'Layout',
          'action': 'string:${object_url}/contentpanels_config_form',
          'permissions': (permissions.ModifyPortalContent,),
        },
        { 'id': 'templates',
          'name': 'Templates',
          'action': 'string:${object_url}/contentpanels_templates_form',
          'permissions': (permissions.ManagePortal,),
        },
    )

    if not HAS_PLONE_3:
        actions += (
            { 'id': 'local_roles',
              'name': 'Sharing',
              'action': 'string:${folder_url}/folder_localrole_form',
              'permissions': ('Manage properties',),
            },
        )

    aliases = {
        '(Default)': 'contentpanels_view',
        'view': '(Default)',
        'index.html': '(Default)',
        'edit': 'base_edit',
        'properties': 'base_metadata',
    }

    def __init__(self, oid, **kw):
        BaseContent.__init__(self, oid, **kw)
        self.clearPanels()
        self.addPage()

    security.declarePublic('ofContext')
    def ofContext(self, context):
        """ used when used as a template, return a contentpanels
        under the context of the new object """
        # create a new object to avoid any security problem
        new_cp = ContentPanels('tmp')
        new_cp.panelsConfig = deepcopy(self.panelsConfig)
        new_cp.pageLayoutMode = self.pageLayoutMode
        new_cp.customCSS = self.customCSS
        return new_cp.__of__(context)

    def getPanelsConfig(self):
        return pprint.pformat(self.panelsConfig)

    def setPanelsConfig(self, value, **kw):
        if not value.strip():
            return
        value = value.replace('\n', ' ').replace('\r', '')
        self.panelsConfig = eval(value)

    def getPortletsPos(self):
        """ get portlet pos of the container """
        portlet_name = 'here/%s/contentpanels_body' % self.getId()
        container = aq_parent(self)
        for slot_name in ['left_slots', 'right_slots']:
            if hasattr(aq_base(container), slot_name):
                if portlet_name in getattr(container, slot_name):
                    return slot_name
        return 'none'

    def setPortletsPos(self, value, **kw):
        self.cleanPortletPos()
        if value == 'none':
            return

        if value not in ('left_slots', 'right_slots'):
            return

        portlet_path = 'here/%s/contentpanels_body' % self.getId()

        folder = aq_parent(aq_inner(self))
        if not folder.hasProperty(value):
            folder.manage_addProperty(value, [portlet_path], 'lines')
        else:
            portlets = folder.getProperty(value)
            new_portlets = list(portlets) + [portlet_path]
            folder.manage_changeProperties({value:new_portlets})

    def cleanPortletPos(self):
        """ cleanup left/right_slots"""
        portlet_path = 'here/%s/contentpanels_body' % self.getId()
        folder = aq_parent(aq_inner(self))
        for slot_name in ('left_slots', 'right_slots'):
            portlets = folder.getProperty(slot_name, ())

            if portlet_path not in portlets:
                continue

            if tuple(portlets) == (portlet_path, ):
                folder.manage_delProperties([slot_name])
            else:
                new_portlets = [portlet for portlet in portlets \
                                if portlet != portlet_path]
                folder.manage_changeProperties({slot_name:new_portlets})

    def manage_beforeDelete(self, item, container):
        """ cleanup left/right slots when delete or rename """
        # delete myself
        if item is self:
            self._v_pos_before_delete = self.getPortletsPos()
            self.cleanPortletPos()
        BaseContent.manage_beforeDelete(self, item, container)

    def manage_afterAdd(self, item, container):
        if item is self:
            last_pos = getattr(self, '_v_pos_before_delete', 'none')
            if last_pos != 'none':
                self.setPortletsPos(last_pos)
        BaseContent.manage_afterAdd(self, item, container)

    def clearPanels(self):
        self.panelsConfig = []
        self._p_changed = 1

    security.declarePublic('toRelativePath')
    def toRelativePath(self, panelObjectPath):
        """ regenerate panelObjectPath, make it a relative path.
        path may be relative to this contentpanels or relate to the portal.
        - if panelObjectPath == '.', it means contentpanels it self
        - if panelObjectPath start with './', it means relative to the folderish context of this contentpanels
        - else, it means rlative to portal
        see also: getPanelObject
        """
        panelContent = self.getPanelObject(panelObjectPath)
        if panelContent is None:
            return '.'

        # folderContext = aq_inner(self)
        folderContext = self
        if not folderContext.isPrincipiaFolderish:
            folderContext = aq_parent(folderContext)

        relativePath = self.portal_url.getRelativeContentURL(panelContent)
        if panelContent is self:
            return '.'
        else:
            folderContextPath = self.portal_url.getRelativeContentURL(folderContext)
            if relativePath.startswith(folderContextPath):
                relativePath = panelObjectPath[len(folderContextPath):]
                relativePath = (relativePath.startswith('/') and  '.' or './')\
                               + relativePath
        return relativePath

    def getPublishContext(self):
        """ We want to display portlet in current context when the contenpanels
        is in left/right slots """
        o = self.REQUEST.get('PUBLISHED', None) # Gets the current object bound to REQUEST
        if hasattr(o, 'im_self'):       # It's a class method
            contextObject = o.im_self     # Gets the class instance bound to this method
            method = o
        elif hasattr(o, '_isPortalContent') or hasattr(o, '_getPortalTypeName'): # It's a CMF Content
            contextObject = o             # Gets the class instance itself
            method = None
        else:                           # It's a python script or ZPT
            contextObject = aq_parent(o)  # Gets parent's context
            method = o
        return (contextObject, method)

    def getPanelObject(self, objectPath):
        """get panel object by path.

        if panelObjectPath == '.', it means contentpanels it self
        if panelObejctPath start with './', it means relative to folderish context of this contentpanels
        else, it means rlative to the portal
        see also: toRelativePath
        """
        panelObject = None
        try:
            if objectPath in ['.', '/']:  # '.'means the contentpanels it self
                panelObject = self
            elif objectPath.startswith('./'):  # relative path to the folderish context
                objectPath = objectPath[2:]

                # folderContext = aq_inner(self)
                folderContext = self
                if not self.isPrincipiaFolderish:
                    folderContext = aq_parent(folderContext)

                panelObject = folderContext.restrictedTraverse(objectPath)
            else:
                panelObject = self.portal_url.getPortalObject().restrictedTraverse(objectPath)
        except:
            panelObject = None
        return panelObject

    security.declareProtected( permissions.ModifyPortalContent, 'addPage' )
    def addPage(self, pageTitle=None, pageIndex=-1):
        """
        add a new page at pageIndex, it has two columns as default.
        if pageIndex is -1 then add at the end of the contentpanels
        return the new page index (from 0)
        """
        if pageTitle is None:
            pageTitle = _(u'Untitled page')
        if pageIndex == -1:
            pageIndex = len(self.panelsConfig)
        self.panelsConfig.insert(pageIndex, {'pageColumns': [],
                         'pageTitle': pageTitle,
                         'pageWidth':'100%',
                         'pageCellSpace':'4',
                         'pageCellPad':'4',
                         'pageAlign':'center',
                         'pageStylesheetFixed':[],
                         'pageStylesheetDynamic':[]})

        # add two default columns for the new page
        self.addColumn(pageIndex)
        self.addColumn(pageIndex)
        self._p_changed = 1
        return pageIndex

    security.declareProtected( permissions.View, 'getPageTitles' )
    def getPageTitles(self):
        ''' get all the tilte of the pages '''
        titles = []
        for pageIndex in range(len(self.panelsConfig) ):
            titles.append(self.panelsConfig[pageIndex]['pageTitle'])
        return titles

    security.declareProtected( permissions.View, 'getPageInfo' )
    def getPageInfo(self, pageIndex, infoName):
        ''' get general info of the page '''
        return self.panelsConfig[pageIndex][infoName]

    security.declareProtected( permissions.ModifyPortalContent, 'changePageInfo' )
    def changePageInfo(self, pageIndex, pageTitle="", pageCellPad='', pageCellSpace='', pageWidth='', pageAlign=''):
        ''' change page's table info '''
        if pageCellPad == '':
            pageCellPad = None
        if pageCellSpace == '':
            pageCellSpace = None
        if pageWidth == '':
            pageWidth = None
        if pageAlign == '' or pageAlign == 'noalign':
            pageAlign = None

        self.panelsConfig[pageIndex]['pageWidth']= pageWidth
        self.panelsConfig[pageIndex]['pageAlign']= pageAlign
        self.panelsConfig[pageIndex]['pageCellPad']= pageCellPad
        self.panelsConfig[pageIndex]['pageCellSpace']= pageCellSpace
        self.panelsConfig[pageIndex]['pageTitle']= pageTitle
        self._p_changed = 1

    security.declareProtected(permissions.ModifyPortalContent, 'movePage')
    def movePage(self, pageIndex, toPage):
        """move a page from fromIndex to toIndex"""
        page = self.panelsConfig.pop(pageIndex)
        self.panelsConfig.insert(toPage, page)
        self._p_changed = 1

    security.declareProtected( permissions.ModifyPortalContent, 'deletePage' )
    def deletePage(self, pageIndex):
        ''' delete a page,
        return next page index to show'''
        nextPageIndex = pageIndex
        if len(self.panelsConfig) > 1:  # can't delete the last page!
            del self.panelsConfig[pageIndex]

            if pageIndex == len(self.panelsConfig):
                nextPageIndex = pageIndex - 1
        self._p_changed = 1
        return nextPageIndex

    security.declareProtected( permissions.ModifyPortalContent, 'addColumn' )
    def addColumn(self, pageIndex, columnIndex=-1):
        """add a new Column to 'pageIndex' at 'columnIndex'
        if 'columnIndex' is -1 then add to the end of the column'
        """
        if columnIndex == -1:
           columnIndex = len(self.panelsConfig[pageIndex]['pageColumns'])

        self.panelsConfig[pageIndex]['pageColumns'].insert(columnIndex, {'columnWidth': '50%',
                                                            'columnPanels':[] })
        self._p_changed = 1

    security.declareProtected( permissions.ModifyPortalContent, 'changeColumnWidth' )
    def changeColumnWidth(self, pageIndex, columnIndex, columnWidth):
        ''' change the width of a column '''
        if columnWidth == '':
            return None

        self.panelsConfig[pageIndex]['pageColumns'][columnIndex]['columnWidth'] = columnWidth
        self._p_changed = 1

    security.declareProtected( permissions.ModifyPortalContent, 'moveColumn')
    def moveColumn(self, pageIndex, columnIndex, toColumn):
        """move a column from 'fromIndex' to 'toIndex'"""
        column = self.panelsConfig[pageIndex]['pageColumns'].pop(columnIndex)
        self.panelsConfig[pageIndex]['pageColumns'].insert(toColumn, column)
        self._p_changed = 1

    security.declareProtected( permissions.ModifyPortalContent, 'deleteColumn' )
    def deleteColumn(self, pageIndex, columnIndex):
        '''# delete column'''
        if len(self.panelsConfig[pageIndex]['pageColumns']) > 1:
            del self.panelsConfig[pageIndex]['pageColumns'][columnIndex]
            self._p_changed = 1

    security.declareProtected( permissions.ModifyPortalContent, 'addPanel' )
    def addPanel(self, pageIndex, columnIndex, panelIndex, panelObjectPath, panelObjectViewlet, panelSkin, viewletOptions):
        ''' insert a new panel at panelIndex'''
        self.panelsConfig[pageIndex]['pageColumns'][columnIndex]['columnPanels'].\
                insert(panelIndex, {'panelSkin':panelSkin,
                        'panelObjectPath':panelObjectPath,
                        'panelObjectViewlet':panelObjectViewlet,
                        'viewletOptions':viewletOptions})
        self._p_changed = 1

    security.declareProtected( permissions.ModifyPortalContent, 'deletePanel' )
    def deletePanel(self, pageIndex, columnIndex, panelIndex):
        ''' delete a Panel '''
        del self.panelsConfig[pageIndex]['pageColumns'][columnIndex]['columnPanels'][panelIndex]
        self._p_changed = 1

    security.declareProtected( permissions.ModifyPortalContent, 'changePanel' )
    def changePanel(self, pageIndex, columnIndex, panelIndex, panelObjectPath='', panelObjectViewlet='', panelSkin='', viewletOptions=None):
        ''' change the skin of a existing panel '''

        if panelSkin:
            self.panelsConfig[pageIndex]['pageColumns'][columnIndex]['columnPanels'][panelIndex]['panelSkin'] = panelSkin
        self.panelsConfig[pageIndex]['pageColumns'][columnIndex]['columnPanels'][panelIndex]['panelObjectPath'] = panelObjectPath
        if panelObjectViewlet:
            self.panelsConfig[pageIndex]['pageColumns'][columnIndex]['columnPanels'][panelIndex]['panelObjectViewlet'] = panelObjectViewlet
        if viewletOptions is not None:
            self.panelsConfig[pageIndex]['pageColumns'][columnIndex]['columnPanels'][panelIndex]['viewletOptions']=viewletOptions
        self._p_changed = 1

    security.declareProtected( permissions.ModifyPortalContent, 'movePanel')
    def movePanel(self, pageIndex, columnIndex, panelIndex, toColumn, toPanel):
        """move a panel from 'toIndex'"""
        if toColumn == -1:
            toColumn = columnIndex
        if toPanel == -1:
            toPanel = panelIndex

        panel = self.panelsConfig[pageIndex]['pageColumns'][columnIndex]['columnPanels'].pop(panelIndex)
        toColumnLen = len(self.panelsConfig[pageIndex]['pageColumns'][toColumn]['columnPanels'])
        if toPanel > toColumnLen:
            toPanel = toColumnLen
        self.panelsConfig[pageIndex]['pageColumns'][toColumn]['columnPanels'].insert(toPanel, panel)
        self._p_changed = 1

registerType(ContentPanels, PROJECTNAME)

