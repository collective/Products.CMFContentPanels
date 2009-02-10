## Script (Python) "contentpanels_submit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=ids=[]
##title=edit the submitted config data

t_contentpanels = context.portal_contentpanels
t_contentpanels.removeFromTemplates(ids)
if ids:
    msg = "Selected items have been deleted."
else:
    msg = "You should select items to delete."
context.REQUEST.RESPONSE.redirect('%s/contentpanels_templates_form' 
    	  % context.absolute_url())
