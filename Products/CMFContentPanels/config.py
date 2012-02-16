from Products.Archetypes.utils import DisplayList
from Products.CMFCore.permissions import AddPortalContent

from zope.i18nmessageid import MessageFactory
_ = MessageFactory = MessageFactory('contentpanels')

try:
    # Plone 4 and higher 
    import plone.app.upgrade
    PLONE_VERSION = 4
except ImportError:
    PLONE_VERSION = 3

if PLONE_VERSION == 3:
    try:
        from Products.CMFPlone.migrations import v3_0
        del v3_0
        PLONE_VERSION = 3
    except ImportError:
        PLONE_VERSION = 2

ADD_CONTENT_PERMISSION = AddPortalContent
PROJECTNAME = 'CMFContentPanels'
SKINS_DIR = 'skins'

GLOBALS = globals()

if PLONE_VERSION == 3:
    NEW_VIEW_METHODS = {
        u'Folder': ('contentpanels_display_view',),
        'Plone Site': ('contentpanels_display_view',),
        'Large Plone Folder': ('contentpanels_display_view',),
    }
else:
    NEW_VIEW_METHODS = {
        u'Folder': ('contentpanels_display_view',),
        'Plone Site': ('contentpanels_display_view',),
    }

STYLESHEETS = [
    {'id':'contentpanels.css'},
    {'id':'contentpanelsCustom.css'},
    {'id':'tabber.css'},
]

JAVASCRIPTS = [
    {'id':'tabberoptions.js'},
    {'id':'tabber-minimizer.js'},
    {'id':'tabber_inline.js'},
]

ACTION_ICONS = {
    'plone': {
        'contentpanels': (
            'contentpanels_icon.gif',
            'Change display template for this view',
        ),
    },
}

VOC_PAGE_LAYOUT = DisplayList( (
     ('tile', _(u'tile mode'), 'page_layout_tile'),
     ('tab', _(u'tab mode'), 'page_layout_tab'),
))


# DEFAULT VIEWLETS TABLE
#
# viewlet are content related portlets. it can be a zpt
# macro or any other(ZPTlet or Script(python)...)
#
# 1. Every viewlet is a CMF action in portal_contentpanels.
#    So you have all the feature action have...
#
# 2. the follow viewlet actions are:
#
#    id, name, url, condition, permision, category, visible
#
# 3. be careful to the catagory's prefix:
#
#    - PT: content specific viewlets.
#      it should be PT:PotalTypeID
#
#    - GL: context sensitive viewlets
#        not content specific, but sensitive with its context
#
#      GL:folder     all folderish content specific
#      GL:content    all non-folderish content specific
#      GL:all        all content specific
#
#    - GN: general portlets. they are not context sensitive
#
#      GN:portal     site-wide viewlets
#      GN:personal   personal related viewlets

