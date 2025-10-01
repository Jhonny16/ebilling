# -*- coding: utf-8 -*-

from .MixedClass import GeneratedsSuper
from .MixedClass import showIndent
from .MixedClass import quote_xml
from .MixedClass import quote_attrib
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


class FacturaElectronicaExportacion(GeneratedsSuper):
    """Elemento Raiz de la Facturacion Electrónica de exportacion"""
    subclass = None
    superclass = None

    def __init__(self, Clave, ProveedorSistemas, CodigoActividadEmisor, NumeroConsecutivo, FechaEmision, Emisor,
                 CondicionVenta, Receptor=None, CodigoActividadReceptor=None, PlazoCredito=None, DetalleServicio=None,
                 OtrosCargos=None, ResumenFactura=None, InformacionReferencia=None, Otros=None):
        self.original_tagname_ = None
        self.Clave = Clave
        self.ProveedorSistemas = ProveedorSistemas
        self.CodigoActividadEmisor = CodigoActividadEmisor
        self.CodigoActividadReceptor = CodigoActividadReceptor
        self.NumeroConsecutivo = NumeroConsecutivo
        self.FechaEmision = FechaEmision
        self.Emisor = Emisor
        self.Receptor = Receptor
        self.CondicionVenta = CondicionVenta
        self.PlazoCredito = PlazoCredito
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

    def get_Clave(self):
        return self.Clave

    def set_Clave(self, Clave):
        self.Clave = Clave

    def get_ProveedorSistemas(self):
        return self.ProveedorSistemas

    def set_ProveedorSistemas(self, ProveedorSistemas):
        self.ProveedorSistemas = ProveedorSistemas

    def get_CodigoActividadEmisor(self):
        return self.CodigoActividadEmisor

    def set_CodigoActividadEmisor(self, CodigoActividadEmisor):
        self.CodigoActividadEmisor = CodigoActividadEmisor

    def get_CodigoActividadReceptor(self):
        return self.CodigoActividadReceptor

    def set_CodigoActividadReceptor(self, CodigoActividadReceptor):
        self.CodigoActividadReceptor = CodigoActividadReceptor

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

    def get_PlazoCredito(self):
        return self.PlazoCredito

    def set_PlazoCredito(self, PlazoCredito):
        self.PlazoCredito = PlazoCredito

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
                self.ProveedorSistemas is not None or
                self.CodigoActividadEmisor is not None or
                self.CodigoActividadReceptor is not None or
                self.NumeroConsecutivo is not None or
                self.FechaEmision is not None or
                self.Emisor is not None or
                self.Receptor is not None or
                self.CondicionVenta is not None or
                self.PlazoCredito is not None or
                self.DetalleServicio is not None or
                self.OtrosCargos or
                self.ResumenFactura is not None or
                self.InformacionReferencia or
                self.Otros is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='FacturaElectronicaExportacion', namespacedef_='',
               pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FacturaElectronicaExportacion')
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
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='FacturaElectronicaExportacion')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='FacturaElectronicaExportacion',
                                pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,).encode())))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='FacturaElectronicaExportacion'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='FacturaElectronicaExportacion', fromsubclass_=False,
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
        if self.CodigoActividadEmisor is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CodigoActividadEmisor>%s</CodigoActividadEmisor>%s' % (
                self.gds_encode(
                    self.gds_format_string(quote_xml(self.CodigoActividadEmisor), input_name='CodigoActividadEmisor')),
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
        if self.PlazoCredito is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<PlazoCredito>%s</PlazoCredito>%s' % (
                self.gds_format_integer(self.PlazoCredito, input_name='PlazoCredito'), eol_)).encode()))
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


class EmisorType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Nombre, Identificacion, Ubicacion, CorreoElectronico, NombreComercial=None,
                 Telefono=None):
        self.original_tagname_ = None
        self.Nombre = Nombre
        self.Identificacion = Identificacion
        self.NombreComercial = NombreComercial
        self.Ubicacion = Ubicacion
        self.Telefono = Telefono
        self.CorreoElectronico = CorreoElectronico

    def get_Nombre(self):
        return self.Nombre

    def set_Nombre(self, Nombre):
        self.Nombre = Nombre

    def get_Identificacion(self):
        return self.Identificacion

    def set_Identificacion(self, Identificacion):
        self.Identificacion = Identificacion

    def get_NombreComercial(self):
        return self.NombreComercial

    def set_NombreComercial(self, NombreComercial):
        self.NombreComercial = NombreComercial

    def get_Ubicacion(self):
        return self.Ubicacion

    def set_Ubicacion(self, Ubicacion):
        self.Ubicacion = Ubicacion

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
                self.NombreComercial is not None or
                self.Ubicacion is not None or
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
        if self.NombreComercial is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<NombreComercial>%s</NombreComercial>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.NombreComercial), input_name='NombreComercial')),
                eol_)).encode()))
        if self.Ubicacion is not None:
            self.Ubicacion.export(outfile, level, namespace_, name_='Ubicacion', pretty_print=pretty_print)
        if self.Telefono is not None:
            self.Telefono.export(outfile, level, namespace_, name_='Telefono', pretty_print=pretty_print)
        if self.CorreoElectronico is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CorreoElectronico>%s</CorreoElectronico>%s' % (
                self.gds_encode(
                    self.gds_format_string(quote_xml(self.CorreoElectronico), input_name='CorreoElectronico')),
                eol_)).encode()))


