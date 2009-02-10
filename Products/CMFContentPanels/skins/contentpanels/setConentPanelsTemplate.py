##parameters=contentpanels_template_id

if not context.hasProperty('contentpanels_template_id'):
    context.manage_addProperty('contentpanels_template_id', contentpanels_template_id, 'string')
else:
    context.manage_changeProperties({'contentpanels_template_id':contentpanels_template_id})

return context.view()
