from odoo import models, fields


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    temp_id = fields.Char(string="Template ID")
    generation = fields.Char(string="Template Generation", default="Dynamic",
                             readonly=True)
    version_status = fields.Selection(
        [('success', 'Success'), ('failed', 'Failed To Create')])
    ver_editor = fields.Selection([('design', "Design"), ('code', "Code")],
                                  string="Version Editor", default="design")
    sedgrid_readonly = fields.Boolean(string="SendGrid Readonly Template",
                                      default=False)


class EmailTemplateDetails(models.Model):
    _name = "email.template"
    _rec_name = "temp_name"
    _description = "SendGrid Template Details"

    temp_name = fields.Char(string="Template Name", required=True)
    operator_id = fields.Many2one('res.company',
                                  default=lambda self: self.env.company)
    generation = fields.Char(string="Template Generation", default="Dynamic",
                             readonly=True)
    ver_name = fields.Char(string="Version Name")
    ver_subject = fields.Char(string="Version Subject", required=True)
    ver_editor = fields.Selection([('design', "Design"), ('code', "Code")],
                                  string="Version Editor", default="design")
    temp_cont = fields.Html(string="Template Content",
                            help="content convert to html code", translate=True,
                            sanitize=False)
    temp_id = fields.Char(string="Template ID")
    version_status = fields.Selection(
        [('success', 'Success'), ('Ffailed', 'Failed To Create')])

    def create_temp(self):
        """
        function is used for creating Mail Template

        """
        api_key = ""
        company_id = self.env.company
        temp_name = self.temp_name
        temp_gen = self.generation
        api_info = self.env['ir.config_parameter'].search(
            [('key', '=', "send_grid_api_value" + "")])
        print(api_info.value)
        if not api_info:
            raise UserError(_("It Needs API Key"))
        api_key = api_info.value
        conn = http.client.HTTPSConnection("api.sendgrid.com")

        payload = "{\"name\":\"" + temp_name + "\",\"generation\":\"dynamic\"}"

        headers = {
            'authorization': "Bearer " + api_key + "",
            'content-type': "application/json"
        }

        conn.request("POST", "/v3/templates", payload, headers)

        res = conn.getresponse()
        data = res.read()
        print("response data:", data)

        temp_data = json.loads(data.decode("utf-8"))
        print("temp_data", temp_data)
        self.temp_id = temp_data['id']

    def create_ver(self):
        """
        Function is used for creating mail content to the
        Created Template.

        """
        api_key = ""
        if self.temp_cont:
            company_id = self.env.company
            temp_cont = self.temp_cont
            temp_id = self.temp_id
            ver_name = self.ver_name
            ver_sub = self.ver_subject
            api_info = self.env['ir.config_parameter'].search(
                [('key', '=', "send_grid_api_value" + "")])
            if not api_info:
                raise UserError(_("It Needs API Key"))
            api_key = api_info.value
            conn = http.client.HTTPSConnection("api.sendgrid.com")
            upt_temp_cnt = (temp_cont.replace('"', ''))
            if not temp_id:
                raise UserError(_("Please create a template first"))
            payload = "{\"template_id\":\"" + temp_id + "\",\"active\":1,\"name\":\"" + ver_name + "\",\"html_content\":\"" + upt_temp_cnt + "\",\"plain_content\":\"<%body%>\",\"subject\":\"" + ver_sub + "\"}"

            headers = {
                'authorization': "Bearer " + api_key + "",
                'content-type': "application/json"
            }

            conn.request("POST", "/v3/templates/" + temp_id + "/versions",
                         payload, headers)
            res = conn.getresponse()
            if res.status in [200, 201]:
                self.version_status = 'success'
            else:
                self.version_status = 'failed'
            data = res.read()
