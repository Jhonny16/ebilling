# -*- coding: utf-8 -*-

from .MixedClass import GeneratedsSuper
from .MixedClass import showIndent
from .MixedClass import quote_xml
from .MixedClass import parsexml_
import re as re_
import sys

try:
    from lxml import etree as etree_
except ImportError:
    from xml.etree import ElementTree as etree_

Validate_simpletypes_ = True
if sys.version_info.major == 2:
    BaseStrType_ = basestring
else:
    BaseStrType_ = str

try:
    from generatedsnamespaces import GenerateDSNamespaceDefs as GenerateDSNamespaceDefs_
except ImportError:
    GenerateDSNamespaceDefs_ = {}

#
# Globals
#

ExternalEncoding = 'utf-8'
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')
CDATA_pattern_ = re_.compile(r"<!\[CDATA\[.*?\]\]>", re_.DOTALL)

# Change this to redirect the generated superclass module to use a
# specific subclass module.
CurrentSubclassModule_ = None


#
# Data representation classes.
#


class ReciboElectronicoPago(GeneratedsSuper):
    """Elemento Raiz de Recibo Electrónico de Pago"""
    subclass = None
    superclass = None

    def __init__(self, Clave, ProveedorSistemas, NumeroConsecutivo, FechaEmision, Emisor,
                 Receptor, CondicionVenta, CodigoActividadReceptor=None,
                 DetalleServicio=None,
                 OtrosCargos=None, ResumenFactura=None, InformacionReferencia=None, Otros=None):
        self.original_tagname_ = None
        self.Clave = Clave
        self.ProveedorSistemas = ProveedorSistemas
        self.CodigoActividadReceptor = CodigoActividadReceptor
        self.NumeroConsecutivo = NumeroConsecutivo
        if isinstance(FechaEmision, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(FechaEmision, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = FechaEmision
        self.FechaEmision = initvalue_
        self.Emisor = Emisor
        self.Receptor = Receptor
        self.CondicionVenta = CondicionVenta
        self.DetalleServicio = DetalleServicio
        if OtrosCargos is None:
            self.OtrosCargos = []
        else:
            self.OtrosCargos = OtrosCargos
        self.ResumenFactura = ResumenFactura
        if InformacionReferencia is None:
            self.InformacionReferencia = []
        else:
            self.InformacionReferencia = InformacionReferencia
        self.Otros = Otros

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReciboElectronicoPago)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReciboElectronicoPago.subclass:
            return ReciboElectronicoPago.subclass(*args_, **kwargs_)
        else:
            return ReciboElectronicoPago(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_Clave(self):
        return self.Clave

    def set_Clave(self, Clave):
        self.Clave = Clave

    def get_CodigoActividadReceptor(self):
        return self.CodigoActividadReceptor

    def set_CodigoActividadReceptor(self, CodigoActividadReceptor):
        self.CodigoActividadReceptor = CodigoActividadReceptor

    def get_ProveedorSistemas(self):
        return self.ProveedorSistemas

    def set_ProveedorSistemas(self, ProveedorSistemas):
        self.ProveedorSistemas = ProveedorSistemas

    def get_NumeroConsecutivo(self):
        return self.NumeroConsecutivo

    def set_NumeroConsecutivo(self, NumeroConsecutivo):
        self.NumeroConsecutivo = NumeroConsecutivo

    def get_FechaEmision(self):
        return self.FechaEmision

    def set_FechaEmision(self, FechaEmision):
        self.FechaEmision = FechaEmision

    def get_Emisor(self):
        return self.Emisor

    def set_Emisor(self, Emisor):
        self.Emisor = Emisor

    def get_Receptor(self):
        return self.Receptor

    def set_Receptor(self, Receptor):
        self.Receptor = Receptor

    def get_CondicionVenta(self):
        return self.CondicionVenta

    def set_CondicionVenta(self, CondicionVenta):
        self.CondicionVenta = CondicionVenta

    def get_DetalleServicio(self):
        return self.DetalleServicio

    def set_DetalleServicio(self, DetalleServicio):
        self.DetalleServicio = DetalleServicio

    def get_OtrosCargos(self):
        return self.OtrosCargos

    def set_OtrosCargos(self, OtrosCargos):
        self.OtrosCargos = OtrosCargos

    def add_OtrosCargos(self, value):
        self.OtrosCargos.append(value)

    def insert_OtrosCargos_at(self, index, value):
        self.OtrosCargos.insert(index, value)

    def replace_OtrosCargos_at(self, index, value):
        self.OtrosCargos[index] = value

    def get_ResumenFactura(self):
        return self.ResumenFactura

    def set_ResumenFactura(self, ResumenFactura):
        self.ResumenFactura = ResumenFactura

    def get_InformacionReferencia(self):
        return self.InformacionReferencia

    def set_InformacionReferencia(self, InformacionReferencia):
        self.InformacionReferencia = InformacionReferencia

    def add_InformacionReferencia(self, value):
        self.InformacionReferencia.append(value)

    def insert_InformacionReferencia_at(self, index, value):
        self.InformacionReferencia.insert(index, value)

    def replace_InformacionReferencia_at(self, index, value):
        self.InformacionReferencia[index] = value

    def get_Otros(self):
        return self.Otros

    def set_Otros(self, Otros):
        self.Otros = Otros

    def hasContent_(self):
        if (
                self.Clave is not None or
                self.CodigoActividadReceptor is not None or
                self.NumeroConsecutivo is not None or
                self.FechaEmision is not None or
                self.Emisor is not None or
                self.Receptor is not None or
                self.CondicionVenta is not None or
                self.DetalleServicio is not None or
                self.OtrosCargos or
                self.ResumenFactura is not None or
                self.InformacionReferencia or
                self.Otros is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='FacturaElectronica', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FacturaElectronica')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='FacturaElectronica')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='FacturaElectronica',
                                pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='FacturaElectronica'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='FacturaElectronica', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Clave is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Clave>%s</Clave>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Clave), input_name='Clave')), eol_)).encode()))
        if self.ProveedorSistemas is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<ProveedorSistemas>%s</ProveedorSistemas>%s' % (
                self.gds_encode(
                    self.gds_format_string(quote_xml(self.ProveedorSistemas), input_name='ProveedorSistemas')),
                eol_)).encode()))
        if self.CodigoActividadReceptor is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CodigoActividadReceptor>%s</CodigoActividadReceptor>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.CodigoActividadReceptor),
                                                       input_name='CodigoActividadReceptor')),
                eol_)).encode()))
        if self.NumeroConsecutivo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<NumeroConsecutivo>%s</NumeroConsecutivo>%s' % (
                self.gds_encode(
                    self.gds_format_string(quote_xml(self.NumeroConsecutivo), input_name='NumeroConsecutivo')),
                eol_)).encode()))
        if self.FechaEmision is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<FechaEmision>%s</FechaEmision>%s' % (
                self.gds_format_datetime(self.FechaEmision, input_name='FechaEmision'), eol_)).encode()))
        if self.Emisor is not None:
            self.Emisor.export(outfile, level, namespace_, name_='Emisor', pretty_print=pretty_print)
        if self.Receptor is not None:
            self.Receptor.export(outfile, level, namespace_, name_='Receptor', pretty_print=pretty_print)
        if self.CondicionVenta is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CondicionVenta>%s</CondicionVenta>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.CondicionVenta), input_name='CondicionVenta')),
                eol_)).encode()))
        if self.DetalleServicio is not None:
            self.DetalleServicio.export(outfile, level, namespace_, name_='DetalleServicio', pretty_print=pretty_print)
        for OtrosCargos_ in self.OtrosCargos:
            OtrosCargos_.export(outfile, level, namespace_, name_='OtrosCargos', pretty_print=pretty_print)
        if self.ResumenFactura is not None:
            self.ResumenFactura.export(outfile, level, namespace_, name_='ResumenFactura', pretty_print=pretty_print)
        for InformacionReferencia_ in self.InformacionReferencia:
            InformacionReferencia_.export(outfile, level, namespace_, name_='InformacionReferencia',
                                          pretty_print=pretty_print)
        if self.Otros is not None:
            self.Otros.export(outfile, level, namespace_, name_='Otros', pretty_print=pretty_print)

    def build(self, node):
        already_processed = set()
        # self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'Clave':
            Clave_ = child_.text
            # Clave_ = self.gds_validate_string(Clave_, node, 'Clave')
            self.Clave = Clave_
        elif nodeName_ == 'CodigoActividad':
            CodigoActividad_ = child_.text
            self.CodigoActividad = CodigoActividad_
        elif nodeName_ == 'NumeroConsecutivo':
            NumeroConsecutivo_ = child_.text
            self.NumeroConsecutivo = NumeroConsecutivo_
        elif nodeName_ == 'FechaEmision':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.FechaEmision = dval_
        elif nodeName_ == 'Emisor':
            obj_ = EmisorType.factory(Nombre=None, Identificacion=None, CorreoElectronico=None)
            obj_.build(child_)
            self.Emisor = obj_
            obj_.original_tagname_ = 'Emisor'
        elif nodeName_ == 'Receptor':
            obj_ = ReceptorType.factory(Nombre=None, Identificacion=None)
            obj_.build(child_)
            self.Receptor = obj_
            obj_.original_tagname_ = 'Receptor'
        elif nodeName_ == 'CondicionVenta':
            CondicionVenta_ = child_.text
            self.CondicionVenta = CondicionVenta_
        elif nodeName_ == 'DetalleServicio':
            obj_ = DetalleServicioType.factory()
            obj_.build(child_)
            self.DetalleServicio = obj_
            obj_.original_tagname_ = 'DetalleServicio'
        elif nodeName_ == 'OtrosCargos':
            obj_ = OtrosCargosType.factory(TipoDocumento=None, MontoCargo=None)
            obj_.build(child_)
            self.OtrosCargos.append(obj_)
            obj_.original_tagname_ = 'OtrosCargos'
        elif nodeName_ == 'ResumenFactura':
            obj_ = ResumenFacturaType.factory()
            obj_.build(child_)
            self.ResumenFactura = obj_
            obj_.original_tagname_ = 'ResumenFactura'
        elif nodeName_ == 'InformacionReferencia':
            obj_ = InformacionReferenciaType.factory()
            obj_.build(child_)
            self.InformacionReferencia.append(obj_)
            obj_.original_tagname_ = 'InformacionReferencia'
        # elif nodeName_ == 'Otros':
        #     obj_ = OtrosType.factory()
        #     obj_.build(child_)
        #     self.Otros = obj_
        #     obj_.original_tagname_ = 'Otros'


