## Script (Python) "cp_edit_panel_form"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=pageIndex=0, panelIndex=0, columnIndex=0
##title=edit the content panels config data

pageIndex=int(pageIndex)
columnIndex=int(columnIndex)
panelIndex=int(panelIndex)

panel = context.getPageInfo(pageIndex, 'pageColumns')[columnIndex]['columnPanels'][panelIndex]
panelContent = context.getPanelObject(panel['panelObjectPath']) or context

return panelContent.cp_new_panel_form(cpPath=context.absolute_url(), 
                                      pageIndex=pageIndex,
                                      columnIndex=columnIndex,
                                      panelIndex=panelIndex,
                                      viewletId=panel['panelObjectViewlet'],
                                      panelSkin=panel['panelSkin'],
                                      viewletOptions = panel.get('viewletOptions', {}))

