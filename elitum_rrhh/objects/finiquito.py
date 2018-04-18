# -*- encoding: utf-8 -*-
#########################################################################
# Copyright (C) 2016 Ing. Harry Alvarez, Elitum Group                   #
#                                                                       #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                       #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                       #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#########################################################################

from odoo import api, fields, models, _
from datetime import datetime, timedelta


class Settlement(models.Model):
    _name = 'eliterp.settlement'

    _description = 'Finiquito'

    def confirm(self):
        # Actualizamos contrato y colocamos nombre a registro
        contrato = self.env['hr.contract'].search([('employee_id', '=', self.employee.id)])[0]
        contrato.write({'state_eliterp': 'pasivo'})
        self.write({
            'name': 'Finiquito de %s' % self.employee.name,
            'state': 'confirm'
        })

    @api.one
    @api.depends('employee', 'date_of_admission', 'departure_date')
    def _get_settlement(self):
        departure = datetime.strptime(self.departure_date, "%Y-%m-%d")
        month = departure.month
        # Roles contabilizado del Empleado
        roles = self.env['hr.payslip'].search([
            ('employee_id', '=', self.employee.id),
            ('state', '=', 'done')
        ])
        # Cálculo de Décimo Tercero
        months_13 = []
        if self.monthly_benefits != 'no': # Está acumulando
            if month < 11:
                for x in range(month, 0, -1):
                    months_13.append({'month': x, 'year': departure.year})
                for x in range(12, 11, -1):
                    months_13.append({'month': x, 'year': departure.year - 1})
            if month > 11:
                months_13.append({'month': 12, 'year': departure.year})
            if month == 11:
                months_13.append({'month': month, 'year': departure.year})
        # Cálculo de Décimo Cuarto
        months_14 = []
        if self.monthly_benefits != 'no':  # Está acumulando
            if month > 3:
                for x in range(month, 2, -1):
                    months_14.append({'month': x, 'year': departure.year})
            if month < 3:
                for y in range(month, 0, -1):
                    months_14.append({'month': y, 'year': departure.year})
                for x in range(12, month, -1):
                    months_14.append({'month': x, 'year': departure.year - 1})
            if month == 3:
                months_14.append({'month': month, 'year': departure.year})
        # Información de Décimo Tercero
        data_13 = []
        # Mes actual
        data_13.append({
            'sueldo': self.last_salary,
            'dias': departure.day
        })
        for mes in months_13:
            rol = roles.filtered(lambda rol: (datetime.strptime(rol.date_from, "%Y-%m-%d")).year == mes['year']
                                             and (datetime.strptime(rol.date_from, "%Y-%m-%d")).month == mes['month'])
            if len(rol) != 0:
                data_13.append({
                    'sueldo': rol.input_line_ids.filtered(lambda rol: rol.name == 'Sueldo').amount,
                    'dias': rol.dias_trabajados
                })
        # Información de Décimo Cuarto
        data_14 = []
        # Mes actual
        data_14.append({
            'dias': departure.day
        })
        for mes in months_14:
            rol = roles.filtered(lambda rol: (datetime.strptime(rol.date_from, "%Y-%m-%d")).year == mes['year']
                                             and (datetime.strptime(rol.date_from, "%Y-%m-%d")).month == mes['month'])
            if len(rol) != 0:
                data_14.append({
                    'dias': rol.dias_trabajados
                })
        # Cálculo
        total_13 = float(float(sum((line['sueldo'] * line['dias'] / float(30))/ float(12) for line in data_13)))
        total_14 = float(float(sum((float(386) / float(360)) * line['dias'] for line in data_14)))
        total_vacation = float(float(self.last_salary) / float(30) * float(self.pending_holidays)) # MARZ
        self.total_thirteenth = total_13
        self.total_fourteenth = total_14
        self.total_vacation = total_vacation
        approximate_settlement = total_13 + total_14 + total_vacation
        self.approximate_settlement = approximate_settlement

    # Información
    name = fields.Char('Nombre', default=False)
    employee = fields.Many2one('hr.employee', string='Empleado')
    date_of_admission = fields.Date(related='employee.fecha_ingreso', string='Fecha de Ingreso')
    departure_date = fields.Date('Fecha de Salida')
    last_salary = fields.Float('Último Sueldo')
    monthly_benefits = fields.Selection(related='employee.acumula_beneficios', string='Acumula Beneficios?')
    pending_holidays = fields.Integer('Vacaciones sin Gozar (Días)')
    reason_of_exit = fields.Char(string='Motivo de Salida')  # Colocamos el texto del campo de selección
    # Campos para calcular
    total_thirteenth = fields.Float('Total Decimotercera Remuneración', compute='_get_settlement')
    total_fourteenth = fields.Float('Total Decimocuarta Remuneración', compute='_get_settlement')
    total_vacation = fields.Float('Total Vacaciones', compute='_get_settlement')
    approximate_settlement = fields.Float('Liquidación Aproximada a Recibir', compute='_get_settlement')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirm', 'Confirmado')
    ], default='draft')
