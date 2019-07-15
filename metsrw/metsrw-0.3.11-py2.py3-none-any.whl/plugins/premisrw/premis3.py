# ./premis3.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:d9a0655d56a168f76c73bfa50dd6fc537086069f
# Generated 2019-05-27 16:42:29.720005 by PyXB version 1.2.6 using Python 3.7.3.final.0
# Namespace http://www.loc.gov/premis/v3

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:171192d2-80d9-11e9-87dd-b8e8562bd27e')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.loc.gov/premis/v3', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 314, 20)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.yes = STD_ANON._CF_enumeration.addEnumeration(unicode_value='yes', tag='yes')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: {http://www.loc.gov/premis/v3}version3
class version3 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'version3')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1166, 1)
    _Documentation = None
version3._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=version3, enum_prefix=None)
version3.n3_0 = version3._CF_enumeration.addEnumeration(unicode_value='3.0', tag='n3_0')
version3._InitializeFacetMap(version3._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'version3', version3)
_module_typeBindings.version3 = version3

# Atomic simple type: {http://www.loc.gov/premis/v3}edtfSimpleType
class edtfSimpleType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'edtfSimpleType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1189, 1)
    _Documentation = None
edtfSimpleType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'edtfSimpleType', edtfSimpleType)
_module_typeBindings.edtfSimpleType = edtfSimpleType

# Complex type {http://www.loc.gov/premis/v3}objectComplexType with content type EMPTY
class objectComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}objectComplexType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'objectComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 100, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.objectComplexType = objectComplexType
Namespace.addCategoryObject('typeBinding', 'objectComplexType', objectComplexType)


