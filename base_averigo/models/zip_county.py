from odoo import models, fields


class ZipCounty(models.Model):
    _name = 'zip.county'
    _rec_name = 'county'
    _description = "Zip County"

    zip = fields.Char()
    city = fields.Char()
    state = fields.Char()
    county = fields.Char()
    area_codes = fields.Char()
    country = fields.Char()
    latitude = fields.Float()
    longitude = fields.Float()