class EmisorType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Nombre, Identificacion, CorreoElectronico=None, Telefono=None):
        self.original_tagname_ = None
        self.Nombre = Nombre
        self.Identificacion = Identificacion
        self.Telefono = Telefono
        self.CorreoElectronico = CorreoElectronico

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EmisorType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EmisorType.subclass:
            return EmisorType.subclass(*args_, **kwargs_)
        else:
            return EmisorType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_Nombre(self):
        return self.Nombre

    def set_Nombre(self, Nombre):
        self.Nombre = Nombre

    def get_Identificacion(self):
        return self.Identificacion

    def set_Identificacion(self, Identificacion):
        self.Identificacion = Identificacion

    def get_Telefono(self):
        return self.Telefono

    def set_Telefono(self, Telefono):
        self.Telefono = Telefono

    def get_CorreoElectronico(self):
        return self.CorreoElectronico

    def set_CorreoElectronico(self, CorreoElectronico):
        self.CorreoElectronico = CorreoElectronico

    def hasContent_(self):
        if (
                self.Nombre is not None or
                self.Identificacion is not None or
                self.Telefono is not None or
                self.CorreoElectronico is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='EmisorType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EmisorType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='EmisorType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='EmisorType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='EmisorType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Nombre is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Nombre>%s</Nombre>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Nombre), input_name='Nombre')), eol_)).encode()))
        if self.Identificacion is not None:
            self.Identificacion.export(outfile, level, namespace_, name_='Identificacion', pretty_print=pretty_print)
        if self.Telefono is not None:
            self.Telefono.export(outfile, level, namespace_, name_='Telefono', pretty_print=pretty_print)
        if self.CorreoElectronico is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CorreoElectronico>%s</CorreoElectronico>%s' % (
                self.gds_encode(
                    self.gds_format_string(quote_xml(self.CorreoElectronico), input_name='CorreoElectronico')),
                eol_)).encode()))

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'Nombre':
            Nombre_ = child_.text
            Nombre_ = self.gds_validate_string(Nombre_, node, 'Nombre')
            self.Nombre = Nombre_
        elif nodeName_ == 'Identificacion':
            obj_ = IdentificacionType.factory()
            obj_.build(child_)
            self.Identificacion = obj_
            obj_.original_tagname_ = 'Identificacion'
        elif nodeName_ == 'Telefono':
            obj_ = TelefonoType.factory()
            obj_.build(child_)
            self.Telefono = obj_
            obj_.original_tagname_ = 'Telefono'
        elif nodeName_ == 'CorreoElectronico':
            CorreoElectronico_ = child_.text
            CorreoElectronico_ = self.gds_validate_string(CorreoElectronico_, node, 'CorreoElectronico')
            self.CorreoElectronico = CorreoElectronico_