# Complex type {http://www.loc.gov/premis/v3}agentIdentifierComplexType with content type ELEMENT_ONLY
class agentIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}agentIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'agentIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 296, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}agentIdentifierValue uses Python identifier agentIdentifierValue
    __agentIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'agentIdentifierValue'), 'agentIdentifierValue', '__httpwww_loc_govpremisv3_agentIdentifierComplexType_httpwww_loc_govpremisv3agentIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 934, 1), )

    
    agentIdentifierValue = property(__agentIdentifierValue.value, __agentIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}agentIdentifierType uses Python identifier agentIdentifierType
    __agentIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'agentIdentifierType'), 'agentIdentifierType', '__httpwww_loc_govpremisv3_agentIdentifierComplexType_httpwww_loc_govpremisv3agentIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 989, 1), )

    
    agentIdentifierType = property(__agentIdentifierType.value, __agentIdentifierType.set, None, None)

    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_agentIdentifierComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 301, 2)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 301, 2)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        __agentIdentifierValue.name() : __agentIdentifierValue,
        __agentIdentifierType.name() : __agentIdentifierType
    })
    _AttributeMap.update({
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.agentIdentifierComplexType = agentIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'agentIdentifierComplexType', agentIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}contentLocationComplexType with content type ELEMENT_ONLY
class contentLocationComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}contentLocationComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'contentLocationComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 327, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}contentLocationValue uses Python identifier contentLocationValue
    __contentLocationValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'contentLocationValue'), 'contentLocationValue', '__httpwww_loc_govpremisv3_contentLocationComplexType_httpwww_loc_govpremisv3contentLocationValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 937, 1), )

    
    contentLocationValue = property(__contentLocationValue.value, __contentLocationValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}contentLocationType uses Python identifier contentLocationType
    __contentLocationType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'contentLocationType'), 'contentLocationType', '__httpwww_loc_govpremisv3_contentLocationComplexType_httpwww_loc_govpremisv3contentLocationType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 992, 1), )

    
    contentLocationType = property(__contentLocationType.value, __contentLocationType.set, None, None)

    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_contentLocationComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 332, 2)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 332, 2)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        __contentLocationValue.name() : __contentLocationValue,
        __contentLocationType.name() : __contentLocationType
    })
    _AttributeMap.update({
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.contentLocationComplexType = contentLocationComplexType
Namespace.addCategoryObject('typeBinding', 'contentLocationComplexType', contentLocationComplexType)


# Complex type {http://www.loc.gov/premis/v3}copyrightDocumentationIdentifierComplexType with content type ELEMENT_ONLY
class copyrightDocumentationIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}copyrightDocumentationIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 338, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}copyrightDocumentationIdentifierValue uses Python identifier copyrightDocumentationIdentifierValue
    __copyrightDocumentationIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationIdentifierValue'), 'copyrightDocumentationIdentifierValue', '__httpwww_loc_govpremisv3_copyrightDocumentationIdentifierComplexType_httpwww_loc_govpremisv3copyrightDocumentationIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 938, 1), )

    
    copyrightDocumentationIdentifierValue = property(__copyrightDocumentationIdentifierValue.value, __copyrightDocumentationIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}copyrightDocumentationIdentifierType uses Python identifier copyrightDocumentationIdentifierType
    __copyrightDocumentationIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationIdentifierType'), 'copyrightDocumentationIdentifierType', '__httpwww_loc_govpremisv3_copyrightDocumentationIdentifierComplexType_httpwww_loc_govpremisv3copyrightDocumentationIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 993, 1), )

    
    copyrightDocumentationIdentifierType = property(__copyrightDocumentationIdentifierType.value, __copyrightDocumentationIdentifierType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}copyrightDocumentationRole uses Python identifier copyrightDocumentationRole
    __copyrightDocumentationRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationRole'), 'copyrightDocumentationRole', '__httpwww_loc_govpremisv3_copyrightDocumentationIdentifierComplexType_httpwww_loc_govpremisv3copyrightDocumentationRole', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 994, 1), )

    
    copyrightDocumentationRole = property(__copyrightDocumentationRole.value, __copyrightDocumentationRole.set, None, None)

    _ElementMap.update({
        __copyrightDocumentationIdentifierValue.name() : __copyrightDocumentationIdentifierValue,
        __copyrightDocumentationIdentifierType.name() : __copyrightDocumentationIdentifierType,
        __copyrightDocumentationRole.name() : __copyrightDocumentationRole
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.copyrightDocumentationIdentifierComplexType = copyrightDocumentationIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'copyrightDocumentationIdentifierComplexType', copyrightDocumentationIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}copyrightInformationComplexType with content type ELEMENT_ONLY
class copyrightInformationComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}copyrightInformationComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'copyrightInformationComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 349, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}copyrightNote uses Python identifier copyrightNote
    __copyrightNote = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'copyrightNote'), 'copyrightNote', '__httpwww_loc_govpremisv3_copyrightInformationComplexType_httpwww_loc_govpremisv3copyrightNote', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 939, 1), )

    
    copyrightNote = property(__copyrightNote.value, __copyrightNote.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}copyrightStatus uses Python identifier copyrightStatus
    __copyrightStatus = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'copyrightStatus'), 'copyrightStatus', '__httpwww_loc_govpremisv3_copyrightInformationComplexType_httpwww_loc_govpremisv3copyrightStatus', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 995, 1), )

    
    copyrightStatus = property(__copyrightStatus.value, __copyrightStatus.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}copyrightJurisdiction uses Python identifier copyrightJurisdiction
    __copyrightJurisdiction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'copyrightJurisdiction'), 'copyrightJurisdiction', '__httpwww_loc_govpremisv3_copyrightInformationComplexType_httpwww_loc_govpremisv3copyrightJurisdiction', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1057, 1), )

    
    copyrightJurisdiction = property(__copyrightJurisdiction.value, __copyrightJurisdiction.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}copyrightDocumentationIdentifier uses Python identifier copyrightDocumentationIdentifier
    __copyrightDocumentationIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationIdentifier'), 'copyrightDocumentationIdentifier', '__httpwww_loc_govpremisv3_copyrightInformationComplexType_httpwww_loc_govpremisv3copyrightDocumentationIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1067, 1), )

    
    copyrightDocumentationIdentifier = property(__copyrightDocumentationIdentifier.value, __copyrightDocumentationIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}copyrightApplicableDates uses Python identifier copyrightApplicableDates
    __copyrightApplicableDates = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'copyrightApplicableDates'), 'copyrightApplicableDates', '__httpwww_loc_govpremisv3_copyrightInformationComplexType_httpwww_loc_govpremisv3copyrightApplicableDates', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1118, 1), )

    
    copyrightApplicableDates = property(__copyrightApplicableDates.value, __copyrightApplicableDates.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}copyrightStatusDeterminationDate uses Python identifier copyrightStatusDeterminationDate
    __copyrightStatusDeterminationDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'copyrightStatusDeterminationDate'), 'copyrightStatusDeterminationDate', '__httpwww_loc_govpremisv3_copyrightInformationComplexType_httpwww_loc_govpremisv3copyrightStatusDeterminationDate', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1119, 1), )

    
    copyrightStatusDeterminationDate = property(__copyrightStatusDeterminationDate.value, __copyrightStatusDeterminationDate.set, None, None)

    _ElementMap.update({
        __copyrightNote.name() : __copyrightNote,
        __copyrightStatus.name() : __copyrightStatus,
        __copyrightJurisdiction.name() : __copyrightJurisdiction,
        __copyrightDocumentationIdentifier.name() : __copyrightDocumentationIdentifier,
        __copyrightApplicableDates.name() : __copyrightApplicableDates,
        __copyrightStatusDeterminationDate.name() : __copyrightStatusDeterminationDate
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.copyrightInformationComplexType = copyrightInformationComplexType
Namespace.addCategoryObject('typeBinding', 'copyrightInformationComplexType', copyrightInformationComplexType)


# Complex type {http://www.loc.gov/premis/v3}creatingApplicationComplexType with content type ELEMENT_ONLY
class creatingApplicationComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}creatingApplicationComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 363, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}creatingApplicationVersion uses Python identifier creatingApplicationVersion
    __creatingApplicationVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationVersion'), 'creatingApplicationVersion', '__httpwww_loc_govpremisv3_creatingApplicationComplexType_httpwww_loc_govpremisv3creatingApplicationVersion', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 940, 1), )

    
    creatingApplicationVersion = property(__creatingApplicationVersion.value, __creatingApplicationVersion.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}creatingApplicationName uses Python identifier creatingApplicationName
    __creatingApplicationName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationName'), 'creatingApplicationName', '__httpwww_loc_govpremisv3_creatingApplicationComplexType_httpwww_loc_govpremisv3creatingApplicationName', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 996, 1), )

    
    creatingApplicationName = property(__creatingApplicationName.value, __creatingApplicationName.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}dateCreatedByApplication uses Python identifier dateCreatedByApplication
    __dateCreatedByApplication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dateCreatedByApplication'), 'dateCreatedByApplication', '__httpwww_loc_govpremisv3_creatingApplicationComplexType_httpwww_loc_govpremisv3dateCreatedByApplication', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1116, 1), )

    
    dateCreatedByApplication = property(__dateCreatedByApplication.value, __dateCreatedByApplication.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}creatingApplicationExtension uses Python identifier creatingApplicationExtension
    __creatingApplicationExtension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationExtension'), 'creatingApplicationExtension', '__httpwww_loc_govpremisv3_creatingApplicationComplexType_httpwww_loc_govpremisv3creatingApplicationExtension', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1133, 1), )

    
    creatingApplicationExtension = property(__creatingApplicationExtension.value, __creatingApplicationExtension.set, None, None)

    _ElementMap.update({
        __creatingApplicationVersion.name() : __creatingApplicationVersion,
        __creatingApplicationName.name() : __creatingApplicationName,
        __dateCreatedByApplication.name() : __dateCreatedByApplication,
        __creatingApplicationExtension.name() : __creatingApplicationExtension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.creatingApplicationComplexType = creatingApplicationComplexType
Namespace.addCategoryObject('typeBinding', 'creatingApplicationComplexType', creatingApplicationComplexType)


# Complex type {http://www.loc.gov/premis/v3}environmentFunctionComplexType with content type ELEMENT_ONLY
class environmentFunctionComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}environmentFunctionComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'environmentFunctionComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 401, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}environmentFunctionLevel uses Python identifier environmentFunctionLevel
    __environmentFunctionLevel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentFunctionLevel'), 'environmentFunctionLevel', '__httpwww_loc_govpremisv3_environmentFunctionComplexType_httpwww_loc_govpremisv3environmentFunctionLevel', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 943, 4), )

    
    environmentFunctionLevel = property(__environmentFunctionLevel.value, __environmentFunctionLevel.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}environmentFunctionType uses Python identifier environmentFunctionType
    __environmentFunctionType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentFunctionType'), 'environmentFunctionType', '__httpwww_loc_govpremisv3_environmentFunctionComplexType_httpwww_loc_govpremisv3environmentFunctionType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 998, 4), )

    
    environmentFunctionType = property(__environmentFunctionType.value, __environmentFunctionType.set, None, None)

    _ElementMap.update({
        __environmentFunctionLevel.name() : __environmentFunctionLevel,
        __environmentFunctionType.name() : __environmentFunctionType
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.environmentFunctionComplexType = environmentFunctionComplexType
Namespace.addCategoryObject('typeBinding', 'environmentFunctionComplexType', environmentFunctionComplexType)


# Complex type {http://www.loc.gov/premis/v3}environmentDesignationComplexType with content type ELEMENT_ONLY
class environmentDesignationComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}environmentDesignationComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'environmentDesignationComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 413, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}environmentDesignationExtension uses Python identifier environmentDesignationExtension
    __environmentDesignationExtension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentDesignationExtension'), 'environmentDesignationExtension', '__httpwww_loc_govpremisv3_environmentDesignationComplexType_httpwww_loc_govpremisv3environmentDesignationExtension', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 941, 4), )

    
    environmentDesignationExtension = property(__environmentDesignationExtension.value, __environmentDesignationExtension.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}environmentDesignationNote uses Python identifier environmentDesignationNote
    __environmentDesignationNote = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentDesignationNote'), 'environmentDesignationNote', '__httpwww_loc_govpremisv3_environmentDesignationComplexType_httpwww_loc_govpremisv3environmentDesignationNote', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 942, 4), )

    
    environmentDesignationNote = property(__environmentDesignationNote.value, __environmentDesignationNote.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}environmentOrigin uses Python identifier environmentOrigin
    __environmentOrigin = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentOrigin'), 'environmentOrigin', '__httpwww_loc_govpremisv3_environmentDesignationComplexType_httpwww_loc_govpremisv3environmentOrigin', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 945, 4), )

    
    environmentOrigin = property(__environmentOrigin.value, __environmentOrigin.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}environmentVersion uses Python identifier environmentVersion
    __environmentVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentVersion'), 'environmentVersion', '__httpwww_loc_govpremisv3_environmentDesignationComplexType_httpwww_loc_govpremisv3environmentVersion', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 948, 4), )

    
    environmentVersion = property(__environmentVersion.value, __environmentVersion.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}environmentName uses Python identifier environmentName
    __environmentName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentName'), 'environmentName', '__httpwww_loc_govpremisv3_environmentDesignationComplexType_httpwww_loc_govpremisv3environmentName', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 999, 4), )

    
    environmentName = property(__environmentName.value, __environmentName.set, None, None)

    _ElementMap.update({
        __environmentDesignationExtension.name() : __environmentDesignationExtension,
        __environmentDesignationNote.name() : __environmentDesignationNote,
        __environmentOrigin.name() : __environmentOrigin,
        __environmentVersion.name() : __environmentVersion,
        __environmentName.name() : __environmentName
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.environmentDesignationComplexType = environmentDesignationComplexType
Namespace.addCategoryObject('typeBinding', 'environmentDesignationComplexType', environmentDesignationComplexType)


# Complex type {http://www.loc.gov/premis/v3}environmentRegistryComplexType with content type ELEMENT_ONLY
class environmentRegistryComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}environmentRegistryComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'environmentRegistryComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 428, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}environmentRegistryKey uses Python identifier environmentRegistryKey
    __environmentRegistryKey = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistryKey'), 'environmentRegistryKey', '__httpwww_loc_govpremisv3_environmentRegistryComplexType_httpwww_loc_govpremisv3environmentRegistryKey', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 946, 4), )

    
    environmentRegistryKey = property(__environmentRegistryKey.value, __environmentRegistryKey.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}environmentRegistryName uses Python identifier environmentRegistryName
    __environmentRegistryName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistryName'), 'environmentRegistryName', '__httpwww_loc_govpremisv3_environmentRegistryComplexType_httpwww_loc_govpremisv3environmentRegistryName', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 947, 4), )

    
    environmentRegistryName = property(__environmentRegistryName.value, __environmentRegistryName.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}environmentRegistryRole uses Python identifier environmentRegistryRole
    __environmentRegistryRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistryRole'), 'environmentRegistryRole', '__httpwww_loc_govpremisv3_environmentRegistryComplexType_httpwww_loc_govpremisv3environmentRegistryRole', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1000, 4), )

    
    environmentRegistryRole = property(__environmentRegistryRole.value, __environmentRegistryRole.set, None, None)

    _ElementMap.update({
        __environmentRegistryKey.name() : __environmentRegistryKey,
        __environmentRegistryName.name() : __environmentRegistryName,
        __environmentRegistryRole.name() : __environmentRegistryRole
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.environmentRegistryComplexType = environmentRegistryComplexType
Namespace.addCategoryObject('typeBinding', 'environmentRegistryComplexType', environmentRegistryComplexType)


# Complex type {http://www.loc.gov/premis/v3}eventDetailInformationComplexType with content type ELEMENT_ONLY
class eventDetailInformationComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}eventDetailInformationComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventDetailInformationComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 441, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}eventDetail uses Python identifier eventDetail
    __eventDetail = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventDetail'), 'eventDetail', '__httpwww_loc_govpremisv3_eventDetailInformationComplexType_httpwww_loc_govpremisv3eventDetail', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 949, 1), )

    
    eventDetail = property(__eventDetail.value, __eventDetail.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}eventDetailExtension uses Python identifier eventDetailExtension
    __eventDetailExtension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventDetailExtension'), 'eventDetailExtension', '__httpwww_loc_govpremisv3_eventDetailInformationComplexType_httpwww_loc_govpremisv3eventDetailExtension', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1135, 4), )

    
    eventDetailExtension = property(__eventDetailExtension.value, __eventDetailExtension.set, None, None)

    _ElementMap.update({
        __eventDetail.name() : __eventDetail,
        __eventDetailExtension.name() : __eventDetailExtension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventDetailInformationComplexType = eventDetailInformationComplexType
Namespace.addCategoryObject('typeBinding', 'eventDetailInformationComplexType', eventDetailInformationComplexType)


# Complex type {http://www.loc.gov/premis/v3}eventIdentifierComplexType with content type ELEMENT_ONLY
class eventIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}eventIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 451, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}eventIdentifierValue uses Python identifier eventIdentifierValue
    __eventIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventIdentifierValue'), 'eventIdentifierValue', '__httpwww_loc_govpremisv3_eventIdentifierComplexType_httpwww_loc_govpremisv3eventIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 950, 1), )

    
    eventIdentifierValue = property(__eventIdentifierValue.value, __eventIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}eventIdentifierType uses Python identifier eventIdentifierType
    __eventIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventIdentifierType'), 'eventIdentifierType', '__httpwww_loc_govpremisv3_eventIdentifierComplexType_httpwww_loc_govpremisv3eventIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1002, 1), )

    
    eventIdentifierType = property(__eventIdentifierType.value, __eventIdentifierType.set, None, None)

    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_eventIdentifierComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 456, 2)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 456, 2)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        __eventIdentifierValue.name() : __eventIdentifierValue,
        __eventIdentifierType.name() : __eventIdentifierType
    })
    _AttributeMap.update({
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.eventIdentifierComplexType = eventIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'eventIdentifierComplexType', eventIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}eventOutcomeDetailComplexType with content type ELEMENT_ONLY
class eventOutcomeDetailComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}eventOutcomeDetailComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetailComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 463, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}eventOutcomeDetailNote uses Python identifier eventOutcomeDetailNote
    __eventOutcomeDetailNote = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetailNote'), 'eventOutcomeDetailNote', '__httpwww_loc_govpremisv3_eventOutcomeDetailComplexType_httpwww_loc_govpremisv3eventOutcomeDetailNote', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 951, 1), )

    
    eventOutcomeDetailNote = property(__eventOutcomeDetailNote.value, __eventOutcomeDetailNote.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}eventOutcomeDetailExtension uses Python identifier eventOutcomeDetailExtension
    __eventOutcomeDetailExtension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetailExtension'), 'eventOutcomeDetailExtension', '__httpwww_loc_govpremisv3_eventOutcomeDetailComplexType_httpwww_loc_govpremisv3eventOutcomeDetailExtension', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1136, 4), )

    
    eventOutcomeDetailExtension = property(__eventOutcomeDetailExtension.value, __eventOutcomeDetailExtension.set, None, None)

    _ElementMap.update({
        __eventOutcomeDetailNote.name() : __eventOutcomeDetailNote,
        __eventOutcomeDetailExtension.name() : __eventOutcomeDetailExtension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventOutcomeDetailComplexType = eventOutcomeDetailComplexType
Namespace.addCategoryObject('typeBinding', 'eventOutcomeDetailComplexType', eventOutcomeDetailComplexType)


# Complex type {http://www.loc.gov/premis/v3}eventOutcomeInformationComplexType with content type ELEMENT_ONLY
class eventOutcomeInformationComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}eventOutcomeInformationComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeInformationComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 480, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}eventOutcome uses Python identifier eventOutcome
    __eventOutcome = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventOutcome'), 'eventOutcome', '__httpwww_loc_govpremisv3_eventOutcomeInformationComplexType_httpwww_loc_govpremisv3eventOutcome', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1003, 1), )

    
    eventOutcome = property(__eventOutcome.value, __eventOutcome.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}eventOutcomeDetail uses Python identifier eventOutcomeDetail
    __eventOutcomeDetail = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetail'), 'eventOutcomeDetail', '__httpwww_loc_govpremisv3_eventOutcomeInformationComplexType_httpwww_loc_govpremisv3eventOutcomeDetail', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1075, 1), )

    
    eventOutcomeDetail = property(__eventOutcomeDetail.value, __eventOutcomeDetail.set, None, None)

    _ElementMap.update({
        __eventOutcome.name() : __eventOutcome,
        __eventOutcomeDetail.name() : __eventOutcomeDetail
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.eventOutcomeInformationComplexType = eventOutcomeInformationComplexType
Namespace.addCategoryObject('typeBinding', 'eventOutcomeInformationComplexType', eventOutcomeInformationComplexType)


# Complex type {http://www.loc.gov/premis/v3}fixityComplexType with content type ELEMENT_ONLY
class fixityComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}fixityComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'fixityComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 493, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}messageDigest uses Python identifier messageDigest
    __messageDigest = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageDigest'), 'messageDigest', '__httpwww_loc_govpremisv3_fixityComplexType_httpwww_loc_govpremisv3messageDigest', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 966, 1), )

    
    messageDigest = property(__messageDigest.value, __messageDigest.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}messageDigestAlgorithm uses Python identifier messageDigestAlgorithm
    __messageDigestAlgorithm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageDigestAlgorithm'), 'messageDigestAlgorithm', '__httpwww_loc_govpremisv3_fixityComplexType_httpwww_loc_govpremisv3messageDigestAlgorithm', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1023, 1), )

    
    messageDigestAlgorithm = property(__messageDigestAlgorithm.value, __messageDigestAlgorithm.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}messageDigestOriginator uses Python identifier messageDigestOriginator
    __messageDigestOriginator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'messageDigestOriginator'), 'messageDigestOriginator', '__httpwww_loc_govpremisv3_fixityComplexType_httpwww_loc_govpremisv3messageDigestOriginator', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1024, 1), )

    
    messageDigestOriginator = property(__messageDigestOriginator.value, __messageDigestOriginator.set, None, None)

    _ElementMap.update({
        __messageDigest.name() : __messageDigest,
        __messageDigestAlgorithm.name() : __messageDigestAlgorithm,
        __messageDigestOriginator.name() : __messageDigestOriginator
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.fixityComplexType = fixityComplexType
Namespace.addCategoryObject('typeBinding', 'fixityComplexType', fixityComplexType)


# Complex type {http://www.loc.gov/premis/v3}formatComplexType with content type ELEMENT_ONLY
class formatComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}formatComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'formatComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 504, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}formatNote uses Python identifier formatNote
    __formatNote = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'formatNote'), 'formatNote', '__httpwww_loc_govpremisv3_formatComplexType_httpwww_loc_govpremisv3formatNote', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 952, 1), )

    
    formatNote = property(__formatNote.value, __formatNote.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}formatDesignation uses Python identifier formatDesignation
    __formatDesignation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'formatDesignation'), 'formatDesignation', '__httpwww_loc_govpremisv3_formatComplexType_httpwww_loc_govpremisv3formatDesignation', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1079, 1), )

    
    formatDesignation = property(__formatDesignation.value, __formatDesignation.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}formatRegistry uses Python identifier formatRegistry
    __formatRegistry = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'formatRegistry'), 'formatRegistry', '__httpwww_loc_govpremisv3_formatComplexType_httpwww_loc_govpremisv3formatRegistry', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1080, 1), )

    
    formatRegistry = property(__formatRegistry.value, __formatRegistry.set, None, None)

    _ElementMap.update({
        __formatNote.name() : __formatNote,
        __formatDesignation.name() : __formatDesignation,
        __formatRegistry.name() : __formatRegistry
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.formatComplexType = formatComplexType
Namespace.addCategoryObject('typeBinding', 'formatComplexType', formatComplexType)


# Complex type {http://www.loc.gov/premis/v3}formatDesignationComplexType with content type ELEMENT_ONLY
class formatDesignationComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}formatDesignationComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'formatDesignationComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 521, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}formatVersion uses Python identifier formatVersion
    __formatVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'formatVersion'), 'formatVersion', '__httpwww_loc_govpremisv3_formatDesignationComplexType_httpwww_loc_govpremisv3formatVersion', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 953, 1), )

    
    formatVersion = property(__formatVersion.value, __formatVersion.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}formatName uses Python identifier formatName
    __formatName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'formatName'), 'formatName', '__httpwww_loc_govpremisv3_formatDesignationComplexType_httpwww_loc_govpremisv3formatName', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1005, 1), )

    
    formatName = property(__formatName.value, __formatName.set, None, None)

    _ElementMap.update({
        __formatVersion.name() : __formatVersion,
        __formatName.name() : __formatName
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.formatDesignationComplexType = formatDesignationComplexType
Namespace.addCategoryObject('typeBinding', 'formatDesignationComplexType', formatDesignationComplexType)


# Complex type {http://www.loc.gov/premis/v3}formatRegistryComplexType with content type ELEMENT_ONLY
class formatRegistryComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}formatRegistryComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'formatRegistryComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 530, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}formatRegistryName uses Python identifier formatRegistryName
    __formatRegistryName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'formatRegistryName'), 'formatRegistryName', '__httpwww_loc_govpremisv3_formatRegistryComplexType_httpwww_loc_govpremisv3formatRegistryName', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1006, 1), )

    
    formatRegistryName = property(__formatRegistryName.value, __formatRegistryName.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}formatRegistryKey uses Python identifier formatRegistryKey
    __formatRegistryKey = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'formatRegistryKey'), 'formatRegistryKey', '__httpwww_loc_govpremisv3_formatRegistryComplexType_httpwww_loc_govpremisv3formatRegistryKey', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1007, 1), )

    
    formatRegistryKey = property(__formatRegistryKey.value, __formatRegistryKey.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}formatRegistryRole uses Python identifier formatRegistryRole
    __formatRegistryRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'formatRegistryRole'), 'formatRegistryRole', '__httpwww_loc_govpremisv3_formatRegistryComplexType_httpwww_loc_govpremisv3formatRegistryRole', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1008, 1), )

    
    formatRegistryRole = property(__formatRegistryRole.value, __formatRegistryRole.set, None, None)

    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_formatRegistryComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 536, 2)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 536, 2)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        __formatRegistryName.name() : __formatRegistryName,
        __formatRegistryKey.name() : __formatRegistryKey,
        __formatRegistryRole.name() : __formatRegistryRole
    })
    _AttributeMap.update({
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.formatRegistryComplexType = formatRegistryComplexType
Namespace.addCategoryObject('typeBinding', 'formatRegistryComplexType', formatRegistryComplexType)


# Complex type {http://www.loc.gov/premis/v3}inhibitorsComplexType with content type ELEMENT_ONLY
class inhibitorsComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}inhibitorsComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'inhibitorsComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 542, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}inhibitorKey uses Python identifier inhibitorKey
    __inhibitorKey = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'inhibitorKey'), 'inhibitorKey', '__httpwww_loc_govpremisv3_inhibitorsComplexType_httpwww_loc_govpremisv3inhibitorKey', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 955, 1), )

    
    inhibitorKey = property(__inhibitorKey.value, __inhibitorKey.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}inhibitorTarget uses Python identifier inhibitorTarget
    __inhibitorTarget = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'inhibitorTarget'), 'inhibitorTarget', '__httpwww_loc_govpremisv3_inhibitorsComplexType_httpwww_loc_govpremisv3inhibitorTarget', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1011, 1), )

    
    inhibitorTarget = property(__inhibitorTarget.value, __inhibitorTarget.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}inhibitorType uses Python identifier inhibitorType
    __inhibitorType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'inhibitorType'), 'inhibitorType', '__httpwww_loc_govpremisv3_inhibitorsComplexType_httpwww_loc_govpremisv3inhibitorType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1012, 1), )

    
    inhibitorType = property(__inhibitorType.value, __inhibitorType.set, None, None)

    _ElementMap.update({
        __inhibitorKey.name() : __inhibitorKey,
        __inhibitorTarget.name() : __inhibitorTarget,
        __inhibitorType.name() : __inhibitorType
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.inhibitorsComplexType = inhibitorsComplexType
Namespace.addCategoryObject('typeBinding', 'inhibitorsComplexType', inhibitorsComplexType)


# Complex type {http://www.loc.gov/premis/v3}licenseDocumentationIdentifierComplexType with content type ELEMENT_ONLY
class licenseDocumentationIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}licenseDocumentationIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 552, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}licenseDocumentationIdentifierValue uses Python identifier licenseDocumentationIdentifierValue
    __licenseDocumentationIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationIdentifierValue'), 'licenseDocumentationIdentifierValue', '__httpwww_loc_govpremisv3_licenseDocumentationIdentifierComplexType_httpwww_loc_govpremisv3licenseDocumentationIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 956, 1), )

    
    licenseDocumentationIdentifierValue = property(__licenseDocumentationIdentifierValue.value, __licenseDocumentationIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}licenseDocumentationIdentifierType uses Python identifier licenseDocumentationIdentifierType
    __licenseDocumentationIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationIdentifierType'), 'licenseDocumentationIdentifierType', '__httpwww_loc_govpremisv3_licenseDocumentationIdentifierComplexType_httpwww_loc_govpremisv3licenseDocumentationIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1013, 1), )

    
    licenseDocumentationIdentifierType = property(__licenseDocumentationIdentifierType.value, __licenseDocumentationIdentifierType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}licenseDocumentationRole uses Python identifier licenseDocumentationRole
    __licenseDocumentationRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationRole'), 'licenseDocumentationRole', '__httpwww_loc_govpremisv3_licenseDocumentationIdentifierComplexType_httpwww_loc_govpremisv3licenseDocumentationRole', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1014, 1), )

    
    licenseDocumentationRole = property(__licenseDocumentationRole.value, __licenseDocumentationRole.set, None, None)

    _ElementMap.update({
        __licenseDocumentationIdentifierValue.name() : __licenseDocumentationIdentifierValue,
        __licenseDocumentationIdentifierType.name() : __licenseDocumentationIdentifierType,
        __licenseDocumentationRole.name() : __licenseDocumentationRole
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.licenseDocumentationIdentifierComplexType = licenseDocumentationIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'licenseDocumentationIdentifierComplexType', licenseDocumentationIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}licenseInformationComplexType with content type ELEMENT_ONLY
class licenseInformationComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}licenseInformationComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'licenseInformationComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 564, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}licenseNote uses Python identifier licenseNote
    __licenseNote = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'licenseNote'), 'licenseNote', '__httpwww_loc_govpremisv3_licenseInformationComplexType_httpwww_loc_govpremisv3licenseNote', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 958, 1), )

    
    licenseNote = property(__licenseNote.value, __licenseNote.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}licenseTerms uses Python identifier licenseTerms
    __licenseTerms = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'licenseTerms'), 'licenseTerms', '__httpwww_loc_govpremisv3_licenseInformationComplexType_httpwww_loc_govpremisv3licenseTerms', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 959, 1), )

    
    licenseTerms = property(__licenseTerms.value, __licenseTerms.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}licenseDocumentationIdentifier uses Python identifier licenseDocumentationIdentifier
    __licenseDocumentationIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationIdentifier'), 'licenseDocumentationIdentifier', '__httpwww_loc_govpremisv3_licenseInformationComplexType_httpwww_loc_govpremisv3licenseDocumentationIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1082, 1), )

    
    licenseDocumentationIdentifier = property(__licenseDocumentationIdentifier.value, __licenseDocumentationIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}licenseApplicableDates uses Python identifier licenseApplicableDates
    __licenseApplicableDates = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'licenseApplicableDates'), 'licenseApplicableDates', '__httpwww_loc_govpremisv3_licenseInformationComplexType_httpwww_loc_govpremisv3licenseApplicableDates', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1121, 1), )

    
    licenseApplicableDates = property(__licenseApplicableDates.value, __licenseApplicableDates.set, None, None)

    _ElementMap.update({
        __licenseNote.name() : __licenseNote,
        __licenseTerms.name() : __licenseTerms,
        __licenseDocumentationIdentifier.name() : __licenseDocumentationIdentifier,
        __licenseApplicableDates.name() : __licenseApplicableDates
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.licenseInformationComplexType = licenseInformationComplexType
Namespace.addCategoryObject('typeBinding', 'licenseInformationComplexType', licenseInformationComplexType)


# Complex type {http://www.loc.gov/premis/v3}linkingAgentIdentifierComplexType with content type ELEMENT_ONLY
class linkingAgentIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}linkingAgentIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 588, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}linkingAgentIdentifierValue uses Python identifier linkingAgentIdentifierValue
    __linkingAgentIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifierValue'), 'linkingAgentIdentifierValue', '__httpwww_loc_govpremisv3_linkingAgentIdentifierComplexType_httpwww_loc_govpremisv3linkingAgentIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 960, 1), )

    
    linkingAgentIdentifierValue = property(__linkingAgentIdentifierValue.value, __linkingAgentIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingAgentIdentifierType uses Python identifier linkingAgentIdentifierType
    __linkingAgentIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifierType'), 'linkingAgentIdentifierType', '__httpwww_loc_govpremisv3_linkingAgentIdentifierComplexType_httpwww_loc_govpremisv3linkingAgentIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1016, 1), )

    
    linkingAgentIdentifierType = property(__linkingAgentIdentifierType.value, __linkingAgentIdentifierType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingAgentRole uses Python identifier linkingAgentRole
    __linkingAgentRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentRole'), 'linkingAgentRole', '__httpwww_loc_govpremisv3_linkingAgentIdentifierComplexType_httpwww_loc_govpremisv3linkingAgentRole', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1017, 1), )

    
    linkingAgentRole = property(__linkingAgentRole.value, __linkingAgentRole.set, None, None)

    
    # Attribute LinkAgentXmlID uses Python identifier LinkAgentXmlID
    __LinkAgentXmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LinkAgentXmlID'), 'LinkAgentXmlID', '__httpwww_loc_govpremisv3_linkingAgentIdentifierComplexType_LinkAgentXmlID', pyxb.binding.datatypes.IDREF)
    __LinkAgentXmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 594, 2)
    __LinkAgentXmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 594, 2)
    
    LinkAgentXmlID = property(__LinkAgentXmlID.value, __LinkAgentXmlID.set, None, None)

    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_linkingAgentIdentifierComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 595, 2)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 595, 2)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        __linkingAgentIdentifierValue.name() : __linkingAgentIdentifierValue,
        __linkingAgentIdentifierType.name() : __linkingAgentIdentifierType,
        __linkingAgentRole.name() : __linkingAgentRole
    })
    _AttributeMap.update({
        __LinkAgentXmlID.name() : __LinkAgentXmlID,
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.linkingAgentIdentifierComplexType = linkingAgentIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'linkingAgentIdentifierComplexType', linkingAgentIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}linkingEnvironmentIdentifierComplexType with content type ELEMENT_ONLY
class linkingEnvironmentIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}linkingEnvironmentIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 604, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}linkingEnvironmentIdentifierType uses Python identifier linkingEnvironmentIdentifierType
    __linkingEnvironmentIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentIdentifierType'), 'linkingEnvironmentIdentifierType', '__httpwww_loc_govpremisv3_linkingEnvironmentIdentifierComplexType_httpwww_loc_govpremisv3linkingEnvironmentIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 961, 4), )

    
    linkingEnvironmentIdentifierType = property(__linkingEnvironmentIdentifierType.value, __linkingEnvironmentIdentifierType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingEnvironmentIdentifierValue uses Python identifier linkingEnvironmentIdentifierValue
    __linkingEnvironmentIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentIdentifierValue'), 'linkingEnvironmentIdentifierValue', '__httpwww_loc_govpremisv3_linkingEnvironmentIdentifierComplexType_httpwww_loc_govpremisv3linkingEnvironmentIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 962, 4), )

    
    linkingEnvironmentIdentifierValue = property(__linkingEnvironmentIdentifierValue.value, __linkingEnvironmentIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingEnvironmentRole uses Python identifier linkingEnvironmentRole
    __linkingEnvironmentRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentRole'), 'linkingEnvironmentRole', '__httpwww_loc_govpremisv3_linkingEnvironmentIdentifierComplexType_httpwww_loc_govpremisv3linkingEnvironmentRole', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1019, 4), )

    
    linkingEnvironmentRole = property(__linkingEnvironmentRole.value, __linkingEnvironmentRole.set, None, None)

    
    # Attribute LinkEventXmlID uses Python identifier LinkEventXmlID
    __LinkEventXmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LinkEventXmlID'), 'LinkEventXmlID', '__httpwww_loc_govpremisv3_linkingEnvironmentIdentifierComplexType_LinkEventXmlID', pyxb.binding.datatypes.IDREF)
    __LinkEventXmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 610, 8)
    __LinkEventXmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 610, 8)
    
    LinkEventXmlID = property(__LinkEventXmlID.value, __LinkEventXmlID.set, None, None)

    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_linkingEnvironmentIdentifierComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 611, 8)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 611, 8)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        __linkingEnvironmentIdentifierType.name() : __linkingEnvironmentIdentifierType,
        __linkingEnvironmentIdentifierValue.name() : __linkingEnvironmentIdentifierValue,
        __linkingEnvironmentRole.name() : __linkingEnvironmentRole
    })
    _AttributeMap.update({
        __LinkEventXmlID.name() : __LinkEventXmlID,
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.linkingEnvironmentIdentifierComplexType = linkingEnvironmentIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'linkingEnvironmentIdentifierComplexType', linkingEnvironmentIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}linkingEventIdentifierComplexType with content type ELEMENT_ONLY
class linkingEventIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}linkingEventIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 617, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}linkingEventIdentifierValue uses Python identifier linkingEventIdentifierValue
    __linkingEventIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifierValue'), 'linkingEventIdentifierValue', '__httpwww_loc_govpremisv3_linkingEventIdentifierComplexType_httpwww_loc_govpremisv3linkingEventIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 963, 1), )

    
    linkingEventIdentifierValue = property(__linkingEventIdentifierValue.value, __linkingEventIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingEventIdentifierType uses Python identifier linkingEventIdentifierType
    __linkingEventIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifierType'), 'linkingEventIdentifierType', '__httpwww_loc_govpremisv3_linkingEventIdentifierComplexType_httpwww_loc_govpremisv3linkingEventIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1018, 1), )

    
    linkingEventIdentifierType = property(__linkingEventIdentifierType.value, __linkingEventIdentifierType.set, None, None)

    
    # Attribute LinkEventXmlID uses Python identifier LinkEventXmlID
    __LinkEventXmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LinkEventXmlID'), 'LinkEventXmlID', '__httpwww_loc_govpremisv3_linkingEventIdentifierComplexType_LinkEventXmlID', pyxb.binding.datatypes.IDREF)
    __LinkEventXmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 622, 2)
    __LinkEventXmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 622, 2)
    
    LinkEventXmlID = property(__LinkEventXmlID.value, __LinkEventXmlID.set, None, None)

    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_linkingEventIdentifierComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 623, 2)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 623, 2)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        __linkingEventIdentifierValue.name() : __linkingEventIdentifierValue,
        __linkingEventIdentifierType.name() : __linkingEventIdentifierType
    })
    _AttributeMap.update({
        __LinkEventXmlID.name() : __LinkEventXmlID,
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.linkingEventIdentifierComplexType = linkingEventIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'linkingEventIdentifierComplexType', linkingEventIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}linkingObjectIdentifierComplexType with content type ELEMENT_ONLY
class linkingObjectIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}linkingObjectIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 629, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}linkingObjectIdentifierValue uses Python identifier linkingObjectIdentifierValue
    __linkingObjectIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifierValue'), 'linkingObjectIdentifierValue', '__httpwww_loc_govpremisv3_linkingObjectIdentifierComplexType_httpwww_loc_govpremisv3linkingObjectIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 964, 1), )

    
    linkingObjectIdentifierValue = property(__linkingObjectIdentifierValue.value, __linkingObjectIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingObjectIdentifierType uses Python identifier linkingObjectIdentifierType
    __linkingObjectIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifierType'), 'linkingObjectIdentifierType', '__httpwww_loc_govpremisv3_linkingObjectIdentifierComplexType_httpwww_loc_govpremisv3linkingObjectIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1020, 1), )

    
    linkingObjectIdentifierType = property(__linkingObjectIdentifierType.value, __linkingObjectIdentifierType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingObjectRole uses Python identifier linkingObjectRole
    __linkingObjectRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectRole'), 'linkingObjectRole', '__httpwww_loc_govpremisv3_linkingObjectIdentifierComplexType_httpwww_loc_govpremisv3linkingObjectRole', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1021, 1), )

    
    linkingObjectRole = property(__linkingObjectRole.value, __linkingObjectRole.set, None, None)

    
    # Attribute LinkObjectXmlID uses Python identifier LinkObjectXmlID
    __LinkObjectXmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LinkObjectXmlID'), 'LinkObjectXmlID', '__httpwww_loc_govpremisv3_linkingObjectIdentifierComplexType_LinkObjectXmlID', pyxb.binding.datatypes.IDREF)
    __LinkObjectXmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 635, 2)
    __LinkObjectXmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 635, 2)
    
    LinkObjectXmlID = property(__LinkObjectXmlID.value, __LinkObjectXmlID.set, None, None)

    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_linkingObjectIdentifierComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 636, 2)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 636, 2)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        __linkingObjectIdentifierValue.name() : __linkingObjectIdentifierValue,
        __linkingObjectIdentifierType.name() : __linkingObjectIdentifierType,
        __linkingObjectRole.name() : __linkingObjectRole
    })
    _AttributeMap.update({
        __LinkObjectXmlID.name() : __LinkObjectXmlID,
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.linkingObjectIdentifierComplexType = linkingObjectIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'linkingObjectIdentifierComplexType', linkingObjectIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}linkingRightsStatementIdentifierComplexType with content type ELEMENT_ONLY
class linkingRightsStatementIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}linkingRightsStatementIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 642, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}linkingRightsStatementIdentifierValue uses Python identifier linkingRightsStatementIdentifierValue
    __linkingRightsStatementIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifierValue'), 'linkingRightsStatementIdentifierValue', '__httpwww_loc_govpremisv3_linkingRightsStatementIdentifierComplexType_httpwww_loc_govpremisv3linkingRightsStatementIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 965, 1), )

    
    linkingRightsStatementIdentifierValue = property(__linkingRightsStatementIdentifierValue.value, __linkingRightsStatementIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingRightsStatementIdentifierType uses Python identifier linkingRightsStatementIdentifierType
    __linkingRightsStatementIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifierType'), 'linkingRightsStatementIdentifierType', '__httpwww_loc_govpremisv3_linkingRightsStatementIdentifierComplexType_httpwww_loc_govpremisv3linkingRightsStatementIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1022, 1), )

    
    linkingRightsStatementIdentifierType = property(__linkingRightsStatementIdentifierType.value, __linkingRightsStatementIdentifierType.set, None, None)

    
    # Attribute LinkPermissionStatementXmlID uses Python identifier LinkPermissionStatementXmlID
    __LinkPermissionStatementXmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LinkPermissionStatementXmlID'), 'LinkPermissionStatementXmlID', '__httpwww_loc_govpremisv3_linkingRightsStatementIdentifierComplexType_LinkPermissionStatementXmlID', pyxb.binding.datatypes.IDREF)
    __LinkPermissionStatementXmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 647, 2)
    __LinkPermissionStatementXmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 647, 2)
    
    LinkPermissionStatementXmlID = property(__LinkPermissionStatementXmlID.value, __LinkPermissionStatementXmlID.set, None, None)

    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_linkingRightsStatementIdentifierComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 648, 2)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 648, 2)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        __linkingRightsStatementIdentifierValue.name() : __linkingRightsStatementIdentifierValue,
        __linkingRightsStatementIdentifierType.name() : __linkingRightsStatementIdentifierType
    })
    _AttributeMap.update({
        __LinkPermissionStatementXmlID.name() : __LinkPermissionStatementXmlID,
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.linkingRightsStatementIdentifierComplexType = linkingRightsStatementIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'linkingRightsStatementIdentifierComplexType', linkingRightsStatementIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}objectCharacteristicsComplexType with content type ELEMENT_ONLY
class objectCharacteristicsComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}objectCharacteristicsComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'objectCharacteristicsComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 654, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}compositionLevel uses Python identifier compositionLevel
    __compositionLevel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'compositionLevel'), 'compositionLevel', '__httpwww_loc_govpremisv3_objectCharacteristicsComplexType_httpwww_loc_govpremisv3compositionLevel', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1066, 4), )

    
    compositionLevel = property(__compositionLevel.value, __compositionLevel.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}creatingApplication uses Python identifier creatingApplication
    __creatingApplication = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'creatingApplication'), 'creatingApplication', '__httpwww_loc_govpremisv3_objectCharacteristicsComplexType_httpwww_loc_govpremisv3creatingApplication', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1069, 1), )

    
    creatingApplication = property(__creatingApplication.value, __creatingApplication.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}fixity uses Python identifier fixity
    __fixity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'fixity'), 'fixity', '__httpwww_loc_govpremisv3_objectCharacteristicsComplexType_httpwww_loc_govpremisv3fixity', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1077, 1), )

    
    fixity = property(__fixity.value, __fixity.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}format uses Python identifier format
    __format = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'format'), 'format', '__httpwww_loc_govpremisv3_objectCharacteristicsComplexType_httpwww_loc_govpremisv3format', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1078, 1), )

    
    format = property(__format.value, __format.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}inhibitors uses Python identifier inhibitors
    __inhibitors = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'inhibitors'), 'inhibitors', '__httpwww_loc_govpremisv3_objectCharacteristicsComplexType_httpwww_loc_govpremisv3inhibitors', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1081, 1), )

    
    inhibitors = property(__inhibitors.value, __inhibitors.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}size uses Python identifier size
    __size = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'size'), 'size', '__httpwww_loc_govpremisv3_objectCharacteristicsComplexType_httpwww_loc_govpremisv3size', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1112, 1), )

    
    size = property(__size.value, __size.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}objectCharacteristicsExtension uses Python identifier objectCharacteristicsExtension
    __objectCharacteristicsExtension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'objectCharacteristicsExtension'), 'objectCharacteristicsExtension', '__httpwww_loc_govpremisv3_objectCharacteristicsComplexType_httpwww_loc_govpremisv3objectCharacteristicsExtension', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1138, 1), )

    
    objectCharacteristicsExtension = property(__objectCharacteristicsExtension.value, __objectCharacteristicsExtension.set, None, None)

    _ElementMap.update({
        __compositionLevel.name() : __compositionLevel,
        __creatingApplication.name() : __creatingApplication,
        __fixity.name() : __fixity,
        __format.name() : __format,
        __inhibitors.name() : __inhibitors,
        __size.name() : __size,
        __objectCharacteristicsExtension.name() : __objectCharacteristicsExtension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.objectCharacteristicsComplexType = objectCharacteristicsComplexType
Namespace.addCategoryObject('typeBinding', 'objectCharacteristicsComplexType', objectCharacteristicsComplexType)


# Complex type {http://www.loc.gov/premis/v3}objectIdentifierComplexType with content type ELEMENT_ONLY
class objectIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}objectIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'objectIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 669, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}objectIdentifierValue uses Python identifier objectIdentifierValue
    __objectIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifierValue'), 'objectIdentifierValue', '__httpwww_loc_govpremisv3_objectIdentifierComplexType_httpwww_loc_govpremisv3objectIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 967, 1), )

    
    objectIdentifierValue = property(__objectIdentifierValue.value, __objectIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}objectIdentifierType uses Python identifier objectIdentifierType
    __objectIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifierType'), 'objectIdentifierType', '__httpwww_loc_govpremisv3_objectIdentifierComplexType_httpwww_loc_govpremisv3objectIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1025, 1), )

    
    objectIdentifierType = property(__objectIdentifierType.value, __objectIdentifierType.set, None, None)

    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_objectIdentifierComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 674, 2)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 674, 2)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        __objectIdentifierValue.name() : __objectIdentifierValue,
        __objectIdentifierType.name() : __objectIdentifierType
    })
    _AttributeMap.update({
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.objectIdentifierComplexType = objectIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'objectIdentifierComplexType', objectIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}originalNameComplexType with content type SIMPLE
class originalNameComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}originalNameComplexType with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'originalNameComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 680, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_originalNameComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 683, 4)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 683, 4)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.originalNameComplexType = originalNameComplexType
Namespace.addCategoryObject('typeBinding', 'originalNameComplexType', originalNameComplexType)


