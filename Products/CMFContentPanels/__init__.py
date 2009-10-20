
try:
    from Products.LinguaPlone.public import process_types, listTypes
except:
    from Products.Archetypes.public import process_types, listTypes
 
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory

from ContentPanelsTool import registerViewlets
from ContentPanelsTool import ContentPanelsTool
from config import SKINS_DIR, GLOBALS,VIEWLETS
from config import PROJECTNAME, ADD_CONTENT_PERMISSION
from config import MessageFactory

registerViewlets(VIEWLETS)
from Products.PythonScripts.Utility import allow_module

allow_module("feedparser")
allow_module('Products.CMFContentPanels.browser.subnavtree')
# Check for Plone versions
try:
    from Products.CMFPlone.migrations import v3_0
except ImportError:
    HAS_PLONE30 = False
else:
    HAS_PLONE30 = True
    
def initialize(context):

    import ContentPanels
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    utils.ToolInit('CMF ContentPanels Tool', tools=(ContentPanelsTool,),
                 product_name='CMFContentPanels', icon='tool.gif',
                 ).initialize( context )

