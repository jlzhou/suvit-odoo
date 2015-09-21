# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class Migration(models.Model):
    _name = 'suvit.migration'
    _description = u"Миграция"

    name = fields.Char(string=u"Название",
                       required=True,
                       )
    description = fields.Text(string=u"Описание",
                              )

    state = fields.Selection(string=u'Состояниe',
                             selection=[('new', u'Получена'),
                                        ('run', u'Выполняется'),
                                        ('done', u'Выполнена'),
                                        ('error', u'Ошибка'),
                                        ('cancel', u'Отменена')],
                             default='new')
    implemented = fields.Boolean(string=u"Выполнена",
                                 compute='compute_implemented',
                                 )

    module_id = fields.Many2one(string=u"Модуль",
                                comodel_name='ir.module.module',
                                compute='compute_model_data',
                                )
    ext_id = fields.Char(string=u"Метод",
                         required=True,
                         )

    @api.multi
    def compute_implemented(self):
        for rec in self:
            rec.implemented = rec.state == 'done'

    @api.one
    @api.constrains('ext_id')
    def check_ext_id(self):
        if not hasattr(self, self.ext_id):
            exceptions.ValidationError(u"Миграция %s не найдена" % self.ext_id)

    @api.multi
    def compute_model_data(self):
        data_obj = self.env['ir.model.data']
        module_obj = self.env['ir.module.module']
        for rec in self:
            data = data_obj.search([('model', '=', rec._name),
                                    ('res_id', '=', rec.id)],
                                   limit=1)
            if data:
                rec.module_id = module_obj.search([('name', '=', data.module)],
                                                  limit=1)

    @api.model
    def run_all(self):
        self.search([('state', '=', 'new')]).run()

    @api.multi
    def run(self):
        for rec in self.filtered(lambda r: not r.implemented):
            try:
                getattr(rec, rec.ext_id)()
            except:
                rec.state = 'error'
            else:
                rec.state = 'done'

    @api.model
    def create(self, values):
        rec = super(Migration, self).create(values)
        rec.run()

        return rec

    @api.multi
    def write(self, values):
        res = super(Migration, self).write(values)
        if values.keys() == ['state']:
            return res
        for rec in self:
            rec.run()

        return res