class ReceptorType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Nombre, Identificacion, IdentificacionExtranjero=None,
                 OtrasSenasExtranjero=None, Telefono=None, CorreoElectronico=None):
        self.original_tagname_ = None
        self.Nombre = Nombre
        self.Identificacion = Identificacion
        self.IdentificacionExtranjero = IdentificacionExtranjero
        self.OtrasSenasExtranjero = OtrasSenasExtranjero
        self.Telefono = Telefono
        self.CorreoElectronico = CorreoElectronico

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReceptorType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReceptorType.subclass:
            return ReceptorType.subclass(*args_, **kwargs_)
        else:
            return ReceptorType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_Nombre(self):
        return self.Nombre

    def set_Nombre(self, Nombre):
        self.Nombre = Nombre

    def get_Identificacion(self):
        return self.Identificacion

    def set_Identificacion(self, Identificacion):
        self.Identificacion = Identificacion

    def get_IdentificacionExtranjero(self):
        return self.IdentificacionExtranjero

    def set_IdentificacionExtranjero(self, IdentificacionExtranjero):
        self.IdentificacionExtranjero = IdentificacionExtranjero

    def get_OtrasSenasExtranjero(self):
        return self.OtrasSenasExtranjero

    def set_OtrasSenasExtranjero(self, OtrasSenasExtranjero):
        self.OtrasSenasExtranjero = OtrasSenasExtranjero

    def get_Telefono(self):
        return self.Telefono

    def set_Telefono(self, Telefono):
        self.Telefono = Telefono

    def get_CorreoElectronico(self):
        return self.CorreoElectronico

    def set_CorreoElectronico(self, CorreoElectronico):
        self.CorreoElectronico = CorreoElectronico

    def hasContent_(self):
        if (
                self.Nombre is not None or
                self.Identificacion is not None or
                self.IdentificacionExtranjero is not None or
                self.OtrasSenasExtranjero is not None or
                self.Telefono is not None or
                self.CorreoElectronico is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='ReceptorType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReceptorType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='ReceptorType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='ReceptorType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='ReceptorType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='ReceptorType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Nombre is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Nombre>%s</Nombre>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Nombre), input_name='Nombre')), eol_)).encode()))
        if self.Identificacion is not None:
            self.Identificacion.export(outfile, level, namespace_, name_='Identificacion', pretty_print=pretty_print)
        if self.IdentificacionExtranjero is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<IdentificacionExtranjero>%s</IdentificacionExtranjero>%s' % (self.gds_encode(
                self.gds_format_string(quote_xml(self.IdentificacionExtranjero),
                                       input_name='IdentificacionExtranjero')), eol_)).encode()))
        if self.OtrasSenasExtranjero is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<OtrasSenasExtranjero>%s</OtrasSenasExtranjero>%s' % (self.gds_encode(
                self.gds_format_string(quote_xml(self.OtrasSenasExtranjero), input_name='OtrasSenasExtranjero')),
                                                                                        eol_)).encode()))
        if self.Telefono is not None:
            self.Telefono.export(outfile, level, namespace_, name_='Telefono', pretty_print=pretty_print)
        if self.CorreoElectronico is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CorreoElectronico>%s</CorreoElectronico>%s' % (
                self.gds_encode(
                    self.gds_format_string(quote_xml(self.CorreoElectronico), input_name='CorreoElectronico')),
                eol_)).encode()))

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'Nombre':
            Nombre_ = child_.text
            Nombre_ = self.gds_validate_string(Nombre_, node, 'Nombre')
            self.Nombre = Nombre_
        elif nodeName_ == 'Identificacion':
            obj_ = IdentificacionType.factory()
            obj_.build(child_)
            self.Identificacion = obj_
            obj_.original_tagname_ = 'Identificacion'
        elif nodeName_ == 'IdentificacionExtranjero':
            IdentificacionExtranjero_ = child_.text
            IdentificacionExtranjero_ = self.gds_validate_string(IdentificacionExtranjero_, node,
                                                                 'IdentificacionExtranjero')
            self.IdentificacionExtranjero = IdentificacionExtranjero_
        elif nodeName_ == 'OtrasSenasExtranjero':
            OtrasSenasExtranjero_ = child_.text
            OtrasSenasExtranjero_ = self.gds_validate_string(OtrasSenasExtranjero_, node, 'OtrasSenasExtranjero')
            self.OtrasSenasExtranjero = OtrasSenasExtranjero_
        elif nodeName_ == 'Telefono':
            obj_ = TelefonoType.factory()
            obj_.build(child_)
            self.Telefono = obj_
            obj_.original_tagname_ = 'Telefono'
        elif nodeName_ == 'CorreoElectronico':
            self.CorreoElectronico = child_.text


class IdentificacionType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Tipo=None, Numero=None):
        self.original_tagname_ = None
        self.Tipo = Tipo
        self.Numero = Numero

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, IdentificacionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if IdentificacionType.subclass:
            return IdentificacionType.subclass(*args_, **kwargs_)
        else:
            return IdentificacionType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_Tipo(self):
        return self.Tipo

    def set_Tipo(self, Tipo):
        self.Tipo = Tipo

    def get_Numero(self):
        return self.Numero

    def set_Numero(self, Numero):
        self.Numero = Numero

    def hasContent_(self):
        if (
                self.Tipo is not None or
                self.Numero is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='IdentificacionType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('IdentificacionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='IdentificacionType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='IdentificacionType',
                                pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='IdentificacionType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='IdentificacionType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Tipo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Tipo>%s</Tipo>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Tipo), input_name='Tipo')), eol_)).encode()))
        if self.Numero is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Numero>%s</Numero>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Numero), input_name='Numero')), eol_)).encode()))

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'Tipo':
            Tipo_ = child_.text
            Tipo_ = self.gds_validate_string(Tipo_, node, 'Tipo')
            self.Tipo = Tipo_
        elif nodeName_ == 'Numero':
            Numero_ = child_.text
            Numero_ = self.gds_validate_string(Numero_, node, 'Numero')
            self.Numero = Numero_


