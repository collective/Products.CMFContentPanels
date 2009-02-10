from Products.Archetypes.utils import DisplayList
from Products.CMFCore.permissions import AddPortalContent

ADD_CONTENT_PERMISSION = AddPortalContent
PROJECTNAME = 'CMFContentPanels'
SKINS_DIR = 'skins'

GLOBALS = globals()

NEW_VIEW_METHODS = {
    'Folder': ('contentpanels_display_view',),
    'Plone Site': ('contentpanels_display_view',),
    'Large Plone Folder': ('contentpanels_display_view',),
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
     ('tile', 'tile mode', 'page_layout_tile'),
     ('tab', 'tab mode', 'page_layout_tab'),
))

VOC_PORTLET_POS = DisplayList((
     ('none', 'none', 'portlet_pos_none'),
     ('left_slots','set to left','portlet_pos_left'),
     ('right_slots', 'set to right', 'portlet_pos_right'),
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

    ('document_viewlet', 'Document content',
     "string: here/viewlet_document_body/macros/portlet",
     '', 'View', 'PT:Document', 1),

    ('view_viewlet', 'Topic result list',
     'string: here/viewlets_topic_list/macros/base_portlet',
     '', 'View', 'PT:Topic', 1),

    ('image_view','image',
     'string:here/viewlet_image_body/macros/portlet',
     '', 'View', 'PT:Image', 1),

    ('contentpanels_viewlet', 'Nested contentpanels',
     'string:here/viewlet_contentpanels_body/macros/portlet',
     '', 'View', 'PT:ContentPanels', 1),

    ('plonechat_viewlet', 'recent messages',
     'string:here/viewlet_plonechat_body/macros/portlet',
     '', 'View', 'PT:PloneChat', 1),

    ('viewlet_dynamicpage', 'dynamic page',
     'string:here/viewlet_dynamicpage/macros/portlet',
     '', 'View', 'PT:DynamicPage', 1),

    ('plonearticle_viewlet', 'Article content',
     'string:here/viewlet_plonearticle_body/macros/portlet',
     '', 'View', 'PT:PloneArticle', 1),

    ('mpoll_viewlet', 'Poll',
     'string:here/viewlet_mpoll/macros/portlet',
     '', 'View', 'PT:MPoll', 1),

     ('popoll_viewlet', 'Plone Popoll',
      'string:here/viewlet_popoll/macros/portlet',
      '', 'View', 'PT:PlonePopoll', 1),

      ('headline_viewlet', 'Editable Headline',
       'string:here/viewlet_headline/macros/portlet',
       '', 'View', 'PT:News item', 1),

    # GL: global viewlets

    ('macro_viewlet', 'ZPT macro',
     'string:here/viewlet_macro_path/macros/viewlet',
     '', 'View', 'GL:all', 1),

    ('default_viewlet', 'Title description',
     'string:here/viewlet_default/macros/portlet',
     '', 'View', 'GL:all', 1),

    ('folder_listing', 'Folder listing',
     'string:here/viewlets_folder_listing/macros/base_portlet',
     '', 'View', 'GL:folder', 1),

    ('latest_updates_viewlet', 'Recent changes',
     'string:here/viewlets_folder_recent/macros/base_portlet',
     '', 'View', 'GL:folder', 1),

    ('recent_comments', 'Recent comments',
     'string:here/viewlets_folder_recent/macros/comments',
     '', 'View', 'GL:folder', 1),

    ('full_recent_changes', 'Folder changes',
     'string:here/viewlet_full_changes/macros/viewlet',
     '', 'View', 'GL:folder', 1),

    ('image_folder_viewlet', 'Image folder',
     'string:here/viewlet_image_folder/macros/portlet',
     '', 'View', 'GL:folder', 1),

    ('news_list', 'Discussion list',
     'string:here/viewlet_news/macros/news_list',
     '', 'View', 'GL:folder', 1),

    ('image_news', 'Image news',
     'string:here/viewlet_news/macros/image_news',
     '', 'View', 'GL:folder', 1),

    ('local_navigation', 'Local navigation',
     'string:here/viewlet_subportal_nav/macros/portlet',
     '', 'View', 'GL:folder', 1),

    # global portlet

    ('my_recent_changes', 'My recent changes',
     'string:here/portlet_mychanges/macros/portlet',
     '', 'View', 'GN:personal', 1),

    ('portlet_favorites', 'My favorites',
     'string:here/portlet_favorites/macros/portlet',
     '', 'View', 'GN:personal', 1),

    ('portlet_review', 'Review list',
     'string:here/portlet_review/macros/portlet',
     '', 'View', 'GN:personal', 1),

    ('portlet_calendar', 'Calendar',
     'string:here/portlet_calendar/macros/portlet',
     '', 'View', 'GN:portal', 1),

    ('viewlet_text', 'Simple text',
     'string:here/viewlet_text/macros/portlet',
     '', 'View', 'GN:portal', 1),

    ('viewlet_rss', 'RSS',
     'string:here/viewlet_rss/macros/portlet',
     '', 'View', 'GN:portal', 1),

    ('inline_frame_viewlet', 'Inline frame',
     'string:here/viewlet_iframe/macros/viewlet',
     '', 'View', 'GN:portal', 1),

]

PLONE_PORTLETS= [

    ('portlet_navigation', 'Navigation',
     'string:here/portlet_navigation/macros/portlet',
     '', 'View', 'GN:portal', 1),

    ('portlet_related', 'Related',
     'string:here/portlet_related/macros/portlet',
     '', 'View', 'GN:portal', 1),

    ('portlet_login', 'Login',
     'string:here/portlet_login/macros/portlet',
     '', 'View', 'GN:portal', 1),

]

# VIEWLETS.extend(PLONE_PORTLETS)

RATING_VIEWLETS = [

    ('top_ratings', 'Top ratings',
     'string:here/viewlet_ratings/macros/top_ratings',
     '', 'View', 'GL:folder', 1),

    ('top_countings', 'Top hit countings',
     'string:here/viewlet_ratings/macros/top_countings',
     '', 'View', 'GL:folder', 1),

]

try:
    import Products.ATRatings
    VIEWLETS.extend(RATING_VIEWLETS)
    del Products.ATRatings
except ImportError:
    pass
