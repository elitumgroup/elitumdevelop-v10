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

from collections import defaultdict
from datetime import datetime, timedelta
from odoo import api, fields, models, _
from itertools import ifilter
import math
from operator import itemgetter

class LineaReporteFlujoCajaIngresos(models.Model):
    _name = 'linea.reporte.flujo.caja.ingresos'

    _description = "Linea Reporte Flujo de Caja Ingresos"

    rubro = fields.Many2one('account.config.reporte.flujo.caja', 'Rubro')
    enero = fields.Float('Enero')
    febrero = fields.Float('Febrero')
    marzo = fields.Float('Marzo')
    abril = fields.Float('Abril')
    mayo = fields.Float('Mayo')
    junio = fields.Float('Junio')
    julio = fields.Float('Julio')
    agosto = fields.Float('Agosto')
    septiembre = fields.Float('Septiembre')
    octubre = fields.Float('Octubre')
    noviembre = fields.Float('Noviembre')
    diciembre = fields.Float('Diciembre')
    total_elementos = fields.Float('Total')
    reporte_flujo_caja_id = fields.Many2one('account.reporte.flujo.caja')


class TotalFlujoCajaEgresos(models.Model):
    _name = 'total.flujo.caja.egresos'

    _description = "Total Flujo de Caja Egresos"

    name = fields.Char('Totales')
    enero = fields.Float('Enero')
    febrero = fields.Float('Febrero')
    marzo = fields.Float('Marzo')
    abril = fields.Float('Abril')
    mayo = fields.Float('Mayo')
    junio = fields.Float('Junio')
    julio = fields.Float('Julio')
    agosto = fields.Float('Agosto')
    septiembre = fields.Float('Septiembre')
    octubre = fields.Float('Octubre')
    noviembre = fields.Float('Noviembre')
    diciembre = fields.Float('Diciembre')
    total_elementos = fields.Float('Total')
    reporte_flujo_caja_id = fields.Many2one('account.reporte.flujo.caja')


class TotalFlujoCajaIngresos(models.Model):
    _name = 'total.flujo.caja.ingresos'

    _description = "Total Flujo de Caja Ingresos"

    name = fields.Char('Totales')
    enero = fields.Float('Enero')
    febrero = fields.Float('Febrero')
    marzo = fields.Float('Marzo')
    abril = fields.Float('Abril')
    mayo = fields.Float('Mayo')
    junio = fields.Float('Junio')
    julio = fields.Float('Julio')
    agosto = fields.Float('Agosto')
    septiembre = fields.Float('Septiembre')
    octubre = fields.Float('Octubre')
    noviembre = fields.Float('Noviembre')
    diciembre = fields.Float('Diciembre')
    total_elementos = fields.Float('Total')
    reporte_flujo_caja_id = fields.Many2one('account.reporte.flujo.caja')


class LineaReporteFlujoCajaEgresos(models.Model):
    _name = 'linea.reporte.flujo.caja.egresos'

    _description = "Linea Reporte Flujo de Caja Egresos"

    rubro = fields.Many2one('account.config.reporte.flujo.caja', 'Rubro')
    enero = fields.Float('Enero')
    febrero = fields.Float('Febrero')
    marzo = fields.Float('Marzo')
    abril = fields.Float('Abril')
    mayo = fields.Float('Mayo')
    junio = fields.Float('Junio')
    julio = fields.Float('Julio')
    agosto = fields.Float('Agosto')
    septiembre = fields.Float('Septiembre')
    octubre = fields.Float('Octubre')
    noviembre = fields.Float('Noviembre')
    diciembre = fields.Float('Diciembre')
    total_elementos = fields.Float('Total')
    reporte_flujo_caja_id = fields.Many2one('account.reporte.flujo.caja')


class AccountReporteFlujoCaja(models.Model):
    _name = 'account.reporte.flujo.caja'

    _description = "Reporte Flujo de Caja"

    def open_reporte(self):
        return self.write({'state': 'open'})

    name = fields.Char('Periodo')
    linea_ingresos = fields.One2many('linea.reporte.flujo.caja.ingresos', 'reporte_flujo_caja_id', 'Ingresos')
    linea_egresos = fields.One2many('linea.reporte.flujo.caja.egresos', 'reporte_flujo_caja_id', 'Egresos')
    linea_totales_ingresos = fields.One2many('total.flujo.caja.ingresos', 'reporte_flujo_caja_id', 'Total Ingresos')
    linea_totales_egresos = fields.One2many('total.flujo.caja.egresos', 'reporte_flujo_caja_id', 'Total Ingresos')
    state = fields.Selection([('draft', 'Borrador'), ('open', 'Iniciado'), ('closed', 'Cerrado')], default='draft')


