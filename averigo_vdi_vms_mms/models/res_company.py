from odoo import models, fields


class VMSCredentials(models.Model):
    _name = 'vms.credentials'
    _description = 'VMS Credentials'

    operator_id = fields.Many2one('res.company')
    name = fields.Char(required=True)
    vms_id = fields.Char(string="VMS Company Id")
    wsdl_url = fields.Char(required=True, string="WSDL URL")
    vms_username = fields.Char(string="VMS Username")
    vms_password = fields.Char(string="VMS Password")
    vms_api_key = fields.Char(string="VMS API Key")
    vms_license_key = fields.Char(string="VMS License Key")
    is_default = fields.Boolean("Default Credential")

    # TODO: add validation to check only one credentials is default


class ResCompany(models.Model):
    _inherit = 'res.company'

    vms_credentials = fields.One2many('vms.credentials', 'operator_id',
                                      string="VMS Credentials")
    vms_operator_id = fields.Char(string="VMS Operator Id")
