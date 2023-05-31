# -*- coding: utf-8 -*-
import self as self

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import time
from odoo.tools.translate import _


class MergeTasksLine(models.Model):
    _name = 'base.task.merge.line'

    min_id = fields.Integer(string='MinID', order='min_id asc')
    aggr_ids = fields.Char('Ids')
    zone = fields.Integer(string="Zone")
    zo = fields.Char(string="Zone")
    secteur = fields.Integer(string="Secteur")
    secteur_to = fields.Integer(string="Secteur")
    date_from = fields.Date(string='Wizard')
    date_to = fields.Date(string='Wizard')
    poteau_t = fields.Float('Time Spent')
    is_display = fields.Boolean(string='Ids')
    plans = fields.Char(string='Ids')
    from_int = fields.Integer(string='MinID')
    to_int = fields.Integer(string='MinID')

    wizard_id = fields.Many2one('base.task.merge.automatic.wizard', string='Wizard')
    employee_id = fields.Many2one('hr.employee', string='Wizard')
    plan_id = fields.Many2one('risk.management.response.category', string='Wizard')
    plan_id2 = fields.Many2one('risk.management.response.category', string='Wizard')
    risk_id = fields.Many2one('risk.management.category', string='Wizard')


def onchange_plan_id_(self, plan_id, plan_id2):
    result = {'value': {}}
    total = 0
    if plan_id and plan_id2:
        plan1 = self.env['risk.management.response.category'].browse(plan_id)
        plan2 = self.env['risk.management.response.category'].browse(plan_id2)
        for x in range(plan_id, plan_id2 + 1):
            plan = self.env['risk.management.response.category'].browse(x)
            if plan:
                total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit

        result['value']['plans'] = plan1.plan + '-' + plan2.plan
        return result


def onchange_plans(self, plans):
    result = {'value': {}}
    total = 0
    count = 0
    if plans:
        if plans.count('-') > 1:
            # Replace the osv.except_osv calls with raise ValidationError to raise validation errors.
            raise ValidationError(_('Erreur !'), _('Format Incorrecte!, un seul tiret est autorisé!'))
        elif plans.count('-') == 1 and plans.count(';') == 0:

            # Replace the self.pool.get calls with self.env['model_name'].search to search for records from the respective models.
            # Update the usage of the search method by passing the search criteria directly as arguments.

            tt = self.env['risk.management.response.category'].search([('plan', '=', plans.split('-')[0])])
            tt1 = self.env['risk.management.response.category'].search([('plan', '=', plans.split('-')[1])])
            if not tt:
                raise ValidationError(_('Erreur !'), _('Element n"est pas dans le tableau de relevé!'))
            else:
                t1 = tt[0]
            if not tt1:
                raise ValidationError(_('Erreur !'), _('Element n"est pas dans le tableau de relevé!'))
            else:
                t2 = tt1[0]
            for x in range(t1, t2):

                # Update the self.pool.get('risk.management.response.category').browse calls to use self.env['risk.management.response.category'].browse to retrieve records.

                plan = self.env['risk.management.response.category'].browse(x)
                if plan:
                    total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
        elif plans.count('-') == 1 and plans.count(';') > 0:
            tt = self.env['risk.management.response.category'].search(
                [('plan', '=', (plans.split(';')[0]).split('-')[0])])
            tt1 = self.env['risk.management.response.category'].search(
                [('plan', '=', (plans.split(';')[0]).split('-')[1])])
            if not tt:
                raise ValidationError(_('Erreur !'), _('Element n"est pas dans le tableau de relevé!'))
            else:
                t1 = tt[0]
            if not tt1:
                raise ValidationError(_('Erreur !'), _('Element n"est pas dans le tableau de relevé!'))
            else:
                t2 = tt1[0]
            for x in range(t1, t2):
                plan = self.env['risk.management.response.category'].browse(x)
                if plan:
                    # Replace the list variable name with lst as list is a reserved keyword in Python.

                    total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
                lst = (plans.split(';')[1]).split(';')
                for kk in lst:
                    tt2 = self.env['risk.management.response.category'].search([('plan', '=', kk)])
                    if not tt2:
                        raise ValidationError(_('Erreur !'), _('Element n"est pas dans le tableau de relevé!'))
                    else:
                        plan = self.env['risk.management.response.category'].browse(tt2[0])
                    if plan:
                        total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
        elif plans.count('-') == 0 and plans.count(';') > 0:
            lst = plans.split(';')
            for kk in lst:
                for kk in lst:
                    tt2 = self.env['risk.management.response.category'].search([('plan', '=', kk)])
                    if not tt2:
                        raise ValidationError(_('Erreur !'), _('Element n"est pas dans le tableau de relevé!'))
                    else:
                        plan = self.env['risk.management.response.category'].browse(tt2[0])
                    if plan:
                        total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
        else:
            raise ValidationError(_('Erreur !'),
                                  _('Format Incorrecte!, seuls les tirets "-" ou les points virgules ";" sont autorisés!'))

    result['value']['poteau_t'] = total / 1000
    return result