# Complex type {http://www.loc.gov/premis/v3}otherRightsDocumentationIdentifierComplexType with content type ELEMENT_ONLY
class otherRightsDocumentationIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}otherRightsDocumentationIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 691, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}otherRightsDocumentationIdentifierValue uses Python identifier otherRightsDocumentationIdentifierValue
    __otherRightsDocumentationIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationIdentifierValue'), 'otherRightsDocumentationIdentifierValue', '__httpwww_loc_govpremisv3_otherRightsDocumentationIdentifierComplexType_httpwww_loc_govpremisv3otherRightsDocumentationIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 968, 1), )

    
    otherRightsDocumentationIdentifierValue = property(__otherRightsDocumentationIdentifierValue.value, __otherRightsDocumentationIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}otherRightsDocumentationRole uses Python identifier otherRightsDocumentationRole
    __otherRightsDocumentationRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationRole'), 'otherRightsDocumentationRole', '__httpwww_loc_govpremisv3_otherRightsDocumentationIdentifierComplexType_httpwww_loc_govpremisv3otherRightsDocumentationRole', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1027, 1), )

    
    otherRightsDocumentationRole = property(__otherRightsDocumentationRole.value, __otherRightsDocumentationRole.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}otherRightsDocumentationIdentifierType uses Python identifier otherRightsDocumentationIdentifierType
    __otherRightsDocumentationIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationIdentifierType'), 'otherRightsDocumentationIdentifierType', '__httpwww_loc_govpremisv3_otherRightsDocumentationIdentifierComplexType_httpwww_loc_govpremisv3otherRightsDocumentationIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1028, 1), )

    
    otherRightsDocumentationIdentifierType = property(__otherRightsDocumentationIdentifierType.value, __otherRightsDocumentationIdentifierType.set, None, None)

    _ElementMap.update({
        __otherRightsDocumentationIdentifierValue.name() : __otherRightsDocumentationIdentifierValue,
        __otherRightsDocumentationRole.name() : __otherRightsDocumentationRole,
        __otherRightsDocumentationIdentifierType.name() : __otherRightsDocumentationIdentifierType
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.otherRightsDocumentationIdentifierComplexType = otherRightsDocumentationIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'otherRightsDocumentationIdentifierComplexType', otherRightsDocumentationIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}otherRightsInformationComplexType with content type ELEMENT_ONLY
class otherRightsInformationComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}otherRightsInformationComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'otherRightsInformationComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 702, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}otherRightsNote uses Python identifier otherRightsNote
    __otherRightsNote = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherRightsNote'), 'otherRightsNote', '__httpwww_loc_govpremisv3_otherRightsInformationComplexType_httpwww_loc_govpremisv3otherRightsNote', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 969, 1), )

    
    otherRightsNote = property(__otherRightsNote.value, __otherRightsNote.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}otherRightsBasis uses Python identifier otherRightsBasis
    __otherRightsBasis = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherRightsBasis'), 'otherRightsBasis', '__httpwww_loc_govpremisv3_otherRightsInformationComplexType_httpwww_loc_govpremisv3otherRightsBasis', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1026, 1), )

    
    otherRightsBasis = property(__otherRightsBasis.value, __otherRightsBasis.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}otherRightsDocumentationIdentifier uses Python identifier otherRightsDocumentationIdentifier
    __otherRightsDocumentationIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationIdentifier'), 'otherRightsDocumentationIdentifier', '__httpwww_loc_govpremisv3_otherRightsInformationComplexType_httpwww_loc_govpremisv3otherRightsDocumentationIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1092, 1), )

    
    otherRightsDocumentationIdentifier = property(__otherRightsDocumentationIdentifier.value, __otherRightsDocumentationIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}otherRightsApplicableDates uses Python identifier otherRightsApplicableDates
    __otherRightsApplicableDates = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherRightsApplicableDates'), 'otherRightsApplicableDates', '__httpwww_loc_govpremisv3_otherRightsInformationComplexType_httpwww_loc_govpremisv3otherRightsApplicableDates', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1124, 1), )

    
    otherRightsApplicableDates = property(__otherRightsApplicableDates.value, __otherRightsApplicableDates.set, None, None)

    _ElementMap.update({
        __otherRightsNote.name() : __otherRightsNote,
        __otherRightsBasis.name() : __otherRightsBasis,
        __otherRightsDocumentationIdentifier.name() : __otherRightsDocumentationIdentifier,
        __otherRightsApplicableDates.name() : __otherRightsApplicableDates
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.otherRightsInformationComplexType = otherRightsInformationComplexType
Namespace.addCategoryObject('typeBinding', 'otherRightsInformationComplexType', otherRightsInformationComplexType)


# Complex type {http://www.loc.gov/premis/v3}preservationLevelComplexType with content type ELEMENT_ONLY
class preservationLevelComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}preservationLevelComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'preservationLevelComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 714, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}preservationLevelRationale uses Python identifier preservationLevelRationale
    __preservationLevelRationale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelRationale'), 'preservationLevelRationale', '__httpwww_loc_govpremisv3_preservationLevelComplexType_httpwww_loc_govpremisv3preservationLevelRationale', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 970, 1), )

    
    preservationLevelRationale = property(__preservationLevelRationale.value, __preservationLevelRationale.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}preservationLevelType uses Python identifier preservationLevelType
    __preservationLevelType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelType'), 'preservationLevelType', '__httpwww_loc_govpremisv3_preservationLevelComplexType_httpwww_loc_govpremisv3preservationLevelType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1029, 4), )

    
    preservationLevelType = property(__preservationLevelType.value, __preservationLevelType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}preservationLevelValue uses Python identifier preservationLevelValue
    __preservationLevelValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelValue'), 'preservationLevelValue', '__httpwww_loc_govpremisv3_preservationLevelComplexType_httpwww_loc_govpremisv3preservationLevelValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1030, 3), )

    
    preservationLevelValue = property(__preservationLevelValue.value, __preservationLevelValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}preservationLevelRole uses Python identifier preservationLevelRole
    __preservationLevelRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelRole'), 'preservationLevelRole', '__httpwww_loc_govpremisv3_preservationLevelComplexType_httpwww_loc_govpremisv3preservationLevelRole', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1031, 1), )

    
    preservationLevelRole = property(__preservationLevelRole.value, __preservationLevelRole.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}preservationLevelDateAssigned uses Python identifier preservationLevelDateAssigned
    __preservationLevelDateAssigned = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelDateAssigned'), 'preservationLevelDateAssigned', '__httpwww_loc_govpremisv3_preservationLevelComplexType_httpwww_loc_govpremisv3preservationLevelDateAssigned', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1122, 1), )

    
    preservationLevelDateAssigned = property(__preservationLevelDateAssigned.value, __preservationLevelDateAssigned.set, None, None)

    _ElementMap.update({
        __preservationLevelRationale.name() : __preservationLevelRationale,
        __preservationLevelType.name() : __preservationLevelType,
        __preservationLevelValue.name() : __preservationLevelValue,
        __preservationLevelRole.name() : __preservationLevelRole,
        __preservationLevelDateAssigned.name() : __preservationLevelDateAssigned
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.preservationLevelComplexType = preservationLevelComplexType
Namespace.addCategoryObject('typeBinding', 'preservationLevelComplexType', preservationLevelComplexType)


# Complex type {http://www.loc.gov/premis/v3}relatedEventIdentifierComplexType with content type ELEMENT_ONLY
class relatedEventIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}relatedEventIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'relatedEventIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 732, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}relatedEventIdentifierValue uses Python identifier relatedEventIdentifierValue
    __relatedEventIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relatedEventIdentifierValue'), 'relatedEventIdentifierValue', '__httpwww_loc_govpremisv3_relatedEventIdentifierComplexType_httpwww_loc_govpremisv3relatedEventIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 971, 1), )

    
    relatedEventIdentifierValue = property(__relatedEventIdentifierValue.value, __relatedEventIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}relatedEventIdentifierType uses Python identifier relatedEventIdentifierType
    __relatedEventIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relatedEventIdentifierType'), 'relatedEventIdentifierType', '__httpwww_loc_govpremisv3_relatedEventIdentifierComplexType_httpwww_loc_govpremisv3relatedEventIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1032, 4), )

    
    relatedEventIdentifierType = property(__relatedEventIdentifierType.value, __relatedEventIdentifierType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}relatedEventSequence uses Python identifier relatedEventSequence
    __relatedEventSequence = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relatedEventSequence'), 'relatedEventSequence', '__httpwww_loc_govpremisv3_relatedEventIdentifierComplexType_httpwww_loc_govpremisv3relatedEventSequence', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1110, 1), )

    
    relatedEventSequence = property(__relatedEventSequence.value, __relatedEventSequence.set, None, None)

    
    # Attribute RelEventXmlID uses Python identifier RelEventXmlID
    __RelEventXmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'RelEventXmlID'), 'RelEventXmlID', '__httpwww_loc_govpremisv3_relatedEventIdentifierComplexType_RelEventXmlID', pyxb.binding.datatypes.IDREF)
    __RelEventXmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 738, 2)
    __RelEventXmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 738, 2)
    
    RelEventXmlID = property(__RelEventXmlID.value, __RelEventXmlID.set, None, None)

    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_relatedEventIdentifierComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 739, 2)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 739, 2)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        __relatedEventIdentifierValue.name() : __relatedEventIdentifierValue,
        __relatedEventIdentifierType.name() : __relatedEventIdentifierType,
        __relatedEventSequence.name() : __relatedEventSequence
    })
    _AttributeMap.update({
        __RelEventXmlID.name() : __RelEventXmlID,
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.relatedEventIdentifierComplexType = relatedEventIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'relatedEventIdentifierComplexType', relatedEventIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}relatedObjectIdentifierComplexType with content type ELEMENT_ONLY
class relatedObjectIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}relatedObjectIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'relatedObjectIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 747, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}relatedObjectIdentifierValue uses Python identifier relatedObjectIdentifierValue
    __relatedObjectIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectIdentifierValue'), 'relatedObjectIdentifierValue', '__httpwww_loc_govpremisv3_relatedObjectIdentifierComplexType_httpwww_loc_govpremisv3relatedObjectIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 972, 1), )

    
    relatedObjectIdentifierValue = property(__relatedObjectIdentifierValue.value, __relatedObjectIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}relatedObjectIdentifierType uses Python identifier relatedObjectIdentifierType
    __relatedObjectIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectIdentifierType'), 'relatedObjectIdentifierType', '__httpwww_loc_govpremisv3_relatedObjectIdentifierComplexType_httpwww_loc_govpremisv3relatedObjectIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1035, 1), )

    
    relatedObjectIdentifierType = property(__relatedObjectIdentifierType.value, __relatedObjectIdentifierType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}relatedObjectSequence uses Python identifier relatedObjectSequence
    __relatedObjectSequence = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectSequence'), 'relatedObjectSequence', '__httpwww_loc_govpremisv3_relatedObjectIdentifierComplexType_httpwww_loc_govpremisv3relatedObjectSequence', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1111, 1), )

    
    relatedObjectSequence = property(__relatedObjectSequence.value, __relatedObjectSequence.set, None, None)

    
    # Attribute RelObjectXmlID uses Python identifier RelObjectXmlID
    __RelObjectXmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'RelObjectXmlID'), 'RelObjectXmlID', '__httpwww_loc_govpremisv3_relatedObjectIdentifierComplexType_RelObjectXmlID', pyxb.binding.datatypes.IDREF)
    __RelObjectXmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 753, 2)
    __RelObjectXmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 753, 2)
    
    RelObjectXmlID = property(__RelObjectXmlID.value, __RelObjectXmlID.set, None, None)

    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_relatedObjectIdentifierComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 754, 2)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 754, 2)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        __relatedObjectIdentifierValue.name() : __relatedObjectIdentifierValue,
        __relatedObjectIdentifierType.name() : __relatedObjectIdentifierType,
        __relatedObjectSequence.name() : __relatedObjectSequence
    })
    _AttributeMap.update({
        __RelObjectXmlID.name() : __RelObjectXmlID,
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.relatedObjectIdentifierComplexType = relatedObjectIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'relatedObjectIdentifierComplexType', relatedObjectIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}relationshipComplexType with content type ELEMENT_ONLY
class relationshipComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}relationshipComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'relationshipComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 759, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}relatedEnvironmentPurpose uses Python identifier relatedEnvironmentPurpose
    __relatedEnvironmentPurpose = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relatedEnvironmentPurpose'), 'relatedEnvironmentPurpose', '__httpwww_loc_govpremisv3_relationshipComplexType_httpwww_loc_govpremisv3relatedEnvironmentPurpose', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1033, 1), )

    
    relatedEnvironmentPurpose = property(__relatedEnvironmentPurpose.value, __relatedEnvironmentPurpose.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}relatedEnvironmentCharacteristic uses Python identifier relatedEnvironmentCharacteristic
    __relatedEnvironmentCharacteristic = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relatedEnvironmentCharacteristic'), 'relatedEnvironmentCharacteristic', '__httpwww_loc_govpremisv3_relationshipComplexType_httpwww_loc_govpremisv3relatedEnvironmentCharacteristic', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1034, 4), )

    
    relatedEnvironmentCharacteristic = property(__relatedEnvironmentCharacteristic.value, __relatedEnvironmentCharacteristic.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}relationshipType uses Python identifier relationshipType
    __relationshipType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relationshipType'), 'relationshipType', '__httpwww_loc_govpremisv3_relationshipComplexType_httpwww_loc_govpremisv3relationshipType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1036, 1), )

    
    relationshipType = property(__relationshipType.value, __relationshipType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}relationshipSubType uses Python identifier relationshipSubType
    __relationshipSubType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relationshipSubType'), 'relationshipSubType', '__httpwww_loc_govpremisv3_relationshipComplexType_httpwww_loc_govpremisv3relationshipSubType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1037, 1), )

    
    relationshipSubType = property(__relationshipSubType.value, __relationshipSubType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}relatedEventIdentifier uses Python identifier relatedEventIdentifier
    __relatedEventIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relatedEventIdentifier'), 'relatedEventIdentifier', '__httpwww_loc_govpremisv3_relationshipComplexType_httpwww_loc_govpremisv3relatedEventIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1095, 1), )

    
    relatedEventIdentifier = property(__relatedEventIdentifier.value, __relatedEventIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}relatedObjectIdentifier uses Python identifier relatedObjectIdentifier
    __relatedObjectIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectIdentifier'), 'relatedObjectIdentifier', '__httpwww_loc_govpremisv3_relationshipComplexType_httpwww_loc_govpremisv3relatedObjectIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1096, 1), )

    
    relatedObjectIdentifier = property(__relatedObjectIdentifier.value, __relatedObjectIdentifier.set, None, None)

    _ElementMap.update({
        __relatedEnvironmentPurpose.name() : __relatedEnvironmentPurpose,
        __relatedEnvironmentCharacteristic.name() : __relatedEnvironmentCharacteristic,
        __relationshipType.name() : __relationshipType,
        __relationshipSubType.name() : __relationshipSubType,
        __relatedEventIdentifier.name() : __relatedEventIdentifier,
        __relatedObjectIdentifier.name() : __relatedObjectIdentifier
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.relationshipComplexType = relationshipComplexType
Namespace.addCategoryObject('typeBinding', 'relationshipComplexType', relationshipComplexType)


# Complex type {http://www.loc.gov/premis/v3}rightsGrantedComplexType with content type ELEMENT_ONLY
class rightsGrantedComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}rightsGrantedComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'rightsGrantedComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 781, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}rightsGrantedNote uses Python identifier rightsGrantedNote
    __rightsGrantedNote = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'rightsGrantedNote'), 'rightsGrantedNote', '__httpwww_loc_govpremisv3_rightsGrantedComplexType_httpwww_loc_govpremisv3rightsGrantedNote', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 973, 1), )

    
    rightsGrantedNote = property(__rightsGrantedNote.value, __rightsGrantedNote.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}act uses Python identifier act
    __act = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'act'), 'act', '__httpwww_loc_govpremisv3_rightsGrantedComplexType_httpwww_loc_govpremisv3act', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 988, 1), )

    
    act = property(__act.value, __act.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}restriction uses Python identifier restriction
    __restriction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'restriction'), 'restriction', '__httpwww_loc_govpremisv3_rightsGrantedComplexType_httpwww_loc_govpremisv3restriction', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1038, 1), )

    
    restriction = property(__restriction.value, __restriction.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}termOfGrant uses Python identifier termOfGrant
    __termOfGrant = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'termOfGrant'), 'termOfGrant', '__httpwww_loc_govpremisv3_rightsGrantedComplexType_httpwww_loc_govpremisv3termOfGrant', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1127, 1), )

    
    termOfGrant = property(__termOfGrant.value, __termOfGrant.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}termOfRestriction uses Python identifier termOfRestriction
    __termOfRestriction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'termOfRestriction'), 'termOfRestriction', '__httpwww_loc_govpremisv3_rightsGrantedComplexType_httpwww_loc_govpremisv3termOfRestriction', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1128, 1), )

    
    termOfRestriction = property(__termOfRestriction.value, __termOfRestriction.set, None, None)

    _ElementMap.update({
        __rightsGrantedNote.name() : __rightsGrantedNote,
        __act.name() : __act,
        __restriction.name() : __restriction,
        __termOfGrant.name() : __termOfGrant,
        __termOfRestriction.name() : __termOfRestriction
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.rightsGrantedComplexType = rightsGrantedComplexType
Namespace.addCategoryObject('typeBinding', 'rightsGrantedComplexType', rightsGrantedComplexType)


# Complex type {http://www.loc.gov/premis/v3}rightsStatementComplexType with content type ELEMENT_ONLY
class rightsStatementComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}rightsStatementComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'rightsStatementComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 795, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}rightsBasis uses Python identifier rightsBasis
    __rightsBasis = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'rightsBasis'), 'rightsBasis', '__httpwww_loc_govpremisv3_rightsStatementComplexType_httpwww_loc_govpremisv3rightsBasis', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1039, 1), )

    
    rightsBasis = property(__rightsBasis.value, __rightsBasis.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}copyrightInformation uses Python identifier copyrightInformation
    __copyrightInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'copyrightInformation'), 'copyrightInformation', '__httpwww_loc_govpremisv3_rightsStatementComplexType_httpwww_loc_govpremisv3copyrightInformation', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1068, 1), )

    
    copyrightInformation = property(__copyrightInformation.value, __copyrightInformation.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}licenseInformation uses Python identifier licenseInformation
    __licenseInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'licenseInformation'), 'licenseInformation', '__httpwww_loc_govpremisv3_rightsStatementComplexType_httpwww_loc_govpremisv3licenseInformation', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1083, 1), )

    
    licenseInformation = property(__licenseInformation.value, __licenseInformation.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingAgentIdentifier uses Python identifier linkingAgentIdentifier
    __linkingAgentIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifier'), 'linkingAgentIdentifier', '__httpwww_loc_govpremisv3_rightsStatementComplexType_httpwww_loc_govpremisv3linkingAgentIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1084, 1), )

    
    linkingAgentIdentifier = property(__linkingAgentIdentifier.value, __linkingAgentIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingObjectIdentifier uses Python identifier linkingObjectIdentifier
    __linkingObjectIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifier'), 'linkingObjectIdentifier', '__httpwww_loc_govpremisv3_rightsStatementComplexType_httpwww_loc_govpremisv3linkingObjectIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1087, 1), )

    
    linkingObjectIdentifier = property(__linkingObjectIdentifier.value, __linkingObjectIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}otherRightsInformation uses Python identifier otherRightsInformation
    __otherRightsInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'otherRightsInformation'), 'otherRightsInformation', '__httpwww_loc_govpremisv3_rightsStatementComplexType_httpwww_loc_govpremisv3otherRightsInformation', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1093, 1), )

    
    otherRightsInformation = property(__otherRightsInformation.value, __otherRightsInformation.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}rightsGranted uses Python identifier rightsGranted
    __rightsGranted = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'rightsGranted'), 'rightsGranted', '__httpwww_loc_govpremisv3_rightsStatementComplexType_httpwww_loc_govpremisv3rightsGranted', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1098, 1), )

    
    rightsGranted = property(__rightsGranted.value, __rightsGranted.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}rightsStatementIdentifier uses Python identifier rightsStatementIdentifier
    __rightsStatementIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'rightsStatementIdentifier'), 'rightsStatementIdentifier', '__httpwww_loc_govpremisv3_rightsStatementComplexType_httpwww_loc_govpremisv3rightsStatementIdentifier', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1100, 1), )

    
    rightsStatementIdentifier = property(__rightsStatementIdentifier.value, __rightsStatementIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}statuteInformation uses Python identifier statuteInformation
    __statuteInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'statuteInformation'), 'statuteInformation', '__httpwww_loc_govpremisv3_rightsStatementComplexType_httpwww_loc_govpremisv3statuteInformation', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1105, 1), )

    
    statuteInformation = property(__statuteInformation.value, __statuteInformation.set, None, None)

    _ElementMap.update({
        __rightsBasis.name() : __rightsBasis,
        __copyrightInformation.name() : __copyrightInformation,
        __licenseInformation.name() : __licenseInformation,
        __linkingAgentIdentifier.name() : __linkingAgentIdentifier,
        __linkingObjectIdentifier.name() : __linkingObjectIdentifier,
        __otherRightsInformation.name() : __otherRightsInformation,
        __rightsGranted.name() : __rightsGranted,
        __rightsStatementIdentifier.name() : __rightsStatementIdentifier,
        __statuteInformation.name() : __statuteInformation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.rightsStatementComplexType = rightsStatementComplexType
Namespace.addCategoryObject('typeBinding', 'rightsStatementComplexType', rightsStatementComplexType)


# Complex type {http://www.loc.gov/premis/v3}rightsStatementIdentifierComplexType with content type ELEMENT_ONLY
class rightsStatementIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}rightsStatementIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'rightsStatementIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 812, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}rightsStatementIdentifierValue uses Python identifier rightsStatementIdentifierValue
    __rightsStatementIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'rightsStatementIdentifierValue'), 'rightsStatementIdentifierValue', '__httpwww_loc_govpremisv3_rightsStatementIdentifierComplexType_httpwww_loc_govpremisv3rightsStatementIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 974, 1), )

    
    rightsStatementIdentifierValue = property(__rightsStatementIdentifierValue.value, __rightsStatementIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}rightsStatementIdentifierType uses Python identifier rightsStatementIdentifierType
    __rightsStatementIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'rightsStatementIdentifierType'), 'rightsStatementIdentifierType', '__httpwww_loc_govpremisv3_rightsStatementIdentifierComplexType_httpwww_loc_govpremisv3rightsStatementIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1040, 1), )

    
    rightsStatementIdentifierType = property(__rightsStatementIdentifierType.value, __rightsStatementIdentifierType.set, None, None)

    
    # Attribute simpleLink uses Python identifier simpleLink
    __simpleLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'simpleLink'), 'simpleLink', '__httpwww_loc_govpremisv3_rightsStatementIdentifierComplexType_simpleLink', pyxb.binding.datatypes.anyURI)
    __simpleLink._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 817, 2)
    __simpleLink._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 817, 2)
    
    simpleLink = property(__simpleLink.value, __simpleLink.set, None, None)

    _ElementMap.update({
        __rightsStatementIdentifierValue.name() : __rightsStatementIdentifierValue,
        __rightsStatementIdentifierType.name() : __rightsStatementIdentifierType
    })
    _AttributeMap.update({
        __simpleLink.name() : __simpleLink
    })