class TelefonoType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, CodigoPais=None, NumTelefono=None):
        self.original_tagname_ = None
        self.CodigoPais = CodigoPais
        self.NumTelefono = NumTelefono

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TelefonoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TelefonoType.subclass:
            return TelefonoType.subclass(*args_, **kwargs_)
        else:
            return TelefonoType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_CodigoPais(self):
        return self.CodigoPais

    def set_CodigoPais(self, CodigoPais):
        self.CodigoPais = CodigoPais

    def get_NumTelefono(self):
        return self.NumTelefono

    def set_NumTelefono(self, NumTelefono):
        self.NumTelefono = NumTelefono

    def hasContent_(self):
        if (
                self.CodigoPais is not None or
                self.NumTelefono is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='TelefonoType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TelefonoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='TelefonoType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='TelefonoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='TelefonoType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='TelefonoType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CodigoPais is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CodigoPais>%s</CodigoPais>%s' % (
                self.gds_format_integer(self.CodigoPais, input_name='CodigoPais'), eol_)).encode()))
        if self.NumTelefono is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<NumTelefono>%s</NumTelefono>%s' % (
                self.gds_format_integer(self.NumTelefono, input_name='NumTelefono'), eol_)).encode()))

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'CodigoPais':
            self.CodigoPais = child_.text
        elif nodeName_ == 'NumTelefono':
            self.NumTelefono = child_.text


class ImpuestoType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Codigo=None, CodigoTarifaIVA=None, Tarifa=None, FactorIVA=None, Monto=None,
                 indicator_prod_service=None):
        self.original_tagname_ = None
        self.Codigo = Codigo
        self.CodigoTarifaIVA = CodigoTarifaIVA
        self.Tarifa = Tarifa
        self.FactorIVA = FactorIVA
        self.Monto = Monto
        self.indicator_prod_service = indicator_prod_service

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ImpuestoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ImpuestoType.subclass:
            return ImpuestoType.subclass(*args_, **kwargs_)
        else:
            return ImpuestoType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_Codigo(self):
        return self.Codigo

    def set_Codigo(self, Codigo):
        self.Codigo = Codigo

    def get_CodigoTarifaIVA(self):
        return self.CodigoTarifaIVA

    def set_CodigoTarifaIVA(self, CodigoTarifaIVA):
        self.CodigoTarifaIVA = CodigoTarifaIVA

    def get_Tarifa(self):
        return self.Tarifa

    def set_Tarifa(self, Tarifa):
        self.Tarifa = Tarifa

    def get_FactorIVA(self):
        return self.FactorIVA

    def set_FactorIVA(self, FactorIVA):
        self.FactorIVA = FactorIVA

    def get_Monto(self):
        return self.Monto

    def set_Monto(self, Monto):
        self.Monto = Monto

    def hasContent_(self):
        if (
                self.Codigo is not None or
                self.CodigoTarifaIVA is not None or
                self.Tarifa is not None or
                self.FactorIVA is not None or
                self.Monto is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='ImpuestoType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ImpuestoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='ImpuestoType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='ImpuestoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='ImpuestoType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='ImpuestoType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Codigo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Codigo>%s</Codigo>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Codigo), input_name='Codigo')), eol_)).encode()))
        if self.CodigoTarifaIVA is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CodigoTarifaIVA>%s</CodigoTarifaIVA>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.CodigoTarifaIVA), input_name='CodigoTarifaIVA')),
                eol_)).encode()))
        if self.Tarifa is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Tarifa>%s</Tarifa>%s' % (
                self.gds_format_float(self.Tarifa, input_name='Tarifa', digits=2), eol_)).encode()))
        if self.FactorIVA is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<FactorIVA>%s</FactorIVA>%s' % (
                self.gds_format_float(self.FactorIVA, input_name='FactorIVA'), eol_)).encode()))
        if self.Monto is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(('<Monto>%s</Monto>%s' % (self.gds_format_float(self.Monto, input_name='Monto'), eol_)).encode()))

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'Codigo':
            self.Codigo = child_.text
        elif nodeName_ == 'CodigoTarifa':
            self.CodigoTarifa = child_.text
        elif nodeName_ == 'Tarifa':
            self.Tarifa = child_.text
        elif nodeName_ == 'FactorIVA':
            self.FactorIVA = child_.text
        elif nodeName_ == 'Monto':
            self.Monto = child_.text


class OtrosCargosType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, TipoDocumento, MontoCargo, NumeroIdentidadTercero=None, NombreTercero=None, Detalle=None,
                 Porcentaje=None):
        self.original_tagname_ = None
        self.TipoDocumento = TipoDocumento
        self.NumeroIdentidadTercero = NumeroIdentidadTercero
        self.NombreTercero = NombreTercero
        self.Detalle = Detalle
        self.Porcentaje = Porcentaje
        self.MontoCargo = MontoCargo

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OtrosCargosType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OtrosCargosType.subclass:
            return OtrosCargosType.subclass(*args_, **kwargs_)
        else:
            return OtrosCargosType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_TipoDocumento(self):
        return self.TipoDocumento

    def set_TipoDocumento(self, TipoDocumento):
        self.TipoDocumento = TipoDocumento

    def get_NumeroIdentidadTercero(self):
        return self.NumeroIdentidadTercero

    def set_NumeroIdentidadTercero(self, NumeroIdentidadTercero):
        self.NumeroIdentidadTercero = NumeroIdentidadTercero

    def get_NombreTercero(self):
        return self.NombreTercero

    def set_NombreTercero(self, NombreTercero):
        self.NombreTercero = NombreTercero

    def get_Detalle(self):
        return self.Detalle

    def set_Detalle(self, Detalle):
        self.Detalle = Detalle

    def get_Porcentaje(self):
        return self.Porcentaje

    def set_Porcentaje(self, Porcentaje):
        self.Porcentaje = Porcentaje

    def get_MontoCargo(self):
        return self.MontoCargo

    def set_MontoCargo(self, MontoCargo):
        self.MontoCargo = MontoCargo

    def hasContent_(self):
        if (
                self.TipoDocumento is not None or
                self.NumeroIdentidadTercero is not None or
                self.NombreTercero is not None or
                self.Detalle is not None or
                self.Porcentaje is not None or
                self.MontoCargo is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='OtrosCargosType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OtrosCargosType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='OtrosCargosType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='OtrosCargosType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='OtrosCargosType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='OtrosCargosType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TipoDocumento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TipoDocumento>%s</TipoDocumento>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.TipoDocumento), input_name='TipoDocumento')),
                eol_)).encode()))
        if self.NumeroIdentidadTercero is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<NumeroIdentidadTercero>%s</NumeroIdentidadTercero>%s' % (self.gds_encode(
                self.gds_format_string(quote_xml(self.NumeroIdentidadTercero), input_name='NumeroIdentidadTercero')),
                                                                                            eol_)).encode()))
        if self.NombreTercero is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<NombreTercero>%s</NombreTercero>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.NombreTercero), input_name='NombreTercero')),
                eol_)).encode()))
        if self.Detalle is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Detalle>%s</Detalle>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Detalle), input_name='Detalle')),
                eol_)).encode()))
        if self.Porcentaje is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Porcentaje>%s</Porcentaje>%s' % (
                self.gds_format_float(self.Porcentaje, input_name='Porcentaje'), eol_)).encode()))
        if self.MontoCargo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<MontoCargo>%s</MontoCargo>%s' % (
                self.gds_format_float(self.MontoCargo, input_name='MontoCargo'), eol_)).encode()))

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'TipoDocumento':
            self.TipoDocumento = child_.text
        elif nodeName_ == 'Detalle':
            self.Detalle = child_.text
        elif nodeName_ == 'Porcentaje':
            self.Porcentaje = child_.text
        elif nodeName_ == 'MontoCargo':
            self.MontoCargo = child_.text


