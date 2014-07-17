# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.component import adapts
from Products.Archetypes import atapi
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.field import ExtensionField
from rt.lastmodifier import permissions
from rt.lastmodifier.interfaces import ILastModifierLayer
from Products.CMFEditions import CMFEditionsMessageFactory as cmfe
from Products.CMFEditions.interfaces import IVersioned


class ExtensionTextField(ExtensionField, atapi.TextField):
    """ derivative of string for extending schemas """

class ExtensionBoolField(ExtensionField, atapi.BooleanField):
    """ derivative of bool for extending schemas """


class HistoryDocInfoExtender(object):
    adapts(IVersioned)
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
