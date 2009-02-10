## Script (Python) "getRSSResult"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=rss_url
##title=get rss result
##

if not rss_url:
    return None

from feedparser import parse

r = dict(parse(rss_url))

if not dict(r['feed']):
    # try again
    r = dict(parse(rss_url))

return r