class ReceptorType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Nombre=None, Identificacion=None, IdentificacionExtranjero=None, NombreComercial=None,
                 OtrasSenasExtranjero=None, Telefono=None, CorreoElectronico=None):
        self.original_tagname_ = None
        self.Nombre = Nombre
        self.Identificacion = Identificacion
        self.IdentificacionExtranjero = IdentificacionExtranjero
        self.NombreComercial = NombreComercial
        self.OtrasSenasExtranjero = OtrasSenasExtranjero
        self.Telefono = Telefono
        self.CorreoElectronico = CorreoElectronico

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

    def get_NombreComercial(self):
        return self.NombreComercial

    def set_NombreComercial(self, NombreComercial):
        self.NombreComercial = NombreComercial

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
                self.NombreComercial is not None or
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
        if self.NombreComercial is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<NombreComercial>%s</NombreComercial>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.NombreComercial), input_name='NombreComercial')),
                eol_)).encode()))
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


class IdentificacionType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Tipo=None, Numero=None):
        self.original_tagname_ = None
        self.Tipo = Tipo
        self.Numero = Numero

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


class UbicacionType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Provincia, Canton, Distrito, Barrio=None, OtrasSenas=None):
        self.original_tagname_ = None
        self.Provincia = Provincia
        self.Canton = Canton
        self.Distrito = Distrito
        self.Barrio = Barrio
        self.OtrasSenas = OtrasSenas

    def get_Provincia(self):
        return self.Provincia

    def set_Provincia(self, Provincia):
        self.Provincia = Provincia

    def get_Canton(self):
        return self.Canton

    def set_Canton(self, Canton):
        self.Canton = Canton

    def get_Distrito(self):
        return self.Distrito

    def set_Distrito(self, Distrito):
        self.Distrito = Distrito

    def get_Barrio(self):
        return self.Barrio

    def set_Barrio(self, Barrio):
        self.Barrio = Barrio

    def get_OtrasSenas(self):
        return self.OtrasSenas

    def set_OtrasSenas(self, OtrasSenas):
        self.OtrasSenas = OtrasSenas

    def hasContent_(self):
        if (
                self.Provincia is not None or
                self.Canton is not None or
                self.Distrito is not None or
                self.Barrio is not None or
                self.OtrasSenas is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='UbicacionType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UbicacionType')
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
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='UbicacionType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='UbicacionType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='UbicacionType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='UbicacionType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Provincia is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes((
                                        '<Provincia>%s</Provincia>%s' % (
                                    self.gds_format_integer(self.Provincia, input_name='Provincia'), eol_)).encode()))
        if self.Canton is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes((
                                        '<Canton>%s</Canton>%s' % (
                                    self.gds_format_integer(self.Canton, input_name='Canton').zfill(2),
                                    eol_)).encode()))
        if self.Distrito is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Distrito>%s</Distrito>%s' % (
                self.gds_format_integer(self.Distrito, input_name='Distrito').zfill(2), eol_)).encode()))
        # if self.Barrio is not None:
        #     showIndent(outfile, level, pretty_print)
        #     outfile.write(bytes((
        #                                 '<Barrio>%s</Barrio>%s' % (
        #                             self.gds_format_integer(self.Barrio, input_name='Barrio').zfill(2),
        #                             eol_)).encode()))
        if self.Barrio is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Barrio>%s</Barrio>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Barrio), input_name='Barrio')),
                eol_)).encode()))
        if self.OtrasSenas is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<OtrasSenas>%s</OtrasSenas>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.OtrasSenas), input_name='OtrasSenas')),
                eol_)).encode()))


class TelefonoType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, CodigoPais=None, NumTelefono=None):
        self.original_tagname_ = None
        self.CodigoPais = CodigoPais
        self.NumTelefono = NumTelefono

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


class ImpuestoType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Codigo=None, CodigoTarifaIVA=None, Tarifa=None, FactorIVA=None, Monto=None,
                 MontoExportacion=None, indicator_prod_service=None):
        self.original_tagname_ = None
        self.Codigo = Codigo
        self.CodigoTarifaIVA = CodigoTarifaIVA
        self.Tarifa = Tarifa
        self.FactorIVA = FactorIVA
        self.Monto = Monto
        self.MontoExportacion = MontoExportacion
        self.indicator_prod_service = indicator_prod_service

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

    def get_MontoExportacion(self):
        return self.MontoExportacion

    def set_MontoExportacion(self, MontoExportacion):
        self.MontoExportacion = MontoExportacion

    def hasContent_(self):
        if (
                self.Codigo is not None or
                self.CodigoTarifaIVA is not None or
                self.Tarifa is not None or
                self.FactorIVA is not None or
                self.Monto is not None or
                self.MontoExportacion is not None
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
            outfile.write(bytes(
                ('<Tarifa>%s</Tarifa>%s' % (
                    self.gds_format_float(self.Tarifa, input_name='Tarifa', digits=2), eol_)).encode()))
        if self.FactorIVA is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes((
                                        '<FactorIVA>%s</FactorIVA>%s' % (
                                    self.gds_format_float(self.FactorIVA, input_name='FactorIVA'), eol_)).encode()))
        if self.Monto is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(
                bytes(('<Monto>%s</Monto>%s' % (self.gds_format_float(self.Monto, input_name='Monto'), eol_)).encode()))
        if self.MontoExportacion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<MontoExportacion>%s</MontoExportacion>%s' % (
                self.gds_format_float(self.MontoExportacion, input_name='MontoExportacion'), eol_)).encode()))


