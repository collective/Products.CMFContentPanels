## Script (Python) "setContentPanelsTemplate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=contentpanels_template_id

if not context.hasProperty('contentpanels_template_id'):
    context.manage_addProperty('contentpanels_template_id', contentpanels_template_id, 'string')
else:
    context.manage_changeProperties({'contentpanels_template_id':contentpanels_template_id})

return context.REQUEST.RESPONSE.redirect(context.absolute_url())
