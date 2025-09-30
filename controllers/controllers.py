# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound, Forbidden
import base64

class CertificateController(http.Controller):

    @http.route('/cert/<string:uuid>', auth='public', website=True)
    def display_certificate(self, uuid, **kwargs):
        certificate = request.env['phytosanitary.certificate'].sudo().search([('uuid', '=', uuid)], limit=1)
        if not certificate:
           raise NotFound()
        
        # Fetch attachments for this certificate
        attachments = request.env['ir.attachment'].sudo().search([
            ('res_model', '=', 'phytosanitary.certificate'),
            ('res_id', '=', certificate.id)
        ])
        
        return request.render('efarm_cert.certificate_public_view', {
            'certificate': certificate,
            'attachments': attachments
        })

    @http.route('/cert/<string:uuid>/attachment/<int:attachment_id>', type='http', auth='public')
    def download_certificate_attachment(self, uuid, attachment_id, download=None, **kwargs):
        """Public endpoint to download certificate attachments"""
        # Verify certificate exists
        certificate = request.env['phytosanitary.certificate'].sudo().search([('uuid', '=', uuid)], limit=1)
        if not certificate:
            raise NotFound("Certificate not found")
        
        # Verify attachment exists and belongs to this certificate
        attachment = request.env['ir.attachment'].sudo().search([
            ('id', '=', attachment_id),
            ('res_model', '=', 'phytosanitary.certificate'),
            ('res_id', '=', certificate.id)
        ], limit=1)
        
        if not attachment:
            raise Forbidden("Attachment not found or does not belong to this certificate")
        
        # Prepare response
        if attachment.datas:
            file_content = base64.b64decode(attachment.datas)
        else:
            raise NotFound("Attachment content not found")
        
        # Set proper headers
        headers = [
            ('Content-Type', attachment.mimetype or 'application/octet-stream'),
            ('Content-Length', len(file_content)),
        ]
        
        # Add download header if requested
        if download:
            headers.append(('Content-Disposition', f'attachment; filename="{attachment.name}"'))
        else:
            headers.append(('Content-Disposition', f'inline; filename="{attachment.name}"'))
        
        return request.make_response(file_content, headers)