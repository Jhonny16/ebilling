# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
from .xades.context2 import XAdESContext2, PolicyId2, create_xades_epes_signature
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
import requests
import base64
import logging

_logger = logging.getLogger(__name__)

try:
    from lxml import etree
except (ImportError, IOError) as err:
    logging.info(err)

HACIENDA_URL_BASE = 'https://api.hacienda.go.cr'
HACIENDA_URL_EXONERATION = 'https://api.hacienda.go.cr/fe/ex?'
HACIENDA_VERSION = '4.4'
HACIENDA_API_PROD_URL = 'https://api.comprobanteselectronicos.go.cr/recepcion/v1/'
HACIENDA_API_STAG_URL = 'https://api-sandbox.comprobanteselectronicos.go.cr/recepcion/v1/'
HACIENDA_TOKEN_STAG_URL = 'https://idp.comprobanteselectronicos.go.cr/auth/realms/rut-stag/protocol/openid-connect/token'
HACIENDA_TOKEN_PROD_URL = 'https://idp.comprobanteselectronicos.go.cr/auth/realms/rut/protocol/openid-connect/token'
HACIENDA_RESOLUTION_URL = 'https://tribunet.hacienda.go.cr/docs/esquemas/2016/v4.1/Resolucion_Comprobantes_Electronicos_DGT-R-48-2016.pdf'
HACIENDA_NAMESPACE_URL = 'xmlns="https://cdn.comprobanteselectronicos.go.cr/xml-schemas/v{version}/'.format(version=HACIENDA_VERSION)


def get_economic_activities(vat):
    url_base = HACIENDA_URL_BASE
    end_point = url_base + '/fe/ae?identificacion=' + str(vat)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Host": "api.hacienda.go.cr"
    }
    # Petición GET a la API
    response = requests.get(end_point, headers=headers, timeout=10)
    _logger.info(response.status_code)
    _logger.info(response.text)

    try:
        vals = response.text
        _logger.debug(vals)
    except (
            ValueError,
            TypeError,
            SyntaxError,
    ):  # could not parse a dict from response text
        vals = {}

    return response, vals


def get_exoneration_info(exoneration_number):
    url_base = HACIENDA_URL_EXONERATION
    end_point = url_base + 'autorizacion=' + exoneration_number
    headers = {
        'content-type': 'application/json',
    }

    response = requests.get(end_point, headers=headers, timeout=10)
    _logger.info(response.status_code)
    _logger.info(response.text)

    try:
        vals = response.text
        _logger.debug(vals)
    except (
            ValueError,
            TypeError,
            SyntaxError,
    ):  # could not parse a dict from response text
        vals = {}

    return response, vals