class EbMergeTasks(models.Model):
    _name = 'base.task.merge.automatic.wizard'
    _description = 'Merge Tasks'

    name = fields.Char(string='Name')

    def name_get(self):
        result = []
        for record in self:
            name = record.name  # Replace 'name' with the field you want to use as the record name
            result.append((record.id, name))
        return result

    @api.model
    def default_get(self, fields_list):
        res = super(EbMergeTasks, self).default_get(fields_list)
        #  I've updated the method signature to use fields_list. Additionally,
        #  I've replaced res['task_ids'] = active_ids with res.update({'task_ids': active_ids})
        #  to ensure the correct behavior in case there are other existing values in the dictionary.
        active_ids = self.env.context.get('active_ids')
        if self.env.context.get('active_model') == 'project.task' and active_ids:
            res.update({'task_ids': active_ids})
        return res

    @api.depends('project_id.user_id')
    def _compute_disponible(self):
        for book in self:
            if book.project_id.user_id.id == self.env.user.id:
                book.disponible = True
            else:
                book.disponible = False

    disponible = fields.Boolean(compute='_compute_disponible', string='Disponible')

    date_from = fields.Date(string='Wizard')
    date_to = fields.Date(string='Wizard')
    project_id = fields.Many2one('project.project', string='Wizard')
    task_id = fields.Many2one('project.task', string='Wizard')
    work_id = fields.Many2one('project.task.work', string='Wizard')
    product_id = fields.Many2one('product.product', string='Wizard')

    choix = fields.Selection([
        ('1', 'Garder Les Taches Sources Actives'),
        ('2', 'Archiver les Taches Sources')

    ],

        string='Priority', select=True)

    type = fields.Selection([
        ('1', 'Nouvelle Subdivision'),
        ('2', 'Modification Subdivision Existante'),
        ('3', 'Ajouter Subdivision A Partir d"une Existante')
    ], string='Type', select=True)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('open', 'Validé')
    ], string='Priority', default='draft', select=True)

    week_no = fields.Selection([
        ('00', '00'),
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('32', '32'),
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
        ('46', '46'),
        ('47', '47'),
        ('48', '48'),
        ('49', '49'),
        ('50', '50'),
        ('51', '51'),
        ('52', '52')
    ], string='Priority', select=True, default=lambda self: str(time.strftime('%W')))

    exist = fields.Boolean(string='Ids', default=True)
    year_no = fields.Char(string='Priority', default=lambda self: str(time.strftime('%Y')))
    is_kit = fields.Boolean(string="Email")
    task_ids = fields.Many2many('project.task', string='Tasks')
    work_ids = fields.Many2many('project.task.work', string='Tasks')
    user_id = fields.Many2one('res.users', string='Assigned to')
    dst_task_id = fields.Many2one('project.task', string='Destination Task')
    dst_project = fields.Many2one('project.project', string='Project')
    line_ids = fields.One2many('base.task.merge.line', 'wizard_id', string='Role Lines', copy=True)
    line_ids1 = fields.One2many('base.group.merge.line2', 'wiz_id', string='Role Lines', copy=True)
   # line_ids2 = fields.One2many('task_line.show.line2', 'wizard_id', string='Role Lines', copy=True)

    zone = fields.Integer(string='Zone')
    secteur = fields.Integer(string='Secteur')

    keep = fields.Selection([
        ('active', 'Actives'),
        ('inactive', 'Archivées'),
        ('both', 'Actives et Archivées')
    ], string='Keep', default='active')


class BaseTaskMergeLine(models.Model):
    _inherit = 'base.task.merge.line'

    wizard_id = fields.One2many('base.task.merge.automatic.wizard')


class BaseGroupMergeLine2(models.Model):
    _inherit = 'base.group.merge.line2'

    wiz_id = fields.One2many('base.task.merge.automatic.wizard')
