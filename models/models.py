# -*- coding: utf-8 -*-
import uuid
from odoo import models, fields, api

class PhytosanitaryCertificate(models.Model):
    _name = 'phytosanitary.certificate'
    _description = 'Phytosanitary Certificate'
    _inherit = ['mail.thread']

    activity_ids = fields.One2many('mail.activity', 'res_id', string='Activities', domain=[('res_model', '=', 'phytosanitary.certificate')])
    name = fields.Char(required = True, copy=False, readonly=True, index=True, default='')
    state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled')
    ], string='State', default='new', required=True, tracking=True)
    exporter_name = fields.Many2one('phytosanitary.exporter', string="Name and Address of Exporter")
    consignee_name = fields.Many2one('phytosanitary.consignee', string="Name and Address of Consignee")
    to_protection_organization = fields.Many2one('phytosanitary.protection.organization', string="To the Protection Organization of")
    means_of_conveyance = fields.Many2one('phytosanitary.conveyance.method', string="Means of Conveyance")
    point_of_entry = fields.Many2one('phytosanitary.entry.point', string="Point of Entry")
    place_of_origin = fields.Many2one('phytosanitary.origin.place', string="Place of Origin")
    produce_name = fields.Many2one('phytosanitary.produce.name', string="Name of Produce")
    botanical_name = fields.Many2one('phytosanitary.botanical.name', string="Botanical Name of Plant")
    packages_number_description = fields.Char(string="Number and Description of Packages")
    distinguishing_marks = fields.Char(string="Distinguishing Marks")
    quantity_declared = fields.Float(string="Quantity Declared")
    quantity_uom = fields.Many2one('phytosanitary.uom', string="Unit of Measurement")
    additional_declaration = fields.Text(string="Additional Declaration")
    disinfection_treatment_type = fields.Many2one('phytosanitary.disinfection.treatment.type', string="Type of Treatment")
    disinfection_chemical_ingredient = fields.Many2one('phytosanitary.disinfection.chemical.ingredient', string="Chemical Ingredient")
    disinfection_duration_and_temperature = fields.Char(string="Duration and Temperature")
    disinfection_concentration = fields.Char(string="Concentration")
    disinfection_date = fields.Date(string="Date of Disinfection")
    disinfection_additional_info = fields.Text(string="Additional Information")
    certificate_place_of_issue = fields.Many2one("phytosanitary.certificate.issue.place", string="Place of Issue")
    certificate_issue_date = fields.Date(string="Date of Issue")
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


    def action_confirm(self):
        """Confirm the certificate and generate certificate number"""
        for record in self:
            if record.state == 'new':
                # Generate certificate number when confirming
                certificate_number = self.env['ir.sequence'].next_by_code('phytosanitary.certificate.code')
                record.write({
                    'name': certificate_number,
                    'state': 'confirmed',
                    'certificate_issue_date': fields.Date.today()
                })

    def action_cancel(self):
        """Cancel the certificate"""
        for record in self:
            if record.state in ('new', 'confirmed'):
                record.write({'state': 'canceled'})

    def action_reset_to_new(self):
        """Reset certificate to new state"""
        for record in self:
            if record.state in ('confirmed', 'canceled'):
                record.write({'state': 'new'})

    @api.onchange('produce_name')
    def _onchange_produce_name(self):
        if not self.botanical_name and self.produce_name and self.produce_name.botanical_name_id:
            self.botanical_name = self.produce_name.botanical_name_id

    @api.onchange('botanical_name')
    def _onchange_botanical_name(self):
        if not self.produce_name and self.botanical_name and self.botanical_name.produce_name_id:
            self.produce_name = self.botanical_name.produce_name_id
    

    def write(self, values):
        res = super().write(values)
        if 'produce_name' in values and 'botanical_name' in values:
            if not self.produce_name.botanical_name_id and not self.botanical_name.produce_name_id:
                self.produce_name.botanical_name_id = self.botanical_name.id
                self.botanical_name.produce_name_id = self.produce_name.id
        return res


class PhytosanitaryExporter(models.Model):
    _name = 'phytosanitary.exporter'
    _description = 'Phytosanitary Exporter'
    _rec_name = 'name'

    name = fields.Char(string="Exporter Name", required=True)
    address = fields.Text(string="Address")
    contact_person = fields.Char(string="Contact Person")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    partner_id = fields.Many2one('res.partner', string="Related Contact", ondelete='cascade')

    @api.model
    def create(self, values):
        # Create corresponding res.partner
        partner_vals = {
            'name': values.get('name', ''),
            'street': values.get('address', ''),
            'phone': values.get('phone', ''),
            'email': values.get('email', ''),
            'is_company': True
        }
        partner = self.env['res.partner'].create(partner_vals)
        values['partner_id'] = partner.id
        return super(PhytosanitaryExporter, self).create(values)

    def write(self, values):
        result = super(PhytosanitaryExporter, self).write(values)
        # Update corresponding res.partner
        for record in self:
            if record.partner_id:
                partner_vals = {}
                if 'name' in values:
                    partner_vals['name'] = values['name']
                if 'address' in values:
                    partner_vals['street'] = values['address']
                if 'phone' in values:
                    partner_vals['phone'] = values['phone']
                if 'email' in values:
                    partner_vals['email'] = values['email']
                if partner_vals:
                    record.partner_id.write(partner_vals)
        return result

    def unlink(self):
        # Delete corresponding res.partner (cascade)
        partners = self.mapped('partner_id')
        result = super(PhytosanitaryExporter, self).unlink()
        partners.unlink()
        return result


