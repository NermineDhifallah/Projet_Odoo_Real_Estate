from odoo import models,fields,api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1, default="New")
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff', store=1, readonly=0)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(groups="app_one.property_manager_group")
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], default='north')
    state= fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ], default="draft")

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!')
    ]

    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    line_ids = fields.One2many('property.line', 'property_id')

    owner_address = fields.Char(related="owner_id.address", readonly=0, store=1)
    owner_phone = fields.Char(related="owner_id.phone", readonly=0, store=1)

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Please add valid number of bedrooms!')

    @api.depends('expected_price', 'selling_price')
    def _compute_diff(self):
        for rec in self:
            print('inside compute_diff method')
            rec.diff = abs(rec.expected_price - rec.selling_price)

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print(rec)
            print('inside _onchange_expected_price method')
            return {
                'warning': {'title': 'warning', 'message': 'negative value', 'type': 'notification'}
            }

    def action_draft(self):
        for rec in self:
            print('inside draft action')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            print('inside pending action')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            print('inside sold action')
            rec.state = 'sold'

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action

    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        print("inside create methode")
        return res

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print("inside search methode")
        return res

    @api.model
    def write(self, vals):
        res = super(Property, self).write(vals)
        print("inside write methode")
        return res

    @api.model
    def unlink(self):
        res = super(Property, self).unlink()
        print("inside unlink methode")
        return res


class PropertyLine (models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()