class LineasAccountFlujoCaja(models.Model):
    _name = 'lines.account.flujo.caja'

    _description = 'Lineas Cuentas Flujo caja'

    account_id = fields.Many2one('account.account', 'Cuenta', domain=[('tipo_contable', '=', 'movimiento')])
    reporte_flujo_caja_id = fields.Many2one('account.config.reporte.flujo.caja')


class AccountConfigReporteFlujoCaja(models.Model):
    _name = 'account.config.reporte.flujo.caja'

    _description = "Config. Reporte Flujo de Caja"

    @api.model
    def create(self, vals):
        res = super(AccountConfigReporteFlujoCaja, self).create(vals)
        if res.tipo == 'ingreso':
            self.env['linea.reporte.flujo.caja.ingresos'].create({'reporte_flujo_caja_id': res.flujo_caja_id.id,
                                                                  'rubro': res.id,
                                                                  'enero': res.valor_mensualizado,
                                                                  'febrero': res.valor_mensualizado,
                                                                  'marzo': res.valor_mensualizado,
                                                                  'abril': res.valor_mensualizado,
                                                                  'mayo': res.valor_mensualizado,
                                                                  'junio': res.valor_mensualizado,
                                                                  'julio': res.valor_mensualizado,
                                                                  'agosto': res.valor_mensualizado,
                                                                  'septiembre': res.valor_mensualizado,
                                                                  'octubre': res.valor_mensualizado,
                                                                  'noviembre': res.valor_mensualizado,
                                                                  'diciembre': res.valor_mensualizado,
                                                                  })
        if res.tipo == 'egreso':
            self.env['linea.reporte.flujo.caja.egresos'].create({'reporte_flujo_caja_id': res.flujo_caja_id.id,
                                                                 'rubro': res.id,
                                                                 'enero': res.valor_mensualizado,
                                                                 'febrero': res.valor_mensualizado,
                                                                 'marzo': res.valor_mensualizado,
                                                                 'abril': res.valor_mensualizado,
                                                                 'mayo': res.valor_mensualizado,
                                                                 'junio': res.valor_mensualizado,
                                                                 'julio': res.valor_mensualizado,
                                                                 'agosto': res.valor_mensualizado,
                                                                 'septiembre': res.valor_mensualizado,
                                                                 'octubre': res.valor_mensualizado,
                                                                 'noviembre': res.valor_mensualizado,
                                                                 'diciembre': res.valor_mensualizado,
                                                                 })

        return res

    name = fields.Char('Nombre')
    lines_account_ids = fields.One2many('lines.account.flujo.caja', 'reporte_flujo_caja_id', 'Cuentas')
    valor_mensualizado = fields.Float('Valor Mensualizado')
    flujo_caja_id = fields.Many2one('account.reporte.flujo.caja', 'Flujo de Caja')
    tipo = fields.Selection([('ingreso', 'Ingreso'), ('egreso', 'Egreso')])


