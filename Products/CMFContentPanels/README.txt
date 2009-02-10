What is CMFContentPanels?

  CMFContentPanels is a plone portlets product to build composite pages.
  You can create new content which is composed of other contents as
  configurable 'content panels'. You can change the layout, the panel
  skin and the content viewlet through the web.

Features

  * support multi-page and mulit-column

  * full function layout management, easy to use: move panels
    left/right/up/down

  * predefined viewlets for Document, Image, Folder, Topic, ZWiki Page,
    PloneChat, mxmDynamicPage.

  * each viewlet is configurable. it is quite easy to add new viewlets.
    You can add a RSS viewlet or a simplet text viewlet.

  * contentpanels content can be a plone portlet and show on the
    left/right column.

  * support multi-rows: use 'tile' page layout mode, and each page
    becomes a new row!

How to Use it?

  1. Install it. See 'INSTALL.txt' for more information.

  2. "http://plone.org/products/cmfcontentpanels":http://plone.org/products/cmfcontentpanels

How to Extend CMFContentPanels? (For Developers)

 How to make more viewlets?

  Viewlet is a view of content which can be selected in contentpanels.
  Viewlet can be a zpt or a zpt macro. Viewlets are registered with
  CMF Action mechanism.

  1. Write a viewlet for your content.
     You can refer to stuff at 'CMFContentPanels/skins/cp_viewlets',
     where are default viewlets.

  2. All viewlets are registered in portal_contentpanels.
     You can also register viewlets using::

      from Products.CMFContentPanels import registerViewlets
      registerViewlets(you_viewlets)

     With this way, if you reinstall CMFContentPanels, your viewlets
     configuration will not lost.

 How to make viewlets configuable?

   1. Viewlet configuration form fields can be define in a macro
      with name: '(your_viewlet_macroname)_viewletconf'

      For example, 'viewlets_folder_recent.pt' has 2 macros:
      'base_portlet' and 'base_portlet_viewletconf'

   2. The form fields will be showed and saved automatically

   3. Your viewlet can use the form variables in a dict named
      'viewletOptions', for example 'viewletOptions["itemCount"]'

 How to add new panel skin?

  You can define a new css wrapper to define a new panel skin:

  1. Customise contentpanels_skin.css.dtml, write your new css wrapper there

  2. Go to ZMI 'portal_contentpanels', in the properties view, add your new
     wrapper there.

Credits

  * "ZopeChina.com":http://www.zopechina.com, a leading Zope Service provider
   in China. ZopeChina.com runs the biggest Chinese Zope community in China -
   "CZUG.org":http://czug.org (China Zope User Group). We are trying to make
   Zope/Plone works better for Chinese people.

  * ausum's "CMFPortlets":http://www.zope.org/Members/ausum/CMFPortlets , many
   idea comes from CMFPortlets. Thanks!

  * The Rounded panels technique is from Denis Mishunoff's how-to:

    http://plone.org/documentation/how-to/portlets-with-rounded-corners-and-shadow

Bug report and feature request

  In the "CMFContentPanels product area":http://plone.org/products/cmfcontentpanels
  you can report bugs and request new features.