_module_typeBindings.rightsStatementIdentifierComplexType = rightsStatementIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'rightsStatementIdentifierComplexType', rightsStatementIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}signatureComplexType with content type ELEMENT_ONLY
class signatureComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}signatureComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'signatureComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 823, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}signatureProperties uses Python identifier signatureProperties
    __signatureProperties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'signatureProperties'), 'signatureProperties', '__httpwww_loc_govpremisv3_signatureComplexType_httpwww_loc_govpremisv3signatureProperties', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 975, 1), )

    
    signatureProperties = property(__signatureProperties.value, __signatureProperties.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}signatureValue uses Python identifier signatureValue
    __signatureValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'signatureValue'), 'signatureValue', '__httpwww_loc_govpremisv3_signatureComplexType_httpwww_loc_govpremisv3signatureValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 976, 1), )

    
    signatureValue = property(__signatureValue.value, __signatureValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}signatureEncoding uses Python identifier signatureEncoding
    __signatureEncoding = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'signatureEncoding'), 'signatureEncoding', '__httpwww_loc_govpremisv3_signatureComplexType_httpwww_loc_govpremisv3signatureEncoding', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1041, 1), )

    
    signatureEncoding = property(__signatureEncoding.value, __signatureEncoding.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}signatureMethod uses Python identifier signatureMethod
    __signatureMethod = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'signatureMethod'), 'signatureMethod', '__httpwww_loc_govpremisv3_signatureComplexType_httpwww_loc_govpremisv3signatureMethod', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1042, 1), )

    
    signatureMethod = property(__signatureMethod.value, __signatureMethod.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}signatureValidationRules uses Python identifier signatureValidationRules
    __signatureValidationRules = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'signatureValidationRules'), 'signatureValidationRules', '__httpwww_loc_govpremisv3_signatureComplexType_httpwww_loc_govpremisv3signatureValidationRules', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1043, 1), )

    
    signatureValidationRules = property(__signatureValidationRules.value, __signatureValidationRules.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}signer uses Python identifier signer
    __signer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'signer'), 'signer', '__httpwww_loc_govpremisv3_signatureComplexType_httpwww_loc_govpremisv3signer', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1044, 1), )

    
    signer = property(__signer.value, __signer.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}keyInformation uses Python identifier keyInformation
    __keyInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'keyInformation'), 'keyInformation', '__httpwww_loc_govpremisv3_signatureComplexType_httpwww_loc_govpremisv3keyInformation', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1137, 1), )

    
    keyInformation = property(__keyInformation.value, __keyInformation.set, None, None)

    _ElementMap.update({
        __signatureProperties.name() : __signatureProperties,
        __signatureValue.name() : __signatureValue,
        __signatureEncoding.name() : __signatureEncoding,
        __signatureMethod.name() : __signatureMethod,
        __signatureValidationRules.name() : __signatureValidationRules,
        __signer.name() : __signer,
        __keyInformation.name() : __keyInformation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.signatureComplexType = signatureComplexType
Namespace.addCategoryObject('typeBinding', 'signatureComplexType', signatureComplexType)


# Complex type {http://www.loc.gov/premis/v3}signatureInformationComplexType with content type ELEMENT_ONLY
class signatureInformationComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}signatureInformationComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'signatureInformationComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 840, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}signature uses Python identifier signature
    __signature = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'signature'), 'signature', '__httpwww_loc_govpremisv3_signatureInformationComplexType_httpwww_loc_govpremisv3signature', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1101, 1), )

    
    signature = property(__signature.value, __signature.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}signatureInformationExtension uses Python identifier signatureInformationExtension
    __signatureInformationExtension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'signatureInformationExtension'), 'signatureInformationExtension', '__httpwww_loc_govpremisv3_signatureInformationComplexType_httpwww_loc_govpremisv3signatureInformationExtension', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1140, 1), )

    
    signatureInformationExtension = property(__signatureInformationExtension.value, __signatureInformationExtension.set, None, None)

    _ElementMap.update({
        __signature.name() : __signature,
        __signatureInformationExtension.name() : __signatureInformationExtension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.signatureInformationComplexType = signatureInformationComplexType
Namespace.addCategoryObject('typeBinding', 'signatureInformationComplexType', signatureInformationComplexType)


# Complex type {http://www.loc.gov/premis/v3}significantPropertiesComplexType with content type ELEMENT_ONLY
class significantPropertiesComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}significantPropertiesComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 856, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}significantPropertiesValue uses Python identifier significantPropertiesValue
    __significantPropertiesValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesValue'), 'significantPropertiesValue', '__httpwww_loc_govpremisv3_significantPropertiesComplexType_httpwww_loc_govpremisv3significantPropertiesValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 977, 1), )

    
    significantPropertiesValue = property(__significantPropertiesValue.value, __significantPropertiesValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}significantPropertiesType uses Python identifier significantPropertiesType
    __significantPropertiesType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesType'), 'significantPropertiesType', '__httpwww_loc_govpremisv3_significantPropertiesComplexType_httpwww_loc_govpremisv3significantPropertiesType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1045, 1), )

    
    significantPropertiesType = property(__significantPropertiesType.value, __significantPropertiesType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}significantPropertiesExtension uses Python identifier significantPropertiesExtension
    __significantPropertiesExtension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesExtension'), 'significantPropertiesExtension', '__httpwww_loc_govpremisv3_significantPropertiesComplexType_httpwww_loc_govpremisv3significantPropertiesExtension', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1141, 1), )

    
    significantPropertiesExtension = property(__significantPropertiesExtension.value, __significantPropertiesExtension.set, None, None)

    _ElementMap.update({
        __significantPropertiesValue.name() : __significantPropertiesValue,
        __significantPropertiesType.name() : __significantPropertiesType,
        __significantPropertiesExtension.name() : __significantPropertiesExtension
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.significantPropertiesComplexType = significantPropertiesComplexType
Namespace.addCategoryObject('typeBinding', 'significantPropertiesComplexType', significantPropertiesComplexType)


# Complex type {http://www.loc.gov/premis/v3}startAndEndDateComplexType with content type ELEMENT_ONLY
class startAndEndDateComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}startAndEndDateComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'startAndEndDateComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 877, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}endDate uses Python identifier endDate
    __endDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'endDate'), 'endDate', '__httpwww_loc_govpremisv3_startAndEndDateComplexType_httpwww_loc_govpremisv3endDate', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1117, 1), )

    
    endDate = property(__endDate.value, __endDate.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}startDate uses Python identifier startDate
    __startDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'startDate'), 'startDate', '__httpwww_loc_govpremisv3_startAndEndDateComplexType_httpwww_loc_govpremisv3startDate', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1123, 1), )

    
    startDate = property(__startDate.value, __startDate.set, None, None)

    _ElementMap.update({
        __endDate.name() : __endDate,
        __startDate.name() : __startDate
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.startAndEndDateComplexType = startAndEndDateComplexType
Namespace.addCategoryObject('typeBinding', 'startAndEndDateComplexType', startAndEndDateComplexType)


# Complex type {http://www.loc.gov/premis/v3}statuteDocumentationIdentifierComplexType with content type ELEMENT_ONLY
class statuteDocumentationIdentifierComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}statuteDocumentationIdentifierComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationIdentifierComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 887, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}statuteDocumentationIdentifierValue uses Python identifier statuteDocumentationIdentifierValue
    __statuteDocumentationIdentifierValue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationIdentifierValue'), 'statuteDocumentationIdentifierValue', '__httpwww_loc_govpremisv3_statuteDocumentationIdentifierComplexType_httpwww_loc_govpremisv3statuteDocumentationIdentifierValue', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 978, 1), )

    
    statuteDocumentationIdentifierValue = property(__statuteDocumentationIdentifierValue.value, __statuteDocumentationIdentifierValue.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}statuteDocumentationIdentifierType uses Python identifier statuteDocumentationIdentifierType
    __statuteDocumentationIdentifierType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationIdentifierType'), 'statuteDocumentationIdentifierType', '__httpwww_loc_govpremisv3_statuteDocumentationIdentifierComplexType_httpwww_loc_govpremisv3statuteDocumentationIdentifierType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1048, 1), )

    
    statuteDocumentationIdentifierType = property(__statuteDocumentationIdentifierType.value, __statuteDocumentationIdentifierType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}statuteDocumentationRole uses Python identifier statuteDocumentationRole
    __statuteDocumentationRole = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationRole'), 'statuteDocumentationRole', '__httpwww_loc_govpremisv3_statuteDocumentationIdentifierComplexType_httpwww_loc_govpremisv3statuteDocumentationRole', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1049, 1), )

    
    statuteDocumentationRole = property(__statuteDocumentationRole.value, __statuteDocumentationRole.set, None, None)

    _ElementMap.update({
        __statuteDocumentationIdentifierValue.name() : __statuteDocumentationIdentifierValue,
        __statuteDocumentationIdentifierType.name() : __statuteDocumentationIdentifierType,
        __statuteDocumentationRole.name() : __statuteDocumentationRole
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.statuteDocumentationIdentifierComplexType = statuteDocumentationIdentifierComplexType
Namespace.addCategoryObject('typeBinding', 'statuteDocumentationIdentifierComplexType', statuteDocumentationIdentifierComplexType)


# Complex type {http://www.loc.gov/premis/v3}statuteInformationComplexType with content type ELEMENT_ONLY
class statuteInformationComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}statuteInformationComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'statuteInformationComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 898, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}statuteNote uses Python identifier statuteNote
    __statuteNote = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'statuteNote'), 'statuteNote', '__httpwww_loc_govpremisv3_statuteInformationComplexType_httpwww_loc_govpremisv3statuteNote', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 979, 1), )

    
    statuteNote = property(__statuteNote.value, __statuteNote.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}statuteCitation uses Python identifier statuteCitation
    __statuteCitation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'statuteCitation'), 'statuteCitation', '__httpwww_loc_govpremisv3_statuteInformationComplexType_httpwww_loc_govpremisv3statuteCitation', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1047, 1), )

    
    statuteCitation = property(__statuteCitation.value, __statuteCitation.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}statuteJurisdiction uses Python identifier statuteJurisdiction
    __statuteJurisdiction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'statuteJurisdiction'), 'statuteJurisdiction', '__httpwww_loc_govpremisv3_statuteInformationComplexType_httpwww_loc_govpremisv3statuteJurisdiction', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1058, 1), )

    
    statuteJurisdiction = property(__statuteJurisdiction.value, __statuteJurisdiction.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}statuteDocumentationIdentifier uses Python identifier statuteDocumentationIdentifier
    __statuteDocumentationIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationIdentifier'), 'statuteDocumentationIdentifier', '__httpwww_loc_govpremisv3_statuteInformationComplexType_httpwww_loc_govpremisv3statuteDocumentationIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1104, 1), )

    
    statuteDocumentationIdentifier = property(__statuteDocumentationIdentifier.value, __statuteDocumentationIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}statuteApplicableDates uses Python identifier statuteApplicableDates
    __statuteApplicableDates = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'statuteApplicableDates'), 'statuteApplicableDates', '__httpwww_loc_govpremisv3_statuteInformationComplexType_httpwww_loc_govpremisv3statuteApplicableDates', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1125, 1), )

    
    statuteApplicableDates = property(__statuteApplicableDates.value, __statuteApplicableDates.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}statuteInformationDeterminationDate uses Python identifier statuteInformationDeterminationDate
    __statuteInformationDeterminationDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'statuteInformationDeterminationDate'), 'statuteInformationDeterminationDate', '__httpwww_loc_govpremisv3_statuteInformationComplexType_httpwww_loc_govpremisv3statuteInformationDeterminationDate', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1126, 1), )

    
    statuteInformationDeterminationDate = property(__statuteInformationDeterminationDate.value, __statuteInformationDeterminationDate.set, None, None)

    _ElementMap.update({
        __statuteNote.name() : __statuteNote,
        __statuteCitation.name() : __statuteCitation,
        __statuteJurisdiction.name() : __statuteJurisdiction,
        __statuteDocumentationIdentifier.name() : __statuteDocumentationIdentifier,
        __statuteApplicableDates.name() : __statuteApplicableDates,
        __statuteInformationDeterminationDate.name() : __statuteInformationDeterminationDate
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.statuteInformationComplexType = statuteInformationComplexType
Namespace.addCategoryObject('typeBinding', 'statuteInformationComplexType', statuteInformationComplexType)


# Complex type {http://www.loc.gov/premis/v3}storageComplexType with content type ELEMENT_ONLY
class storageComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}storageComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'storageComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 913, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}storageMedium uses Python identifier storageMedium
    __storageMedium = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'storageMedium'), 'storageMedium', '__httpwww_loc_govpremisv3_storageComplexType_httpwww_loc_govpremisv3storageMedium', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1046, 1), )

    
    storageMedium = property(__storageMedium.value, __storageMedium.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}contentLocation uses Python identifier contentLocation
    __contentLocation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'contentLocation'), 'contentLocation', '__httpwww_loc_govpremisv3_storageComplexType_httpwww_loc_govpremisv3contentLocation', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1065, 1), )

    
    contentLocation = property(__contentLocation.value, __contentLocation.set, None, None)

    _ElementMap.update({
        __storageMedium.name() : __storageMedium,
        __contentLocation.name() : __contentLocation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.storageComplexType = storageComplexType
Namespace.addCategoryObject('typeBinding', 'storageComplexType', storageComplexType)


# Complex type {http://www.loc.gov/premis/v3}extensionComplexType with content type ELEMENT_ONLY
class extensionComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}extensionComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'extensionComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1174, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.extensionComplexType = extensionComplexType
Namespace.addCategoryObject('typeBinding', 'extensionComplexType', extensionComplexType)


# Complex type {http://www.loc.gov/premis/v3}stringPlusAuthority with content type SIMPLE
class stringPlusAuthority (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}stringPlusAuthority with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'stringPlusAuthority')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1214, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute authority uses Python identifier authority
    __authority = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'authority'), 'authority', '__httpwww_loc_govpremisv3_stringPlusAuthority_authority', pyxb.binding.datatypes.string)
    __authority._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1207, 2)
    __authority._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1207, 2)
    
    authority = property(__authority.value, __authority.set, None, None)

    
    # Attribute authorityURI uses Python identifier authorityURI
    __authorityURI = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'authorityURI'), 'authorityURI', '__httpwww_loc_govpremisv3_stringPlusAuthority_authorityURI', pyxb.binding.datatypes.anyURI)
    __authorityURI._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1208, 2)
    __authorityURI._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1208, 2)
    
    authorityURI = property(__authorityURI.value, __authorityURI.set, None, None)

    
    # Attribute valueURI uses Python identifier valueURI
    __valueURI = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'valueURI'), 'valueURI', '__httpwww_loc_govpremisv3_stringPlusAuthority_valueURI', pyxb.binding.datatypes.anyURI)
    __valueURI._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1209, 2)
    __valueURI._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1209, 2)
    
    valueURI = property(__valueURI.value, __valueURI.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __authority.name() : __authority,
        __authorityURI.name() : __authorityURI,
        __valueURI.name() : __valueURI
    })
_module_typeBindings.stringPlusAuthority = stringPlusAuthority
Namespace.addCategoryObject('typeBinding', 'stringPlusAuthority', stringPlusAuthority)


# Complex type {http://www.loc.gov/premis/v3}premisComplexType with content type ELEMENT_ONLY
class premisComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}premisComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'premisComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 82, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}object uses Python identifier object
    __object = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'object'), 'object', '__httpwww_loc_govpremisv3_premisComplexType_httpwww_loc_govpremisv3object', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 67, 1), )

    
    object = property(__object.value, __object.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}event uses Python identifier event
    __event = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'event'), 'event', '__httpwww_loc_govpremisv3_premisComplexType_httpwww_loc_govpremisv3event', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 68, 1), )

    
    event = property(__event.value, __event.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}agent uses Python identifier agent
    __agent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'agent'), 'agent', '__httpwww_loc_govpremisv3_premisComplexType_httpwww_loc_govpremisv3agent', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 69, 1), )

    
    agent = property(__agent.value, __agent.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}rights uses Python identifier rights
    __rights = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'rights'), 'rights', '__httpwww_loc_govpremisv3_premisComplexType_httpwww_loc_govpremisv3rights', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 70, 1), )

    
    rights = property(__rights.value, __rights.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_loc_govpremisv3_premisComplexType_version', _module_typeBindings.version3, required=True)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 89, 2)
    __version._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 89, 2)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __object.name() : __object,
        __event.name() : __event,
        __agent.name() : __agent,
        __rights.name() : __rights
    })
    _AttributeMap.update({
        __version.name() : __version
    })
_module_typeBindings.premisComplexType = premisComplexType
Namespace.addCategoryObject('typeBinding', 'premisComplexType', premisComplexType)


# Complex type {http://www.loc.gov/premis/v3}file with content type ELEMENT_ONLY
class file (objectComplexType):
    """Complex type {http://www.loc.gov/premis/v3}file with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'file')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 114, 1)
    _ElementMap = objectComplexType._ElementMap.copy()
    _AttributeMap = objectComplexType._AttributeMap.copy()
    # Base type is objectComplexType
    
    # Element {http://www.loc.gov/premis/v3}linkingEventIdentifier uses Python identifier linkingEventIdentifier
    __linkingEventIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier'), 'linkingEventIdentifier', '__httpwww_loc_govpremisv3_file_httpwww_loc_govpremisv3linkingEventIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1086, 4), )

    
    linkingEventIdentifier = property(__linkingEventIdentifier.value, __linkingEventIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingRightsStatementIdentifier uses Python identifier linkingRightsStatementIdentifier
    __linkingRightsStatementIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier'), 'linkingRightsStatementIdentifier', '__httpwww_loc_govpremisv3_file_httpwww_loc_govpremisv3linkingRightsStatementIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1088, 1), )

    
    linkingRightsStatementIdentifier = property(__linkingRightsStatementIdentifier.value, __linkingRightsStatementIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}objectCharacteristics uses Python identifier objectCharacteristics
    __objectCharacteristics = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'objectCharacteristics'), 'objectCharacteristics', '__httpwww_loc_govpremisv3_file_httpwww_loc_govpremisv3objectCharacteristics', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1089, 1), )

    
    objectCharacteristics = property(__objectCharacteristics.value, __objectCharacteristics.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}objectIdentifier uses Python identifier objectIdentifier
    __objectIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifier'), 'objectIdentifier', '__httpwww_loc_govpremisv3_file_httpwww_loc_govpremisv3objectIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1090, 1), )

    
    objectIdentifier = property(__objectIdentifier.value, __objectIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}originalName uses Python identifier originalName
    __originalName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'originalName'), 'originalName', '__httpwww_loc_govpremisv3_file_httpwww_loc_govpremisv3originalName', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1091, 1), )

    
    originalName = property(__originalName.value, __originalName.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}preservationLevel uses Python identifier preservationLevel
    __preservationLevel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'preservationLevel'), 'preservationLevel', '__httpwww_loc_govpremisv3_file_httpwww_loc_govpremisv3preservationLevel', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1094, 1), )

    
    preservationLevel = property(__preservationLevel.value, __preservationLevel.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}relationship uses Python identifier relationship
    __relationship = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relationship'), 'relationship', '__httpwww_loc_govpremisv3_file_httpwww_loc_govpremisv3relationship', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1097, 4), )

    
    relationship = property(__relationship.value, __relationship.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}signatureInformation uses Python identifier signatureInformation
    __signatureInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'signatureInformation'), 'signatureInformation', '__httpwww_loc_govpremisv3_file_httpwww_loc_govpremisv3signatureInformation', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1102, 1), )

    
    signatureInformation = property(__signatureInformation.value, __signatureInformation.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}significantProperties uses Python identifier significantProperties
    __significantProperties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'significantProperties'), 'significantProperties', '__httpwww_loc_govpremisv3_file_httpwww_loc_govpremisv3significantProperties', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1103, 1), )

    
    significantProperties = property(__significantProperties.value, __significantProperties.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}storage uses Python identifier storage
    __storage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'storage'), 'storage', '__httpwww_loc_govpremisv3_file_httpwww_loc_govpremisv3storage', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1106, 1), )

    
    storage = property(__storage.value, __storage.set, None, None)

    
    # Attribute xmlID uses Python identifier xmlID
    __xmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'xmlID'), 'xmlID', '__httpwww_loc_govpremisv3_file_xmlID', pyxb.binding.datatypes.ID)
    __xmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 135, 4)
    __xmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 135, 4)
    
    xmlID = property(__xmlID.value, __xmlID.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_loc_govpremisv3_file_version', _module_typeBindings.version3)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 136, 4)
    __version._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 136, 4)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __linkingEventIdentifier.name() : __linkingEventIdentifier,
        __linkingRightsStatementIdentifier.name() : __linkingRightsStatementIdentifier,
        __objectCharacteristics.name() : __objectCharacteristics,
        __objectIdentifier.name() : __objectIdentifier,
        __originalName.name() : __originalName,
        __preservationLevel.name() : __preservationLevel,
        __relationship.name() : __relationship,
        __signatureInformation.name() : __signatureInformation,
        __significantProperties.name() : __significantProperties,
        __storage.name() : __storage
    })
    _AttributeMap.update({
        __xmlID.name() : __xmlID,
        __version.name() : __version
    })
_module_typeBindings.file = file
Namespace.addCategoryObject('typeBinding', 'file', file)


# Complex type {http://www.loc.gov/premis/v3}representation with content type ELEMENT_ONLY
class representation (objectComplexType):
    """Complex type {http://www.loc.gov/premis/v3}representation with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'representation')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 143, 1)
    _ElementMap = objectComplexType._ElementMap.copy()
    _AttributeMap = objectComplexType._AttributeMap.copy()
    # Base type is objectComplexType
    
    # Element {http://www.loc.gov/premis/v3}linkingEventIdentifier uses Python identifier linkingEventIdentifier
    __linkingEventIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier'), 'linkingEventIdentifier', '__httpwww_loc_govpremisv3_representation_httpwww_loc_govpremisv3linkingEventIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1086, 4), )

    
    linkingEventIdentifier = property(__linkingEventIdentifier.value, __linkingEventIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingRightsStatementIdentifier uses Python identifier linkingRightsStatementIdentifier
    __linkingRightsStatementIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier'), 'linkingRightsStatementIdentifier', '__httpwww_loc_govpremisv3_representation_httpwww_loc_govpremisv3linkingRightsStatementIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1088, 1), )

    
    linkingRightsStatementIdentifier = property(__linkingRightsStatementIdentifier.value, __linkingRightsStatementIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}objectIdentifier uses Python identifier objectIdentifier
    __objectIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifier'), 'objectIdentifier', '__httpwww_loc_govpremisv3_representation_httpwww_loc_govpremisv3objectIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1090, 1), )

    
    objectIdentifier = property(__objectIdentifier.value, __objectIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}originalName uses Python identifier originalName
    __originalName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'originalName'), 'originalName', '__httpwww_loc_govpremisv3_representation_httpwww_loc_govpremisv3originalName', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1091, 1), )

    
    originalName = property(__originalName.value, __originalName.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}preservationLevel uses Python identifier preservationLevel
    __preservationLevel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'preservationLevel'), 'preservationLevel', '__httpwww_loc_govpremisv3_representation_httpwww_loc_govpremisv3preservationLevel', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1094, 1), )

    
    preservationLevel = property(__preservationLevel.value, __preservationLevel.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}relationship uses Python identifier relationship
    __relationship = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relationship'), 'relationship', '__httpwww_loc_govpremisv3_representation_httpwww_loc_govpremisv3relationship', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1097, 4), )

    
    relationship = property(__relationship.value, __relationship.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}significantProperties uses Python identifier significantProperties
    __significantProperties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'significantProperties'), 'significantProperties', '__httpwww_loc_govpremisv3_representation_httpwww_loc_govpremisv3significantProperties', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1103, 1), )

    
    significantProperties = property(__significantProperties.value, __significantProperties.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}storage uses Python identifier storage
    __storage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'storage'), 'storage', '__httpwww_loc_govpremisv3_representation_httpwww_loc_govpremisv3storage', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1106, 1), )

    
    storage = property(__storage.value, __storage.set, None, None)

    
    # Attribute xmlID uses Python identifier xmlID
    __xmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'xmlID'), 'xmlID', '__httpwww_loc_govpremisv3_representation_xmlID', pyxb.binding.datatypes.ID)
    __xmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 162, 4)
    __xmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 162, 4)
    
    xmlID = property(__xmlID.value, __xmlID.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_loc_govpremisv3_representation_version', _module_typeBindings.version3)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 163, 4)
    __version._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 163, 4)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __linkingEventIdentifier.name() : __linkingEventIdentifier,
        __linkingRightsStatementIdentifier.name() : __linkingRightsStatementIdentifier,
        __objectIdentifier.name() : __objectIdentifier,
        __originalName.name() : __originalName,
        __preservationLevel.name() : __preservationLevel,
        __relationship.name() : __relationship,
        __significantProperties.name() : __significantProperties,
        __storage.name() : __storage
    })
    _AttributeMap.update({
        __xmlID.name() : __xmlID,
        __version.name() : __version
    })
