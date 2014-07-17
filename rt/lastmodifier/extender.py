# -*- coding: utf-8 -*-

import sys
from zope.interface import implements
from zope.component import adapts
from zope.component import queryUtility
from plone.memoize.instance import memoize
from Products.Archetypes import atapi
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.field import ExtensionField
from rt.lastmodifier import _
from rt.lastmodifier import permissions
from rt.lastmodifier.interfaces import ILastModifierLayer
from Products.CMFEditions import CMFEditionsMessageFactory as cmfe

if sys.version_info < (2, 6):
    from Products.ATContentTypes.interface import IATContentType
else:
    from Products.ATContentTypes.interfaces import IATContentType


class ExtensionTextField(ExtensionField, atapi.TextField):
    """ derivative of string for extending schemas """

class ExtensionBoolField(ExtensionField, atapi.BooleanField):
    """ derivative of bool for extending schemas """


class HistoryDocInfoExtender(object):
    adapts(IATContentType)
    implements(IBrowserLayerAwareExtender)

    layer = ILastModifierLayer

    fields = [
        # Same name as the one used in CMFEdition viewlet
        ExtensionTextField('hidden_cmfeditions_version_comment',
            write_permission=permissions.EditChangeNoteShowState,
            widget=atapi.TextAreaWidget(
                visible={'edit': 'invisible', 'view': 'invisible'},
                label=cmfe('label_version_comment',
                           default=u"Change note"),
                description=cmfe('help_version_comment',
                                 default=u'Enter a comment that describes the changes you made.'),
            ),
            required=False,
            searchable=False,
        ),

    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
