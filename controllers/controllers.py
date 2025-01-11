# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound

class CertificateController(http.Controller):

    @http.route('/cert/<string:uuid>', auth='public', website=True)
    def display_certificate(self, uuid, **kwargs):
        certificate = request.env['phytosanitary.certificate'].sudo().search([('uuid', '=', uuid)], limit=1)
        if not certificate:
           raise NotFound()
        return request.render('efarm_cert.certificate_public_view', {'certificate': certificate})