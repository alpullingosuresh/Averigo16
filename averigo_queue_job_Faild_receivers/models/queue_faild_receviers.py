from odoo import models, fields


class QueueJobFaildRecevers(models.Model):
    _name = "queue.faild.receivers"
    _rec_name = "job_functions_id"

    job_functions_id = fields.Many2one('queue.job.function', string="Job Function")
    faild_receivers = fields.Char(string="Mail Receivers")