class AccountReportesFinancieros(models.TransientModel):
    _name = 'account.reportes.financieros'

    _description = "Reporte Estado de Situacion Financiera"

    def imprimir_reporte_estado_situacion_financiero(self):
        return self.env['report'].get_action(self, 'elitum_contabilidad.reporte_estado_financiero')

    def imprimir_reporte_estado_situacion_financiero_xls(self):
        reporte = []
        reporte.append(self.id)
        result = {
            'type': 'ir.actions.report.xml',
            'report_name': 'elitum_contabilidad.reporte_situacion',
            'datas': {'ids': reporte},
            'context': {
                'reporte_situacion': True,
                'fecha_inicio': self.fecha_inicio,
                'fecha_fin': self.fecha_fin
            }
        }
        return result

    def get_reporte(self, doc, tipo):
        oject_report = self.env['report.elitum_contabilidad.reporte_estado_financiero']
        cuentas_contables = self.env['account.account'].search([('user_type_id.name', '!=', 'odoo')], order="code")
        cuentas = []
        movimientos = []
        padre = False
        total_movimiento = 0.00
        for cuenta in cuentas_contables:
            if (cuenta.code.split("."))[0] == tipo:
                if cuentas == []:
                    # Cuentas Principales (Sin Movimiento)
                    if tipo == '1':
                        name = "ACTIVOS"
                    if tipo == '2':
                        name = "PASIVOS"
                    if tipo == '3':
                        name = "PATRIMONIO NETO"
                    cuentas.append({'code': self.env['account.account'].search([('code', '=', tipo)])[0].code,
                                    'name': name,
                                    'tipo': 'padre',
                                    'sub_cuenta': [],
                                    'monto': 0.00,
                                    'cuenta': self.env['account.account'].search([('code', '=', tipo)])[0],
                                    'padre': padre})
                else:
                    if cuenta.tipo_contable == 'vista':
                        # Cuentas Vistas
                        padre = oject_report.buscar_padre(cuenta)
                        cuentas = oject_report.update_saldo(cuentas)
                        cuentas.append({'code': cuenta.code,
                                        'tipo': 'vista',
                                        'sub_cuenta': [],
                                        'name': cuenta.name,
                                        'monto': 0.00,
                                        'cuenta': cuenta,
                                        'padre': padre})
                    else:
                        # Cuentas con Movimientos
                        conciliacion_bancaria = []
                        if cuenta.user_type_id.type == 'bank':
                            conciliacion_bancaria = self.env['concilacion.bancaria'].search(
                                [('fecha_inicio', '=', doc['fecha_inicio']),
                                 ('fecha_fin', '=', doc['fecha_fin']),
                                 ('account_id', '=', cuenta.id)])
                            if len(conciliacion_bancaria) != 0:
                                monto_movimiento = conciliacion_bancaria[0].saldo_cuenta
                            else:
                                monto_movimiento = oject_report.get_saldo(cuenta, tipo, doc)
                        else:
                            monto_movimiento = oject_report.get_saldo(cuenta, tipo, doc)
                        padre = oject_report.buscar_padre(cuenta)
                        if cuenta.code:  # Imprimimos Cuentas (tipo = movimiento)
                            print (cuenta.code)
                        index = map(itemgetter('code'), cuentas).index(padre)
                        cuentas[index]['sub_cuenta'].append({'code': cuenta.code,
                                                             'tipo': 'movimiento',
                                                             'name': cuenta.name,
                                                             'monto': round(monto_movimiento, 2)})
                        cuentas[index]['monto'] = cuentas[index]['monto'] + monto_movimiento
            cuentas = oject_report.update_saldo(cuentas)
        if tipo == '3':
            movimientos = []
            cuenta_estado = filter(lambda x: x['code'] == '3.3', cuentas)[0]
            if cuenta_estado['monto'] != 0.00:
                # MARZ
                monto = oject_report.estado_resultado(doc['fecha_inicio'], doc['fecha_fin'])
                movimientos_internos = {}
                if monto >= 0:
                    movimientos_internos['code'] = '3.3.1.1'
                    movimientos_internos['tipo'] = 'movimiento'
                    movimientos_internos['name'] = 'GANANCIA NETA DEL PERIODO'
                    movimientos_internos['monto'] = monto
                else:
                    movimientos_internos['code'] = '3.3.2.1'
                    movimientos_internos['tipo'] = 'movimiento'
                    movimientos_internos['name'] = '(-) PERDIDA NETA DEL PERIODO'
                    movimientos_internos['monto'] = monto
                for cuenta in cuentas:
                    if cuenta['code'] == '3.3':
                        cuenta['sub_cuenta'].append(movimientos_internos)
                return cuentas
            # Si Estado de Resultados es igual a 0
            monto = oject_report.estado_resultado(doc['fecha_inicio'], doc['fecha_fin'])
            if monto >= 0:
                movimientos.append({'code': '3.3.1.1',
                                    'tipo': 'movimiento',
                                    'name': 'GANANCIA NETA DEL PERIODO',
                                    'monto': monto})
            else:
                movimientos.append({'code': '3.3.2.1',
                                    'tipo': 'movimiento',
                                    'name': '(-) PERDIDA NETA DEL PERIODO',
                                    'monto': monto})
            cuentas.append({'code': '3.3',
                            'tipo': 'vista',
                            'sub_cuenta': movimientos,
                            'name': 'RESULTADO DEL EJERCICIO',
                            'monto': monto,
                            'cuenta': False,
                            'padre': False})
            cuentas[0]['monto'] = cuentas[0]['monto'] + monto
        return cuentas

    fecha_inicio = fields.Date('Fecha Inicio', required=True)
    fecha_fin = fields.Date('Fecha Fin', required=True)


