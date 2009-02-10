## Script (Python) "getLocalSiteMapItems"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=depth=2, listTypes=[], listStates=None, curURL=''
##title=get data for locat navigation or site map
##

ntp = context.portal_properties.navtree_properties
stp = context.portal_properties.site_properties
view_action_types = stp.getProperty('typesUseViewActionInListings')

pretty_title_or_id = context.plone_utils.pretty_title_or_id
parentTypesNQ = ntp.getProperty('parentMetaTypesNotToQuery', ())
# Get ids not to list and make a dict to make the search fast
ids_not_to_list = ntp.getProperty('idsNotToList', ())
excluded_ids = {}
for exc_id in ids_not_to_list:
    excluded_ids[exc_id] = 1

catalog = context.portal_catalog

rootpath = '/'.join(context.getPhysicalPath())
query = {'path':{'query':rootpath,
	         'depth':depth},
         'sort_on':'getObjPositionInParent',
	 'sort_order':'asc',
	 }

if listTypes:
    query['portal_type'] = listTypes
if listStates:
    query['review_state']=listStates

query['is_default_page'] = False

rawresults = catalog(**query)

results = {}
currentItem = None

for item in rawresults:
    path = item.getPath()
    # Some types may require the 'view' action, respect this
    item_url = (item.portal_type in view_action_types and
                            item.getURL() + '/view') or item.getURL()
    data = {'Title':pretty_title_or_id(item),
            'currentItem':False,
	    'absolute_url': item_url,
	    'getURL':item_url,
	    'path': path,
	    'icon':item.getIcon,
	    'creation_date': item.CreationDate,
	    'portal_type': item.portal_type,
	    'review_state': item.review_state,
	    'Description':item.Description,
	    'show_children':item.is_folderish and item.portal_type not in parentTypesNQ,
	    'children':[], 
            'no_display':excluded_ids.has_key(item.getId) or not not item.exclude_from_nav,
	    }

    # Adds a piece of content to the result tree.
    parentpath = '/'.join(path.split('/')[:-1])
    # Tell parent about self
    if results.has_key(parentpath):
        results[parentpath]['children'].append(data)
    else:
        results[parentpath] = {'children':[data]}

    # If we have processed a child already, make sure we register it
    # as a child
    if results.has_key(path):
        data['children'] = results[path]['children']
    results[path] = data

    if curURL.startswith(item_url):
        if currentItem is None or \
	   ( len(item_url) > len(currentItem['absolute_url']) ):
	    currentItem = data
	
if currentItem is not None:
    currentItem['currentItem']=True
data = results.get(rootpath, {})
data['currentItem'] = currentItem is None
return data