class CodigoMonedaType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, CodigoMoneda=None, TipoCambio=None):
        self.original_tagname_ = None
        self.CodigoMoneda = CodigoMoneda
        self.TipoCambio = TipoCambio

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CodigoMonedaType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CodigoMonedaType.subclass:
            return CodigoMonedaType.subclass(*args_, **kwargs_)
        else:
            return CodigoMonedaType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_CodigoMoneda(self):
        return self.CodigoMoneda

    def set_CodigoMoneda(self, CodigoMoneda):
        self.CodigoMoneda = CodigoMoneda

    def get_TipoCambio(self):
        return self.TipoCambio

    def set_TipoCambio(self, TipoCambio):
        self.TipoCambio = TipoCambio

    def hasContent_(self):
        if (
                self.CodigoMoneda is not None or
                self.TipoCambio is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='CodigoMonedaType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CodigoMonedaType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='CodigoMonedaType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='CodigoMonedaType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='CodigoMonedaType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='CodigoMonedaType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CodigoMoneda is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CodigoMoneda>%s</CodigoMoneda>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.CodigoMoneda), input_name='CodigoMoneda')),
                eol_)).encode()))
        if self.TipoCambio is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TipoCambio>%s</TipoCambio>%s' % (
                self.gds_format_float(self.TipoCambio, input_name='TipoCambio'), eol_)).encode()))

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'CodigoMoneda':
            self.CodigoMoneda = child_.text
        elif nodeName_ == 'TipoCambio':
            self.TipoCambio = child_.text


class DetalleServicioType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, LineaDetalle=None):
        self.original_tagname_ = None
        if LineaDetalle is None:
            self.LineaDetalle = []
        else:
            self.LineaDetalle = LineaDetalle

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DetalleServicioType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DetalleServicioType.subclass:
            return DetalleServicioType.subclass(*args_, **kwargs_)
        else:
            return DetalleServicioType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_LineaDetalle(self):
        return self.LineaDetalle

    def set_LineaDetalle(self, LineaDetalle):
        self.LineaDetalle = LineaDetalle

    def add_LineaDetalle(self, value):
        self.LineaDetalle.append(value)

    def insert_LineaDetalle_at(self, index, value):
        self.LineaDetalle.insert(index, value)

    def replace_LineaDetalle_at(self, index, value):
        self.LineaDetalle[index] = value

    def hasContent_(self):
        if (
                self.LineaDetalle
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='DetalleServicioType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DetalleServicioType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='DetalleServicioType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='DetalleServicioType',
                                pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='DetalleServicioType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='DetalleServicioType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for LineaDetalle_ in self.LineaDetalle:
            LineaDetalle_.export(outfile, level, namespace_, name_='LineaDetalle', pretty_print=pretty_print)

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'LineaDetalle':
            obj_ = LineaDetalleType.factory(NumeroLinea=None, Codigo=None, Cantidad=None)
            obj_.build(child_)
            self.LineaDetalle.append(obj_)
            obj_.original_tagname_ = 'LineaDetalle'


class LineaDetalleType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, NumeroLinea, Detalle=None,
                 MontoTotal=0.00, SubTotal=None,
                 Impuesto=None, ImpuestoNeto=None, MontoTotalLinea=None):
        self.original_tagname_ = None
        self.NumeroLinea = NumeroLinea
        self.Detalle = Detalle
        self.MontoTotal = MontoTotal
        self.SubTotal = SubTotal
        if Impuesto is None:
            self.Impuesto = []
        else:
            self.Impuesto = Impuesto
        self.ImpuestoNeto = ImpuestoNeto
        self.MontoTotalLinea = MontoTotalLinea

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LineaDetalleType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LineaDetalleType.subclass:
            return LineaDetalleType.subclass(*args_, **kwargs_)
        else:
            return LineaDetalleType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_NumeroLinea(self):
        return self.NumeroLinea

    def set_NumeroLinea(self, NumeroLinea):
        self.NumeroLinea = NumeroLinea

    def set_UnidadMedida(self, UnidadMedida):
        self.UnidadMedida = UnidadMedida

    def get_Detalle(self):
        return self.Detalle

    def set_Detalle(self, Detalle):
        self.Detalle = Detalle

    def get_MontoTotal(self):
        return self.MontoTotal

    def set_MontoTotal(self, MontoTotal):
        self.MontoTotal = MontoTotal

    def get_SubTotal(self):
        return self.SubTotal

    def set_SubTotal(self, SubTotal):
        self.SubTotal = SubTotal

    def get_Impuesto(self):
        return self.Impuesto

    def set_Impuesto(self, Impuesto):
        self.Impuesto = Impuesto

    def add_Impuesto(self, value):
        self.Impuesto.append(value)

    def insert_Impuesto_at(self, index, value):
        self.Impuesto.insert(index, value)

    def replace_Impuesto_at(self, index, value):
        self.Impuesto[index] = value

    def get_ImpuestoNeto(self):
        return self.ImpuestoNeto

    def set_ImpuestoNeto(self, ImpuestoNeto):
        self.ImpuestoNeto = ImpuestoNeto

    def get_MontoTotalLinea(self):
        return self.MontoTotalLinea

    def set_MontoTotalLinea(self, MontoTotalLinea):
        self.MontoTotalLinea = MontoTotalLinea

    def hasContent_(self):
        if (
                self.NumeroLinea is not None or
                self.Detalle is not None or
                self.MontoTotal is not None or
                self.SubTotal is not None or
                self.Impuesto or
                self.ImpuestoNeto is not None or
                self.MontoTotalLinea is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='LineaDetalleType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LineaDetalleType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='LineaDetalleType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='LineaDetalleType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='LineaDetalleType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='LineaDetalleType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NumeroLinea is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<NumeroLinea>%s</NumeroLinea>%s' % (
                self.gds_format_integer(self.NumeroLinea, input_name='NumeroLinea'), eol_)).encode()))
        if self.Detalle is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Detalle>%s</Detalle>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Detalle), input_name='Detalle')),
                eol_)).encode()))
        if self.MontoTotal is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<MontoTotal>%s</MontoTotal>%s' % (
                self.gds_format_float(self.MontoTotal, input_name='MontoTotal'), eol_)).encode()))
        if self.SubTotal is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<SubTotal>%s</SubTotal>%s' % (
                self.gds_format_float(self.SubTotal, input_name='SubTotal'), eol_)).encode()))
        for Impuesto_ in self.Impuesto:
            Impuesto_.export(outfile, level, namespace_, name_='Impuesto', pretty_print=pretty_print)
        if self.ImpuestoNeto is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<ImpuestoNeto>%s</ImpuestoNeto>%s' % (
                self.gds_format_float(self.ImpuestoNeto, input_name='ImpuestoNeto'), eol_)).encode()))
        if self.MontoTotalLinea is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<MontoTotalLinea>%s</MontoTotalLinea>%s' % (
                self.gds_format_float(self.MontoTotalLinea, input_name='MontoTotalLinea'), eol_)).encode()))

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'NumeroLinea':
            self.NumeroLinea = child_.text
        elif nodeName_ == 'Codigo':
            self.Codigo = child_.text
        elif nodeName_ == 'Detalle':
            self.Detalle = child_.text
        elif nodeName_ == 'MontoTotal':
            self.MontoTotal = child_.text
        elif nodeName_ == 'SubTotal':
            self.SubTotal = child_.text
        elif nodeName_ == 'Impuesto':
            obj_ = ImpuestoType.factory()
            obj_.build(child_)
            self.Impuesto.append(obj_)
            obj_.original_tagname_ = 'Impuesto'
        elif nodeName_ == 'ImpuestoNeto':
            self.ImpuestoNeto = child_.text
        elif nodeName_ == 'MontoTotalLinea':
            self.MontoTotalLinea = child_.text