class CodigoType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Tipo=None, Codigo=None):
        self.original_tagname_ = None
        self.Tipo = Tipo
        self.Codigo = Codigo

    def get_Tipo(self):
        return self.Tipo

    def set_Tipo(self, Tipo):
        self.Tipo = Tipo

    def get_Codigo(self):
        return self.Codigo

    def set_Codigo(self, Codigo):
        self.Codigo = Codigo

    def hasContent_(self):
        if (
                self.Tipo is not None or
                self.Codigo is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='CodigoType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CodigoType')
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
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='CodigoType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='CodigoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='CodigoType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='CodigoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Tipo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Tipo>%s</Tipo>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Tipo), input_name='Tipo')), eol_)).encode()))
        if self.Codigo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Codigo>%s</Codigo>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Codigo), input_name='Codigo')), eol_)).encode()))


class DescuentoType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, CodigoDescuento, MontoDescuento=0.00, NaturalezaDescuento=None):
        self.original_tagname_ = None
        self.MontoDescuento = MontoDescuento
        self.CodigoDescuento = CodigoDescuento
        self.NaturalezaDescuento = NaturalezaDescuento

    def get_MontoDescuento(self):
        return self.MontoDescuento

    def set_MontoDescuento(self, MontoDescuento):
        self.MontoDescuento = MontoDescuento

    def get_CodigoDescuento(self):
        return self.CodigoDescuento

    def set_CodigoDescuento(self, CodigoDescuento):
        self.CodigoDescuento = CodigoDescuento

    def get_NaturalezaDescuento(self):
        return self.NaturalezaDescuento

    def set_NaturalezaDescuento(self, NaturalezaDescuento):
        self.NaturalezaDescuento = NaturalezaDescuento

    def hasContent_(self):
        if (
                self.MontoDescuento is not None or
                self.CodigoDescuento is not None or
                self.NaturalezaDescuento is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='DescuentoType', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DescuentoType')
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
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='DescuentoType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='DescuentoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='DescuentoType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='DescuentoType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.MontoDescuento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<MontoDescuento>%s</MontoDescuento>%s' % (
                self.gds_format_float(self.MontoDescuento, input_name='MontoDescuento'), eol_)).encode()))
        if self.CodigoDescuento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CodigoDescuento>%s</CodigoDescuento>%s' % (self.gds_encode(
                self.gds_format_string(quote_xml(self.CodigoDescuento), input_name='CodigoDescuento')),
                                                                                      eol_)).encode()))
        if self.NaturalezaDescuento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<NaturalezaDescuento>%s</NaturalezaDescuento>%s' % (self.gds_encode(
                self.gds_format_string(quote_xml(self.NaturalezaDescuento), input_name='NaturalezaDescuento')),
                                                                                      eol_)).encode()))


class OtrosCargosType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, TipoDocumento=None, Detalle=None, Porcentaje=None, MontoCargo=None):
        self.original_tagname_ = None
        self.TipoDocumento = TipoDocumento
        self.Detalle = Detalle
        self.Porcentaje = Porcentaje
        self.MontoCargo = MontoCargo

    def get_TipoDocumento(self):
        return self.TipoDocumento

    def set_TipoDocumento(self, TipoDocumento):
        self.TipoDocumento = TipoDocumento

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


class CodigoMonedaType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, CodigoMoneda=None, TipoCambio=None):
        self.original_tagname_ = None
        self.CodigoMoneda = CodigoMoneda
        self.TipoCambio = TipoCambio

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


class DetalleServicioType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, LineaDetalle=None):
        self.original_tagname_ = None
        if LineaDetalle is None:
            self.LineaDetalle = []
        else:
            self.LineaDetalle = LineaDetalle

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