VIEWLETS = [

    # PT: portal type specific viewlets

    ('document_viewlet', _(u'Document content'),
     "string: here/viewlet_document_body/macros/portlet",
     '', 'View', 'PT:Document', 1),

    ('view_viewlet', _(u'Topic result list'),
     'string: here/viewlets_topic_list/macros/base_portlet',
     '', 'View', 'PT:Topic', 1),
     
    ('viewlets_master_list.pt', _(u'Advanced Topic Result list'),
     'string: here/viewlets_master_list/macros/base_portlet',
     '', 'View', 'PT:Topic', 1),

    ('viewlets_banners',_(u'Banner'),
     'string:here/viewlets_banners/macros/viewlet',
     '', 'View', 'PT:Image', 1),

    ('image_view',_(u'image'),
     'string:here/viewlet_image_body/macros/portlet',
     '', 'View', 'PT:Image', 1),

    ('contentpanels_viewlet', _(u'Nested contentpanels'),
     'string:here/viewlet_contentpanels_body/macros/portlet',
     '', 'View', 'PT:ContentPanels', 1),

    ('plonechat_viewlet', _(u'recent messages'),
     'string:here/viewlet_plonechat_body/macros/portlet',
     '', 'View', 'PT:PloneChat', 1),

    ('viewlet_dynamicpage', _(u'dynamic page'),
     'string:here/viewlet_dynamicpage/macros/portlet',
     '', 'View', 'PT:DynamicPage', 1),

    ('plonearticle_viewlet', _(u'Article content'),
     'string:here/viewlet_plonearticle_body/macros/portlet',
     '', 'View', 'PT:PloneArticle', 1),

    ('mpoll_viewlet', _(u'Poll'),
     'string:here/viewlet_mpoll/macros/portlet',
     '', 'View', 'PT:MPoll', 1),

     ('popoll_viewlet', _(u'Plone Popoll'),
      'string:here/viewlet_popoll/macros/portlet',
      '', 'View', 'PT:PlonePopoll', 1),

      ('headline_viewlet', _(u'Editable Headline'),
       'string:here/viewlet_headline/macros/portlet',
       '', 'View', 'PT:News item', 1),

    # GL: global viewlets

    ('viewlet_flexible', _(u'Flexible'),
     'string:here/viewlet_flexible/macros/portlet',
     '', 'View', 'GL:all', 1),
    
    ('macro_viewlet', _(u'ZPT macro'),
     'string:here/viewlet_macro_path/macros/viewlet',
     '', 'View', 'GL:all', 1),

    ('default_viewlet', _(u'Title description'),
     'string:here/viewlet_default/macros/portlet',
     '', 'View', 'GL:all', 1),

    ('folder_listing', _(u'Folder listing'),
     'string:here/viewlets_folder_listing/macros/base_portlet',
     '', 'View', 'GL:folder', 1),

    ('latest_updates_viewlet', _(u'Recent changes'),
     'string:here/viewlets_folder_recent/macros/base_portlet',
     '', 'View', 'GL:folder', 1),

    ('recent_comments', _(u'Recent comments'),
     'string:here/viewlets_folder_recent/macros/comments',
     '', 'View', 'GL:folder', 1),

    ('full_recent_changes', _(u'Folder changes'),
     'string:here/viewlet_full_changes/macros/viewlet',
     '', 'View', 'GL:folder', 1),

    ('image_folder_viewlet', _(u'Image folder'),
     'string:here/viewlet_image_folder/macros/portlet',
     '', 'View', 'GL:folder', 1),

    ('news_list', _(u'Discussion list'),
     'string:here/viewlet_news/macros/news_list',
     '', 'View', 'GL:folder', 1),

    ('image_news', _(u'Image news'),
     'string:here/viewlet_news/macros/image_news',
     '', 'View', 'GL:folder', 1),

    ('local_navigation', _(u'Local navigation'),
     'string:here/viewlet_subportal_nav/macros/portlet',
     '', 'View', 'GL:folder', 1),

    # global portlet

    ('my_recent_changes', _(u'My recent changes'),
     'string:here/portlet_mychanges/macros/portlet',
     '', 'View', 'GN:personal', 1),

    ('portlet_favorites', _(u'My favorites'),
     'string:here/portlet_favorites/macros/portlet',
     '', 'View', 'GN:personal', 1),

    ('portlet_review', _(u'Review list'),
     'string:here/portlet_review/macros/portlet',
     '', 'View', 'GN:personal', 1),

    #('portlet_calendar', _(u'Calendar'),
    # 'string:here/portlet_calendar/macros/portlet',
    # '', 'View', 'GN:portal', 1),

    ('viewlet_text', _(u'Simple text'),
     'string:here/viewlet_text/macros/portlet',
     '', 'View', 'GN:portal', 1),

    ('viewlet_rss', _(u'RSS'),
     'string:here/viewlet_rss/macros/portlet',
     '', 'View', 'GN:portal', 1),

    ('inline_frame_viewlet', _(u'Inline frame'),
     'string:here/viewlet_iframe/macros/viewlet',
     '', 'View', 'GN:portal', 1),

]

PLONE_PORTLETS= [

    ('portlet_navigation', _(u'Navigation'),
     'string:here/portlet_navigation/macros/portlet',
     '', 'View', 'GN:portal', 1),

    ('portlet_related', _(u'Related'),
     'string:here/portlet_related/macros/portlet',
     '', 'View', 'GN:portal', 1),

    ('portlet_login', _(u'Login'),
     'string:here/portlet_login/macros/portlet',
     '', 'View', 'GN:portal', 1),

]

# VIEWLETS.extend(PLONE_PORTLETS)

RATING_VIEWLETS = [

    ('top_ratings', _(u'Top ratings'),
     'string:here/viewlet_ratings/macros/top_ratings',
     '', 'View', 'GL:folder', 1),

    ('top_countings', _(u'Top hit countings'),
     'string:here/viewlet_ratings/macros/top_countings',
     '', 'View', 'GL:folder', 1),

]

try:
    import Products.ATRatings
    VIEWLETS.extend(RATING_VIEWLETS)
    del Products.ATRatings
except ImportError:
    pass
