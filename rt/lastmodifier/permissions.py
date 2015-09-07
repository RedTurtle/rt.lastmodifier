# -*- coding: utf-8 -*-
from Products.CMFCore.permissions import setDefaultRoles
from AccessControl.SecurityInfo import ModuleSecurityInfo


security = ModuleSecurityInfo('rt.lastmodifier.permissions')

security.declarePublic('DocumentByLineViewAuthor')
DocumentByLineViewAuthor = 'rt.lastmodifier: documentByLine view author'
setDefaultRoles(DocumentByLineViewAuthor, ())

security.declarePublic('DocumentByLineViewLastModifier')
DocumentByLineViewLastModifier = 'rt.lastmodifier: documentByLine view last modifier'
setDefaultRoles(DocumentByLineViewLastModifier, ())

security.declarePublic('DocumentByLineViewModifiedDate')
DocumentByLineViewModifiedDate = 'rt.lastmodifier: documentByLine view modification date'
setDefaultRoles(DocumentByLineViewModifiedDate, ())

security.declarePublic('DocumentByLineViewPublishedDate')
DocumentByLineViewPublishedDate = 'rt.lastmodifier: documentByLine view publication date'
setDefaultRoles(DocumentByLineViewPublishedDate, ())

security.declarePublic('DocumentByLineViewChangeNote')
DocumentByLineViewChangeNote = 'rt.lastmodifier: documentByLine view change note'
setDefaultRoles(DocumentByLineViewChangeNote, ())

security.declarePublic('EditChangeNoteShowState')
EditChangeNoteShowState = 'rt.lastmodifier: choose to show change note'
setDefaultRoles(EditChangeNoteShowState, ())

security.declarePublic('DocumentByLineViewLongTimeFormat')
DocumentByLineViewLongTimeFormat = 'rt.lastmodifier: show long time format'
setDefaultRoles(DocumentByLineViewLongTimeFormat, ('Anonymous', ))