class LineaDetalleType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, NumeroLinea, Cantidad, CodigoCABYS=None, PartidaArancelaria=None, CodigoComercial=None,
                       UnidadMedida=None, UnidadMedidaComercial=None, Detalle=None, PrecioUnitario=None, DetalleSurtido=None,
                       MontoTotal=None, Descuento=None, SubTotal=None, Impuesto=None, ImpuestoNeto=None, MontoTotalLinea=None):
        self.original_tagname_ = None
        self.NumeroLinea = NumeroLinea
        self.PartidaArancelaria = PartidaArancelaria
        self.CodigoCABYS = CodigoCABYS
        if CodigoComercial is None:
            self.CodigoComercial = []
        else:
            self.CodigoComercial = CodigoComercial
        self.Cantidad = Cantidad
        self.UnidadMedida = UnidadMedida
        self.UnidadMedidaComercial = UnidadMedidaComercial
        self.Detalle = Detalle
        self.DetalleSurtido = DetalleSurtido
        self.PrecioUnitario = PrecioUnitario
        self.MontoTotal = MontoTotal
        if Descuento is None:
            self.Descuento = []
        else:
            self.Descuento = Descuento
        self.SubTotal = SubTotal
        if Impuesto is None:
            self.Impuesto = []
        else:
            self.Impuesto = Impuesto
        self.ImpuestoNeto = ImpuestoNeto
        self.MontoTotalLinea = MontoTotalLinea

    def get_NumeroLinea(self):
        return self.NumeroLinea

    def set_NumeroLinea(self, NumeroLinea):
        self.NumeroLinea = NumeroLinea

    def get_PartidaArancelaria(self):
        return self.PartidaArancelaria

    def set_PartidaArancelaria(self, PartidaArancelaria):
        self.PartidaArancelaria = PartidaArancelaria

    def get_CodigoCABYS(self):
        return self.CodigoCABYS

    def set_CodigoCABYS(self, CodigoCABYS):
        self.CodigoCABYS = CodigoCABYS

    def get_CodigoComercial(self):
        return self.CodigoComercial

    def set_CodigoComercial(self, CodigoComercial):
        self.CodigoComercial = CodigoComercial

    def add_CodigoComercial(self, value):
        self.CodigoComercial.append(value)

    def insert_CodigoComercial_at(self, index, value):
        self.CodigoComercial.insert(index, value)

    def replace_CodigoComercial_at(self, index, value):
        self.CodigoComercial[index] = value

    def get_Cantidad(self):
        return self.Cantidad

    def set_Cantidad(self, Cantidad):
        self.Cantidad = Cantidad

    def get_UnidadMedida(self):
        return self.UnidadMedida

    def set_UnidadMedida(self, UnidadMedida):
        self.UnidadMedida = UnidadMedida

    def get_UnidadMedidaComercial(self):
        return self.UnidadMedidaComercial

    def set_UnidadMedidaComercial(self, UnidadMedidaComercial):
        self.UnidadMedidaComercial = UnidadMedidaComercial

    def get_Detalle(self):
        return self.Detalle

    def set_Detalle(self, Detalle):
        self.Detalle = Detalle

    def get_DetalleSurtido(self):
        return self.DetalleSurtido

    def set_DetalleSurtido(self, DetalleSurtido):
        self.DetalleSurtido = DetalleSurtido

    def get_PrecioUnitario(self):
        return self.PrecioUnitario

    def set_PrecioUnitario(self, PrecioUnitario):
        self.PrecioUnitario = PrecioUnitario

    def get_MontoTotal(self):
        return self.MontoTotal

    def set_MontoTotal(self, MontoTotal):
        self.MontoTotal = MontoTotal

    def get_Descuento(self):
        return self.Descuento

    def set_Descuento(self, Descuento):
        self.Descuento = Descuento

    def add_Descuento(self, value):
        self.Descuento.append(value)

    def insert_Descuento_at(self, index, value):
        self.Descuento.insert(index, value)

    def replace_Descuento_at(self, index, value):
        self.Descuento[index] = value

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
                self.PartidaArancelaria is not None or
                self.CodigoCABYS is not None or
                self.CodigoComercial or
                self.Cantidad is not None or
                self.UnidadMedida is not None or
                self.UnidadMedidaComercial is not None or
                self.Detalle is not None or
                self.DetalleSurtido is not None or
                self.PrecioUnitario is not None or
                self.MontoTotal is not None or
                self.Descuento or
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
        if self.PartidaArancelaria is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<PartidaArancelaria>%s</PartidaArancelaria>%s' % (self.gds_encode(
                self.gds_format_string(quote_xml(self.PartidaArancelaria), input_name='PartidaArancelaria')),
                                                                                    eol_)).encode()))
        if self.CodigoCABYS is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CodigoCABYS>%s</CodigoCABYS>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.CodigoCABYS), input_name='CodigoCABYS')), eol_)).encode()))
        for CodigoComercial_ in self.CodigoComercial:
            CodigoComercial_.export(outfile, level, namespace_, name_='CodigoComercial', pretty_print=pretty_print)
        if self.Cantidad is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Cantidad>%s</Cantidad>%s' % (
                self.gds_format_float(self.Cantidad, input_name='Cantidad', digits=3), eol_)).encode()))
        if self.UnidadMedida is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<UnidadMedida>%s</UnidadMedida>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.UnidadMedida), input_name='UnidadMedida')),
                eol_)).encode()))
        if self.UnidadMedidaComercial is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<UnidadMedidaComercial>%s</UnidadMedidaComercial>%s' % (self.gds_encode(
                self.gds_format_string(quote_xml(self.UnidadMedidaComercial), input_name='UnidadMedidaComercial')),
                                                                                          eol_)).encode()))
        if self.Detalle is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Detalle>%s</Detalle>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Detalle), input_name='Detalle')),
                eol_)).encode()))
        if self.DetalleSurtido is not None:
            self.DetalleSurtido.export(outfile, level, namespace_, name_='DetalleSurtido',
                                       pretty_print=pretty_print)
        if self.PrecioUnitario is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<PrecioUnitario>%s</PrecioUnitario>%s' % (
                self.gds_format_float(self.PrecioUnitario, input_name='PrecioUnitario'), eol_)).encode()))
        if self.MontoTotal is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<MontoTotal>%s</MontoTotal>%s' % (
                self.gds_format_float(self.MontoTotal, input_name='MontoTotal'), eol_)).encode()))
        for Descuento_ in self.Descuento:
            Descuento_.export(outfile, level, namespace_, name_='Descuento', pretty_print=pretty_print)
        if self.SubTotal is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes((
                                        '<SubTotal>%s</SubTotal>%s' % (
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


class DetalleSurtido(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, LineaDetalleSurtido=None):
        self.original_tagname_ = None
        if LineaDetalleSurtido is None:
            self.LineaDetalleSurtido = []
        else:
            self.LineaDetalleSurtido = LineaDetalleSurtido

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

    def get_LineaDetalleSurtido(self):
        return self.LineaDetalleSurtido

    def set_LineaDetalleSurtido(self, LineaDetalleSurtido):
        self.LineaDetalleSurtido = LineaDetalleSurtido

    def add_LineaDetalleSurtido(self, value):
        self.LineaDetalleSurtido.append(value)

    def insert_LineaDetalleSurtido_at(self, index, value):
        self.LineaDetalleSurtido.insert(index, value)

    def replace_LineaDetalle_at(self, index, value):
        self.LineaDetalleSurtido[index] = value

    def hasContent_(self):
        if (
                self.LineaDetalleSurtido
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='DetalleSurtido', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DetalleSurtido')
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
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='DetalleSurtido')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='DetalleSurtido',
                                pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='DetalleSurtido'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='DetalleServicioType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for LineaDetalleSurtido_ in self.LineaDetalleSurtido:
            LineaDetalleSurtido_.export(outfile, level, namespace_, name_='LineaDetalleSurtido', pretty_print=pretty_print)

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
        if nodeName_ == 'LineaDetalleSurtido':
            obj_ = LineaDetalleType.factory(NumeroLinea=None, CodigoCABYS=None, Cantidad=None)
            obj_.build(child_)
            self.LineaDetalleSurtido.append(obj_)
            obj_.original_tagname_ = 'LineaDetalleSurtido'


class LineaDetalleSurtido(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, CodigoCABYSSurtido, CantidadSurtido, UnidadMedidaSurtido, DetalleSurtido=None,
                 PrecioUnitarioSurtido=None, MontoTotalSurtido=None, DescuentoSurtido=None,
                 SubTotalSurtido=None, BaseImponibleSurtido=None, ImpuestoSurtido=None):
        self.original_tagname_ = None
        self.CodigoCABYSSurtido = CodigoCABYSSurtido
        self.CantidadSurtido = CantidadSurtido
        self.UnidadMedidaSurtido = UnidadMedidaSurtido
        self.DetalleSurtido = DetalleSurtido
        self.PrecioUnitarioSurtido = PrecioUnitarioSurtido
        self.MontoTotalSurtido = MontoTotalSurtido
        self.DescuentoSurtido = DescuentoSurtido
        self.SubTotalSurtido = SubTotalSurtido
        self.BaseImponibleSurtido = BaseImponibleSurtido
        if ImpuestoSurtido is None:
            self.ImpuestoSurtido = []
        else:
            self.ImpuestoSurtido = ImpuestoSurtido

    # def factory(*args_, **kwargs_):
    #     if CurrentSubclassModule_ is not None:
    #         subclass = getSubclassFromModule_(
    #             CurrentSubclassModule_, LineaDetalleType)
    #         if subclass is not None:
    #             return subclass(*args_, **kwargs_)
    #     if LineaDetalleType.subclass:
    #         return LineaDetalleType.subclass(*args_, **kwargs_)
    #     else:
    #         return LineaDetalleType(*args_, **kwargs_)
    #
    # factory = staticmethod(factory)

    def get_CodigoCABYSSurtido(self):
        return self.CodigoCABYSSurtido

    def set_CodigoCABYSSurtido(self, CodigoCABYSSurtido):
        self.CodigoCABYSSurtido = CodigoCABYSSurtido

    def get_CantidadSurtido(self):
        return self.CantidadSurtido

    def set_CantidadSurtido(self, CantidadSurtido):
        self.CantidadSurtido = CantidadSurtido

    def get_UnidadMedidaSurtido(self):
        return self.UnidadMedidaSurtido

    def set_UnidadMedidaSurtido(self, UnidadMedidaSurtido):
        self.UnidadMedidaSurtido = UnidadMedidaSurtido

    def get_DetalleSurtido(self):
        return self.DetalleSurtido

    def set_DetalleSurtido(self, DetalleSurtido):
        self.DetalleSurtido = DetalleSurtido

    def get_PrecioUnitarioSurtido(self):
        return self.PrecioUnitarioSurtido

    def set_PrecioUnitarioSurtido(self, PrecioUnitarioSurtido):
        self.PrecioUnitarioSurtido = PrecioUnitarioSurtido

    def get_MontoTotalSurtido(self):
        return self.MontoTotalSurtido

    def set_MontoTotalSurtido(self, MontoTotalSurtido):
        self.MontoTotalSurtido = MontoTotalSurtido

    def get_DescuentoSurtido(self):
        return self.DescuentoSurtido

    def set_DescuentoSurtido(self, DescuentoSurtido):
        self.DescuentoSurtido = DescuentoSurtido

    def get_SubTotalSurtido(self):
        return self.SubTotalSurtido

    def set_SubTotalSurtido(self, SubTotalSurtido):
        self.SubTotalSurtido = SubTotalSurtido

    def get_BaseImponibleSurtido(self):
        return self.BaseImponibleSurtido

    def set_BaseImponibleSurtido(self, BaseImponibleSurtido):
        self.BaseImponibleSurtido = BaseImponibleSurtido

    def get_ImpuestoSurtido(self):
        return self.ImpuestoSurtido

    def set_ImpuestoSurtido(self, ImpuestoSurtido):
        self.ImpuestoSurtido = ImpuestoSurtido

    def add_ImpuestoSurtido(self, value):
        self.ImpuestoSurtido.append(value)

    def insert_ImpuestoSurtido_at(self, index, value):
        self.ImpuestoSurtido.insert(index, value)

    def replace_ImpuestoSurtido_at(self, index, value):
        self.ImpuestoSurtido[index] = value

    def hasContent_(self):
        if (
                self.CodigoCABYSSurtido is not None or
                self.CantidadSurtido is not None or
                self.UnidadMedidaSurtido or
                self.DetalleSurtido is not None or
                self.PrecioUnitarioSurtido is not None or
                self.MontoTotalSurtido is not None or
                self.DescuentoSurtido is not None or
                self.SubTotalSurtido is not None or
                self.BaseImponibleSurtido is not None or
                self.ImpuestoSurtido is not None
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
        if self.CodigoCABYSSurtido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CodigoCABYSSurtido>%s</CodigoCABYSSurtido>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.CodigoCABYSSurtido), input_name='CodigoCABYSSurtido')),
                eol_)).encode()))
        if self.CantidadSurtido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CantidadSurtido>%s</CantidadSurtido>%s' % (
                self.gds_format_integer(self.CantidadSurtido, input_name='CantidadSurtido'), eol_)).encode()))
        if self.UnidadMedidaSurtido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<UnidadMedidaSurtido>%s</UnidadMedidaSurtido>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.UnidadMedidaSurtido), input_name='UnidadMedidaSurtido')),
                eol_)).encode()))
        if self.DetalleSurtido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<DetalleSurtido>%s</DetalleSurtido>%s' % (self.gds_encode(
                self.gds_format_string(quote_xml(self.DetalleSurtido), input_name='DetalleSurtido')),
                                                                                          eol_)).encode()))
        if self.PrecioUnitarioSurtido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<PrecioUnitarioSurtido>%s</PrecioUnitarioSurtido>%s' % (
                self.gds_format_float(self.PrecioUnitarioSurtido, input_name='PrecioUnitarioSurtido'), eol_)).encode()))
        if self.MontoTotalSurtido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<MontoTotalSurtido>%s</MontoTotalSurtido>%s' % (
                self.gds_format_float(self.MontoTotalSurtido, input_name='MontoTotalSurtido'), eol_)).encode()))
        if self.DescuentoSurtido is not None:
            self.DescuentoSurtido.export(outfile, level, namespace_, name_='DescuentoSurtido',
                                         pretty_print=pretty_print)
        if self.SubTotalSurtido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<SubTotalSurtido>%s</SubTotalSurtido>%s' % (
                self.gds_format_float(self.SubTotalSurtido, input_name='SubTotalSurtido'), eol_)).encode()))
        if self.BaseImponibleSurtido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<BaseImponibleSurtido>%s</BaseImponibleSurtido>%s' % (
                self.gds_format_float(self.BaseImponibleSurtido, input_name='SubTotalSurtido'), eol_)).encode()))
        for ImpuestoSurtido_ in self.ImpuestoSurtido:
            ImpuestoSurtido_.export(outfile, level, namespace_, name_='ImpuestoSurtido', pretty_print=pretty_print)

    # def build(self, node):
    #     already_processed = set()
    #     self.buildAttributes(node, node.attrib, already_processed)
    #     for child in node:
    #         nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
    #         self.buildChildren(child, node, nodeName_)
    #     return self
    #
    # def buildAttributes(self, node, attrs, already_processed):
    #     pass
    #
    # def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
    #     if nodeName_ == 'NumeroLinea':
    #         self.NumeroLinea = child_.text
    #     elif nodeName_ == 'CodigoCABYS':
    #         self.CodigoCABYS = child_.text
    #     elif nodeName_ == 'CodigoComercial':
    #         obj_ = CodigoType.factory()
    #         obj_.build(child_)
    #         self.CodigoComercial.append(obj_)
    #         obj_.original_tagname_ = 'CodigoComercial'
    #     elif nodeName_ == 'Cantidad':
    #         self.Cantidad = child_.text
    #     elif nodeName_ == 'UnidadMedida':
    #         self.UnidadMedida = child_.text
    #     elif nodeName_ == 'UnidadMedidaComercial':
    #         self.UnidadMedidaComercial = child_.text
    #     elif nodeName_ == 'Detalle':
    #         self.Detalle = child_.text
    #     elif nodeName_ == 'PrecioUnitario':
    #         self.PrecioUnitario = child_.text
    #     elif nodeName_ == 'MontoTotal':
    #         self.MontoTotal = child_.text
    #     elif nodeName_ == 'Descuento':
    #         obj_ = DescuentoType.factory()
    #         obj_.build(child_)
    #         self.Descuento.append(obj_)
    #         obj_.original_tagname_ = 'Descuento'
    #     elif nodeName_ == 'SubTotal':
    #         self.SubTotal = child_.text
    #     elif nodeName_ == 'BaseImponible':
    #         self.BaseImponible = child_.text
    #     elif nodeName_ == 'Impuesto':
    #         obj_ = ImpuestoType.factory()
    #         obj_.build(child_)
    #         self.Impuesto.append(obj_)
    #         obj_.original_tagname_ = 'Impuesto'
    #     elif nodeName_ == 'ImpuestoNeto':
    #         self.ImpuestoNeto = child_.text
    #     elif nodeName_ == 'MontoTotalLinea':
    #         self.MontoTotalLinea = child_.text


