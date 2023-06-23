from odoo import api, models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    state_id = fields.Many2one('res.country.state', inverse='_inverse_state',
                               string="State")
    county = fields.Char(string="County")
    zip = fields.Char(string="ZIP", size=5)
    active = fields.Boolean(string="Active", default=True)
    report_logo = fields.Binary(string="Report Logo")
    support_email = fields.Char(string="Support Email")
    legal_name = fields.Char(string="Legal Name")
    language = fields.Many2one('res.lang', 'Language', required=True)
    decimal_precision = fields.Integer('Decimal Precision')
    date_format = fields.Char(string="Date Format")
    time_format = fields.Char(string="Time Format")
    is_main_company = fields.Boolean(string="Is Main Company", default=False)
    department_ids = fields.One2many('hr.department', 'company_id',
                                     string="Departments")
    division_ids = fields.One2many('res.division', 'company_id',
                                   string="Branches")
    enable_item_code = fields.Boolean(string="Enable Product Code")
    operator_domain = fields.Char(string="Operator Domain")
    base_domain = fields.Char(string="Base Domain")
    exact_domain = fields.Char(string="Exact Domain")
    date_format_selection = fields.Selection(
        [('mdy', 'MM/DD/YYYY'), ('dmy', 'DD/MM/YYYY'),
         ('ymd', 'YYYY/MM/DD')], string="Date Format", default='mdy')
    time_format_selection = fields.Selection(
        [('hm', 'HH:MM'), ('hms', 'HH:MM:SS'), ('imp', 'HH:MM AM/PM'),
         ('ims', 'HH:MM:SS AM/PM')],
        string="Time Format",
        default='hm')

    shipping_zip = fields.Char(size=5)
    shipping_street = fields.Char(string="Street",
                                  default=lambda self: self.street)
    shipping_street2 = fields.Char(string="Street2",
                                   default=lambda self: self.street2)
    shipping_city = fields.Char(string="City", default=lambda self: self.city)
    shipping_county = fields.Char(default=lambda self: self.county)
    shipping_state_id = fields.Many2one('res.country.state', string="State",
                                        default=lambda self: self.state_id.id)
    shipping_country_id = fields.Many2one('res.country', string="Country",
                                          store=True)
    preview_date = fields.Date()
    loaded_coa = fields.Boolean()
