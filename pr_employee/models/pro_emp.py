from odoo import models, fields, api
from odoo.exceptions import ValidationError


# La classe `ProjectEmployee` représente l'association entre un employé et un projet,
# le champ `project_id` de type `Many2one` pour choisir un projet,
# et le champ `weighting` de type `Integer` pour spécifier la pondération

class ProjectEmployee(models.Model):
    _name = 'project.employee'
    _description = 'Project Employee'

    project_id = fields.Many2one('project.project', string='Project')
    weighting = fields.Float(string='Weighting', digits=(1, 10))
    active = fields.Boolean(string="Active", default=True)
    employee_ids = fields.Many2many('project.project', 'employee_id', string='Employees')



    @api.constrains('weighting')
    def _check_weighting(self):
        for record in self:
            if record.weighting < 1 or record.weighting > 10:
                raise ValidationError("Weighting must be between 1 and 10.")


#  La classe `ProjectEmployeeTest`
#  hérite de la classe `project.project` existante dans Odoo.
#  ajoute un champ `employee_ids` de type `Many2many` pour stocker les employés associés à un projet

class ProjectEmployeeTest(models.Model):
    _inherit = 'project.project'

    employee_ids = fields.Many2many('hr.employee', string='Employees')