class AccountReporteLibroMayor(models.TransientModel):
    _name = 'account.reporte.libro.mayor'

    _description = "Reporte Libro Mayor"

    def imprimir_reporte_libro_mayor(self):
        return self.env['report'].get_action(self, 'elitum_contabilidad.reporte_libro_mayor')

    tipo_reporte = fields.Selection([('all', 'Todas'), ('one', 'Individual')], default='all')
    cuenta = fields.Many2one('account.account', 'Cuenta', domain=[('tipo_contable', '=', 'movimiento')])
    fecha_inicio = fields.Date('Fecha Inicio', required=True)
    fecha_fin = fields.Date('Fecha Fin', required=True)


class AccountReporteEstadoResultado(models.TransientModel):
    _name = 'account.reporte.estado.resultado'

    _description = "Reporte Estado Resultado"

    def imprimir_reporte_estado_resultado(self):
        return self.env['report'].get_action(self, 'elitum_contabilidad.reporte_estado_resultado')

    def imprimir_reporte_estado_resultado_xls(self):
        reporte = []
        reporte.append(self.id)
        result = {
            'type': 'ir.actions.report.xml',
            'report_name': 'elitum_contabilidad.reporte_resultado',
            'datas': {'ids': reporte},
            'context': {
                'reporte_resultado': True,
                'fecha_inicio': self.fecha_inicio,
                'fecha_fin': self.fecha_fin
            }
        }
        return result

    def get_reporte(self, doc, tipo):
        oject_report = self.env['report.elitum_contabilidad.reporte_estado_resultado']
        cuentas_contables = self.env['account.account'].search([('user_type_id.name', '!=', 'odoo')], order="code")
        cuentas_contables = cuentas_contables.filtered(lambda x: (x.code.split("."))[0] == tipo)
        cuentas = []
        movimientos = []
        padre = False
        cuenta_code_comparativo = False
        total_movimiento = 0.00
        for cuenta in cuentas_contables:
            if (cuenta.code.split("."))[0] == tipo:
                if cuentas == []:
                    if tipo == '4':
                        name = "INGRESOS"
                    if tipo == '5':
                        name = "COSTOS Y GASTOS"
                    cuentas.append({'code': self.env['account.account'].search([('code', '=', tipo)])[0].code,
                                    'name': name,
                                    'tipo': 'padre',
                                    'sub_cuenta': [],
                                    'monto': 0.00,
                                    'cuenta': self.env['account.account'].search([('code', '=', tipo)])[0],
                                    'padre': padre})
                else:
                    if cuenta.tipo_contable == 'vista':
                        padre = oject_report.buscar_padre(cuenta)
                        cuentas = oject_report.update_saldo(cuentas)
                        cuentas.append({'code': cuenta.code,
                                        'tipo': 'vista',
                                        'sub_cuenta': [],
                                        'name': cuenta.name,
                                        'monto': 0.00,
                                        'cuenta': cuenta,
                                        'padre': padre})
                    else:
                        padre = oject_report.buscar_padre(cuenta)
                        print (cuenta.code)
                        index = map(itemgetter('code'), cuentas).index(padre)
                        cuentas[index]['sub_cuenta'].append({'code': cuenta.code,
                                                             'tipo': 'movimiento',
                                                             'name': cuenta.name,
                                                             'monto': oject_report.get_saldo(cuenta.id, tipo, doc)})
                        cuentas[index]['monto'] = cuentas[index]['monto'] + oject_report.get_saldo(cuenta.id, tipo, doc)
        cuentas = oject_report.update_saldo(cuentas)
        return cuentas

    fecha_inicio = fields.Date('Fecha Inicio', required=True)
    fecha_fin = fields.Date('Fecha Fin', required=True)
