from zope.interface import Interface


class IContentPanelsTool(Interface):
    """Tool for ContentPanels."""

    description = schema.TextLine(
        title=_(u"label_description"),
        required=False,
        description=_(u"help_description"),
    )

    panelsConfig = schema.TextLine()

    pageLayoutMode = schema.TextLine(
        title=_(u"label_page_layout_mode"),
        required=False,
        description=_(u"help_page_layout_mode"),
    )

    portletsPos = schema.TextLine(
        title=_(u"label_portlet_pos"),
        required=False,
        description=_(u"help_portlet_pos"),
    )

    customCSS = schema.TextLine(
        title=_(u"label_custom_css"),
        required=False,
        description=_(u"help_custom_css"),
    )

class IContentPanels(Interface):
    """ContentPanels."""
