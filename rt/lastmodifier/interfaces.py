# -*- coding: utf-8 -*-

from zope.interface import Interface


class ILastModifierLayer(Interface):
    """rt.lastmodifier product layer"""


class ILastModifierInertContent(Interface):
    """Marker interfaces for contents that must not display any byline info
    """
