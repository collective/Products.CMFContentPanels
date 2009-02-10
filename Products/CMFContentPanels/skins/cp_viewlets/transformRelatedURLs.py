## Script (Python) "transformRelatedURLs"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=htmltext, base_url
##title=make a-href and img-src use absolute_url
##

# this is a quick hack
a_splitted = htmltext.split(' href="')
result = a_splitted[0]

for href in a_splitted[1:]:
    if not href.startswith('http') and not href.startswith('/') and not href.startswith('file://') and not href.startswith('mailto:'):
        result += ' href="' + base_url + '/../' + href
    else:
        result += ' href="' + href

htmltext = result
img_splitted = htmltext.split(' src="')
result = img_splitted[0]

for src in img_splitted[1:]:
    if not src.startswith('http') and not src.startswith('/') and not src.startswith('file://'):
        result += ' src="' + base_url + '/../' + src
    else:
        result += ' src="' + src
htmltext = result

return result
