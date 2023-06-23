from odoo import models, fields


class SendGridApiConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    send_grid_api_check = fields.Boolean(string="SendGrid API")
    send_grid_api_value = fields.Char(string='API key',
                                      config_parameter='sendgrid.api_value')

    def set_values(self):
        """ save values in the settings fields """

        super(SendGridApiConfig, self).set_values()
        company_id = self.env.company
        self.env['ir.config_parameter'].sudo().set_param("send_grid_api_check",
                                                         self.send_grid_api_value)
        self.env['ir.config_parameter'].sudo().set_param("send_grid_api_value",
                                                         self.send_grid_api_value)

    def get_values(self):
        res = super(SendGridApiConfig, self).get_values()
        send_grid_api_check = self.env['ir.config_parameter'].sudo().get_param(
            "send_grid_api_check",
            False)
        send_grid_api_value = self.env['ir.config_parameter'].sudo().get_param(
            "send_grid_api_value",
            False)
        # res.update(send_grid_api_value=str("**************" if send_grid_api_value else ""))
        res.update(send_grid_api_check=bool(send_grid_api_check))
        return res

    def pick_report_template(self, headers):
        print("Picking report template")
        payload = json.dumps({
            "name": "AveriGo Inventory - Pick Report",
            "generation": "dynamic"
        })
        conn = http.client.HTTPSConnection("api.sendgrid.com")
        # selecting the template
        template = self.env.ref('web_service.pick_order_report')
        if template and not template.temp_id:
            print("template", template)
            conn.request("POST", "/v3/templates", payload, headers)
            res = conn.getresponse()
            _logger.info("Create Reconcile Report response")
            print("reason", res.reason)
            # _logger.info(res.text)
            print("response reconsile", res.reason)
            temp_data = json.loads(res.read())
            temp_code = temp_data.get('id')
        elif template and template.temp_id:
            print("templappp")
            temp_code = template.temp_id
        print("temp code", temp_code)
        template.temp_id = temp_code
        print("temp_code", temp_code)
        template.sedgrid_readonly = True
        # Creating Template Version
        html_body = """
        <div ><b>User Name:&nbsp;</b>{{user_name}}</div>
<div><b>Micromarket:&nbsp;</b>{{market_name}}</div>
<div ><b>Order Number:&nbsp;</b>{{OrderNo}}</div>
<div ><b>Version:&nbsp;</b>{{version_number}}</div>
<table>
	<tbody>
		<tr>
			<td style="padding: 7.5pt">
				<div style="margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif"><b>Item Name</b><u></u><u></u></div>
			</td>
			<td style="padding: 5pt">
				<div style="margin: 0in; font-size: 11pt;font-family: Calibri, sans-serif"><b>Order Qty</b><u></u><u></u></div>
			</td>
			<td style="padding: 5pt">
				<div style="margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif"><b>Pick Qty</b><u></u><u></u></div>
			</td>
		</tr>{{#each move_ids_without_package}}
		<tr>
			<td style="padding:7.5pt">
				<div style="margin:0in;font-size:11pt;font-family:Calibri,sans-serif">{{product_name}}<u></u><u></u></div>
			</td>
			<td style="padding:0.75pt">
				<div style="margin:0in;font-size:11pt;font-family:Calibri,sans-serif;text-align:center">{{product_uom_qty}}<u></u><u></u></div>
			</td>
			<td style="padding:0.75pt">
				<div style="margin:0in;font-size:11pt;font-family:Calibri,sans-serif;text-align:center">{{picking_qty}}<u></u><u></u></div>
			</td>
		</tr>{{/each}}</tbody>
</table>"""
        payload = json.dumps({
            "template_id": template.temp_id,
            "active": 1,
            "name": "AveriGo Inventory - Pick Report",
            "html_content": html_body,
            "generate_plain_content": False,
            "subject": "AveriGo Inventory - Pick Report -  {{ market_name }}",
            "editor": "design",
            "plain_content": "labore dolore"
        })
        conn.request("POST", "/v3/templates/" + template.temp_id + "/versions",
                     payload, headers)
        res = conn.getresponse()
        if res.status in [200, 201]:
            print("response data:", res.status)
            template.version_status = 'success'
            conn.close()
            return "Success"
        else:
            print("faild reason", res.reason)
            # print("response data:", res.status, res.text)
            _logger.info("Receive Reconcile Report text failed")
            # _logger.info(res.text)
            template.version_status = 'failed'
            conn.close()
            return "Failed"

    def reconcile_report_template(self, headers, html_body):
        # Create reconsile report template
        payload = json.dumps({
            "name": "AveriGo Inventory - Reconcile Report",
            "generation": "dynamic"
        })
        # Creating connection with sendgrid
        conn = http.client.HTTPSConnection("api.sendgrid.com")
        # selecting the template
        template = self.env.ref('web_service.send_inventory_report')
        # checking the template have a template id
        if template and not template.temp_id:
            print("template", template)
            conn.request("POST", "/v3/templates", payload, headers)
            res = conn.getresponse()
            _logger.info("Create Reconcile Report response")
            print("reason", res.reason)
            # _logger.info(res.text)
            print("response reconsile", res.reason)
            temp_data = json.loads(res.read())
            temp_code = temp_data.get('id')
        elif template and template.temp_id:
            print("templappp")
            temp_code = template.temp_id
        template.temp_id = temp_code
        print("temp_code", temp_code)
        template.sedgrid_readonly = True
        # Creating Template Version
        payload = json.dumps({
            "template_id": template.temp_id,
            "active": 1,
            "name": "AveriGo Inventory - Reconcile Report",
            "html_content": html_body,
            "generate_plain_content": False,
            "subject": "AveriGo Inventory - Reconcile Report  {{ market_name }}",
            "editor": "design",
            "plain_content": "labore dolore"
        })
        conn.request("POST", "/v3/templates/" + template.temp_id + "/versions",
                     payload, headers)
        res = conn.getresponse()
        if res.status in [200, 201]:
            print("response data:", res.status)
            template.version_status = 'success'
            conn.close()
            return "Success"
        else:
            print("faild reason", res.reason)
            # print("response data:", res.status, res.text)
            _logger.info("Receive Reconcile Report text failed")
            # _logger.info(res.text)
            template.version_status = 'failed'
            conn.close()
            return "Failed"

    def sopilage_report_template(self, headers, html_body):
        "Creating Spoilage template and version"
        template = self.env.ref('web_service.spoilage_inventory_report')

        payload = json.dumps({
            "name": "AveriGo Inventory - Spoilage Report",
            "generation": "dynamic"})
        conn = http.client.HTTPSConnection("api.sendgrid.com")
        if template and not template.temp_id:
            conn.request("POST", "/v3/templates", payload, headers)
            res = conn.getresponse()
            _logger.info("Create Spoilage Report response")
            # _logger.info(res.text)
            print("response spoilage", res.reason)
            temp_data = json.loads(res.read())
            temp_code = temp_data.get('id')
        elif template and template.temp_id:
            temp_code = template.temp_id
        template.temp_id = temp_code
        template.sedgrid_readonly = True
        payload = json.dumps({
            "template_id": template.temp_id,
            "active": 1,
            "name": "AveriGo Inventory - Spoilage Report",
            "html_content": html_body,
            "generate_plain_content": False,
            "subject": "AveriGo Inventory - Spoilage Report  {{ market_name }}",
            "editor": "design",
            "plain_content": "labore dolore"
        })
        conn.request("POST", "/v3/templates/" + template.temp_id + "/versions",
                     payload, headers)
        res = conn.getresponse()
        if res.status in [200, 201]:
            print("response data:", res.msg)
            template.version_status = 'success'
            conn.close()
            return "Success"
        else:
            print("response data:", res.status, res.reason)
            _logger.info("Receive Spoilage Report text failed")
            # _logger.info(res.text)
            template.version_status = 'failed'
            conn.close()
            return "Failed"

    def receive_report_template(self, headers):
        # Creating Receive Report Template
        template = self.env.ref('web_service.open_order_report')
        payload = json.dumps({"name": "AveriGo Inventory - Receive Report",
                              "generation": "dynamic"})
        conn = http.client.HTTPSConnection("api.sendgrid.com")
        if template and not template.temp_id:
            conn.request("POST", "/v3/templates", payload, headers)
            res = conn.getresponse()
            print("response Receive", res.reason)
            _logger.info("Create Receive Report response")
            temp_data = json.loads(res.read())
            temp_code = temp_data.get('id')
        elif template and template.temp_id:
            temp_code = template.temp_id
        template.temp_id = temp_code
        template.sedgrid_readonly = True
        html_body = """
        <div ><b>User Name:&nbsp;</b>{{user_email}}</div>
        <div ><b>Micromarket:&nbsp;</b>{{market_name}}</div>
        <div ><b>Order Number:&nbsp;</b>{{version_number}}</div>
        <div ><b>Version:&nbsp;</b>{{app_version}}</div>
    <table>
    <tbody>
      <tr>
         <td style="padding: 7.5pt">
            <div style="margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif"><b>Item Name</b><u></u><u></u></div>
         </td>
         <td style="padding: 5pt">
            <div style="margin: 0in; font-size: 11pt;font-family: Calibri, sans-serif"><b>Starting Qty</b><u></u><u></u></div>
         </td>
         <td style="padding: 5pt">
            <div style="margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif"><b>Added/Reduced Qty</b><u></u><u></u></div>
         </td>
         <td style="padding: 5pt">
            <div style="margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif"><b>Ending Qty</b><u></u><u></u></div>
         </td>
         <td style="padding: 5pt">
            <div style="margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif"><b>Product Status</b><u></u><u></u></div>
         </td>
      </tr>
      {{#each reconciliation_ids}} {{#notEquals this.item_status 'Not reconciled'}}
      <tr>
         <td style="padding: 7.5pt">
            <div style="margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif">{{ this.product_name }}<u></u><u></u></div>
         </td>
         <td style="padding: 0.75pt">
            <div style="margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;">{{ this.start_qty }}<u></u><u></u></div>
         </td>
         <td style="padding: 0.75pt">
            <div style="margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;">{{ this.add_qty }}<u></u><u></u></div>
         </td>
         <td style="padding: 0.75pt">
            <div style="margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;">{{ this.end_qty }}<u></u><u></u></div>
         </td>
         {{#equals this.item_status 'Received More'}}
         <td style="background-color: #ffa500; padding: 2.25pt">
            <div style="margin: 0in;font-size: 11pt;font-family:Calibri,sans-serif;text-align:center;"><span>{{ this.item_status }}</span><u></u><u></u></div>
         </td>
         {{/equals}} {{#equals this.item_status 'Received'}}
         <td style="background-color: #2ab357; padding: 2.25pt">
            <div style="margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;"><span>{{ this.item_status }}</span><u></u><u></u></div>
         </td>
         {{/equals}} {{#equals this.item_status 'Received Less'}}
         <td style="background-color: #ffa500; padding: 2.25pt">
            <div style="margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;"><span>{{this.item_status }}</span><u></u><u></u></div>
            {{/equals}}
      </td></tr>
      {{/notEquals}}{{/each}}
    </tbody>
    </table>
    """
        payload = json.dumps({
            "template_id": template.temp_id,
            "active": 1,
            "name": "AveriGo Inventory - Receive Report",
            "html_content": html_body,
            "generate_plain_content": False,
            "subject": "AveriGo Inventory - Receive Report  {{ market_name }}",
            "editor": "design",
            "plain_content": "labore dolore"
        })
        conn.request("POST", "/v3/templates/" + template.temp_id + "/versions",
                     payload, headers)
        res = conn.getresponse()
        if res.status in [200, 201]:
            print("response data:", res.status)
            template.version_status = 'success'
            conn.close()
            return "Success"
        else:
            # print("response data:", res.status, res.text)
            _logger.info("Receive Report Response text failed")
            # _logger.info(res.text)
            template.version_status = 'failed'
            conn.close()
            return "Failed"

        # Creating Terminal Online Template'

    def create_terminal_offline(self, headers):
        template = self.env.ref('web_service.email_template_terminal_offline')
        payload = json.dumps(
            {'name': "GrabScanGo Terminal OFFLINE", "generation": "dynamic"})
        conn = http.client.HTTPSConnection("api.sendgrid.com")
        if template and not template.temp_id:
            conn.request("POST", "/v3/templates", payload, headers)
            res = conn.getresponse()
            print("response Receive", res.reason)
            _logger.info("Create Receive Report response")
            temp_data = json.loads(res.read())
            temp_code = temp_data.get('id')
        elif template and template.temp_id:
            temp_code = template.temp_id
        print("old", template.temp_id, temp_code)
        template.temp_id = temp_code
        template.sedgrid_readonly = True
        html_body = """<html>
               <head>
                  <div >
                     <div style="text-align:center;border:black solid 1px;border-radius:10px;min-width: 20%;max-width: 70%;min-height:100%;max-height:100%;">
                        <h2>OFFLINE - {{market}} - {{operator}} </h2>
                        <hr>
                        <div style="font-size:17x">Market name: {{market}}<br>
                           Device ID:&nbsp;{{deviceid}}<br>
                           Beacons:&nbsp;{{beacon_major}}:{{beacon_minor}}<br>
                           Version:&nbsp;{{version}}<br>
                           Last Beat: {{last_beat}} {{timezone}}
                           <br>Error Code:3
                        </div>
                     </div>
                  </div>
                  </body>
            </html>
            """
        payload = json.dumps({
            "template_id": template.temp_id,
            "active": 1,
            "name": "OFFLINE - {{market}} - {{operator}}",
            "html_content": html_body,
            "generate_plain_content": False,
            "subject": "OFFLINE - {{{market}}} - {{operator}}",
            "editor": "design",
            "plain_content": "labore dolore"
        })
        conn.request("POST", "/v3/templates/" + template.temp_id + "/versions",
                     payload, headers)
        res = conn.getresponse()
        if res.status in [200, 201]:
            print("response data:", res.status)
            template.version_status = 'success'
            conn.close()
            return "Success"
        else:
            # print("response data:", res.status, res.text)
            _logger.info("Receive Report Response text failed")
            # _logger.info(res.text)
            template.version_status = 'failed'
            conn.close()
            return "Failed"

    def create_terminal_online(self, headers):
        template = self.env.ref('web_service.email_template_terminal_online')
        payload = json.dumps(
            {"name": "GrabScanGo TerminalBACK ONLINE", "generation": "dynamic"})
        conn = http.client.HTTPSConnection("api.sendgrid.com")
        if template and not template.temp_id:
            conn.request("POST", "/v3/templates", payload, headers)
            res = conn.getresponse()
            print("response Receive", res.reason)
            _logger.info("Create Receive Report response")
            temp_data = json.loads(res.read())
            temp_code = temp_data.get('id')
        elif template and template.temp_id:
            temp_code = template.temp_id
        template.temp_id = temp_code
        template.sedgrid_readonly = True
        html_body = """<html>
       <head>
          <div >
             <div style="text-align:center;border:black solid 1px;border-radius:10px;min-width: 20%;max-width: 70%;min-height:100%;max-height:100%;">
                <h2>ONLINE - {{market}} - {{operator}} </h2>
                <hr>
                <div style="font-size:17x">Market name: {{market}}<br>
                   Device ID:&nbsp;{{deviceid}}<br>
                   Beacons:&nbsp;{{beacon_major}}:{{beacon_minor}}<br>
                   Version:&nbsp;{{version}}<br>
                   <br>Error Code:3
                </div>
             </div>
          </div>
          </body>
    </html>
    """
        payload = json.dumps({
            "template_id": template.temp_id,
            "active": 1,
            "name": "ONLINE - {{market}} - {{operator}}",
            "html_content": html_body,
            "generate_plain_content": False,
            "subject": "ONLINE - {{{market}}} - {{operator}}",
            "editor": "design",
            "plain_content": "labore dolore"
        })
        print("payload", payload)
        conn.request("POST", "/v3/templates/" + template.temp_id + "/versions",
                     payload, headers)
        res = conn.getresponse()
        if res.status in [200, 201]:
            print("response data:", res.status)
            template.version_status = 'success'
            conn.close()
            return "Success"
        else:
            # print("response data:", res.status, res.text)
            _logger.info("Receive Report Response text failed")
            # _logger.info(res.text)
            template.version_status = 'failed'
            conn.close()
            return "Failed"

    def create_sendgrid_template(self):
        """Function to create SendGrid Template"""
        api_key = self.env['ir.config_parameter'].sudo().get_param(
            'sendgrid.api_value')
        if not api_key:
            raise UserError(_("It Needs API Key"))
        headers = {
            'Authorization': "Bearer " + api_key + "",
            'Content-Type': 'application/json'
        }
        # saved the html body of reconcile report in this function, so we can reuse in spoilage template
        html_body = """
        <div ><b>User Name:&nbsp;</b>{{user_email}}</div>
        <div><b>Micromarket:&nbsp;</b>{{market_name}}</div>
        <div ><b>Version:&nbsp;</b>{{app_version}}</div>
        <table>
            <tbody>
              <tr>
                 <td style='padding: 7.5pt'>
                    <div style='margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif'><strong>Item Name</strong></div>
                 </td>
                 <td style='padding: 5pt'>
                    <div style='margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif'><strong>Starting Qty</strong></div>
                 </td>
                 <td style='padding: 5pt'>
                    <div style='margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif'><strong>Added/Reduced Qty</strong></div>
                 </td>
                 <td style='padding: 5pt'>
                    <div style='margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif'><strong>Ending Qty</strong></div>
                 </td>
                 <td style='padding: 5pt'>
                    <div style='margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif'><strong>Product Status</strong></div>
                 </td>
              </tr>
              {{#each reconciliation_ids}}{{#notEquals this.item_status 'Not reconciled'}}
              <tr>
                 <td style='padding: 7.5pt'>
                    <div style='margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif'>{{ this.product_name }}</div>
                 </td>
                 <td style='padding: 0.75pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'>{{ this.start_qty }}</div>
                 </td>
                 <td style='padding: 0.75pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'>{{ this.add_qty }}</div>
                 </td>
                 <td style='padding: 0.75pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'>{{ this.end_qty }}</div>
                 </td>
                 {{#equals this.item_status 'Shrinkage'}}
                 <td style='background-color: #ff0000; padding: 2.25pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'><span>{{ this.item_status }}</span></div>
                 </td>
                 {{/equals}}{{#equals this.item_status 'Reconciled'}}
                 <td style='background-color: #2ab357; padding: 2.25pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'><span>{{ this.item_status }}</span></div>
                 </td>
                 {{/equals}}{{#equals this.item_status 'Overage'}}
                 <td style='background-color: #2ab357; padding: 2.25pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'><span>{{ this.item_status }}</span></div>
                 </td>
                 {{/equals}}{{#equals this.item_status 'Sent to Warehouse'}}
                 <td style='background-color: #2ab357; padding: 2.25pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'><span>{{ this.item_status }}</span></div>
                 </td>
                 {{/equals}}{{#equals this.item_status 'Spoilage'}}
                 <td style='background-color: #f3ff00; padding: 2.25pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'><span>{{ this.item_status }}</span></div>
                 </td>
                 {{/equals}}{{#equals this.item_status 'Theft'}}
                 <td style='background-color: #f3ff00; padding: 2.25pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'><span>{{ this.item_status }}</span></div>
                 </td>
                 {{/equals}}{{#equals this.item_status 'Other'}}
                 <td style='background-color: #2ab357; padding: 2.25pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'><span>{{ this.item_status }}</span></div>
                 </td>
              </tr>
              {{/equals}}</tr>{{/notEquals}}{{/each}}{{#each reconciliation_ids}}{{#equals this.item_status 'Not reconciled'}}
              <tr>
                 <td style='padding: 7.5pt'>
                    <div style='margin: 0in; font-size: 11pt; font-family: Calibri, sans-serif'>{{ this.product_name }}</div>
                 </td>
                 <td style='padding: 0.75pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'>{{ this.start_qty }}</div>
                 </td>
                 <td style='padding: 0.75pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'>{{ this.add_qty }}</div>
                 </td>
                 <td style='padding: 0.75pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'>{{ this.end_qty }}</div>
                 </td>
                 <td style='background-color: #b4b3b3; padding: 2.25pt'>
                    <div style='margin: 0in;font-size: 11pt;font-family: Calibri, sans-serif;text-align: center;'><span>{{ this.item_status }}</span></div>
                 </td>
              </tr>
              {{/equals}}{{/each}}
            </tbody>
            </table>
            """
        # reconcile_report_response = self.reconcile_report_template(headers, html_body)
        # print("Reconcile Report Response -------------------", reconcile_report_response)
        # _logger.info("------------Reconcile Report Template Response ------------------")
        # _logger.info(reconcile_report_response)
        #
        # spoilage_report_response = self.sopilage_report_template(headers, html_body)
        # print("Spoilage Report Response --------------------", spoilage_report_response)
        # _logger.info("------------Spoilage Report Template Response ------------------")
        # _logger.info(spoilage_report_response)
        # #
        # receive_report_response = self.receive_report_template(headers)
        # print("Receive Report Response ----------------------", receive_report_response)
        # _logger.info("------------Receive Report Template Response ------------------")
        # _logger.info(receive_report_response)

        receive_terminal_response = self.create_terminal_online(headers)
        print("Receive Terminal Response ----------------------",
              receive_terminal_response)
        _logger.info(
            "------------Receive Report Template Response ------------------")
        _logger.info(receive_terminal_response)

        # report_pick_response = self.pick_report_template(headers)
        # print("Receive Picking Response ----------------------", report_pick_response)
        # _logger.info("------------Receive Report Template Response ------------------")
        # _logger.info(receive_terminal_response)
        #
        report_terminal_response = self.create_terminal_offline(headers)
        print("terminal offline Response ------- ", report_terminal_response)
        _logger.info(
            "------------Terminal Offline Template Response ------------------")
        _logger.info(report_terminal_response)
