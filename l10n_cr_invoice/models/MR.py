# -*- coding: utf-8 -*-

from .MixedClass import GeneratedsSuper
from .MixedClass import showIndent
from .MixedClass import quote_xml
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


class MensajeReceptor(GeneratedsSuper):
    """Mensaje de aceptacion o rechazo de los documentos electronicos por
    parte del obligado tributario"""
    subclass = None
    superclass = None

    def __init__(self, Clave, NumeroCedulaEmisor, FechaEmisionDoc, Mensaje, NumeroCedulaReceptor,
                 NumeroConsecutivoReceptor, DetalleMensaje=None,
                 MontoTotalImpuesto=None, CodigoActividad=None, CondicionImpuesto=None,
                 MontoTotalImpuestoAcreditar=None, MontoTotalDeGastoAplicable=None, TotalFactura=None):
        self.original_tagname_ = None
        self.Clave = Clave
        self.NumeroCedulaEmisor = NumeroCedulaEmisor
        self.FechaEmisionDoc = FechaEmisionDoc
        self.Mensaje = Mensaje
        self.DetalleMensaje = DetalleMensaje
        self.MontoTotalImpuesto = MontoTotalImpuesto
        self.CodigoActividad = CodigoActividad
        self.CondicionImpuesto = CondicionImpuesto
        self.MontoTotalImpuestoAcreditar = MontoTotalImpuestoAcreditar
        self.MontoTotalDeGastoAplicable = MontoTotalDeGastoAplicable
        self.TotalFactura = TotalFactura
        self.NumeroCedulaReceptor = NumeroCedulaReceptor
        self.NumeroConsecutivoReceptor = NumeroConsecutivoReceptor

    def get_Clave(self):
        return self.Clave

    def set_Clave(self, Clave):
        self.Clave = Clave

    def get_NumeroCedulaEmisor(self):
        return self.NumeroCedulaEmisor

    def set_NumeroCedulaEmisor(self, NumeroCedulaEmisor):
        self.NumeroCedulaEmisor = NumeroCedulaEmisor

    def get_FechaEmisionDoc(self):
        return self.FechaEmisionDoc

    def set_FechaEmisionDoc(self, FechaEmisionDoc):
        self.FechaEmisionDoc = FechaEmisionDoc

    def get_Mensaje(self):
        return self.Mensaje

    def set_Mensaje(self, Mensaje):
        self.Mensaje = Mensaje

    def get_DetalleMensaje(self):
        return self.DetalleMensaje

    def set_DetalleMensaje(self, DetalleMensaje):
        self.DetalleMensaje = DetalleMensaje

    def get_MontoTotalImpuesto(self):
        return self.MontoTotalImpuesto

    def set_MontoTotalImpuesto(self, MontoTotalImpuesto):
        self.MontoTotalImpuesto = MontoTotalImpuesto

    def get_CodigoActividad(self):
        return self.CodigoActividad

    def set_CodigoActividad(self, CodigoActividad):
        self.CodigoActividad = CodigoActividad

    def get_CondicionImpuesto(self):
        return self.CondicionImpuesto

    def set_CondicionImpuesto(self, CondicionImpuesto):
        self.CondicionImpuesto = CondicionImpuesto

    def get_MontoTotalImpuestoAcreditar(self):
        return self.MontoTotalImpuestoAcreditar

    def set_MontoTotalImpuestoAcreditar(self, MontoTotalImpuestoAcreditar):
        self.MontoTotalImpuestoAcreditar = MontoTotalImpuestoAcreditar

    def get_MontoTotalDeGastoAplicable(self):
        return self.MontoTotalDeGastoAplicable

    def set_MontoTotalDeGastoAplicable(self, MontoTotalDeGastoAplicable):
        self.MontoTotalDeGastoAplicable = MontoTotalDeGastoAplicable

    def get_TotalFactura(self):
        return self.TotalFactura

    def set_TotalFactura(self, TotalFactura):
        self.TotalFactura = TotalFactura

    def get_NumeroCedulaReceptor(self):
        return self.NumeroCedulaReceptor

    def set_NumeroCedulaReceptor(self, NumeroCedulaReceptor):
        self.NumeroCedulaReceptor = NumeroCedulaReceptor

    def get_NumeroConsecutivoReceptor(self):
        return self.NumeroConsecutivoReceptor

    def set_NumeroConsecutivoReceptor(self, NumeroConsecutivoReceptor):
        self.NumeroConsecutivoReceptor = NumeroConsecutivoReceptor

    def hasContent_(self):
        if (
                self.Clave is not None or
                self.NumeroCedulaEmisor is not None or
                self.FechaEmisionDoc is not None or
                self.Mensaje is not None or
                self.DetalleMensaje is not None or
                self.MontoTotalImpuesto is not None or
                self.CodigoActividad is not None or
                self.CondicionImpuesto is not None or
                self.MontoTotalImpuestoAcreditar is not None or
                self.MontoTotalDeGastoAplicable is not None or
                self.TotalFactura is not None or
                self.NumeroCedulaReceptor is not None or
                self.NumeroConsecutivoReceptor is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='MensajeReceptor', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('MensajeReceptor')
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
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='MensajeReceptor')
        if self.hasContent_():
            outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='MensajeReceptor', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='MensajeReceptor'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='MensajeReceptor', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Clave is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Clave>%s</Clave>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.Clave), input_name='Clave')), eol_)).encode()))
        if self.NumeroCedulaEmisor is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<NumeroCedulaEmisor>%s</NumeroCedulaEmisor>%s' % (self.gds_encode(
                self.gds_format_string(quote_xml(self.NumeroCedulaEmisor), input_name='NumeroCedulaEmisor')), eol_)).encode()))
        if self.FechaEmisionDoc is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<FechaEmisionDoc>%s</FechaEmisionDoc>%s' % (
                self.gds_format_string(self.FechaEmisionDoc, input_name='FechaEmisionDoc'), eol_)).encode()))
        if self.Mensaje is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<Mensaje>%s</Mensaje>%s' % (
                self.gds_format_integer(self.Mensaje, input_name='Mensaje'), eol_)).encode()))
        if self.DetalleMensaje is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<DetalleMensaje>%s</DetalleMensaje>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.DetalleMensaje), input_name='DetalleMensaje')), eol_)).encode()))
        if self.MontoTotalImpuesto is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<MontoTotalImpuesto>%s</MontoTotalImpuesto>%s' % (
                self.gds_format_float(self.MontoTotalImpuesto, input_name='MontoTotalImpuesto'), eol_)).encode()))
        if self.CodigoActividad is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<CodigoActividad>%s</CodigoActividad>%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.CodigoActividad), input_name='CodigoActividad')), eol_)).encode()))
        # if self.CondicionImpuesto is not None:
        #     showIndent(outfile, level, pretty_print)
        #     outfile.write('<CondicionImpuesto>%s</CondicionImpuesto>%s' % (
        #     self.gds_encode(self.gds_format_string(quote_xml(self.CondicionImpuesto), input_name='CondicionImpuesto')),
        #     eol_))
        # if self.MontoTotalImpuestoAcreditar is not None:
        #     showIndent(outfile, level, pretty_print)
        #     outfile.write('<MontoTotalImpuestoAcreditar>%s</MontoTotalImpuestoAcreditar>%s' % (
        #     self.gds_format_float(self.MontoTotalImpuestoAcreditar, input_name='MontoTotalImpuestoAcreditar'), eol_))
        # if self.MontoTotalDeGastoAplicable is not None:
        #     showIndent(outfile, level, pretty_print)
        #     outfile.write('<MontoTotalDeGastoAplicable>%s</MontoTotalDeGastoAplicable>%s' % (
        #     self.gds_format_float(self.MontoTotalDeGastoAplicable, input_name='MontoTotalDeGastoAplicable'), eol_))
        if self.TotalFactura is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<TotalFactura>%s</TotalFactura>%s' % (
                self.gds_format_float(self.TotalFactura, input_name='TotalFactura'), eol_)).encode()))
        if self.NumeroCedulaReceptor is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<NumeroCedulaReceptor>%s</NumeroCedulaReceptor>%s' % (self.gds_encode(
                self.gds_format_string(quote_xml(self.NumeroCedulaReceptor), input_name='NumeroCedulaReceptor')), eol_)).encode()))
        if self.NumeroConsecutivoReceptor is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('<NumeroConsecutivoReceptor>%s</NumeroConsecutivoReceptor>%s' % (self.gds_encode(
                self.gds_format_string(quote_xml(self.NumeroConsecutivoReceptor),
                                       input_name='NumeroConsecutivoReceptor')), eol_)).encode()))