class HaciendaApi:
    def __init__(self, company_id=None):
        self.company_id = company_id
        self._api_prod_url = HACIENDA_API_PROD_URL
        self._api_stag_url = HACIENDA_API_STAG_URL
        self._token_stag_url = HACIENDA_TOKEN_STAG_URL
        self._token_prod_url = HACIENDA_TOKEN_PROD_URL
        self._environment = 'api-stag' if company_id.l10n_cr_test_env else 'api-prod'
        self.cert = company_id.setting_id.p12_file
        self.password = company_id.setting_id.p12_pin

    def generate_signature(self, xml, policy_id):
        # root = etree.fromstring(xml)
        # signature = create_xades_epes_signature()
        # policy = PolicyId2()
        # policy.id = policy_id
        # root.append(signature)
        # ctx = XAdESContext2(policy)
        # private_key, cert, additional_certs = load_key_and_certificates(base64.b64decode(self.cert), self.password.encode())
        # ctx.load_pkcs12(cert, private_key)
        # ctx.sign(signature)
        # return etree.tostring(root,
        #                       encoding="UTF-8",
        #                       method="xml",
        #                       pretty_print=True,
        #                       doctype='<?xml version="1.0" encoding="UTF-8"?>')

        from cryptography.hazmat.backends import default_backend
        policy_id = 'https://www.hacienda.go.cr/ATV/ComprobanteElectronico/docs/esquemas/2016/v4.2/ResolucionComprobantesElectronicosDGT-R-48-2016_4.2.pdf'

        # 3. Convertir bytes a string XML
        decoded_xml = xml.decode('utf-8')
        xml = decoded_xml.replace('&', '&amp;')
        root = etree.fromstring(xml)
        signature = create_xades_epes_signature()
        policy = PolicyId2()
        policy.id = policy_id
        root.append(signature)
        ctx = XAdESContext2(policy)
        certificate = load_key_and_certificates(base64.b64decode(self.cert),
                                                self.password.encode(),
                                                backend=default_backend()
                                                )
        ctx.load_pkcs12(certificate)
        ctx.sign(signature)
        signed = etree.tostring(root,
                                encoding="UTF-8",
                                method="xml",
                                xml_declaration=True,
                                pretty_print=True,
                                with_tail=False)

        return signed

    def getToken(self):
        headers = {}
        data = {'client_id': self._environment,
                'client_secret': '',
                'grant_type': 'password',
                'username': self.company_id.l10n_cr_auth_user,
                'password': self.company_id.l10n_cr_auth_pass,
                }

        if self._environment == 'api-stag':
            endpoint = self._token_stag_url
        else:
            endpoint = self._token_prod_url

        error = False

        try:
            # enviando solicitud post y guardando la respuesta como un objeto json
            response = requests.request("POST", endpoint, data=data, headers=headers)
            response_json = response.json()
            if 200 <= response.status_code <= 299:
                token_hacienda = response_json.get('access_token')
            else:
                error = True
                error_message = 'MAB - token_hacienda failed.  Error: ' + str(response.content)
                _logger.error('MAB - token_hacienda failed.  Error: %s', response.content)

        except requests.exceptions.RequestException as e:
            raise UserError('Error Obteniendo el Token desde MH. Excepcion %s' % e)
            token_hacienda = False

        if error:
            raise UserError(str(error_message))

        return token_hacienda

    def postMH(self, doc, date):
        token = self.getToken()
        headers = {'Authorization': 'Bearer ' +
                                    token, 'Content-type': 'application/json'}

        if self._environment == 'api-stag':
            endpoint = self._api_stag_url + 'recepcion'
        else:
            endpoint = self._api_prod_url + 'recepcion'

        em_ident = doc.company_id.partner_id.identification_id.code
        em_vat = doc.company_id.partner_id.vat
        if doc.partner_id:
            rec_ident = doc.partner_id.identification_id.code
            rec_vat = doc.partner_id.vat

        data = {'clave': doc.name,
                'fecha': date,
                'emisor': {
                    'tipoIdentificacion': em_ident,
                    'numeroIdentificacion': em_vat,
                },
                'comprobanteXml': doc.xml_file.decode()
                }

        if doc.partner_id and doc.partner_id.vat:
            data['receptor'] = {
                'tipoIdentificacion': rec_ident,
                'numeroIdentificacion': rec_vat,
            }

        try:
            response = requests.post(endpoint, json=data, headers=headers)
            _logger.info('\n postMH\n %r\n\n',
                         [response.status_code, response.headers or '', response.reason or '', response])
            if response.status_code != 202:
                error_caused_by = response.headers.get('X-Error-Cause') if 'X-Error-Cause' in response.headers else ''
                error_caused_by += response.headers.get('validation-exception', '')
                if not error_caused_by:
                    error_caused_by += response.reason
                ret = {'status': response.status_code, 'text': error_caused_by}

                return ret
            else:
                return {'status': response.status_code, 'text': response.reason}

        except ImportError:
            raise Warning('Error enviando el XML al Ministerior de Hacienda')

    def getMH(self, doc):
        token = self.getToken()
        if self._environment == 'api-stag':
            url = "%s%s/%s" % (self._api_stag_url, 'recepcion', doc.name)
        else:
            url = "%s%s/%s" % (self._api_prod_url, 'recepcion', doc.name)

        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            return {'status': -1, 'text': 'Excepcion %s' % e}

        if 200 <= response.status_code <= 299:
            _logger.info('\n getMH response.json() \n%r\n\n', response.json())
            response_json = response.json()
            response_json['status'] = response.status_code
        elif 400 <= response.status_code <= 499:
            _logger.info('\n\n%r\n\n', response.status_code)
            response_json = {
                'status': 400,
                'ind-estado': 'error',
            }
        elif response.status_code == 504:
            _logger.info('\n\n%r\n\n', response.status_code)
            response_json = {
                'status': 504,
                'text': 'Timeout'
            }
        else:
            response_json = response.json()
            response_json['status'] = response.status_code
            response_json['text'] = 'token_hacienda failed: %s' % response.reason

        return response_json

    def getHaciendaStatus(self, clave):
        token = self.getToken()
        if self._environment == 'api-stag':
            url = "%s%s/%s" % (self._api_stag_url, 'recepcion', clave)
        else:
            url = "%s%s/%s" % (self._api_prod_url, 'recepcion', clave)

        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            return {'status': -1, 'text': 'Excepcion %s' % e}

        if 200 <= response.status_code <= 299:
            _logger.info('\n getMH response.json() \n%r\n\n', response.json())
            response_json = response.json()
            response_json['status'] = response.status_code
        elif 400 <= response.status_code <= 499:
            _logger.info('\n\n%r\n\n', response.status_code)
            response_json = {
                'status': 400,
                'ind-estado': 'error'
            }
        elif response.status_code == 504:
            _logger.info('\n\n%r\n\n', response.status_code)
            response_json = {
                'status': 504,
                'text': 'Timeout',
            }
        else:
            response_json = response.json()
            response_json['status'] = response.status_code
            response_json['text'] = 'token_hacienda failed: %s' % response.reason

        return response_json

    def postMR(self, data_sent, xml_file):
        token = self.getToken()
        headers = {'Authorization': 'Bearer ' +
                                    token, 'Content-type': 'application/json'}

        if self._environment == 'api-stag':
            endpoint = self._api_stag_url + 'recepcion'
        else:
            endpoint = self._api_prod_url + 'recepcion'

        date = data_sent['date']
        em_ident = data_sent['em_ident']
        em_vat = data_sent['em_vat']
        rec_ident = data_sent['rec_ident']
        rec_vat = data_sent['rec_vat']

        data = {'clave': data_sent['name'],
                'fecha': date,
                'emisor': {
                    'tipoIdentificacion': em_ident,
                    'numeroIdentificacion': em_vat,
                },
                'comprobanteXml': xml_file.decode(),
                'consecutivoReceptor': data_sent['consecutivo']}

        if data_sent['em_vat']:
            data['receptor'] = {
                'tipoIdentificacion': rec_ident,
                'numeroIdentificacion': rec_vat,
            }

        try:
            response = requests.post(endpoint, json=data, headers=headers)
            _logger.info('\n postMR\n %r\n\n',
                         [response.status_code, response.headers or '', response.reason or '', response])
            if response.status_code != 202:
                error_caused_by = response.headers.get('X-Error-Cause') if 'X-Error-Cause' in response.headers else ''
                error_caused_by += response.headers.get('validation-exception', '')
                if not error_caused_by:
                    error_caused_by += response.reason
                ret = {'status': response.status_code, 'text': error_caused_by}

                return ret
            else:
                return {'status': response.status_code, 'text': response.reason}

        except ImportError:
            raise Warning('Error enviando el XML al Ministerior de Hacienda')
