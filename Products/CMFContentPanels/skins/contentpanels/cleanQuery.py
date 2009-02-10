## Script (Python) "cleanQuery"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=query
##title=clean the catalog query
##

catalog=context.portal_catalog
indexes=catalog.indexes()
cleaned={}

for k, v in query.items():
    if v and k in indexes:
        cleaned.update({k:v})
    elif v and k.endswith('_usage'):
        key = k[:-6]
        if key in indexes:
            cleaned.update({k:v})
    elif k=='sort_on' or k=='sort_order' or k=='sort_limit':
        if k=='sort_limit' and not same_type(v, 0):
            cleaned.update({k:int(v)})
        else:
            cleaned.update({k:v})

return cleaned