class ImpuestoSurtido(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, CodigoImpuestoSurtido=None, CodigoTarifaIVASurtido=None, TarifaSurtido=None,
                 MontoImpuestoSurtido=None):
        self.original_tagname_ = None
        self.CodigoImpuestoSurtido = CodigoImpuestoSurtido
        self.CodigoTarifaIVASurtido = CodigoTarifaIVASurtido
        self.TarifaSurtido = TarifaSurtido
        self.MontoImpuestoSurtido = MontoImpuestoSurtido

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

    def get_CodigoImpuestoSurtido(self):
        return self.CodigoImpuestoSurtido

    def set_CodigoImpuestoSurtido(self, CodigoImpuestoSurtido):
        self.CodigoImpuestoSurtido = CodigoImpuestoSurtido

    def get_CodigoTarifaIVASurtido(self):
        return self.CodigoTarifaIVASurtido

    def set_CodigoTarifaIVASurtido(self, CodigoTarifaIVASurtido):
        self.CodigoTarifaIVASurtido = CodigoTarifaIVASurtido

    def get_TarifaSurtido(self):
        return self.TarifaSurtido

    def set_TarifaSurtido(self, TarifaSurtido):
        self.TarifaSurtido = TarifaSurtido

    def get_MontoImpuestoSurtido(self):
        return self.MontoImpuestoSurtido

    def set_MontoImpuestoSurtido(self, MontoImpuestoSurtido):
        self.MontoImpuestoSurtido = MontoImpuestoSurtido

    def hasContent_(self):
        if (
                self.CodigoImpuestoSurtido is not None or
                self.CodigoTarifaIVASurtido is not None or
                self.TarifaSurtido is not None or
                self.MontoImpuestoSurtido is not None
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
        if self.CodigoImpuestoSurtido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CodigoImpuestoSurtido>%s</CodigoImpuestoSurtido>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.CodigoImpuestoSurtido), input_name='CodigoImpuestoSurtido')), eol_)).encode()))
        if self.CodigoTarifaIVASurtido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CodigoTarifaIVASurtido>%s</CodigoTarifaIVASurtido>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.CodigoTarifaIVASurtido), input_name='CodigoTarifaIVASurtido')),
                eol_)).encode()))
        if self.TarifaSurtido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TarifaSurtido>%s</TarifaSurtido>%s' % (
                self.gds_format_float(self.TarifaSurtido, input_name='TarifaSurtido', digits=2), eol_)).encode()))
        if self.MontoImpuestoSurtido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<MontoImpuestoSurtido>%s</MontoImpuestoSurtido>%s' % (
                self.gds_format_float(self.MontoImpuestoSurtido, input_name='MontoImpuestoSurtido'), eol_)).encode()))

    # def build(self, node):
    #     already_processed = set()
    #     self.buildAttributes(node, node.attrib, already_processed)
    #     for child in node:
    #         nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
    #         self.buildChildren(child, node, nodeName_)
    #     return self
    #
    # def buildAttributes(self, node, attrs, already_processed):
    #     pass
    #
    # def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
    #     if nodeName_ == 'Codigo':
    #         self.Codigo = child_.text
    #     elif nodeName_ == 'CodigoTarifaIVA':
    #         self.CodigoTarifaIVA = child_.text
    #     elif nodeName_ == 'Tarifa':
    #         self.Tarifa = child_.text
    #     elif nodeName_ == 'FactorIVA':
    #         self.FactorIVA = child_.text
    #     elif nodeName_ == 'Monto':
    #         self.Monto = child_.text
    #     elif nodeName_ == 'Exoneracion':
    #         obj_ = ExoneracionType.factory()
    #         obj_.build(child_)
    #         self.Exoneracion = obj_
    #         obj_.original_tagname_ = 'Exoneracion'