class PhytosanitaryConsignee(models.Model):
    _name = 'phytosanitary.consignee'
    _description = 'Phytosanitary Consignee'
    _rec_name = 'name'

    name = fields.Char(string="Consignee Name", required=True)
    address = fields.Text(string="Address")
    contact_person = fields.Char(string="Contact Person")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    partner_id = fields.Many2one('res.partner', string="Related Contact", ondelete='cascade')

    @api.model
    def create(self, values):
        # Create corresponding res.partner
        partner_vals = {
            'name': values.get('name', ''),
            'street': values.get('address', ''),
            'phone': values.get('phone', ''),
            'email': values.get('email', ''),
            'is_company': True
        }
        partner = self.env['res.partner'].create(partner_vals)
        values['partner_id'] = partner.id
        return super(PhytosanitaryConsignee, self).create(values)

    def write(self, values):
        result = super(PhytosanitaryConsignee, self).write(values)
        # Update corresponding res.partner
        for record in self:
            if record.partner_id:
                partner_vals = {}
                if 'name' in values:
                    partner_vals['name'] = values['name']
                if 'address' in values:
                    partner_vals['street'] = values['address']
                if 'phone' in values:
                    partner_vals['phone'] = values['phone']
                if 'email' in values:
                    partner_vals['email'] = values['email']
                if partner_vals:
                    record.partner_id.write(partner_vals)
        return result

    def unlink(self):
        # Delete corresponding res.partner (cascade)
        partners = self.mapped('partner_id')
        result = super(PhytosanitaryConsignee, self).unlink()
        partners.unlink()
        return result


class PhytosanitaryProtectionOrganization(models.Model):
    _name = 'phytosanitary.protection.organization'
    _description = 'Phytosanitary Protection Organization'
    _rec_name = 'name'

    name = fields.Char(string="Organization Name", required=True)


class PhytosanitaryConveyanceMethod(models.Model):
    _name = 'phytosanitary.conveyance.method'
    _description = 'Phytosanitary Conveyance Method'
    _rec_name = 'name'

    name = fields.Char(string="Conveyance Method", required=True)


class PhytosanitaryEntryPoint(models.Model):
    _name = 'phytosanitary.entry.point'
    _description = 'Phytosanitary Entry Point'
    _rec_name = 'name'

    name = fields.Char(string="Entry Point Name", required=True)


class PhytosanitaryOriginPlace(models.Model):
    _name = 'phytosanitary.origin.place'
    _description = 'Phytosanitary Place of Origin'
    _rec_name = 'name'

    name = fields.Char(string="Place of Origin", required=True)


class PhytosanitaryProduceName(models.Model):
    _name = 'phytosanitary.produce.name'
    _description = 'Phytosanitary Produce Name'
    _rec_name = 'name'

    name = fields.Char(string="Produce Name", required=True)
    botanical_name_id = fields.Many2one('phytosanitary.botanical.name', string="Botanical Name")

    def write(self, values):
        if 'botanical_name_id' in values and not self.env.context.get('skip_product_name_link'):
            if values.get('botanical_name_id'):
                self.botanical_name_id.with_context({'skip_product_name_link': True}).produce_name_id = self.id
            else:
                self.botanical_name_id.with_context({'skip_product_name_link': True}).produce_name_id = False
        result = super().write(values)
        return result


class PhytosanitaryBotanicalName(models.Model):
    _name = 'phytosanitary.botanical.name'
    _description = 'Phytosanitary Botanical Name'
    _rec_name = 'name'

    name = fields.Char(string="Botanical Name", required=True)
    produce_name_id = fields.Many2one('phytosanitary.produce.name', string="Common Produce Name")

    def write(self, values):
        result = super().write(values)
        if 'produce_name_id' in values and not self.env.context.get('skip_product_name_link'):
            if values.get('produce_name_id'):
                self.produce_name_id.with_context({'skip_product_name_link': True}).botanical_name_id = self.id
            else:
                self.produce_name_id.with_context({'skip_product_name_link': True}).botanical_name_id = False
        return result


class PhytosanitaryUom(models.Model):
    _name = 'phytosanitary.uom'
    _description = 'Phytosanitary Unit of Measurement'
    _rec_name = 'name'

    name = fields.Char(string="Unit Name", required=True)


class PhytosanitaryDisinfectionTreatmentType(models.Model):
    _name = 'phytosanitary.disinfection.treatment.type'
    _description = 'Phytosanitary Disinfection Treatment Type'
    _rec_name = 'name'

    name = fields.Char(string="Treatment Type", required=True)


class PhytosanitaryDisinfectionChemicalIngredient(models.Model):
    _name = 'phytosanitary.disinfection.chemical.ingredient'
    _description = 'Phytosanitary Disinfection Chemical Ingredient'
    _rec_name = 'name'

    name = fields.Char(string="Chemical Name", required=True)


class PhytosanitaryCertificateIssuePlace(models.Model):
    _name = 'phytosanitary.certificate.issue.place'
    _description = 'Phytosanitary Certificate Issue Place'
    _rec_name = 'name'

    name = fields.Char(string="Issue Place", required=True)