_module_typeBindings.representation = representation
Namespace.addCategoryObject('typeBinding', 'representation', representation)


# Complex type {http://www.loc.gov/premis/v3}bitstream with content type ELEMENT_ONLY
class bitstream (objectComplexType):
    """Complex type {http://www.loc.gov/premis/v3}bitstream with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'bitstream')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 170, 1)
    _ElementMap = objectComplexType._ElementMap.copy()
    _AttributeMap = objectComplexType._AttributeMap.copy()
    # Base type is objectComplexType
    
    # Element {http://www.loc.gov/premis/v3}linkingEventIdentifier uses Python identifier linkingEventIdentifier
    __linkingEventIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier'), 'linkingEventIdentifier', '__httpwww_loc_govpremisv3_bitstream_httpwww_loc_govpremisv3linkingEventIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1086, 4), )

    
    linkingEventIdentifier = property(__linkingEventIdentifier.value, __linkingEventIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingRightsStatementIdentifier uses Python identifier linkingRightsStatementIdentifier
    __linkingRightsStatementIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier'), 'linkingRightsStatementIdentifier', '__httpwww_loc_govpremisv3_bitstream_httpwww_loc_govpremisv3linkingRightsStatementIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1088, 1), )

    
    linkingRightsStatementIdentifier = property(__linkingRightsStatementIdentifier.value, __linkingRightsStatementIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}objectCharacteristics uses Python identifier objectCharacteristics
    __objectCharacteristics = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'objectCharacteristics'), 'objectCharacteristics', '__httpwww_loc_govpremisv3_bitstream_httpwww_loc_govpremisv3objectCharacteristics', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1089, 1), )

    
    objectCharacteristics = property(__objectCharacteristics.value, __objectCharacteristics.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}objectIdentifier uses Python identifier objectIdentifier
    __objectIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifier'), 'objectIdentifier', '__httpwww_loc_govpremisv3_bitstream_httpwww_loc_govpremisv3objectIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1090, 1), )

    
    objectIdentifier = property(__objectIdentifier.value, __objectIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}relationship uses Python identifier relationship
    __relationship = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relationship'), 'relationship', '__httpwww_loc_govpremisv3_bitstream_httpwww_loc_govpremisv3relationship', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1097, 4), )

    
    relationship = property(__relationship.value, __relationship.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}signatureInformation uses Python identifier signatureInformation
    __signatureInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'signatureInformation'), 'signatureInformation', '__httpwww_loc_govpremisv3_bitstream_httpwww_loc_govpremisv3signatureInformation', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1102, 1), )

    
    signatureInformation = property(__signatureInformation.value, __signatureInformation.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}significantProperties uses Python identifier significantProperties
    __significantProperties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'significantProperties'), 'significantProperties', '__httpwww_loc_govpremisv3_bitstream_httpwww_loc_govpremisv3significantProperties', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1103, 1), )

    
    significantProperties = property(__significantProperties.value, __significantProperties.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}storage uses Python identifier storage
    __storage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'storage'), 'storage', '__httpwww_loc_govpremisv3_bitstream_httpwww_loc_govpremisv3storage', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1106, 1), )

    
    storage = property(__storage.value, __storage.set, None, None)

    
    # Attribute xmlID uses Python identifier xmlID
    __xmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'xmlID'), 'xmlID', '__httpwww_loc_govpremisv3_bitstream_xmlID', pyxb.binding.datatypes.ID)
    __xmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 185, 4)
    __xmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 185, 4)
    
    xmlID = property(__xmlID.value, __xmlID.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_loc_govpremisv3_bitstream_version', _module_typeBindings.version3)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 186, 4)
    __version._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 186, 4)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __linkingEventIdentifier.name() : __linkingEventIdentifier,
        __linkingRightsStatementIdentifier.name() : __linkingRightsStatementIdentifier,
        __objectCharacteristics.name() : __objectCharacteristics,
        __objectIdentifier.name() : __objectIdentifier,
        __relationship.name() : __relationship,
        __signatureInformation.name() : __signatureInformation,
        __significantProperties.name() : __significantProperties,
        __storage.name() : __storage
    })
    _AttributeMap.update({
        __xmlID.name() : __xmlID,
        __version.name() : __version
    })
_module_typeBindings.bitstream = bitstream
Namespace.addCategoryObject('typeBinding', 'bitstream', bitstream)


# Complex type {http://www.loc.gov/premis/v3}intellectualEntity with content type ELEMENT_ONLY
class intellectualEntity (objectComplexType):
    """Complex type {http://www.loc.gov/premis/v3}intellectualEntity with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'intellectualEntity')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 196, 4)
    _ElementMap = objectComplexType._ElementMap.copy()
    _AttributeMap = objectComplexType._AttributeMap.copy()
    # Base type is objectComplexType
    
    # Element {http://www.loc.gov/premis/v3}environmentFunction uses Python identifier environmentFunction
    __environmentFunction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentFunction'), 'environmentFunction', '__httpwww_loc_govpremisv3_intellectualEntity_httpwww_loc_govpremisv3environmentFunction', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1070, 4), )

    
    environmentFunction = property(__environmentFunction.value, __environmentFunction.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}environmentDesignation uses Python identifier environmentDesignation
    __environmentDesignation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentDesignation'), 'environmentDesignation', '__httpwww_loc_govpremisv3_intellectualEntity_httpwww_loc_govpremisv3environmentDesignation', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1071, 4), )

    
    environmentDesignation = property(__environmentDesignation.value, __environmentDesignation.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}environmentRegistry uses Python identifier environmentRegistry
    __environmentRegistry = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistry'), 'environmentRegistry', '__httpwww_loc_govpremisv3_intellectualEntity_httpwww_loc_govpremisv3environmentRegistry', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1072, 4), )

    
    environmentRegistry = property(__environmentRegistry.value, __environmentRegistry.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingEventIdentifier uses Python identifier linkingEventIdentifier
    __linkingEventIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier'), 'linkingEventIdentifier', '__httpwww_loc_govpremisv3_intellectualEntity_httpwww_loc_govpremisv3linkingEventIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1086, 4), )

    
    linkingEventIdentifier = property(__linkingEventIdentifier.value, __linkingEventIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingRightsStatementIdentifier uses Python identifier linkingRightsStatementIdentifier
    __linkingRightsStatementIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier'), 'linkingRightsStatementIdentifier', '__httpwww_loc_govpremisv3_intellectualEntity_httpwww_loc_govpremisv3linkingRightsStatementIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1088, 1), )

    
    linkingRightsStatementIdentifier = property(__linkingRightsStatementIdentifier.value, __linkingRightsStatementIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}objectIdentifier uses Python identifier objectIdentifier
    __objectIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifier'), 'objectIdentifier', '__httpwww_loc_govpremisv3_intellectualEntity_httpwww_loc_govpremisv3objectIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1090, 1), )

    
    objectIdentifier = property(__objectIdentifier.value, __objectIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}originalName uses Python identifier originalName
    __originalName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'originalName'), 'originalName', '__httpwww_loc_govpremisv3_intellectualEntity_httpwww_loc_govpremisv3originalName', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1091, 1), )

    
    originalName = property(__originalName.value, __originalName.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}preservationLevel uses Python identifier preservationLevel
    __preservationLevel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'preservationLevel'), 'preservationLevel', '__httpwww_loc_govpremisv3_intellectualEntity_httpwww_loc_govpremisv3preservationLevel', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1094, 1), )

    
    preservationLevel = property(__preservationLevel.value, __preservationLevel.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}relationship uses Python identifier relationship
    __relationship = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'relationship'), 'relationship', '__httpwww_loc_govpremisv3_intellectualEntity_httpwww_loc_govpremisv3relationship', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1097, 4), )

    
    relationship = property(__relationship.value, __relationship.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}significantProperties uses Python identifier significantProperties
    __significantProperties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'significantProperties'), 'significantProperties', '__httpwww_loc_govpremisv3_intellectualEntity_httpwww_loc_govpremisv3significantProperties', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1103, 1), )

    
    significantProperties = property(__significantProperties.value, __significantProperties.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}environmentExtension uses Python identifier environmentExtension
    __environmentExtension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'environmentExtension'), 'environmentExtension', '__httpwww_loc_govpremisv3_intellectualEntity_httpwww_loc_govpremisv3environmentExtension', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1134, 1), )

    
    environmentExtension = property(__environmentExtension.value, __environmentExtension.set, None, None)

    
    # Attribute xmlID uses Python identifier xmlID
    __xmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'xmlID'), 'xmlID', '__httpwww_loc_govpremisv3_intellectualEntity_xmlID', pyxb.binding.datatypes.ID)
    __xmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 216, 16)
    __xmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 216, 16)
    
    xmlID = property(__xmlID.value, __xmlID.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_loc_govpremisv3_intellectualEntity_version', _module_typeBindings.version3)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 217, 16)
    __version._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 217, 16)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __environmentFunction.name() : __environmentFunction,
        __environmentDesignation.name() : __environmentDesignation,
        __environmentRegistry.name() : __environmentRegistry,
        __linkingEventIdentifier.name() : __linkingEventIdentifier,
        __linkingRightsStatementIdentifier.name() : __linkingRightsStatementIdentifier,
        __objectIdentifier.name() : __objectIdentifier,
        __originalName.name() : __originalName,
        __preservationLevel.name() : __preservationLevel,
        __relationship.name() : __relationship,
        __significantProperties.name() : __significantProperties,
        __environmentExtension.name() : __environmentExtension
    })
    _AttributeMap.update({
        __xmlID.name() : __xmlID,
        __version.name() : __version
    })
_module_typeBindings.intellectualEntity = intellectualEntity
Namespace.addCategoryObject('typeBinding', 'intellectualEntity', intellectualEntity)


# Complex type {http://www.loc.gov/premis/v3}eventComplexType with content type ELEMENT_ONLY
class eventComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}eventComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'eventComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 229, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}eventType uses Python identifier eventType
    __eventType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventType'), 'eventType', '__httpwww_loc_govpremisv3_eventComplexType_httpwww_loc_govpremisv3eventType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1004, 1), )

    
    eventType = property(__eventType.value, __eventType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}eventDetailInformation uses Python identifier eventDetailInformation
    __eventDetailInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventDetailInformation'), 'eventDetailInformation', '__httpwww_loc_govpremisv3_eventComplexType_httpwww_loc_govpremisv3eventDetailInformation', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1073, 4), )

    
    eventDetailInformation = property(__eventDetailInformation.value, __eventDetailInformation.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}eventIdentifier uses Python identifier eventIdentifier
    __eventIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventIdentifier'), 'eventIdentifier', '__httpwww_loc_govpremisv3_eventComplexType_httpwww_loc_govpremisv3eventIdentifier', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1074, 4), )

    
    eventIdentifier = property(__eventIdentifier.value, __eventIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}eventOutcomeInformation uses Python identifier eventOutcomeInformation
    __eventOutcomeInformation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeInformation'), 'eventOutcomeInformation', '__httpwww_loc_govpremisv3_eventComplexType_httpwww_loc_govpremisv3eventOutcomeInformation', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1076, 1), )

    
    eventOutcomeInformation = property(__eventOutcomeInformation.value, __eventOutcomeInformation.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingAgentIdentifier uses Python identifier linkingAgentIdentifier
    __linkingAgentIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifier'), 'linkingAgentIdentifier', '__httpwww_loc_govpremisv3_eventComplexType_httpwww_loc_govpremisv3linkingAgentIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1084, 1), )

    
    linkingAgentIdentifier = property(__linkingAgentIdentifier.value, __linkingAgentIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingObjectIdentifier uses Python identifier linkingObjectIdentifier
    __linkingObjectIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifier'), 'linkingObjectIdentifier', '__httpwww_loc_govpremisv3_eventComplexType_httpwww_loc_govpremisv3linkingObjectIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1087, 1), )

    
    linkingObjectIdentifier = property(__linkingObjectIdentifier.value, __linkingObjectIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}eventDateTime uses Python identifier eventDateTime
    __eventDateTime = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'eventDateTime'), 'eventDateTime', '__httpwww_loc_govpremisv3_eventComplexType_httpwww_loc_govpremisv3eventDateTime', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1120, 1), )

    
    eventDateTime = property(__eventDateTime.value, __eventDateTime.set, None, None)

    
    # Attribute xmlID uses Python identifier xmlID
    __xmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'xmlID'), 'xmlID', '__httpwww_loc_govpremisv3_eventComplexType_xmlID', pyxb.binding.datatypes.ID)
    __xmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 242, 2)
    __xmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 242, 2)
    
    xmlID = property(__xmlID.value, __xmlID.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_loc_govpremisv3_eventComplexType_version', _module_typeBindings.version3)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 243, 2)
    __version._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 243, 2)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __eventType.name() : __eventType,
        __eventDetailInformation.name() : __eventDetailInformation,
        __eventIdentifier.name() : __eventIdentifier,
        __eventOutcomeInformation.name() : __eventOutcomeInformation,
        __linkingAgentIdentifier.name() : __linkingAgentIdentifier,
        __linkingObjectIdentifier.name() : __linkingObjectIdentifier,
        __eventDateTime.name() : __eventDateTime
    })
    _AttributeMap.update({
        __xmlID.name() : __xmlID,
        __version.name() : __version
    })
_module_typeBindings.eventComplexType = eventComplexType
Namespace.addCategoryObject('typeBinding', 'eventComplexType', eventComplexType)


# Complex type {http://www.loc.gov/premis/v3}agentComplexType with content type ELEMENT_ONLY
class agentComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}agentComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'agentComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 249, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}agentNote uses Python identifier agentNote
    __agentNote = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'agentNote'), 'agentNote', '__httpwww_loc_govpremisv3_agentComplexType_httpwww_loc_govpremisv3agentNote', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 935, 1), )

    
    agentNote = property(__agentNote.value, __agentNote.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}agentVersion uses Python identifier agentVersion
    __agentVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'agentVersion'), 'agentVersion', '__httpwww_loc_govpremisv3_agentComplexType_httpwww_loc_govpremisv3agentVersion', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 936, 4), )

    
    agentVersion = property(__agentVersion.value, __agentVersion.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}agentName uses Python identifier agentName
    __agentName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'agentName'), 'agentName', '__httpwww_loc_govpremisv3_agentComplexType_httpwww_loc_govpremisv3agentName', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 990, 1), )

    
    agentName = property(__agentName.value, __agentName.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}agentType uses Python identifier agentType
    __agentType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'agentType'), 'agentType', '__httpwww_loc_govpremisv3_agentComplexType_httpwww_loc_govpremisv3agentType', False, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 991, 1), )

    
    agentType = property(__agentType.value, __agentType.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}agentIdentifier uses Python identifier agentIdentifier
    __agentIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'agentIdentifier'), 'agentIdentifier', '__httpwww_loc_govpremisv3_agentComplexType_httpwww_loc_govpremisv3agentIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1064, 1), )

    
    agentIdentifier = property(__agentIdentifier.value, __agentIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingEnvironmentIdentifier uses Python identifier linkingEnvironmentIdentifier
    __linkingEnvironmentIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentIdentifier'), 'linkingEnvironmentIdentifier', '__httpwww_loc_govpremisv3_agentComplexType_httpwww_loc_govpremisv3linkingEnvironmentIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1085, 4), )

    
    linkingEnvironmentIdentifier = property(__linkingEnvironmentIdentifier.value, __linkingEnvironmentIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingEventIdentifier uses Python identifier linkingEventIdentifier
    __linkingEventIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier'), 'linkingEventIdentifier', '__httpwww_loc_govpremisv3_agentComplexType_httpwww_loc_govpremisv3linkingEventIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1086, 4), )

    
    linkingEventIdentifier = property(__linkingEventIdentifier.value, __linkingEventIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}linkingRightsStatementIdentifier uses Python identifier linkingRightsStatementIdentifier
    __linkingRightsStatementIdentifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier'), 'linkingRightsStatementIdentifier', '__httpwww_loc_govpremisv3_agentComplexType_httpwww_loc_govpremisv3linkingRightsStatementIdentifier', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1088, 1), )

    
    linkingRightsStatementIdentifier = property(__linkingRightsStatementIdentifier.value, __linkingRightsStatementIdentifier.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}agentExtension uses Python identifier agentExtension
    __agentExtension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'agentExtension'), 'agentExtension', '__httpwww_loc_govpremisv3_agentComplexType_httpwww_loc_govpremisv3agentExtension', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1132, 1), )

    
    agentExtension = property(__agentExtension.value, __agentExtension.set, None, None)

    
    # Attribute xmlID uses Python identifier xmlID
    __xmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'xmlID'), 'xmlID', '__httpwww_loc_govpremisv3_agentComplexType_xmlID', pyxb.binding.datatypes.ID)
    __xmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 267, 2)
    __xmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 267, 2)
    
    xmlID = property(__xmlID.value, __xmlID.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_loc_govpremisv3_agentComplexType_version', _module_typeBindings.version3)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 268, 2)
    __version._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 268, 2)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __agentNote.name() : __agentNote,
        __agentVersion.name() : __agentVersion,
        __agentName.name() : __agentName,
        __agentType.name() : __agentType,
        __agentIdentifier.name() : __agentIdentifier,
        __linkingEnvironmentIdentifier.name() : __linkingEnvironmentIdentifier,
        __linkingEventIdentifier.name() : __linkingEventIdentifier,
        __linkingRightsStatementIdentifier.name() : __linkingRightsStatementIdentifier,
        __agentExtension.name() : __agentExtension
    })
    _AttributeMap.update({
        __xmlID.name() : __xmlID,
        __version.name() : __version
    })
_module_typeBindings.agentComplexType = agentComplexType
Namespace.addCategoryObject('typeBinding', 'agentComplexType', agentComplexType)


# Complex type {http://www.loc.gov/premis/v3}rightsComplexType with content type ELEMENT_ONLY
class rightsComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}rightsComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'rightsComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 275, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/premis/v3}rightsStatement uses Python identifier rightsStatement
    __rightsStatement = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'rightsStatement'), 'rightsStatement', '__httpwww_loc_govpremisv3_rightsComplexType_httpwww_loc_govpremisv3rightsStatement', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1099, 1), )

    
    rightsStatement = property(__rightsStatement.value, __rightsStatement.set, None, None)

    
    # Element {http://www.loc.gov/premis/v3}rightsExtension uses Python identifier rightsExtension
    __rightsExtension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'rightsExtension'), 'rightsExtension', '__httpwww_loc_govpremisv3_rightsComplexType_httpwww_loc_govpremisv3rightsExtension', True, pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1139, 1), )

    
    rightsExtension = property(__rightsExtension.value, __rightsExtension.set, None, None)

    
    # Attribute xmlID uses Python identifier xmlID
    __xmlID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'xmlID'), 'xmlID', '__httpwww_loc_govpremisv3_rightsComplexType_xmlID', pyxb.binding.datatypes.ID)
    __xmlID._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 280, 2)
    __xmlID._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 280, 2)
    
    xmlID = property(__xmlID.value, __xmlID.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpwww_loc_govpremisv3_rightsComplexType_version', _module_typeBindings.version3)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 281, 2)
    __version._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 281, 2)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __rightsStatement.name() : __rightsStatement,
        __rightsExtension.name() : __rightsExtension
    })
    _AttributeMap.update({
        __xmlID.name() : __xmlID,
        __version.name() : __version
    })
_module_typeBindings.rightsComplexType = rightsComplexType
Namespace.addCategoryObject('typeBinding', 'rightsComplexType', rightsComplexType)


# Complex type {http://www.loc.gov/premis/v3}compositionLevelComplexType with content type SIMPLE
class compositionLevelComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://www.loc.gov/premis/v3}compositionLevelComplexType with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.nonNegativeInteger
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'compositionLevelComplexType')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 310, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.nonNegativeInteger
    
    # Attribute unknown uses Python identifier unknown
    __unknown = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'unknown'), 'unknown', '__httpwww_loc_govpremisv3_compositionLevelComplexType_unknown', _module_typeBindings.STD_ANON)
    __unknown._DeclarationLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 313, 16)
    __unknown._UseLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 313, 16)
    
    unknown = property(__unknown.value, __unknown.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __unknown.name() : __unknown
    })
_module_typeBindings.compositionLevelComplexType = compositionLevelComplexType
Namespace.addCategoryObject('typeBinding', 'compositionLevelComplexType', compositionLevelComplexType)