class ResumenFacturaType(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, CodigoTipoMoneda=None, TotalServGravados=None, TotalServExentos=None,
                 TotalMercanciasGravadas=None, TotalMercanciasExentas=None, TotalGravado=0.00, TotalExento=0.00,
                 TotalVenta=None, TotalDescuentos=0.00, TotalVentaNeta=None, TotalImpuesto=0.00, TotalOtrosCargos=0.00,
                 TotalComprobante=None, TotalDesgloseImpuesto=None, MedioPago=None):
        self.original_tagname_ = None
        self.CodigoTipoMoneda = CodigoTipoMoneda
        self.TotalServGravados = TotalServGravados
        self.TotalServExentos = TotalServExentos
        self.TotalMercanciasGravadas = TotalMercanciasGravadas
        self.TotalMercanciasExentas = TotalMercanciasExentas
        self.TotalGravado = TotalGravado
        self.TotalExento = TotalExento
        self.TotalVenta = TotalVenta
        self.TotalDescuentos = TotalDescuentos
        self.TotalVentaNeta = TotalVentaNeta
        self.TotalImpuesto = TotalImpuesto
        self.TotalOtrosCargos = TotalOtrosCargos
        if MedioPago is None:
            self.MedioPago = []
        else:
            self.MedioPago = MedioPago
        if TotalDesgloseImpuesto is None:
            self.TotalDesgloseImpuesto = []
        else:
            self.TotalDesgloseImpuesto = TotalDesgloseImpuesto
        self.TotalComprobante = TotalComprobante

    def get_CodigoTipoMoneda(self):
        return self.CodigoTipoMoneda

    def set_CodigoTipoMoneda(self, CodigoTipoMoneda):
        self.CodigoTipoMoneda = CodigoTipoMoneda

    def get_TotalServGravados(self):
        return self.TotalServGravados

    def set_TotalServGravados(self, TotalServGravados):
        self.TotalServGravados = TotalServGravados

    def get_TotalServExentos(self):
        return self.TotalServExentos

    def set_TotalServExentos(self, TotalServExentos):
        self.TotalServExentos = TotalServExentos

    def get_TotalMercanciasGravadas(self):
        return self.TotalMercanciasGravadas

    def set_TotalMercanciasGravadas(self, TotalMercanciasGravadas):
        self.TotalMercanciasGravadas = TotalMercanciasGravadas

    def get_TotalMercanciasExentas(self):
        return self.TotalMercanciasExentas

    def set_TotalMercanciasExentas(self, TotalMercanciasExentas):
        self.TotalMercanciasExentas = TotalMercanciasExentas

    def get_TotalGravado(self):
        return self.TotalGravado

    def set_TotalGravado(self, TotalGravado):
        self.TotalGravado = TotalGravado

    def get_TotalExento(self):
        return self.TotalExento

    def set_TotalExento(self, TotalExento):
        self.TotalExento = TotalExento

    def get_TotalVenta(self):
        return self.TotalVenta

    def set_TotalVenta(self, TotalVenta):
        self.TotalVenta = TotalVenta

    def get_TotalDescuentos(self):
        return self.TotalDescuentos

    def set_TotalDescuentos(self, TotalDescuentos):
        self.TotalDescuentos = TotalDescuentos

    def get_TotalVentaNeta(self):
        return self.TotalVentaNeta

    def set_TotalVentaNeta(self, TotalVentaNeta):
        self.TotalVentaNeta = TotalVentaNeta

    def get_TotalImpuesto(self):
        return self.TotalImpuesto

    def set_TotalImpuesto(self, TotalImpuesto):
        self.TotalImpuesto = TotalImpuesto

    def get_TotalOtrosCargos(self):
        return self.TotalOtrosCargos

    def set_TotalOtrosCargos(self, TotalOtrosCargos):
        self.TotalOtrosCargos = TotalOtrosCargos

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
                self.TotalServGravados is not None or
                self.TotalServExentos is not None or
                self.TotalMercanciasGravadas is not None or
                self.TotalMercanciasExentas is not None or
                self.TotalGravado is not None or
                self.TotalExento is not None or
                self.TotalVenta is not None or
                self.TotalDescuentos is not None or
                self.TotalVentaNeta is not None or
                self.TotalImpuesto is not None or
                self.TotalOtrosCargos is not None or
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
        if self.TotalServGravados is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalServGravados>%s</TotalServGravados>%s' % (
                self.gds_format_float(self.TotalServGravados, input_name='TotalServGravados'), eol_)).encode()))
        if self.TotalServExentos is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalServExentos>%s</TotalServExentos>%s' % (
                self.gds_format_float(self.TotalServExentos, input_name='TotalServExentos'), eol_)).encode()))
        if self.TotalMercanciasGravadas is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalMercanciasGravadas>%s</TotalMercanciasGravadas>%s' % (
                self.gds_format_float(self.TotalMercanciasGravadas, input_name='TotalMercanciasGravadas'),
                eol_)).encode()))
        if self.TotalMercanciasExentas is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalMercanciasExentas>%s</TotalMercanciasExentas>%s' % (
                self.gds_format_float(self.TotalMercanciasExentas, input_name='TotalMercanciasExentas'),
                eol_)).encode()))
        if self.TotalGravado is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalGravado>%s</TotalGravado>%s' % (
                self.gds_format_float(self.TotalGravado, input_name='TotalGravado'), eol_)).encode()))
        if self.TotalExento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalExento>%s</TotalExento>%s' % (
                self.gds_format_float(self.TotalExento, input_name='TotalExento'), eol_)).encode()))
        if self.TotalVenta is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalVenta>%s</TotalVenta>%s' % (
                self.gds_format_float(self.TotalVenta, input_name='TotalVenta'), eol_)).encode()))
        if self.TotalDescuentos is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalDescuentos>%s</TotalDescuentos>%s' % (
                self.gds_format_float(self.TotalDescuentos, input_name='TotalDescuentos'), eol_)).encode()))
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
        if self.TotalOtrosCargos is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalOtrosCargos>%s</TotalOtrosCargos>%s' % (
                self.gds_format_float(self.TotalOtrosCargos, input_name='TotalOtrosCargos'), eol_)).encode()))
        for MedioPago_ in self.MedioPago:
            MedioPago_.export(outfile, level, namespace_, name_='MedioPago',
                              pretty_print=pretty_print)
        if self.TotalComprobante is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalComprobante>%s</TotalComprobante>%s' % (
                self.gds_format_float(self.TotalComprobante, input_name='TotalComprobante'), eol_)).encode()))


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
            outfile.write(bytes(('<TipoDoc>%s</TipoDoc>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.TipoDoc), input_name='TipoDoc')),
                eol_)).encode()))
        if self.Numero is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Numero>%s</Numero>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Numero), input_name='Numero')), eol_)).encode()))
        if self.FechaEmision is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<FechaEmision>%s</FechaEmision>%s' % (
                self.gds_format_datetime(self.FechaEmision, input_name='FechaEmision'), eol_)).encode()))
        if self.Codigo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Codigo>%s</Codigo>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Codigo), input_name='Codigo')), eol_)).encode()))
        if self.Razon is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Razon>%s</Razon>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Razon), input_name='Razon')), eol_)).encode()))


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
        # self.codigo = _cast(None, codigo)
        self.codigo = codigo
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
        # outfile.write(bytes('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)))
        outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='OtroTextoType')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % ('',)).encode()))
            # outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespace_='', name_='OtroTextoType', pretty_print=False)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='OtroTextoType'):
        if self.codigo is not None and 'codigo' not in already_processed:
            already_processed.add('codigo')
            outfile.write(bytes((' codigo=%s' % (quote_attrib(self.codigo),)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='OtroTextoType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.valueOf_ is not None:
            outfile.write(bytes(('%s%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.valueOf_),
                                                       input_name='valueOf_')), eol_)).encode()))


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
