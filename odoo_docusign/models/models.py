from odoo import models, fields


class DocusignSettingModel(models.Model):
    _name = 'docu.credentials'
    _description = "Docusign Credentials"

    name = fields.Char(string="Name", required=True)
    useremail = fields.Char(string="Email", required=True)
    userpassword = fields.Char(string="Password", required=True)
    auth_key = fields.Char(string="Docusign Integrator Key", required=True)
    account_id = fields.Char(string='Docusign Account Id', required=True)
    user_id = fields.Char(string='Docusign User Id', required=True)
    private_key_id = fields.Many2many('ir.attachment',
                                      string='Private Key File',
                                      required=True)
    company_id = fields.Many2one('res.company', string="Operator",
                                 default=lambda self: self.env.user.company_id,
                                 context={'user_preference': True})


class AdobeSignAgreement(models.Model):
    _name = 'docusign.agreement'

    name = fields.Char(string="Document Name", readonly="1")
    agreement_id = fields.Char(string="Agreement Id", readonly="1")
    customer_agreement_id = fields.Char(string="Agreement Id", readonly="1")
    agreement_status = fields.Char(string="Salesperson Agreement Status")
    customer_agreement_status = fields.Char(string="Customer Agreement Status")
    salesperson_signed = fields.Boolean("Salesperson Signed")
    customer_signed = fields.Boolean("Customer Signed")
    unsigned_file_data_adobesign = fields.Many2many('ir.attachment',
                                                    'unsigneddocuagreement_ir_attachments_rel',
                                                    'unsigneddocuagreement_id',
                                                    'attachment_id',
                                                    'Unsigned Attachments')
    upload_file_data_adobesign = fields.Many2many('ir.attachment',
                                                  'docuagreement_ir_attachments_rel',
                                                  'docuagreement_id',
                                                  'attachment_id',
                                                  'Salesperson Signed Attachments')
    salesperson_signed_file_data_adobesign = fields.Many2many('ir.attachment',
                                                              'customerdocuagreement_ir_attachments_rel',
                                                              'docuagreementsale_id',
                                                              'attachment_id',
                                                              'Customer Signed Attachments')


class AdobeSignAgreementSale(models.Model):
    _name = 'docusignsale.agreement'

    name = fields.Char(string="Document Name", readonly="1")
    agreement_id = fields.Char(string="Agreement Id", readonly="1")
    customer_agreement_id = fields.Char(string="Customer Agreement Id",
                                        readonly="1")
    agreement_status = fields.Char(string="Status")
    customer_agreement_status = fields.Char(string="Customer Agreement Status")
    salesperson_signed = fields.Boolean("Salesperson Signed")
    customer_signed = fields.Boolean("Customer Signed")
    unsigned_file_data_adobesign = fields.Many2many('ir.attachment',
                                                    'unsigneddocuagreementsale_ir_attachments_rel',
                                                    'unsigneddocuagreementsale_id',
                                                    'attachment_id',
                                                    'Unsigned Attachments')
    upload_file_data_adobesign = fields.Many2many('ir.attachment',
                                                  'docuagreementsale_ir_attachments_rel',
                                                  'docuagreementsale_id',
                                                  'attachment_id',
                                                  'Salesperson Signed Attachments')
    salesperson_signed_file_data_adobesign = fields.Many2many('ir.attachment',
                                                              'customerdocuagreementsale_ir_attachments_rel',
                                                              'docuagreementsale_id',
                                                              'attachment_id',
                                                              'Customer Signed Attachments')


class SendDocument(models.Model):
    _name = "docusign.send"
