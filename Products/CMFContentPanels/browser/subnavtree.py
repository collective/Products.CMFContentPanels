from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy

class SubNavtreeStrategy(SitemapNavtreeStrategy):

    def __init__(self, context, view=None):
        SitemapNavtreeStrategy.__init__(self, context, view)
        self.rootPath = '/'.join(context.getPhysicalPath())
        self.bottomLevel = 65535

    def subtreeFilter(self, node):
        sitemapDecision = SitemapNavtreeStrategy.subtreeFilter(self, node)
        if sitemapDecision == False:
            return False
        depth = node.get('depth', 0)
        if depth > 0 and self.bottomLevel > 0 and depth >= self.bottomLevel:
            return False
        else:
            return True