class ResumenFacturaType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, CodigoTipoMoneda=None, TotalVenta=None, TotalVentaNeta=None,
                 TotalImpuesto=0.00, TotalIVADevuelto=None, TotalComprobante=None,
                 TotalDesgloseImpuesto=None, MedioPago=None):
        self.original_tagname_ = None
        self.CodigoTipoMoneda = CodigoTipoMoneda
        self.TotalVenta = TotalVenta
        self.TotalImpuesto = TotalImpuesto
        self.TotalIVADevuelto = TotalIVADevuelto
        if MedioPago is None:
            self.MedioPago = []
        else:
            self.MedioPago = MedioPago
        self.TotalComprobante = TotalComprobante
        self.TotalVentaNeta = TotalVentaNeta
        if TotalDesgloseImpuesto is None:
            self.TotalDesgloseImpuesto = []
        else:
            self.TotalDesgloseImpuesto = TotalDesgloseImpuesto

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ResumenFacturaType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ResumenFacturaType.subclass:
            return ResumenFacturaType.subclass(*args_, **kwargs_)
        else:
            return ResumenFacturaType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_CodigoTipoMoneda(self):
        return self.CodigoTipoMoneda

    def set_CodigoTipoMoneda(self, CodigoTipoMoneda):
        self.CodigoTipoMoneda = CodigoTipoMoneda

    def get_TotalVenta(self):
        return self.TotalVenta

    def set_TotalVenta(self, TotalVenta):
        self.TotalVenta = TotalVenta

    def get_TotalVentaNeta(self):
        return self.TotalVentaNeta

    def set_TotalVentaNeta(self, TotalVentaNeta):
        self.TotalVentaNeta = TotalVentaNeta

    def get_TotalImpuesto(self):
        return self.TotalImpuesto

    def set_TotalImpuesto(self, TotalImpuesto):
        self.TotalImpuesto = TotalImpuesto

    def get_TotalIVADevuelto(self):
        return self.TotalIVADevuelto

    def set_TotalIVADevuelto(self, TotalIVADevuelto):
        self.TotalIVADevuelto = TotalIVADevuelto

    def get_MedioPago(self):
        return self.MedioPago

    def set_MedioPago(self, MedioPago):
        self.MedioPago = MedioPago

    def add_MedioPago(self, value):
        self.MedioPago.append(value)

    def insert_MedioPago_at(self, index, value):
        self.MedioPago.insert(index, value)

    def replace_MedioPago_at(self, index, value):
        self.MedioPago[index] = value

    def get_TotalComprobante(self):
        return self.TotalComprobante

    def set_TotalComprobante(self, TotalComprobante):
        self.TotalComprobante = TotalComprobante

    def get_TotalDesgloseImpuesto(self):
        return self.TotalDesgloseImpuesto

    def set_TotalDesgloseImpuesto(self, TotalDesgloseImpuesto):
        self.TotalDesgloseImpuesto = TotalDesgloseImpuesto

    def add_TotalDesgloseImpuesto(self, value):
        self.TotalDesgloseImpuesto.append(value)

    def insert_TotalDesgloseImpuesto_at(self, index, value):
        self.TotalDesgloseImpuesto.insert(index, value)

    def replace_TotalDesgloseImpuesto_at(self, index, value):
        self.TotalDesgloseImpuesto[index] = value

    def hasContent_(self):
        if (
                self.CodigoTipoMoneda is not None or
                self.TotalVenta is not None or
                self.TotalVentaNeta is not None or
                self.TotalImpuesto is not None or
                self.TotalIVADevuelto is not None or
                self.MedioPago or
                self.TotalComprobante is not None or
                self.TotalDesgloseImpuesto is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='ResumenFacturaType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ResumenFacturaType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='ResumenFacturaType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='ResumenFacturaType',
                                pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='ResumenFacturaType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='ResumenFacturaType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CodigoTipoMoneda is not None:
            self.CodigoTipoMoneda.export(outfile, level, namespace_, name_='CodigoTipoMoneda',
                                         pretty_print=pretty_print)
        if self.TotalVenta is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalVenta>%s</TotalVenta>%s' % (
                self.gds_format_float(self.TotalVenta, input_name='TotalVenta'), eol_)).encode()))
        if self.TotalVentaNeta is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalVentaNeta>%s</TotalVentaNeta>%s' % (
                self.gds_format_float(self.TotalVentaNeta, input_name='TotalVentaNeta'), eol_)).encode()))
        for TotalDesgloseImpuesto_ in self.TotalDesgloseImpuesto:
            TotalDesgloseImpuesto_.export(outfile, level, namespace_, name_='TotalDesgloseImpuesto',
                                          pretty_print=pretty_print)
        if self.TotalImpuesto is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalImpuesto>%s</TotalImpuesto>%s' % (
                self.gds_format_float(self.TotalImpuesto, input_name='TotalImpuesto'), eol_)).encode()))
        if self.TotalIVADevuelto is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalIVADevuelto>%s</TotalIVADevuelto>%s' % (
                self.gds_format_float(self.TotalIVADevuelto, input_name='TotalIVADevuelto'), eol_)).encode()))
        for MedioPago_ in self.MedioPago:
            MedioPago_.export(outfile, level, namespace_, name_='MedioPago',
                              pretty_print=pretty_print)
        if self.TotalComprobante is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalComprobante>%s</TotalComprobante>%s' % (
                self.gds_format_float(self.TotalComprobante, input_name='TotalComprobante'), eol_)).encode()))

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'CodigoTipoMoneda':
            obj_ = CodigoMonedaType.factory()
            obj_.build(child_)
            self.CodigoTipoMoneda = obj_
            obj_.original_tagname_ = 'CodigoTipoMoneda'
        elif nodeName_ == 'TotalServGravados':
            self.TotalServGravados = child_.text
        elif nodeName_ == 'TotalServExentos':
            self.TotalServExentos = child_.text
        elif nodeName_ == 'TotalMercanciasGravadas':
            self.TotalMercanciasGravadas = child_.text
        elif nodeName_ == 'TotalMercanciasExentas':
            self.TotalMercanciasExentas = child_.text
        elif nodeName_ == 'TotalGravado':
            self.TotalGravado = child_.text
        elif nodeName_ == 'TotalExento':
            self.TotalExento = child_.text
        elif nodeName_ == 'TotalVenta':
            self.TotalVenta = child_.text
        elif nodeName_ == 'TotalVentaNeta':
            self.TotalVentaNeta = child_.text
        elif nodeName_ == 'TotalImpuesto':
            self.TotalImpuesto = child_.text
        elif nodeName_ == 'TotalIVADevuelto':
            self.TotalIVADevuelto = child_.text
        elif nodeName_ == 'TotalOtrosCargos':
            self.TotalOtrosCargos = child_.text
        elif nodeName_ == 'TotalComprobante':
            self.TotalComprobante = child_.text


