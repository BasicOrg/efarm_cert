# -*- coding: utf-8 -*-
import uuid
from odoo import models, fields, api

class PhytosanitaryCertificate(models.Model):
    _name = 'phytosanitary.certificate'
    _description = 'Phytosanitary Certificate'

    name = fields.Char(required = True, copy=False, readonly=True, index=True, default='New')
    exporter_name = fields.Char(string="Name and Address of Exporter")
    consignee_name = fields.Char(string="Name and Address of Consignee")
    means_of_conveyance = fields.Char(string="Means of Conveyance")
    point_of_entry = fields.Char(string="Point of Entry")
    botanical_name = fields.Char(string="Botanical Name of Plant")
    produce_name = fields.Char(string="Name of Produce")
    quantity_declared = fields.Char(string="Quantity Declared")
    additional_declaration = fields.Text(string="Additional Declaration")
    treatment_type = fields.Char(string="Type of Treatment")
    treatment_date = fields.Date(string="Date of Treatment")
    place_of_issue = fields.Char(string="Place of Issue")
    issue_date = fields.Date(string="Date of Issue")
    uuid = fields.Char(string="UUID", compute='_compute_uuid', store=True, index=True, copy=False)


    @api.depends('create_date')
    def _compute_uuid(self):
        for record in self:
            if record.create_date:
                # Convert create_date to a string suitable for UUID generation.
                date_str = record.create_date.strftime('%Y%m%d%H%M%S%f')
                record.uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, date_str))
            else:
                record.uuid = False

    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].next_by_code('phytosanitary.certificate.code')
        res = super(PhytosanitaryCertificate, self).create(values)
        return res