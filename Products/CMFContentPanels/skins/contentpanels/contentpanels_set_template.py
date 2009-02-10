## Script (Python) "contentpanels_submit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id ,title
##title=edit the submitted config data

t_contentpanels = context.portal_contentpanels
t_contentpanels.setTemplate(id, title, context)
context.REQUEST.RESPONSE.redirect('%s/contentpanels_templates_form' 
    	  % context.absolute_url())
