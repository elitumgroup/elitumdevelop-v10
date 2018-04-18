# -*- encoding: utf-8 -*-
#########################################################################
# Copyright (C) 2018 Ing. Mario Rangel, Elitum Group                   #
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

import json
from odoo import models, api, _, fields, SUPERUSER_ID

import datetime


class BeginDashboard(models.Model):
    _name = 'elitumgroup.begin.dashboard'

    _description = 'Tablero de Inicio'


    name = fields.Char('Nombre')
    kanban_dashboard = fields.Text(compute='_kanban_dashboard')
    kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard_graph')
    show_on_dashboard = fields.Boolean(string='Mostrar en Tablero', default=True)
    type_dashboard = fields.Selection([
        ('tipo', 'Tipo de Registro')
    ], string='Tipo de Tablero')
    type = fields.Selection([('bar', 'Barra')], string=u"Tipo de Gráfica")

    @api.one
    def _kanban_dashboard(self):
        self.kanban_dashboard = json.dumps(self.get_journal_dashboard_datas())

    @api.one
    def _kanban_dashboard_graph(self):
        if (self.type in ['bar']):
            self.kanban_dashboard_graph = json.dumps(self.get_bar_graph_datas())

    @api.multi
    def toggle_favorite(self):
        self.write({'show_on_dashboard': False if self.show_on_dashboard else True})
        return False

    @api.multi
    def get_bar_graph_datas(self):
        '''Gráfica de barras'''
        data = []
        # Ausencias
        cantidad_ausencias = 0
        cantidad_ausencias = len(self.env['hr.holidays'].search([('type','=','remove'),('state','=','confirm')]))
        data.append({
            'label': 'Ausencias',
            'value': cantidad_ausencias
        })
        # Caja Chica
        cantidad_caja_chica = 0
        cantidad_caja_chica = len(self.env['petty.cash.replacement'].search([('state', '=', 'para_aprobrar')]))
        data.append({
            'label': 'Caja Chica',
            'value': cantidad_caja_chica
        })
        # Compras - Facturas
        cantidad_facturas = 0
        cantidad_facturas = len(self.env['account.invoice'].search([('type','=','in_invoice'),('line_approval','=','pendiente'), ('state', 'not in',
                ('paid', 'cancel'))]))
        data.append({
            'label': 'Compras - Facturas',
            'value': cantidad_facturas
        })
        # Anticipos de Quincena
        cantidad_anticipos = 0
        cantidad_anticipos = len(self.env['salary.advanced.eliterp'].search([('state', '=', 'para_aprobar')]))
        data.append({
            'label': 'Anticipos de Quincena',
            'value': cantidad_anticipos
        })
        # Roles de Empleados
        cantidad_roles = 0
        cantidad_roles = len(self.env['hr.payslip.run'].search([('state','=','for_approval')]))
        data.append({
            'label': 'Roles de Empleados',
            'value': cantidad_roles
        })
        # Solicitudes de Viáticos
        cantidad_sv = 0
        cantidad_sv = len(self.env['eliterp.provision'].search([('state','=','for_approved')]))
        data.append({
            'label': 'Solicitudes de Viáticos',
            'value': cantidad_sv
        })

        return [{
            'key': 'No. Aprobaciones Pendientes',
            'values': data,
            'flag': False
        }]


    def get_dashboard_1(self):
        data = []
        data = self.get_bar_graph_datas()
        return data[0]['values']

    @api.multi
    def get_journal_dashboard_datas(self):
        '''Información en botones Más'''
        return {
            'dashboard_1': self.get_dashboard_1(),
        }

    @api.multi
    def open_action(self):
        '''Acciones dentro de botones Más'''
        action_name = self._context.get('action_name', False)
        [action] = self.env.ref(action_name).read()
        return action

    # Acción planificada, enviar correo a gerencia con pendientes de aprobar
    @api.multi
    def send_email(self):
        data = self.get_dashboard_1()
        if data:
            html_li = ''
            for line in data:
                if line['value'] != 0:
                    html_li += '<li>' + str(line['value']) + ' --- ' + line['label'] + '</li>'
            body = '<html><head></head><body><h4>Buena día estimado, tiene aprobaciones pendientes en el sistema:</h4><ul>' + html_li + '</ul></body></html>'
            ir_model_data = self.env['ir.model.data']
            try:
                template_id = \
                    ir_model_data.get_object_reference('elitum_inicio', 'eliterp_mail_template_begin')[1]
            except ValueError:
                template_id = False
            template = self.env['mail.template'].browse(template_id)
            if template:
                template.write({'body_html': body})
                template.send_mail(self.id, force_send=True, raise_exception=True)

