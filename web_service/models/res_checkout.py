

from odoo import models, fields


class CheckOut(models.Model):

    _name = 'res.checkout'
    _description = "store checkout details"

    createdate = fields.Datetime()
    # aprivatransactiondate = fields.Char()
    # aprivaresponsedate = fields.Char()
    timestampclient = fields.Char()
    emailid = fields.Char()
    last4 = fields.Char()
    zipcode = fields.Char()
    processstatus = fields.Char()
    processinfo = fields.Char()
    responsecode = fields.Char()
    processorresponsecode = fields.Char()
    processorresponsetext = fields.Char()
    totalamount = fields.Char()
    transactionamount = fields.Char()
    hosttransactionid = fields.Char()
    uniqueidentifier = fields.Char()
    crvamount = fields.Char()
    paymethod = fields.Char()
    taxamount = fields.Char()
    beaconmajor = fields.Char()
    beaconminor = fields.Char()
    payrollstatus = fields.Char()
    payrollstatus = fields.Char()
    payuserid = fields.Char()
    desktype = fields.Char()
    deskuserid = fields.Char()
    cash_amount = fields.Char()
    room_no = fields.Char()


class CheckOutDetails(models.Model):
    _name = 'res.checkout.details'
    _description = "store all checkout data"

    user_id = fields.Many2one('res.app.users')
    item_id = fields.Many2one('product.template')
    itemname = fields.Char()
    checkout_id = fields.Many2one('res.checkout')
    taxable = fields.Selection([('Y', 'Y'), ('N', 'N')])
    tax = fields.Char()
    crvenabled = fields.Selection([('Y', 'Y'), ('N', 'N')])
    crv = fields.Float()
    itemprice = fields.Float()
    itemid = fields.Char()
    quantity = fields.Integer()
    categoryid = fields.Char()