class TotalDesgloseImpuesto(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Codigo, CodigoTarifaIVA=None, TotalMontoImpuesto=None):
        self.original_tagname_ = None
        self.Codigo = Codigo
        self.CodigoTarifaIVA = CodigoTarifaIVA
        self.TotalMontoImpuesto = TotalMontoImpuesto

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ResumenFacturaType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ResumenFacturaType.subclass:
            return ResumenFacturaType.subclass(*args_, **kwargs_)
        else:
            return ResumenFacturaType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_Codigo(self):
        return self.Codigo

    def set_Codigo(self, Codigo):
        self.Codigo = Codigo

    def get_CodigoTarifaIVA(self):
        return self.CodigoTarifaIVA

    def set_CodigoTarifaIVA(self, CodigoTarifaIVA):
        self.CodigoTarifaIVA = CodigoTarifaIVA

    def get_TotalMontoImpuesto(self):
        return self.TotalMontoImpuesto

    def set_TotalMontoImpuesto(self, TotalMontoImpuesto):
        self.TotalMontoImpuesto = TotalMontoImpuesto

    def hasContent_(self):
        if (
                self.Codigo is not None or
                self.CodigoTarifaIVA is not None or
                self.TotalMontoImpuesto is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='ResumenFacturaType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ResumenFacturaType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='ResumenFacturaType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='ResumenFacturaType',
                                pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='ResumenFacturaType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='ResumenFacturaType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Codigo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Codigo>%s</Codigo>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Codigo), input_name='Codigo')), eol_)).encode()))
        if self.CodigoTarifaIVA is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CodigoTarifaIVA>%s</CodigoTarifaIVA>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.CodigoTarifaIVA), input_name='CodigoTarifaIVA')),
                eol_)).encode()))
        if self.TotalMontoImpuesto is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalMontoImpuesto>%s</TotalMontoImpuesto>%s' % (
                self.gds_format_float(self.TotalMontoImpuesto, input_name='TotalMontoImpuesto'), eol_)).encode()))

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        pass


class MedioPago(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, TipoMedioPago=None, TotalMedioPago=None):
        self.original_tagname_ = None
        self.TipoMedioPago = TipoMedioPago
        self.TotalMedioPago = TotalMedioPago

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ResumenFacturaType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ResumenFacturaType.subclass:
            return ResumenFacturaType.subclass(*args_, **kwargs_)
        else:
            return ResumenFacturaType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_TipoMedioPago(self):
        return self.TipoMedioPago

    def set_TipoMedioPago(self, TipoMedioPago):
        self.TipoMedioPago = TipoMedioPago

    def get_TotalMedioPago(self):
        return self.TotalMedioPago

    def set_TotalMedioPago(self, TotalMedioPago):
        self.TotalMedioPago = TotalMedioPago

    def hasContent_(self):
        if (
                self.TipoMedioPago is not None or
                self.TotalMedioPago is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='ResumenFacturaType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ResumenFacturaType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='ResumenFacturaType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='ResumenFacturaType',
                                pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='ResumenFacturaType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='ResumenFacturaType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TipoMedioPago is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TipoMedioPago>%s</TipoMedioPago>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.TipoMedioPago), input_name='TipoMedioPago')), eol_)).encode()))
        if self.TotalMedioPago is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalMedioPago>%s</TotalMedioPago>%s' % (
                self.gds_format_float(self.TotalMedioPago, input_name='TotalMedioPago'), eol_)).encode()))

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        pass