# Complex type {http://www.loc.gov/premis/v3}countryCode with content type SIMPLE
class countryCode (stringPlusAuthority):
    """Complex type {http://www.loc.gov/premis/v3}countryCode with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'countryCode')
    _XSDLocation = pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1157, 1)
    _ElementMap = stringPlusAuthority._ElementMap.copy()
    _AttributeMap = stringPlusAuthority._AttributeMap.copy()
    # Base type is stringPlusAuthority
    
    # Attribute authority inherited from {http://www.loc.gov/premis/v3}stringPlusAuthority
    
    # Attribute authorityURI inherited from {http://www.loc.gov/premis/v3}stringPlusAuthority
    
    # Attribute valueURI inherited from {http://www.loc.gov/premis/v3}stringPlusAuthority
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.countryCode = countryCode
Namespace.addCategoryObject('typeBinding', 'countryCode', countryCode)


agentIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 934, 1))
Namespace.addCategoryObject('elementBinding', agentIdentifierValue.name().localName(), agentIdentifierValue)

agentNote = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentNote'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 935, 1))
Namespace.addCategoryObject('elementBinding', agentNote.name().localName(), agentNote)

agentVersion = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentVersion'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 936, 4))
Namespace.addCategoryObject('elementBinding', agentVersion.name().localName(), agentVersion)

contentLocationValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contentLocationValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 937, 1))
Namespace.addCategoryObject('elementBinding', contentLocationValue.name().localName(), contentLocationValue)

copyrightDocumentationIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 938, 1))
Namespace.addCategoryObject('elementBinding', copyrightDocumentationIdentifierValue.name().localName(), copyrightDocumentationIdentifierValue)

copyrightNote = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightNote'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 939, 1))
Namespace.addCategoryObject('elementBinding', copyrightNote.name().localName(), copyrightNote)

creatingApplicationVersion = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationVersion'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 940, 1))
Namespace.addCategoryObject('elementBinding', creatingApplicationVersion.name().localName(), creatingApplicationVersion)

environmentDesignationExtension = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentDesignationExtension'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 941, 4))
Namespace.addCategoryObject('elementBinding', environmentDesignationExtension.name().localName(), environmentDesignationExtension)

environmentDesignationNote = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentDesignationNote'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 942, 4))
Namespace.addCategoryObject('elementBinding', environmentDesignationNote.name().localName(), environmentDesignationNote)

environmentFunctionLevel = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentFunctionLevel'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 943, 4))
Namespace.addCategoryObject('elementBinding', environmentFunctionLevel.name().localName(), environmentFunctionLevel)

environmentNote = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentNote'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 944, 1))
Namespace.addCategoryObject('elementBinding', environmentNote.name().localName(), environmentNote)

environmentOrigin = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentOrigin'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 945, 4))
Namespace.addCategoryObject('elementBinding', environmentOrigin.name().localName(), environmentOrigin)

environmentRegistryKey = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistryKey'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 946, 4))
Namespace.addCategoryObject('elementBinding', environmentRegistryKey.name().localName(), environmentRegistryKey)

environmentRegistryName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistryName'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 947, 4))
Namespace.addCategoryObject('elementBinding', environmentRegistryName.name().localName(), environmentRegistryName)

environmentVersion = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentVersion'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 948, 4))
Namespace.addCategoryObject('elementBinding', environmentVersion.name().localName(), environmentVersion)

eventDetail = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventDetail'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 949, 1))
Namespace.addCategoryObject('elementBinding', eventDetail.name().localName(), eventDetail)

eventIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 950, 1))
Namespace.addCategoryObject('elementBinding', eventIdentifierValue.name().localName(), eventIdentifierValue)

eventOutcomeDetailNote = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetailNote'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 951, 1))
Namespace.addCategoryObject('elementBinding', eventOutcomeDetailNote.name().localName(), eventOutcomeDetailNote)

formatNote = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatNote'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 952, 1))
Namespace.addCategoryObject('elementBinding', formatNote.name().localName(), formatNote)

formatVersion = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatVersion'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 953, 1))
Namespace.addCategoryObject('elementBinding', formatVersion.name().localName(), formatVersion)

hwOtherInformation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'hwOtherInformation'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 954, 1))
Namespace.addCategoryObject('elementBinding', hwOtherInformation.name().localName(), hwOtherInformation)

inhibitorKey = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'inhibitorKey'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 955, 1))
Namespace.addCategoryObject('elementBinding', inhibitorKey.name().localName(), inhibitorKey)

licenseDocumentationIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 956, 1))
Namespace.addCategoryObject('elementBinding', licenseDocumentationIdentifierValue.name().localName(), licenseDocumentationIdentifierValue)

licenseIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 957, 1))
Namespace.addCategoryObject('elementBinding', licenseIdentifierValue.name().localName(), licenseIdentifierValue)

licenseNote = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseNote'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 958, 1))
Namespace.addCategoryObject('elementBinding', licenseNote.name().localName(), licenseNote)

licenseTerms = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseTerms'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 959, 1))
Namespace.addCategoryObject('elementBinding', licenseTerms.name().localName(), licenseTerms)

linkingAgentIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 960, 1))
Namespace.addCategoryObject('elementBinding', linkingAgentIdentifierValue.name().localName(), linkingAgentIdentifierValue)

linkingEnvironmentIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentIdentifierType'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 961, 4))
Namespace.addCategoryObject('elementBinding', linkingEnvironmentIdentifierType.name().localName(), linkingEnvironmentIdentifierType)

linkingEnvironmentIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 962, 4))
Namespace.addCategoryObject('elementBinding', linkingEnvironmentIdentifierValue.name().localName(), linkingEnvironmentIdentifierValue)

linkingEventIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 963, 1))
Namespace.addCategoryObject('elementBinding', linkingEventIdentifierValue.name().localName(), linkingEventIdentifierValue)

linkingObjectIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 964, 1))
Namespace.addCategoryObject('elementBinding', linkingObjectIdentifierValue.name().localName(), linkingObjectIdentifierValue)

linkingRightsStatementIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 965, 1))
Namespace.addCategoryObject('elementBinding', linkingRightsStatementIdentifierValue.name().localName(), linkingRightsStatementIdentifierValue)

messageDigest = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageDigest'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 966, 1))
Namespace.addCategoryObject('elementBinding', messageDigest.name().localName(), messageDigest)

objectIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 967, 1))
Namespace.addCategoryObject('elementBinding', objectIdentifierValue.name().localName(), objectIdentifierValue)

otherRightsDocumentationIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 968, 1))
Namespace.addCategoryObject('elementBinding', otherRightsDocumentationIdentifierValue.name().localName(), otherRightsDocumentationIdentifierValue)

otherRightsNote = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsNote'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 969, 1))
Namespace.addCategoryObject('elementBinding', otherRightsNote.name().localName(), otherRightsNote)

preservationLevelRationale = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelRationale'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 970, 1))
Namespace.addCategoryObject('elementBinding', preservationLevelRationale.name().localName(), preservationLevelRationale)

relatedEventIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedEventIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 971, 1))
Namespace.addCategoryObject('elementBinding', relatedEventIdentifierValue.name().localName(), relatedEventIdentifierValue)

relatedObjectIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 972, 1))
Namespace.addCategoryObject('elementBinding', relatedObjectIdentifierValue.name().localName(), relatedObjectIdentifierValue)

rightsGrantedNote = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsGrantedNote'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 973, 1))
Namespace.addCategoryObject('elementBinding', rightsGrantedNote.name().localName(), rightsGrantedNote)

rightsStatementIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsStatementIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 974, 1))
Namespace.addCategoryObject('elementBinding', rightsStatementIdentifierValue.name().localName(), rightsStatementIdentifierValue)

signatureProperties = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureProperties'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 975, 1))
Namespace.addCategoryObject('elementBinding', signatureProperties.name().localName(), signatureProperties)

signatureValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 976, 1))
Namespace.addCategoryObject('elementBinding', signatureValue.name().localName(), signatureValue)

significantPropertiesValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 977, 1))
Namespace.addCategoryObject('elementBinding', significantPropertiesValue.name().localName(), significantPropertiesValue)

statuteDocumentationIdentifierValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationIdentifierValue'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 978, 1))
Namespace.addCategoryObject('elementBinding', statuteDocumentationIdentifierValue.name().localName(), statuteDocumentationIdentifierValue)

statuteNote = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteNote'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 979, 1))
Namespace.addCategoryObject('elementBinding', statuteNote.name().localName(), statuteNote)

swVersion = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'swVersion'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 980, 1))
Namespace.addCategoryObject('elementBinding', swVersion.name().localName(), swVersion)

swOtherInformation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'swOtherInformation'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 981, 1))
Namespace.addCategoryObject('elementBinding', swOtherInformation.name().localName(), swOtherInformation)

relatedEventSequence = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedEventSequence'), pyxb.binding.datatypes.nonNegativeInteger, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1110, 1))
Namespace.addCategoryObject('elementBinding', relatedEventSequence.name().localName(), relatedEventSequence)

relatedObjectSequence = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectSequence'), pyxb.binding.datatypes.nonNegativeInteger, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1111, 1))
Namespace.addCategoryObject('elementBinding', relatedObjectSequence.name().localName(), relatedObjectSequence)

size = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'size'), pyxb.binding.datatypes.long, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1112, 1))
Namespace.addCategoryObject('elementBinding', size.name().localName(), size)

eventDateTime = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventDateTime'), pyxb.binding.datatypes.string, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1120, 1))
Namespace.addCategoryObject('elementBinding', eventDateTime.name().localName(), eventDateTime)

object = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'object'), objectComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 67, 1))
Namespace.addCategoryObject('elementBinding', object.name().localName(), object)

act = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'act'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 988, 1))
Namespace.addCategoryObject('elementBinding', act.name().localName(), act)

agentIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 989, 1))
Namespace.addCategoryObject('elementBinding', agentIdentifierType.name().localName(), agentIdentifierType)

agentName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentName'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 990, 1))
Namespace.addCategoryObject('elementBinding', agentName.name().localName(), agentName)

agentType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 991, 1))
Namespace.addCategoryObject('elementBinding', agentType.name().localName(), agentType)

contentLocationType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contentLocationType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 992, 1))
Namespace.addCategoryObject('elementBinding', contentLocationType.name().localName(), contentLocationType)

copyrightDocumentationIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 993, 1))
Namespace.addCategoryObject('elementBinding', copyrightDocumentationIdentifierType.name().localName(), copyrightDocumentationIdentifierType)

copyrightDocumentationRole = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationRole'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 994, 1))
Namespace.addCategoryObject('elementBinding', copyrightDocumentationRole.name().localName(), copyrightDocumentationRole)

copyrightStatus = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightStatus'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 995, 1))
Namespace.addCategoryObject('elementBinding', copyrightStatus.name().localName(), copyrightStatus)

creatingApplicationName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationName'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 996, 1))
Namespace.addCategoryObject('elementBinding', creatingApplicationName.name().localName(), creatingApplicationName)

environmentCharacteristic = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentCharacteristic'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 997, 1))
Namespace.addCategoryObject('elementBinding', environmentCharacteristic.name().localName(), environmentCharacteristic)

environmentFunctionType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentFunctionType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 998, 4))
Namespace.addCategoryObject('elementBinding', environmentFunctionType.name().localName(), environmentFunctionType)

environmentName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentName'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 999, 4))
Namespace.addCategoryObject('elementBinding', environmentName.name().localName(), environmentName)

environmentRegistryRole = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistryRole'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1000, 4))
Namespace.addCategoryObject('elementBinding', environmentRegistryRole.name().localName(), environmentRegistryRole)

environmentPurpose = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentPurpose'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1001, 1))
Namespace.addCategoryObject('elementBinding', environmentPurpose.name().localName(), environmentPurpose)

eventIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1002, 1))
Namespace.addCategoryObject('elementBinding', eventIdentifierType.name().localName(), eventIdentifierType)

eventOutcome = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventOutcome'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1003, 1))
Namespace.addCategoryObject('elementBinding', eventOutcome.name().localName(), eventOutcome)

eventType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1004, 1))
Namespace.addCategoryObject('elementBinding', eventType.name().localName(), eventType)

formatName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatName'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1005, 1))
Namespace.addCategoryObject('elementBinding', formatName.name().localName(), formatName)

formatRegistryName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatRegistryName'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1006, 1))
Namespace.addCategoryObject('elementBinding', formatRegistryName.name().localName(), formatRegistryName)

formatRegistryKey = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatRegistryKey'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1007, 1))
Namespace.addCategoryObject('elementBinding', formatRegistryKey.name().localName(), formatRegistryKey)

formatRegistryRole = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatRegistryRole'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1008, 1))
Namespace.addCategoryObject('elementBinding', formatRegistryRole.name().localName(), formatRegistryRole)

hwName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'hwName'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1009, 1))
Namespace.addCategoryObject('elementBinding', hwName.name().localName(), hwName)

hwType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'hwType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1010, 1))
Namespace.addCategoryObject('elementBinding', hwType.name().localName(), hwType)

inhibitorTarget = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'inhibitorTarget'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1011, 1))
Namespace.addCategoryObject('elementBinding', inhibitorTarget.name().localName(), inhibitorTarget)

inhibitorType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'inhibitorType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1012, 1))
Namespace.addCategoryObject('elementBinding', inhibitorType.name().localName(), inhibitorType)

licenseDocumentationIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1013, 1))
Namespace.addCategoryObject('elementBinding', licenseDocumentationIdentifierType.name().localName(), licenseDocumentationIdentifierType)

licenseDocumentationRole = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationRole'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1014, 1))
Namespace.addCategoryObject('elementBinding', licenseDocumentationRole.name().localName(), licenseDocumentationRole)

licenseIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1015, 1))
Namespace.addCategoryObject('elementBinding', licenseIdentifierType.name().localName(), licenseIdentifierType)

linkingAgentIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1016, 1))
Namespace.addCategoryObject('elementBinding', linkingAgentIdentifierType.name().localName(), linkingAgentIdentifierType)

linkingAgentRole = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentRole'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1017, 1))
Namespace.addCategoryObject('elementBinding', linkingAgentRole.name().localName(), linkingAgentRole)

linkingEventIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1018, 1))
Namespace.addCategoryObject('elementBinding', linkingEventIdentifierType.name().localName(), linkingEventIdentifierType)

linkingEnvironmentRole = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentRole'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1019, 4))
Namespace.addCategoryObject('elementBinding', linkingEnvironmentRole.name().localName(), linkingEnvironmentRole)

linkingObjectIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1020, 1))
Namespace.addCategoryObject('elementBinding', linkingObjectIdentifierType.name().localName(), linkingObjectIdentifierType)

linkingObjectRole = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectRole'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1021, 1))
Namespace.addCategoryObject('elementBinding', linkingObjectRole.name().localName(), linkingObjectRole)

linkingRightsStatementIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1022, 1))
Namespace.addCategoryObject('elementBinding', linkingRightsStatementIdentifierType.name().localName(), linkingRightsStatementIdentifierType)

messageDigestAlgorithm = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageDigestAlgorithm'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1023, 1))
Namespace.addCategoryObject('elementBinding', messageDigestAlgorithm.name().localName(), messageDigestAlgorithm)

messageDigestOriginator = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageDigestOriginator'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1024, 1))
Namespace.addCategoryObject('elementBinding', messageDigestOriginator.name().localName(), messageDigestOriginator)

objectIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1025, 1))
Namespace.addCategoryObject('elementBinding', objectIdentifierType.name().localName(), objectIdentifierType)

otherRightsBasis = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsBasis'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1026, 1))
Namespace.addCategoryObject('elementBinding', otherRightsBasis.name().localName(), otherRightsBasis)

otherRightsDocumentationRole = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationRole'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1027, 1))
Namespace.addCategoryObject('elementBinding', otherRightsDocumentationRole.name().localName(), otherRightsDocumentationRole)

otherRightsDocumentationIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1028, 1))
Namespace.addCategoryObject('elementBinding', otherRightsDocumentationIdentifierType.name().localName(), otherRightsDocumentationIdentifierType)

preservationLevelType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1029, 4))
Namespace.addCategoryObject('elementBinding', preservationLevelType.name().localName(), preservationLevelType)

preservationLevelValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelValue'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1030, 3))
Namespace.addCategoryObject('elementBinding', preservationLevelValue.name().localName(), preservationLevelValue)

preservationLevelRole = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelRole'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1031, 1))
Namespace.addCategoryObject('elementBinding', preservationLevelRole.name().localName(), preservationLevelRole)

relatedEventIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedEventIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1032, 4))
Namespace.addCategoryObject('elementBinding', relatedEventIdentifierType.name().localName(), relatedEventIdentifierType)

relatedEnvironmentPurpose = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedEnvironmentPurpose'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1033, 1))
Namespace.addCategoryObject('elementBinding', relatedEnvironmentPurpose.name().localName(), relatedEnvironmentPurpose)

relatedEnvironmentCharacteristic = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedEnvironmentCharacteristic'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1034, 4))
Namespace.addCategoryObject('elementBinding', relatedEnvironmentCharacteristic.name().localName(), relatedEnvironmentCharacteristic)

relatedObjectIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1035, 1))
Namespace.addCategoryObject('elementBinding', relatedObjectIdentifierType.name().localName(), relatedObjectIdentifierType)

relationshipType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relationshipType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1036, 1))
Namespace.addCategoryObject('elementBinding', relationshipType.name().localName(), relationshipType)

relationshipSubType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relationshipSubType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1037, 1))
Namespace.addCategoryObject('elementBinding', relationshipSubType.name().localName(), relationshipSubType)

restriction = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'restriction'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1038, 1))
Namespace.addCategoryObject('elementBinding', restriction.name().localName(), restriction)

rightsBasis = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsBasis'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1039, 1))
Namespace.addCategoryObject('elementBinding', rightsBasis.name().localName(), rightsBasis)

rightsStatementIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsStatementIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1040, 1))
Namespace.addCategoryObject('elementBinding', rightsStatementIdentifierType.name().localName(), rightsStatementIdentifierType)

signatureEncoding = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureEncoding'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1041, 1))
Namespace.addCategoryObject('elementBinding', signatureEncoding.name().localName(), signatureEncoding)

signatureMethod = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureMethod'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1042, 1))
Namespace.addCategoryObject('elementBinding', signatureMethod.name().localName(), signatureMethod)

signatureValidationRules = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureValidationRules'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1043, 1))
Namespace.addCategoryObject('elementBinding', signatureValidationRules.name().localName(), signatureValidationRules)

signer = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signer'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1044, 1))
Namespace.addCategoryObject('elementBinding', signer.name().localName(), signer)

significantPropertiesType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1045, 1))
Namespace.addCategoryObject('elementBinding', significantPropertiesType.name().localName(), significantPropertiesType)

storageMedium = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'storageMedium'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1046, 1))
Namespace.addCategoryObject('elementBinding', storageMedium.name().localName(), storageMedium)

statuteCitation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteCitation'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1047, 1))
Namespace.addCategoryObject('elementBinding', statuteCitation.name().localName(), statuteCitation)

statuteDocumentationIdentifierType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationIdentifierType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1048, 1))
Namespace.addCategoryObject('elementBinding', statuteDocumentationIdentifierType.name().localName(), statuteDocumentationIdentifierType)

statuteDocumentationRole = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationRole'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1049, 1))
Namespace.addCategoryObject('elementBinding', statuteDocumentationRole.name().localName(), statuteDocumentationRole)

swName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'swName'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1050, 1))
Namespace.addCategoryObject('elementBinding', swName.name().localName(), swName)

swType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'swType'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1051, 1))
Namespace.addCategoryObject('elementBinding', swType.name().localName(), swType)

swDependency = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'swDependency'), stringPlusAuthority, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1052, 1))
Namespace.addCategoryObject('elementBinding', swDependency.name().localName(), swDependency)

agentIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentIdentifier'), agentIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1064, 1))
Namespace.addCategoryObject('elementBinding', agentIdentifier.name().localName(), agentIdentifier)

contentLocation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contentLocation'), contentLocationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1065, 1))
Namespace.addCategoryObject('elementBinding', contentLocation.name().localName(), contentLocation)

copyrightDocumentationIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationIdentifier'), copyrightDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1067, 1))
Namespace.addCategoryObject('elementBinding', copyrightDocumentationIdentifier.name().localName(), copyrightDocumentationIdentifier)

copyrightInformation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightInformation'), copyrightInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1068, 1))
Namespace.addCategoryObject('elementBinding', copyrightInformation.name().localName(), copyrightInformation)

creatingApplication = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'creatingApplication'), creatingApplicationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1069, 1))
Namespace.addCategoryObject('elementBinding', creatingApplication.name().localName(), creatingApplication)

environmentFunction = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentFunction'), environmentFunctionComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1070, 4))
Namespace.addCategoryObject('elementBinding', environmentFunction.name().localName(), environmentFunction)

environmentDesignation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentDesignation'), environmentDesignationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1071, 4))
Namespace.addCategoryObject('elementBinding', environmentDesignation.name().localName(), environmentDesignation)

environmentRegistry = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistry'), environmentRegistryComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1072, 4))
Namespace.addCategoryObject('elementBinding', environmentRegistry.name().localName(), environmentRegistry)

eventDetailInformation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventDetailInformation'), eventDetailInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1073, 4))
Namespace.addCategoryObject('elementBinding', eventDetailInformation.name().localName(), eventDetailInformation)

eventIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventIdentifier'), eventIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1074, 4))
Namespace.addCategoryObject('elementBinding', eventIdentifier.name().localName(), eventIdentifier)

eventOutcomeDetail = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetail'), eventOutcomeDetailComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1075, 1))
Namespace.addCategoryObject('elementBinding', eventOutcomeDetail.name().localName(), eventOutcomeDetail)

eventOutcomeInformation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeInformation'), eventOutcomeInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1076, 1))
Namespace.addCategoryObject('elementBinding', eventOutcomeInformation.name().localName(), eventOutcomeInformation)

fixity = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'fixity'), fixityComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1077, 1))
Namespace.addCategoryObject('elementBinding', fixity.name().localName(), fixity)

format = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'format'), formatComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1078, 1))
Namespace.addCategoryObject('elementBinding', format.name().localName(), format)

formatDesignation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatDesignation'), formatDesignationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1079, 1))
Namespace.addCategoryObject('elementBinding', formatDesignation.name().localName(), formatDesignation)

formatRegistry = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatRegistry'), formatRegistryComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1080, 1))
Namespace.addCategoryObject('elementBinding', formatRegistry.name().localName(), formatRegistry)

inhibitors = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'inhibitors'), inhibitorsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1081, 1))
Namespace.addCategoryObject('elementBinding', inhibitors.name().localName(), inhibitors)

licenseDocumentationIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationIdentifier'), licenseDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1082, 1))
Namespace.addCategoryObject('elementBinding', licenseDocumentationIdentifier.name().localName(), licenseDocumentationIdentifier)

licenseInformation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseInformation'), licenseInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1083, 1))
Namespace.addCategoryObject('elementBinding', licenseInformation.name().localName(), licenseInformation)

linkingAgentIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifier'), linkingAgentIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1084, 1))
Namespace.addCategoryObject('elementBinding', linkingAgentIdentifier.name().localName(), linkingAgentIdentifier)

linkingEnvironmentIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentIdentifier'), linkingEnvironmentIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1085, 4))
Namespace.addCategoryObject('elementBinding', linkingEnvironmentIdentifier.name().localName(), linkingEnvironmentIdentifier)

linkingEventIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier'), linkingEventIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1086, 4))
Namespace.addCategoryObject('elementBinding', linkingEventIdentifier.name().localName(), linkingEventIdentifier)

linkingObjectIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifier'), linkingObjectIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1087, 1))
Namespace.addCategoryObject('elementBinding', linkingObjectIdentifier.name().localName(), linkingObjectIdentifier)

linkingRightsStatementIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier'), linkingRightsStatementIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1088, 1))
Namespace.addCategoryObject('elementBinding', linkingRightsStatementIdentifier.name().localName(), linkingRightsStatementIdentifier)

objectCharacteristics = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectCharacteristics'), objectCharacteristicsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1089, 1))
Namespace.addCategoryObject('elementBinding', objectCharacteristics.name().localName(), objectCharacteristics)

objectIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifier'), objectIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1090, 1))
Namespace.addCategoryObject('elementBinding', objectIdentifier.name().localName(), objectIdentifier)

originalName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'originalName'), originalNameComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1091, 1))
Namespace.addCategoryObject('elementBinding', originalName.name().localName(), originalName)

otherRightsDocumentationIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationIdentifier'), otherRightsDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1092, 1))
Namespace.addCategoryObject('elementBinding', otherRightsDocumentationIdentifier.name().localName(), otherRightsDocumentationIdentifier)

otherRightsInformation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsInformation'), otherRightsInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1093, 1))
Namespace.addCategoryObject('elementBinding', otherRightsInformation.name().localName(), otherRightsInformation)

preservationLevel = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevel'), preservationLevelComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1094, 1))
Namespace.addCategoryObject('elementBinding', preservationLevel.name().localName(), preservationLevel)

relatedEventIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedEventIdentifier'), relatedEventIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1095, 1))
Namespace.addCategoryObject('elementBinding', relatedEventIdentifier.name().localName(), relatedEventIdentifier)

relatedObjectIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectIdentifier'), relatedObjectIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1096, 1))
Namespace.addCategoryObject('elementBinding', relatedObjectIdentifier.name().localName(), relatedObjectIdentifier)

relationship = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relationship'), relationshipComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1097, 4))
Namespace.addCategoryObject('elementBinding', relationship.name().localName(), relationship)

rightsGranted = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsGranted'), rightsGrantedComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1098, 1))
Namespace.addCategoryObject('elementBinding', rightsGranted.name().localName(), rightsGranted)

rightsStatement = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsStatement'), rightsStatementComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1099, 1))
Namespace.addCategoryObject('elementBinding', rightsStatement.name().localName(), rightsStatement)

rightsStatementIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsStatementIdentifier'), rightsStatementIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1100, 1))
Namespace.addCategoryObject('elementBinding', rightsStatementIdentifier.name().localName(), rightsStatementIdentifier)

signature = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signature'), signatureComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1101, 1))
Namespace.addCategoryObject('elementBinding', signature.name().localName(), signature)

signatureInformation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureInformation'), signatureInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1102, 1))
Namespace.addCategoryObject('elementBinding', signatureInformation.name().localName(), signatureInformation)

significantProperties = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'significantProperties'), significantPropertiesComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1103, 1))
Namespace.addCategoryObject('elementBinding', significantProperties.name().localName(), significantProperties)

statuteDocumentationIdentifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationIdentifier'), statuteDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1104, 1))
Namespace.addCategoryObject('elementBinding', statuteDocumentationIdentifier.name().localName(), statuteDocumentationIdentifier)

statuteInformation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteInformation'), statuteInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1105, 1))
Namespace.addCategoryObject('elementBinding', statuteInformation.name().localName(), statuteInformation)

storage = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'storage'), storageComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1106, 1))
Namespace.addCategoryObject('elementBinding', storage.name().localName(), storage)

dateCreatedByApplication = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateCreatedByApplication'), edtfSimpleType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1116, 1))
Namespace.addCategoryObject('elementBinding', dateCreatedByApplication.name().localName(), dateCreatedByApplication)

endDate = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'endDate'), edtfSimpleType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1117, 1))
Namespace.addCategoryObject('elementBinding', endDate.name().localName(), endDate)

copyrightApplicableDates = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightApplicableDates'), startAndEndDateComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1118, 1))
Namespace.addCategoryObject('elementBinding', copyrightApplicableDates.name().localName(), copyrightApplicableDates)

copyrightStatusDeterminationDate = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightStatusDeterminationDate'), edtfSimpleType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1119, 1))
Namespace.addCategoryObject('elementBinding', copyrightStatusDeterminationDate.name().localName(), copyrightStatusDeterminationDate)

licenseApplicableDates = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseApplicableDates'), startAndEndDateComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1121, 1))
Namespace.addCategoryObject('elementBinding', licenseApplicableDates.name().localName(), licenseApplicableDates)

preservationLevelDateAssigned = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelDateAssigned'), edtfSimpleType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1122, 1))
Namespace.addCategoryObject('elementBinding', preservationLevelDateAssigned.name().localName(), preservationLevelDateAssigned)

startDate = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'startDate'), edtfSimpleType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1123, 1))
Namespace.addCategoryObject('elementBinding', startDate.name().localName(), startDate)

otherRightsApplicableDates = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsApplicableDates'), startAndEndDateComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1124, 1))
Namespace.addCategoryObject('elementBinding', otherRightsApplicableDates.name().localName(), otherRightsApplicableDates)

statuteApplicableDates = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteApplicableDates'), startAndEndDateComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1125, 1))
Namespace.addCategoryObject('elementBinding', statuteApplicableDates.name().localName(), statuteApplicableDates)

statuteInformationDeterminationDate = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteInformationDeterminationDate'), edtfSimpleType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1126, 1))
Namespace.addCategoryObject('elementBinding', statuteInformationDeterminationDate.name().localName(), statuteInformationDeterminationDate)

termOfGrant = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'termOfGrant'), startAndEndDateComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1127, 1))
Namespace.addCategoryObject('elementBinding', termOfGrant.name().localName(), termOfGrant)

termOfRestriction = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'termOfRestriction'), startAndEndDateComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1128, 1))
Namespace.addCategoryObject('elementBinding', termOfRestriction.name().localName(), termOfRestriction)

agentExtension = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentExtension'), extensionComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1132, 1))
Namespace.addCategoryObject('elementBinding', agentExtension.name().localName(), agentExtension)

creatingApplicationExtension = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationExtension'), extensionComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1133, 1))
Namespace.addCategoryObject('elementBinding', creatingApplicationExtension.name().localName(), creatingApplicationExtension)

environmentExtension = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentExtension'), extensionComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1134, 1))
Namespace.addCategoryObject('elementBinding', environmentExtension.name().localName(), environmentExtension)

eventDetailExtension = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventDetailExtension'), extensionComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1135, 4))
Namespace.addCategoryObject('elementBinding', eventDetailExtension.name().localName(), eventDetailExtension)

eventOutcomeDetailExtension = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetailExtension'), extensionComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1136, 4))
Namespace.addCategoryObject('elementBinding', eventOutcomeDetailExtension.name().localName(), eventOutcomeDetailExtension)

keyInformation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'keyInformation'), extensionComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1137, 1))
Namespace.addCategoryObject('elementBinding', keyInformation.name().localName(), keyInformation)

objectCharacteristicsExtension = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectCharacteristicsExtension'), extensionComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1138, 1))
Namespace.addCategoryObject('elementBinding', objectCharacteristicsExtension.name().localName(), objectCharacteristicsExtension)

rightsExtension = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsExtension'), extensionComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1139, 1))
Namespace.addCategoryObject('elementBinding', rightsExtension.name().localName(), rightsExtension)

signatureInformationExtension = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureInformationExtension'), extensionComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1140, 1))
Namespace.addCategoryObject('elementBinding', signatureInformationExtension.name().localName(), signatureInformationExtension)

significantPropertiesExtension = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesExtension'), extensionComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1141, 1))
Namespace.addCategoryObject('elementBinding', significantPropertiesExtension.name().localName(), significantPropertiesExtension)

premis = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'premis'), premisComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 66, 1))
Namespace.addCategoryObject('elementBinding', premis.name().localName(), premis)

event = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'event'), eventComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 68, 1))
Namespace.addCategoryObject('elementBinding', event.name().localName(), event)

agent = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agent'), agentComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 69, 1))
Namespace.addCategoryObject('elementBinding', agent.name().localName(), agent)

rights = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rights'), rightsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 70, 1))
Namespace.addCategoryObject('elementBinding', rights.name().localName(), rights)

copyrightJurisdiction = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightJurisdiction'), countryCode, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1057, 1))
Namespace.addCategoryObject('elementBinding', copyrightJurisdiction.name().localName(), copyrightJurisdiction)

statuteJurisdiction = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteJurisdiction'), countryCode, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1058, 1))
Namespace.addCategoryObject('elementBinding', statuteJurisdiction.name().localName(), statuteJurisdiction)

compositionLevel = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'compositionLevel'), compositionLevelComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1066, 4))
Namespace.addCategoryObject('elementBinding', compositionLevel.name().localName(), compositionLevel)



agentIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentIdentifierValue'), pyxb.binding.datatypes.string, scope=agentIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 934, 1)))

agentIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentIdentifierType'), stringPlusAuthority, scope=agentIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 989, 1)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(agentIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'agentIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 298, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(agentIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'agentIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 299, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
agentIdentifierComplexType._Automaton = _BuildAutomaton()




contentLocationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contentLocationValue'), pyxb.binding.datatypes.string, scope=contentLocationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 937, 1)))

contentLocationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contentLocationType'), stringPlusAuthority, scope=contentLocationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 992, 1)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(contentLocationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'contentLocationType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 329, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(contentLocationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'contentLocationValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 330, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
contentLocationComplexType._Automaton = _BuildAutomaton_()




copyrightDocumentationIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationIdentifierValue'), pyxb.binding.datatypes.string, scope=copyrightDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 938, 1)))

copyrightDocumentationIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationIdentifierType'), stringPlusAuthority, scope=copyrightDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 993, 1)))

copyrightDocumentationIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationRole'), stringPlusAuthority, scope=copyrightDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 994, 1)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 342, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(copyrightDocumentationIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 340, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(copyrightDocumentationIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 341, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(copyrightDocumentationIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationRole')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 342, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
copyrightDocumentationIdentifierComplexType._Automaton = _BuildAutomaton_2()




copyrightInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightNote'), pyxb.binding.datatypes.string, scope=copyrightInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 939, 1)))

copyrightInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightStatus'), stringPlusAuthority, scope=copyrightInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 995, 1)))

copyrightInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightJurisdiction'), countryCode, scope=copyrightInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1057, 1)))

copyrightInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationIdentifier'), copyrightDocumentationIdentifierComplexType, scope=copyrightInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1067, 1)))

copyrightInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightApplicableDates'), startAndEndDateComplexType, scope=copyrightInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1118, 1)))

copyrightInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightStatusDeterminationDate'), edtfSimpleType, scope=copyrightInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1119, 1)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 353, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 354, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 355, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 356, 3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(copyrightInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'copyrightStatus')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 351, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(copyrightInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'copyrightJurisdiction')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 352, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(copyrightInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'copyrightStatusDeterminationDate')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 353, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(copyrightInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'copyrightNote')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 354, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(copyrightInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'copyrightDocumentationIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 355, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(copyrightInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'copyrightApplicableDates')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 356, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
copyrightInformationComplexType._Automaton = _BuildAutomaton_3()




creatingApplicationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationVersion'), pyxb.binding.datatypes.string, scope=creatingApplicationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 940, 1)))

creatingApplicationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationName'), stringPlusAuthority, scope=creatingApplicationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 996, 1)))

creatingApplicationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dateCreatedByApplication'), edtfSimpleType, scope=creatingApplicationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1116, 1)))

creatingApplicationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationExtension'), extensionComplexType, scope=creatingApplicationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1133, 1)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 367, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 368, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 369, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 374, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 375, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 380, 4))
    counters.add(cc_5)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(creatingApplicationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationName')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 366, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(creatingApplicationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationVersion')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 367, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(creatingApplicationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateCreatedByApplication')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 368, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(creatingApplicationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 369, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(creatingApplicationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationVersion')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 373, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(creatingApplicationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateCreatedByApplication')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 374, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(creatingApplicationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 375, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(creatingApplicationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dateCreatedByApplication')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 379, 4))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(creatingApplicationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 380, 4))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(creatingApplicationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'creatingApplicationExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 383, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
         ]))
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
creatingApplicationComplexType._Automaton = _BuildAutomaton_4()




environmentFunctionComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentFunctionLevel'), pyxb.binding.datatypes.string, scope=environmentFunctionComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 943, 4)))

environmentFunctionComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentFunctionType'), stringPlusAuthority, scope=environmentFunctionComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 998, 4)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(environmentFunctionComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentFunctionType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 403, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(environmentFunctionComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentFunctionLevel')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 404, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
environmentFunctionComplexType._Automaton = _BuildAutomaton_5()




environmentDesignationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentDesignationExtension'), pyxb.binding.datatypes.string, scope=environmentDesignationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 941, 4)))

environmentDesignationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentDesignationNote'), pyxb.binding.datatypes.string, scope=environmentDesignationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 942, 4)))

environmentDesignationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentOrigin'), pyxb.binding.datatypes.string, scope=environmentDesignationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 945, 4)))

environmentDesignationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentVersion'), pyxb.binding.datatypes.string, scope=environmentDesignationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 948, 4)))

environmentDesignationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentName'), stringPlusAuthority, scope=environmentDesignationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 999, 4)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 416, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 417, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 418, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 419, 12))
    counters.add(cc_3)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(environmentDesignationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentName')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 415, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(environmentDesignationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentVersion')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 416, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(environmentDesignationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentOrigin')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 417, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(environmentDesignationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentDesignationNote')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 418, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(environmentDesignationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentDesignationExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 419, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
environmentDesignationComplexType._Automaton = _BuildAutomaton_6()




environmentRegistryComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistryKey'), pyxb.binding.datatypes.string, scope=environmentRegistryComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 946, 4)))

environmentRegistryComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistryName'), pyxb.binding.datatypes.string, scope=environmentRegistryComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 947, 4)))

environmentRegistryComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistryRole'), stringPlusAuthority, scope=environmentRegistryComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1000, 4)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 432, 12))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(environmentRegistryComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistryName')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 430, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(environmentRegistryComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistryKey')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 431, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(environmentRegistryComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistryRole')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 432, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
environmentRegistryComplexType._Automaton = _BuildAutomaton_7()




eventDetailInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventDetail'), pyxb.binding.datatypes.string, scope=eventDetailInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 949, 1)))

eventDetailInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventDetailExtension'), extensionComplexType, scope=eventDetailInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1135, 4)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 443, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 444, 12))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(eventDetailInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventDetail')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 443, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(eventDetailInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventDetailExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 444, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
eventDetailInformationComplexType._Automaton = _BuildAutomaton_8()




eventIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventIdentifierValue'), pyxb.binding.datatypes.string, scope=eventIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 950, 1)))

eventIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventIdentifierType'), stringPlusAuthority, scope=eventIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1002, 1)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 453, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 454, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventIdentifierComplexType._Automaton = _BuildAutomaton_9()




eventOutcomeDetailComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetailNote'), pyxb.binding.datatypes.string, scope=eventOutcomeDetailComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 951, 1)))

eventOutcomeDetailComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetailExtension'), extensionComplexType, scope=eventOutcomeDetailComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1136, 4)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 468, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventOutcomeDetailComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetailNote')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 467, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(eventOutcomeDetailComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetailExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 468, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventOutcomeDetailComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetailExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 471, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventOutcomeDetailComplexType._Automaton = _BuildAutomaton_10()




eventOutcomeInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventOutcome'), stringPlusAuthority, scope=eventOutcomeInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1003, 1)))

eventOutcomeInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetail'), eventOutcomeDetailComplexType, scope=eventOutcomeInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1075, 1)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 484, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventOutcomeInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventOutcome')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 483, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(eventOutcomeInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetail')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 484, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventOutcomeInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeDetail')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 486, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventOutcomeInformationComplexType._Automaton = _BuildAutomaton_11()




fixityComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageDigest'), pyxb.binding.datatypes.string, scope=fixityComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 966, 1)))

fixityComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageDigestAlgorithm'), stringPlusAuthority, scope=fixityComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1023, 1)))

fixityComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'messageDigestOriginator'), stringPlusAuthority, scope=fixityComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1024, 1)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 497, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(fixityComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageDigestAlgorithm')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 495, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(fixityComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageDigest')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 496, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(fixityComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'messageDigestOriginator')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 497, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
fixityComplexType._Automaton = _BuildAutomaton_12()




formatComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatNote'), pyxb.binding.datatypes.string, scope=formatComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 952, 1)))

formatComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatDesignation'), formatDesignationComplexType, scope=formatComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1079, 1)))

formatComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatRegistry'), formatRegistryComplexType, scope=formatComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1080, 1)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 511, 5))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 515, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(formatComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'formatDesignation')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 510, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(formatComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'formatRegistry')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 511, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(formatComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'formatRegistry')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 513, 4))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(formatComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'formatNote')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 515, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
formatComplexType._Automaton = _BuildAutomaton_13()




formatDesignationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatVersion'), pyxb.binding.datatypes.string, scope=formatDesignationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 953, 1)))

formatDesignationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatName'), stringPlusAuthority, scope=formatDesignationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1005, 1)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 524, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(formatDesignationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'formatName')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 523, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(formatDesignationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'formatVersion')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 524, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
formatDesignationComplexType._Automaton = _BuildAutomaton_14()




formatRegistryComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatRegistryName'), stringPlusAuthority, scope=formatRegistryComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1006, 1)))

formatRegistryComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatRegistryKey'), stringPlusAuthority, scope=formatRegistryComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1007, 1)))

formatRegistryComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'formatRegistryRole'), stringPlusAuthority, scope=formatRegistryComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1008, 1)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 534, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(formatRegistryComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'formatRegistryName')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 532, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(formatRegistryComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'formatRegistryKey')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 533, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(formatRegistryComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'formatRegistryRole')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 534, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
formatRegistryComplexType._Automaton = _BuildAutomaton_15()




inhibitorsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'inhibitorKey'), pyxb.binding.datatypes.string, scope=inhibitorsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 955, 1)))

inhibitorsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'inhibitorTarget'), stringPlusAuthority, scope=inhibitorsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1011, 1)))

inhibitorsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'inhibitorType'), stringPlusAuthority, scope=inhibitorsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1012, 1)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 545, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 546, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(inhibitorsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'inhibitorType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 544, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(inhibitorsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'inhibitorTarget')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 545, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(inhibitorsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'inhibitorKey')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 546, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
inhibitorsComplexType._Automaton = _BuildAutomaton_16()




licenseDocumentationIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationIdentifierValue'), pyxb.binding.datatypes.string, scope=licenseDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 956, 1)))

licenseDocumentationIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationIdentifierType'), stringPlusAuthority, scope=licenseDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1013, 1)))

licenseDocumentationIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationRole'), stringPlusAuthority, scope=licenseDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1014, 1)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 556, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(licenseDocumentationIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 554, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(licenseDocumentationIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 555, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(licenseDocumentationIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationRole')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 556, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
licenseDocumentationIdentifierComplexType._Automaton = _BuildAutomaton_17()




licenseInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseNote'), pyxb.binding.datatypes.string, scope=licenseInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 958, 1)))

licenseInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseTerms'), pyxb.binding.datatypes.string, scope=licenseInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 959, 1)))

licenseInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationIdentifier'), licenseDocumentationIdentifierComplexType, scope=licenseInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1082, 1)))

licenseInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseApplicableDates'), startAndEndDateComplexType, scope=licenseInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1121, 1)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 568, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 569, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 570, 4))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 574, 4))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 575, 4))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 579, 10))
    counters.add(cc_5)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(licenseInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseDocumentationIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 567, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(licenseInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseTerms')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 568, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(licenseInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseNote')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 569, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(licenseInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseApplicableDates')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 570, 4))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(licenseInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseTerms')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 573, 4))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(licenseInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseNote')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 574, 4))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(licenseInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseApplicableDates')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 575, 4))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(licenseInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseNote')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 578, 7))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(licenseInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseApplicableDates')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 579, 10))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(licenseInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseApplicableDates')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 581, 4))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
licenseInformationComplexType._Automaton = _BuildAutomaton_18()




linkingAgentIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifierValue'), pyxb.binding.datatypes.string, scope=linkingAgentIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 960, 1)))

linkingAgentIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifierType'), stringPlusAuthority, scope=linkingAgentIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1016, 1)))

linkingAgentIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentRole'), stringPlusAuthority, scope=linkingAgentIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1017, 1)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 592, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(linkingAgentIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 590, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(linkingAgentIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 591, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(linkingAgentIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentRole')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 592, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
linkingAgentIdentifierComplexType._Automaton = _BuildAutomaton_19()




linkingEnvironmentIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentIdentifierType'), pyxb.binding.datatypes.string, scope=linkingEnvironmentIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 961, 4)))

linkingEnvironmentIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentIdentifierValue'), pyxb.binding.datatypes.string, scope=linkingEnvironmentIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 962, 4)))

linkingEnvironmentIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentRole'), stringPlusAuthority, scope=linkingEnvironmentIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1019, 4)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 608, 12))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(linkingEnvironmentIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 606, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(linkingEnvironmentIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 607, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(linkingEnvironmentIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentRole')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 608, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
linkingEnvironmentIdentifierComplexType._Automaton = _BuildAutomaton_20()




linkingEventIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifierValue'), pyxb.binding.datatypes.string, scope=linkingEventIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 963, 1)))

linkingEventIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifierType'), stringPlusAuthority, scope=linkingEventIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1018, 1)))

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(linkingEventIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 619, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(linkingEventIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 620, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
linkingEventIdentifierComplexType._Automaton = _BuildAutomaton_21()




linkingObjectIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifierValue'), pyxb.binding.datatypes.string, scope=linkingObjectIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 964, 1)))

linkingObjectIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifierType'), stringPlusAuthority, scope=linkingObjectIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1020, 1)))

linkingObjectIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectRole'), stringPlusAuthority, scope=linkingObjectIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1021, 1)))

def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 633, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(linkingObjectIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 631, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(linkingObjectIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 632, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(linkingObjectIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectRole')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 633, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
linkingObjectIdentifierComplexType._Automaton = _BuildAutomaton_22()




linkingRightsStatementIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifierValue'), pyxb.binding.datatypes.string, scope=linkingRightsStatementIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 965, 1)))

linkingRightsStatementIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifierType'), stringPlusAuthority, scope=linkingRightsStatementIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1022, 1)))

def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(linkingRightsStatementIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 644, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(linkingRightsStatementIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 645, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
linkingRightsStatementIdentifierComplexType._Automaton = _BuildAutomaton_23()




objectCharacteristicsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'compositionLevel'), compositionLevelComplexType, scope=objectCharacteristicsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1066, 4)))

objectCharacteristicsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'creatingApplication'), creatingApplicationComplexType, scope=objectCharacteristicsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1069, 1)))

objectCharacteristicsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'fixity'), fixityComplexType, scope=objectCharacteristicsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1077, 1)))

objectCharacteristicsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'format'), formatComplexType, scope=objectCharacteristicsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1078, 1)))

objectCharacteristicsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'inhibitors'), inhibitorsComplexType, scope=objectCharacteristicsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1081, 1)))

objectCharacteristicsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'size'), pyxb.binding.datatypes.long, scope=objectCharacteristicsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1112, 1)))

objectCharacteristicsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectCharacteristicsExtension'), extensionComplexType, scope=objectCharacteristicsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1138, 1)))

def _BuildAutomaton_24 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 656, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 657, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 658, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 660, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 661, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 662, 3))
    counters.add(cc_5)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(objectCharacteristicsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'compositionLevel')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 656, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(objectCharacteristicsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'fixity')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 657, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(objectCharacteristicsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'size')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 658, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(objectCharacteristicsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'format')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 659, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(objectCharacteristicsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'creatingApplication')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 660, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(objectCharacteristicsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'inhibitors')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 661, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(objectCharacteristicsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'objectCharacteristicsExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 662, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
objectCharacteristicsComplexType._Automaton = _BuildAutomaton_24()




objectIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifierValue'), pyxb.binding.datatypes.string, scope=objectIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 967, 1)))

objectIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifierType'), stringPlusAuthority, scope=objectIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1025, 1)))

def _BuildAutomaton_25 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(objectIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 671, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(objectIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 672, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
objectIdentifierComplexType._Automaton = _BuildAutomaton_25()




otherRightsDocumentationIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationIdentifierValue'), pyxb.binding.datatypes.string, scope=otherRightsDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 968, 1)))

otherRightsDocumentationIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationRole'), stringPlusAuthority, scope=otherRightsDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1027, 1)))

otherRightsDocumentationIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationIdentifierType'), stringPlusAuthority, scope=otherRightsDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1028, 1)))

def _BuildAutomaton_26 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_26
    del _BuildAutomaton_26
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 695, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(otherRightsDocumentationIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 693, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(otherRightsDocumentationIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 694, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(otherRightsDocumentationIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationRole')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 695, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
otherRightsDocumentationIdentifierComplexType._Automaton = _BuildAutomaton_26()




otherRightsInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsNote'), pyxb.binding.datatypes.string, scope=otherRightsInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 969, 1)))

otherRightsInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsBasis'), stringPlusAuthority, scope=otherRightsInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1026, 1)))

otherRightsInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationIdentifier'), otherRightsDocumentationIdentifierComplexType, scope=otherRightsInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1092, 1)))

otherRightsInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsApplicableDates'), startAndEndDateComplexType, scope=otherRightsInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1124, 1)))

def _BuildAutomaton_27 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_27
    del _BuildAutomaton_27
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 704, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 706, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 707, 3))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(otherRightsInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherRightsDocumentationIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 704, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(otherRightsInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherRightsBasis')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 705, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(otherRightsInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherRightsApplicableDates')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 706, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(otherRightsInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherRightsNote')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 707, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
otherRightsInformationComplexType._Automaton = _BuildAutomaton_27()




preservationLevelComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelRationale'), pyxb.binding.datatypes.string, scope=preservationLevelComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 970, 1)))

preservationLevelComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelType'), stringPlusAuthority, scope=preservationLevelComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1029, 4)))

preservationLevelComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelValue'), stringPlusAuthority, scope=preservationLevelComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1030, 3)))

preservationLevelComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelRole'), stringPlusAuthority, scope=preservationLevelComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1031, 1)))

preservationLevelComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelDateAssigned'), edtfSimpleType, scope=preservationLevelComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1122, 1)))

def _BuildAutomaton_28 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_28
    del _BuildAutomaton_28
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 718, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 721, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 722, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 723, 3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(preservationLevelComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 718, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(preservationLevelComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 720, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(preservationLevelComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelRole')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 721, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(preservationLevelComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelRationale')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 722, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(preservationLevelComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'preservationLevelDateAssigned')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 723, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
preservationLevelComplexType._Automaton = _BuildAutomaton_28()




relatedEventIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedEventIdentifierValue'), pyxb.binding.datatypes.string, scope=relatedEventIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 971, 1)))

relatedEventIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedEventIdentifierType'), stringPlusAuthority, scope=relatedEventIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1032, 4)))

relatedEventIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedEventSequence'), pyxb.binding.datatypes.nonNegativeInteger, scope=relatedEventIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1110, 1)))

def _BuildAutomaton_29 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_29
    del _BuildAutomaton_29
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 736, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(relatedEventIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relatedEventIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 734, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(relatedEventIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relatedEventIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 735, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(relatedEventIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relatedEventSequence')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 736, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
relatedEventIdentifierComplexType._Automaton = _BuildAutomaton_29()




relatedObjectIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectIdentifierValue'), pyxb.binding.datatypes.string, scope=relatedObjectIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 972, 1)))

relatedObjectIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectIdentifierType'), stringPlusAuthority, scope=relatedObjectIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1035, 1)))

relatedObjectIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectSequence'), pyxb.binding.datatypes.nonNegativeInteger, scope=relatedObjectIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1111, 1)))

def _BuildAutomaton_30 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_30
    del _BuildAutomaton_30
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 751, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(relatedObjectIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 749, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(relatedObjectIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 750, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(relatedObjectIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectSequence')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 751, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
relatedObjectIdentifierComplexType._Automaton = _BuildAutomaton_30()




relationshipComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedEnvironmentPurpose'), stringPlusAuthority, scope=relationshipComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1033, 1)))

relationshipComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedEnvironmentCharacteristic'), stringPlusAuthority, scope=relationshipComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1034, 4)))

relationshipComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relationshipType'), stringPlusAuthority, scope=relationshipComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1036, 1)))

relationshipComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relationshipSubType'), stringPlusAuthority, scope=relationshipComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1037, 1)))

relationshipComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedEventIdentifier'), relatedEventIdentifierComplexType, scope=relationshipComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1095, 1)))

relationshipComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectIdentifier'), relatedObjectIdentifierComplexType, scope=relationshipComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1096, 1)))

def _BuildAutomaton_31 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_31
    del _BuildAutomaton_31
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 768, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 773, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 774, 3))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(relationshipComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relationshipType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 761, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(relationshipComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relationshipSubType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 762, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(relationshipComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relatedObjectIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 767, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(relationshipComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relatedEventIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 768, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(relationshipComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relatedEnvironmentPurpose')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 773, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(relationshipComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relatedEnvironmentCharacteristic')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 774, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
relationshipComplexType._Automaton = _BuildAutomaton_31()




rightsGrantedComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsGrantedNote'), pyxb.binding.datatypes.string, scope=rightsGrantedComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 973, 1)))

rightsGrantedComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'act'), stringPlusAuthority, scope=rightsGrantedComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 988, 1)))

rightsGrantedComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'restriction'), stringPlusAuthority, scope=rightsGrantedComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1038, 1)))

rightsGrantedComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'termOfGrant'), startAndEndDateComplexType, scope=rightsGrantedComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1127, 1)))

rightsGrantedComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'termOfRestriction'), startAndEndDateComplexType, scope=rightsGrantedComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1128, 1)))

def _BuildAutomaton_32 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_32
    del _BuildAutomaton_32
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 784, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 786, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 787, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 789, 3))
    counters.add(cc_3)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(rightsGrantedComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'act')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 783, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(rightsGrantedComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'restriction')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 784, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(rightsGrantedComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'termOfGrant')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 786, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(rightsGrantedComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'termOfRestriction')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 787, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(rightsGrantedComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'rightsGrantedNote')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 789, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
rightsGrantedComplexType._Automaton = _BuildAutomaton_32()




rightsStatementComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsBasis'), stringPlusAuthority, scope=rightsStatementComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1039, 1)))

rightsStatementComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'copyrightInformation'), copyrightInformationComplexType, scope=rightsStatementComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1068, 1)))

rightsStatementComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'licenseInformation'), licenseInformationComplexType, scope=rightsStatementComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1083, 1)))

rightsStatementComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifier'), linkingAgentIdentifierComplexType, scope=rightsStatementComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1084, 1)))

rightsStatementComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifier'), linkingObjectIdentifierComplexType, scope=rightsStatementComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1087, 1)))

rightsStatementComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'otherRightsInformation'), otherRightsInformationComplexType, scope=rightsStatementComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1093, 1)))

rightsStatementComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsGranted'), rightsGrantedComplexType, scope=rightsStatementComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1098, 1)))

rightsStatementComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsStatementIdentifier'), rightsStatementIdentifierComplexType, scope=rightsStatementComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1100, 1)))

rightsStatementComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteInformation'), statuteInformationComplexType, scope=rightsStatementComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1105, 1)))

def _BuildAutomaton_33 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_33
    del _BuildAutomaton_33
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 799, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 800, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 801, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 802, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 803, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 804, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 805, 3))
    counters.add(cc_6)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(rightsStatementComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'rightsStatementIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 797, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(rightsStatementComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'rightsBasis')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 798, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(rightsStatementComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'copyrightInformation')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 799, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(rightsStatementComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'licenseInformation')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 800, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(rightsStatementComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'statuteInformation')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 801, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(rightsStatementComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'otherRightsInformation')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 802, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(rightsStatementComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'rightsGranted')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 803, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(rightsStatementComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 804, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(rightsStatementComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 805, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
rightsStatementComplexType._Automaton = _BuildAutomaton_33()




rightsStatementIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsStatementIdentifierValue'), pyxb.binding.datatypes.string, scope=rightsStatementIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 974, 1)))

rightsStatementIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsStatementIdentifierType'), stringPlusAuthority, scope=rightsStatementIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1040, 1)))

def _BuildAutomaton_34 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_34
    del _BuildAutomaton_34
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(rightsStatementIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'rightsStatementIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 814, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(rightsStatementIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'rightsStatementIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 815, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
rightsStatementIdentifierComplexType._Automaton = _BuildAutomaton_34()




signatureComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureProperties'), pyxb.binding.datatypes.string, scope=signatureComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 975, 1)))

signatureComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureValue'), pyxb.binding.datatypes.string, scope=signatureComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 976, 1)))

signatureComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureEncoding'), stringPlusAuthority, scope=signatureComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1041, 1)))

signatureComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureMethod'), stringPlusAuthority, scope=signatureComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1042, 1)))

signatureComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureValidationRules'), stringPlusAuthority, scope=signatureComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1043, 1)))

signatureComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signer'), stringPlusAuthority, scope=signatureComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1044, 1)))

signatureComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'keyInformation'), extensionComplexType, scope=signatureComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1137, 1)))

def _BuildAutomaton_35 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_35
    del _BuildAutomaton_35
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 826, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 830, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 831, 3))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(signatureComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'signatureEncoding')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 825, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(signatureComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'signer')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 826, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(signatureComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'signatureMethod')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 827, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(signatureComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'signatureValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 828, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(signatureComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'signatureValidationRules')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 829, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(signatureComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'signatureProperties')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 830, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(signatureComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'keyInformation')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 831, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
signatureComplexType._Automaton = _BuildAutomaton_35()




signatureInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signature'), signatureComplexType, scope=signatureInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1101, 1)))

signatureInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureInformationExtension'), extensionComplexType, scope=signatureInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1140, 1)))

def _BuildAutomaton_36 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_36
    del _BuildAutomaton_36
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 844, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(signatureInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'signature')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 843, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(signatureInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'signatureInformationExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 844, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(signatureInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'signatureInformationExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 847, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
signatureInformationComplexType._Automaton = _BuildAutomaton_36()




significantPropertiesComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesValue'), pyxb.binding.datatypes.string, scope=significantPropertiesComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 977, 1)))

significantPropertiesComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesType'), stringPlusAuthority, scope=significantPropertiesComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1045, 1)))

significantPropertiesComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesExtension'), extensionComplexType, scope=significantPropertiesComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1141, 1)))

def _BuildAutomaton_37 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_37
    del _BuildAutomaton_37
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 860, 4))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 861, 4))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 866, 4))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(significantPropertiesComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 859, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(significantPropertiesComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 860, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(significantPropertiesComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 861, 4))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(significantPropertiesComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 865, 4))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(significantPropertiesComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 866, 4))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(significantPropertiesComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'significantPropertiesExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 869, 6))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
significantPropertiesComplexType._Automaton = _BuildAutomaton_37()




startAndEndDateComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'endDate'), edtfSimpleType, scope=startAndEndDateComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1117, 1)))

startAndEndDateComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'startDate'), edtfSimpleType, scope=startAndEndDateComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1123, 1)))

def _BuildAutomaton_38 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_38
    del _BuildAutomaton_38
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 880, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(startAndEndDateComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'startDate')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 879, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(startAndEndDateComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'endDate')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 880, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
startAndEndDateComplexType._Automaton = _BuildAutomaton_38()




statuteDocumentationIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationIdentifierValue'), pyxb.binding.datatypes.string, scope=statuteDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 978, 1)))

statuteDocumentationIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationIdentifierType'), stringPlusAuthority, scope=statuteDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1048, 1)))

statuteDocumentationIdentifierComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationRole'), stringPlusAuthority, scope=statuteDocumentationIdentifierComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1049, 1)))

def _BuildAutomaton_39 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_39
    del _BuildAutomaton_39
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 891, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(statuteDocumentationIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationIdentifierType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 889, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(statuteDocumentationIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationIdentifierValue')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 890, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(statuteDocumentationIdentifierComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationRole')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 891, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
statuteDocumentationIdentifierComplexType._Automaton = _BuildAutomaton_39()




statuteInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteNote'), pyxb.binding.datatypes.string, scope=statuteInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 979, 1)))

statuteInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteCitation'), stringPlusAuthority, scope=statuteInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1047, 1)))

statuteInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteJurisdiction'), countryCode, scope=statuteInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1058, 1)))

statuteInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationIdentifier'), statuteDocumentationIdentifierComplexType, scope=statuteInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1104, 1)))

statuteInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteApplicableDates'), startAndEndDateComplexType, scope=statuteInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1125, 1)))

statuteInformationComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'statuteInformationDeterminationDate'), edtfSimpleType, scope=statuteInformationComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1126, 1)))

def _BuildAutomaton_40 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_40
    del _BuildAutomaton_40
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 902, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 903, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 904, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 905, 3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(statuteInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'statuteJurisdiction')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 900, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(statuteInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'statuteCitation')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 901, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(statuteInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'statuteInformationDeterminationDate')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 902, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(statuteInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'statuteNote')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 903, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(statuteInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'statuteDocumentationIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 904, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(statuteInformationComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'statuteApplicableDates')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 905, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
statuteInformationComplexType._Automaton = _BuildAutomaton_40()




storageComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'storageMedium'), stringPlusAuthority, scope=storageComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1046, 1)))

storageComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contentLocation'), contentLocationComplexType, scope=storageComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1065, 1)))

def _BuildAutomaton_41 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_41
    del _BuildAutomaton_41
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 917, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(storageComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'contentLocation')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 916, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(storageComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'storageMedium')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 917, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(storageComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'storageMedium')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 919, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
storageComplexType._Automaton = _BuildAutomaton_41()




def _BuildAutomaton_42 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_42
    del _BuildAutomaton_42
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1176, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
extensionComplexType._Automaton = _BuildAutomaton_42()




premisComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'object'), objectComplexType, scope=premisComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 67, 1)))

premisComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'event'), eventComplexType, scope=premisComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 68, 1)))

premisComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agent'), agentComplexType, scope=premisComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 69, 1)))

premisComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rights'), rightsComplexType, scope=premisComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 70, 1)))

def _BuildAutomaton_43 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_43
    del _BuildAutomaton_43
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 85, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 86, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 87, 3))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(premisComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'object')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 84, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(premisComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'event')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 85, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(premisComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'agent')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 86, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(premisComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'rights')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 87, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
premisComplexType._Automaton = _BuildAutomaton_43()




file._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier'), linkingEventIdentifierComplexType, scope=file, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1086, 4)))

file._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier'), linkingRightsStatementIdentifierComplexType, scope=file, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1088, 1)))

file._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectCharacteristics'), objectCharacteristicsComplexType, scope=file, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1089, 1)))

file._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifier'), objectIdentifierComplexType, scope=file, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1090, 1)))

file._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'originalName'), originalNameComplexType, scope=file, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1091, 1)))

file._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevel'), preservationLevelComplexType, scope=file, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1094, 1)))

file._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relationship'), relationshipComplexType, scope=file, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1097, 4)))

file._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureInformation'), signatureInformationComplexType, scope=file, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1102, 1)))

file._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'significantProperties'), significantPropertiesComplexType, scope=file, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1103, 1)))

file._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'storage'), storageComplexType, scope=file, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1106, 1)))

def _BuildAutomaton_44 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_44
    del _BuildAutomaton_44
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 124, 5))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 125, 5))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 127, 5))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 128, 5))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 129, 5))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 130, 5))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 131, 5))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 133, 5))
    counters.add(cc_7)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(file._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 118, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(file._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'preservationLevel')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 124, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(file._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'significantProperties')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 125, 5))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(file._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'objectCharacteristics')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 126, 5))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(file._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'originalName')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 127, 5))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(file._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'storage')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 128, 5))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(file._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'signatureInformation')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 129, 5))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(file._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relationship')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 130, 5))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(file._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 131, 5))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(file._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 133, 5))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
file._Automaton = _BuildAutomaton_44()




representation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier'), linkingEventIdentifierComplexType, scope=representation, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1086, 4)))

representation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier'), linkingRightsStatementIdentifierComplexType, scope=representation, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1088, 1)))

representation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifier'), objectIdentifierComplexType, scope=representation, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1090, 1)))

representation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'originalName'), originalNameComplexType, scope=representation, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1091, 1)))

representation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevel'), preservationLevelComplexType, scope=representation, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1094, 1)))

representation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relationship'), relationshipComplexType, scope=representation, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1097, 4)))

representation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'significantProperties'), significantPropertiesComplexType, scope=representation, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1103, 1)))

representation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'storage'), storageComplexType, scope=representation, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1106, 1)))

def _BuildAutomaton_45 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_45
    del _BuildAutomaton_45
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 148, 5))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 149, 5))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 150, 5))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 153, 8))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 157, 5))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 158, 5))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 160, 5))
    counters.add(cc_6)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(representation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 147, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(representation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'preservationLevel')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 148, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(representation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'significantProperties')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 149, 5))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(representation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'originalName')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 150, 5))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(representation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'storage')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 153, 8))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(representation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relationship')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 157, 5))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(representation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 158, 5))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(representation._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 160, 5))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
representation._Automaton = _BuildAutomaton_45()




bitstream._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier'), linkingEventIdentifierComplexType, scope=bitstream, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1086, 4)))

bitstream._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier'), linkingRightsStatementIdentifierComplexType, scope=bitstream, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1088, 1)))

bitstream._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectCharacteristics'), objectCharacteristicsComplexType, scope=bitstream, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1089, 1)))

bitstream._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifier'), objectIdentifierComplexType, scope=bitstream, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1090, 1)))

bitstream._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relationship'), relationshipComplexType, scope=bitstream, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1097, 4)))

bitstream._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'signatureInformation'), signatureInformationComplexType, scope=bitstream, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1102, 1)))

bitstream._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'significantProperties'), significantPropertiesComplexType, scope=bitstream, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1103, 1)))

bitstream._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'storage'), storageComplexType, scope=bitstream, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1106, 1)))

def _BuildAutomaton_46 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_46
    del _BuildAutomaton_46
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 175, 5))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 177, 5))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 179, 5))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 180, 5))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 181, 5))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 183, 5))
    counters.add(cc_5)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(bitstream._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 174, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(bitstream._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'significantProperties')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 175, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(bitstream._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'objectCharacteristics')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 176, 5))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(bitstream._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'storage')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 177, 5))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(bitstream._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'signatureInformation')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 179, 5))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(bitstream._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relationship')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 180, 5))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(bitstream._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 181, 5))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(bitstream._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 183, 5))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
bitstream._Automaton = _BuildAutomaton_46()




intellectualEntity._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentFunction'), environmentFunctionComplexType, scope=intellectualEntity, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1070, 4)))

intellectualEntity._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentDesignation'), environmentDesignationComplexType, scope=intellectualEntity, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1071, 4)))

intellectualEntity._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistry'), environmentRegistryComplexType, scope=intellectualEntity, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1072, 4)))

intellectualEntity._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier'), linkingEventIdentifierComplexType, scope=intellectualEntity, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1086, 4)))

intellectualEntity._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier'), linkingRightsStatementIdentifierComplexType, scope=intellectualEntity, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1088, 1)))

intellectualEntity._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifier'), objectIdentifierComplexType, scope=intellectualEntity, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1090, 1)))

intellectualEntity._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'originalName'), originalNameComplexType, scope=intellectualEntity, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1091, 1)))

intellectualEntity._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'preservationLevel'), preservationLevelComplexType, scope=intellectualEntity, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1094, 1)))

intellectualEntity._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'relationship'), relationshipComplexType, scope=intellectualEntity, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1097, 4)))

intellectualEntity._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'significantProperties'), significantPropertiesComplexType, scope=intellectualEntity, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1103, 1)))

intellectualEntity._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'environmentExtension'), extensionComplexType, scope=intellectualEntity, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1134, 1)))

def _BuildAutomaton_47 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_47
    del _BuildAutomaton_47
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 201, 20))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 202, 20))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 203, 20))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 207, 20))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 208, 20))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 209, 20))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 210, 20))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 212, 20))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 213, 20))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 214, 20))
    counters.add(cc_9)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(intellectualEntity._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'objectIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 200, 20))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(intellectualEntity._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'preservationLevel')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 201, 20))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(intellectualEntity._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'significantProperties')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 202, 20))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(intellectualEntity._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'originalName')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 203, 20))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(intellectualEntity._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentFunction')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 207, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(intellectualEntity._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentDesignation')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 208, 20))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(intellectualEntity._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentRegistry')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 209, 20))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(intellectualEntity._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'environmentExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 210, 20))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(intellectualEntity._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'relationship')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 212, 20))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(intellectualEntity._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 213, 20))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(intellectualEntity._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 214, 20))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, True) ]))
    st_10._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
intellectualEntity._Automaton = _BuildAutomaton_47()




eventComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventType'), stringPlusAuthority, scope=eventComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1004, 1)))

eventComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventDetailInformation'), eventDetailInformationComplexType, scope=eventComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1073, 4)))

eventComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventIdentifier'), eventIdentifierComplexType, scope=eventComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1074, 4)))

eventComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeInformation'), eventOutcomeInformationComplexType, scope=eventComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1076, 1)))

eventComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifier'), linkingAgentIdentifierComplexType, scope=eventComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1084, 1)))

eventComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifier'), linkingObjectIdentifierComplexType, scope=eventComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1087, 1)))

eventComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'eventDateTime'), pyxb.binding.datatypes.string, scope=eventComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1120, 1)))

def _BuildAutomaton_48 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_48
    del _BuildAutomaton_48
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 236, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 238, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 239, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 240, 3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 231, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(eventComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 232, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(eventComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventDateTime')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 233, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(eventComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventDetailInformation')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 236, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(eventComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'eventOutcomeInformation')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 238, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(eventComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingAgentIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 239, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(eventComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingObjectIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 240, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
eventComplexType._Automaton = _BuildAutomaton_48()




agentComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentNote'), pyxb.binding.datatypes.string, scope=agentComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 935, 1)))

agentComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentVersion'), pyxb.binding.datatypes.string, scope=agentComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 936, 4)))

agentComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentName'), stringPlusAuthority, scope=agentComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 990, 1)))

agentComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentType'), stringPlusAuthority, scope=agentComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 991, 1)))

agentComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentIdentifier'), agentIdentifierComplexType, scope=agentComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1064, 1)))

agentComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentIdentifier'), linkingEnvironmentIdentifierComplexType, scope=agentComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1085, 4)))

agentComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier'), linkingEventIdentifierComplexType, scope=agentComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1086, 4)))

agentComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier'), linkingRightsStatementIdentifierComplexType, scope=agentComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1088, 1)))

agentComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agentExtension'), extensionComplexType, scope=agentComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1132, 1)))

def _BuildAutomaton_49 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_49
    del _BuildAutomaton_49
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 252, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 253, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 256, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 258, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 259, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 260, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 261, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 264, 6))
    counters.add(cc_7)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(agentComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'agentIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 251, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(agentComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'agentName')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 252, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(agentComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'agentType')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 253, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(agentComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'agentVersion')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 256, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(agentComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'agentNote')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 258, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(agentComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'agentExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 259, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(agentComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingEventIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 260, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(agentComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingRightsStatementIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 261, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(agentComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'linkingEnvironmentIdentifier')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 264, 6))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
agentComplexType._Automaton = _BuildAutomaton_49()




rightsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsStatement'), rightsStatementComplexType, scope=rightsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1099, 1)))

rightsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsExtension'), extensionComplexType, scope=rightsComplexType, location=pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 1139, 1)))

def _BuildAutomaton_50 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_50
    del _BuildAutomaton_50
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(rightsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'rightsStatement')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 277, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(rightsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'rightsExtension')), pyxb.utils.utility.Location('/Users/cole/Projects/mets-reader-writer/metsrw/plugins/premisrw/premis3.xsd.txt', 278, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
rightsComplexType._Automaton = _BuildAutomaton_50()