class InformacionReferenciaType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, TipoDoc=None, Numero=None, FechaEmision=None, Codigo=None, Razon=None):
        self.original_tagname_ = None
        self.TipoDoc = TipoDoc
        self.Numero = Numero
        if isinstance(FechaEmision, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(FechaEmision, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = FechaEmision
        self.FechaEmision = initvalue_
        self.Codigo = Codigo
        self.Razon = Razon

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, InformacionReferenciaType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if InformacionReferenciaType.subclass:
            return InformacionReferenciaType.subclass(*args_, **kwargs_)
        else:
            return InformacionReferenciaType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_TipoDoc(self):
        return self.TipoDoc

    def set_TipoDoc(self, TipoDoc):
        self.TipoDoc = TipoDoc

    def get_Numero(self):
        return self.Numero

    def set_Numero(self, Numero):
        self.Numero = Numero

    def get_FechaEmision(self):
        return self.FechaEmision

    def set_FechaEmision(self, FechaEmision):
        self.FechaEmision = FechaEmision

    def get_Codigo(self):
        return self.Codigo

    def set_Codigo(self, Codigo):
        self.Codigo = Codigo

    def get_Razon(self):
        return self.Razon

    def set_Razon(self, Razon):
        self.Razon = Razon

    def hasContent_(self):
        if (
                self.TipoDoc is not None or
                self.Numero is not None or
                self.FechaEmision is not None or
                self.Codigo is not None or
                self.Razon is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='InformacionReferenciaType', namespacedef_='',
               pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('InformacionReferenciaType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='InformacionReferenciaType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='InformacionReferenciaType',
                                pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='InformacionReferenciaType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='InformacionReferenciaType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TipoDoc is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TipoDocIR>%s</TipoDocIR>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.TipoDoc), input_name='TipoDoc')),
                eol_)).encode()))
        if self.Numero is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Numero>%s</Numero>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Numero), input_name='Numero')), eol_)).encode()))
        if self.FechaEmision is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<FechaEmisionIR>%s</FechaEmisionIR>%s' % (
                self.gds_format_datetime(self.FechaEmision, input_name='FechaEmision'), eol_)).encode()))
        if self.Codigo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Codigo>%s</Codigo>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Codigo), input_name='Codigo')), eol_)).encode()))
        if self.Razon is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Razon>%s</Razon>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Razon), input_name='Razon')), eol_)).encode()))

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'TipoDoc':
            self.TipoDoc = child_.text
        elif nodeName_ == 'Numero':
            self.Numero = child_.text
        elif nodeName_ == 'FechaEmision':
            self.FechaEmision = child_.text
        elif nodeName_ == 'Codigo':
            self.Codigo = child_.text
        elif nodeName_ == 'Razon':
            self.Razon = child_.text


class OtrosType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, OtroTexto=None, OtroContenido=None):
        self.original_tagname_ = None
        if OtroTexto is None:
            self.OtroTexto = []
        else:
            self.OtroTexto = OtroTexto
        if OtroContenido is None:
            self.OtroContenido = []
        else:
            self.OtroContenido = OtroContenido

    def get_OtroTexto(self):
        return self.OtroTexto

    def set_OtroTexto(self, OtroTexto):
        self.OtroTexto = OtroTexto

    def add_OtroTexto(self, value):
        self.OtroTexto.append(value)

    def insert_OtroTexto_at(self, index, value):
        self.OtroTexto.insert(index, value)

    def replace_OtroTexto_at(self, index, value):
        self.OtroTexto[index] = value

    def get_OtroContenido(self):
        return self.OtroContenido

    def set_OtroContenido(self, OtroContenido):
        self.OtroContenido = OtroContenido

    def add_OtroContenido(self, value):
        self.OtroContenido.append(value)

    def insert_OtroContenido_at(self, index, value):
        self.OtroContenido.insert(index, value)

    def replace_OtroContenido_at(self, index, value):
        self.OtroContenido[index] = value

    def hasContent_(self):
        if (
                self.OtroTexto or
                self.OtroContenido
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='OtrosType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OtrosType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='OtrosType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='OtrosType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='OtrosType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='OtrosType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for OtroTexto_ in self.OtroTexto:
            OtroTexto_.export(outfile, level, namespace_, name_='OtroTexto', pretty_print=pretty_print)
        for OtroContenido_ in self.OtroContenido:
            OtroContenido_.export(outfile, level, namespace_, name_='OtroContenido', pretty_print=pretty_print)


class OtroTextoType(GeneratedsSuper):
    """Código opcional para facilitar la identificación del elemento."""
    subclass = None
    superclass = None

    def __init__(self, codigo=None, valueOf_=None):
        self.original_tagname_ = None
        self.codigo = _cast(None, codigo)
        self.valueOf_ = valueOf_

    def get_codigo(self):
        return self.codigo

    def set_codigo(self, codigo):
        self.codigo = codigo

    def get_valueOf_(self):
        return self.valueOf_

    def set_valueOf_(self, valueOf_):
        self.valueOf_ = valueOf_

    def hasContent_(self):
        if (
                (1 if type(self.valueOf_) in [int, float] else self.valueOf_)
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='OtroTextoType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OtroTextoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='OtroTextoType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespace_='', name_='OtroTextoType', pretty_print=pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='OtroTextoType'):
        if self.codigo is not None and 'codigo' not in already_processed:
            already_processed.add('codigo')
            outfile.write(' codigo=%s' % (
                self.gds_encode(self.gds_format_string(quote_attrib(self.codigo), input_name='codigo')),))

    def exportChildren(self, outfile, level, namespace_='', name_='OtroTextoType', fromsubclass_=False,
                       pretty_print=True):
        pass


class OtroContenidoType(GeneratedsSuper):
    """Código opcional para facilitar la identificación del elemento."""
    subclass = None
    superclass = None

    def __init__(self, codigo=None, anytypeobjs_=None):
        self.original_tagname_ = None
        self.codigo = _cast(None, codigo)
        self.anytypeobjs_ = anytypeobjs_

    def get_anytypeobjs_(self):
        return self.anytypeobjs_

    def set_anytypeobjs_(self, anytypeobjs_):
        self.anytypeobjs_ = anytypeobjs_

    def get_codigo(self):
        return self.codigo

    def set_codigo(self, codigo):
        self.codigo = codigo

    def hasContent_(self):
        if (
                self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='OtroContenidoType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OtroContenidoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='OtroContenidoType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='OtroContenidoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='OtroContenidoType'):
        if self.codigo is not None and 'codigo' not in already_processed:
            already_processed.add('codigo')
            outfile.write(' codigo=%s' % (
                self.gds_encode(self.gds_format_string(quote_attrib(self.codigo), input_name='codigo')),))

    def exportChildren(self, outfile, level, namespace_='', name_='OtroContenidoType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.anytypeobjs_ is not None:
            self.anytypeobjs_.export(outfile, level, namespace_, pretty_print=pretty_print)


# end class OtroContenidoType


def parseString(inString, silence=False):
    if sys.version_info.major == 2:
        from StringIO import StringIO as IOBuffer
    else:
        from io import BytesIO as IOBuffer
    parser = None
    doc = parsexml_(IOBuffer(inString), parser)
    rootNode = doc.getroot()
    # rootTag, rootClass = get_root_tag(rootNode)
    # if rootClass is None:
    #     rootTag = 'FacturaElectronica'
    rootClass = FacturaElectronica
    rootObj = rootClass.factory(Clave=None, CodigoActividad=None, NumeroConsecutivo=None, FechaEmision=None,
                                Emisor=None, Receptor=None, CondicionVenta=None, MedioPago=None)
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    # doc = None
    # if not silence:
    #     sys.stdout.write(b'<?xml version="1.0" ?>\n')
    #     rootObj.export(
    #         sys.stdout, 0, name_=rootTag,
    #         namespacedef_='xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="https://cdn.comprobanteselectronicos.go.cr/xml-schemas/v4.3/facturaElectronica')
    return rootObj
