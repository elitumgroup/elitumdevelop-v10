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
from datetime import datetime,timedelta
from odoo.exceptions import UserError

REASON_OF_EXIT = [
    ('0', 'Por acuerdo de partes'),
    ('1', 'Por la conclusión de la obra, período de labor o servicios objeto del contrato'),
    ('2', 'Por muerte o incapacidad del empleador o extinción de la persona jurídica contratante'),
    ('3', 'Por muerte del trabajador o incapacidad permanente y total para el trabajo'),
    ('4',
     'Por caso fortuito o fuerza mayor que imposibiliten el trabajo, como incendio, terremoto, tempestad, explosión, plagas del campo, guerra y, en general, cualquier otro acontecimiento extraordinario que los contratantes no pudieron prever o que previsto no lo pudieron evitar'),
    ('5', 'Por voluntad del empleador previo visto bueno'),
    ('6', 'Por voluntad del trabajador previo visto bueno'),
    ('7', 'Por desahucio'),
    ('8', 'Por despido Intempestivo'),
    ('9', 'Por terminación del contrato antes del plazo convenido'),
    ('10', 'Por terminación dentro del período de prueba'),
    ('11', 'Por las causas legalmente previstas en el contrato')
]


class hr_employee_documentos_line(models.Model):
    _name = 'hr.employee.documentos.line'

    _description = 'Linea de Documento'

    name = fields.Char('Documento')
    adjunto = fields.Binary('Adjunto')
    hr_employee_documentos_id = fields.Many2one('hr.employee.documentos')


class hr_employee_documentos(models.Model):
    _name = 'hr.employee.documentos'

    _description = 'Documentos'

    def _get_lines_documentos(self, tipo):
        res = []
        if tipo == 1:
            lista_documentos = ['Acuerdo de Confidencialidad',
                                'Aviso de Entrada IESS',
                                'Contrato de Trabajo',
                                'Hoja de Vida',
                                ]
        if tipo == 2:
            lista_documentos = ['Copia de certificados de cursos, seminarios, talleres',
                                'Copia de título o acta de grado',
                                'Copia de título o prefesional registrado en Senescyt',
                                ]
        if tipo == 3:
            lista_documentos = ['Copia a color Cédula de identidad',
                                'Copia a color Certificado de Votación',
                                'Fotografía tamaño carnet a color',
                                ]
        if tipo == 4:
            lista_documentos = ['Copia acta de matrimonio ò declaración juramentada unión libre',
                                'Copia de cédula de cargas familiares',
                                ]
        if tipo == 5:
            lista_documentos = ['Certificado de salud del MSP',
                                'Certificado de trabajo con números de contacto',
                                'Copia de planilla de servicios básicos',
                                'Referencias personales con números de contacto',
                                ]

        if tipo == 6:
            lista_documentos = ['Aviso de Salida IESS',
                                'Acta de Finiquito',
                                ]

        list_lines = []
        for line in lista_documentos:
            list_lines.append([0, 0, {'name': line, }])
        return list_lines

    def _get_lines_ingreso(self):
        res = self._get_lines_documentos(1)
        return res

    def _get_lines_academica(self):
        res = self._get_lines_documentos(2)
        return res

    def _get_lines_personales(self):
        res = self._get_lines_documentos(3)
        return res

    def _get_lines_familiares(self):
        res = self._get_lines_documentos(4)
        return res

    def _get_lines_otros(self):
        res = self._get_lines_documentos(5)
        return res

    def _get_lines_salida(self):
        res = self._get_lines_documentos(6)
        return res

    name = fields.Char('Documentos')
    line_documentos_ingreso = fields.One2many('hr.employee.documentos.line', 'hr_employee_documentos_id', 'Ingreso',
                                              default=_get_lines_ingreso)
    line_documentos_formacion_academica = fields.One2many('hr.employee.documentos.line', 'hr_employee_documentos_id',
                                                          u'Formación Académica', default=_get_lines_academica)
    line_documentos_documentos_personales = fields.One2many('hr.employee.documentos.line', 'hr_employee_documentos_id',
                                                            'Documentos Personales', default=_get_lines_personales)
    line_documentos_cargas_familiares = fields.One2many('hr.employee.documentos.line', 'hr_employee_documentos_id',
                                                        'Cargas Familiares', default=_get_lines_familiares)
    line_documentos_otros = fields.One2many('hr.employee.documentos.line', 'hr_employee_documentos_id', 'Otros',
                                            default=_get_lines_otros)
    line_documentos_salida = fields.One2many('hr.employee.documentos.line', 'hr_employee_documentos_id', 'Salida',
                                             default=_get_lines_salida)
    hr_employee_id = fields.Many2one('hr.employee', 'Empleado')


class hr_employee_codigo_sectorial(models.Model):
    _name = 'hr.employee.codigo.sectorial'

    _description = 'Codigo Sectorial'

    name = fields.Char('Codigo')


class hr_employee_discapacidad_grado(models.Model):
    _name = 'hr.employee.discapacidad.grado'

    _description = 'Grado de Discapacidad'

    name = fields.Char('Grado')
    discapacidad_id = fields.Many2one('hr.employee.discapacidad')


class hr_employee_discapacidad_tipo(models.Model):
    _name = 'hr.employee.discapacidad.tipo'

    _description = 'Tipo de Discapacidad'

    name = fields.Char('Tipo')
    discapacidad_id = fields.Many2one('hr.employee.discapacidad')


class hr_employee_discapacidad(models.Model):
    _name = 'hr.employee.discapacidad'

    _description = 'Discapacidad'

    Discapacidad = fields.Char('Discapacidad')
    discapacidad_grado = fields.One2many('hr.employee.discapacidad.tipo', 'discapacidad_id')
    discapacidad_tipo = fields.One2many('hr.employee.discapacidad.grado', 'discapacidad_id')


class hr_employee_hijos(models.Model):
    _name = 'hr.employee.hijos'

    _description = 'Hijos de Empleados'

    def get_edad_hijos(self):
        for hijo in self:
            if (hijo.fecha_nacimiento):
                edad = (datetime.now().date() - datetime.strptime(hijo.fecha_nacimiento, '%Y-%m-%d').date()).days / 365
            else:
                edad = 0
            hijo.update({'edad': edad})

    name = fields.Char('Nombres')
    identificacion = fields.Char('Identificacion')
    fecha_nacimiento = fields.Date('Fecha de Nacimiento')
    edad = fields.Integer('Edad', readonly=True, compute='get_edad_hijos')
    employee_id = fields.Many2one('hr.employee')


class hr_employee_uniformes(models.Model):
    _name = 'hr.employee.uniformes'

    _description = 'Uniformes de Empleados'

    name = fields.Char('Articulo')
    talla = fields.Char('Talla')
    cantidad = fields.Integer('Cantidad')
    employee_id = fields.Many2one('hr.employee')


class HrEmployeeTipoNotas(models.Model):
    _name = 'hr.employee.tipo.notas'

    _description = 'Tipo de Notas'

    name = fields.Char('Tipo de Notas')


class HrEmployeeHistorialNotas(models.Model):
    _name = 'hr.employee.historial.notas'

    _description = 'Historial de Notas'

    name = fields.Many2one('hr.employee.tipo.notas', 'Tipo de Notas')
    fecha = fields.Date('Fecha Registro')
    comentarios = fields.Text('Comentario')
    fecha_vigencia = fields.Date('Fecha Vigencia')
    employee_id = fields.Many2one('hr.employee', 'Empleado')


class SettlementWizard(models.TransientModel):
    _name = 'eliterp.settlement.wizard'

    _description = 'Formulario de Finiquito'

    def create_settlement(self):
        if self.employee.settlement_id:
            raise UserError(_('El empleado %s ya tiene una liquidación') %self.employee)
        reason = filter(lambda x: x[0] == self.reason_of_exit, REASON_OF_EXIT)
        settlement = self.env['eliterp.settlement'].create({
            'employee': self.employee.id,
            'departure_date': self.departure_date,
            'last_salary': self.last_salary,
            'pending_holidays': self.pending_holidays,
            'reason_of_exit': reason[0][1]
        })
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('elitum_rrhh.eliterp_action_settlement_query')
        form_view_id = imd.xmlid_to_res_id('elitum_rrhh.eliterp_settlement_view_form')
        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'res_id': settlement.id,
            'views': [[form_view_id, 'form']],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }
        return result

    def get_holidays(self, employee):
        data = self.env['reporte.vacaciones.personal'].get_vacaciones(employee)
        global DAYS
        DAYS = 0
        for line in data:
            DAYS += line['vacaciones_disponibles']
        return DAYS

    @api.onchange('employee')
    def onchange_employee(self):
        if self.employee:
            roles = self.env['hr.payslip'].search([
                ('employee_id', '=', self.employee.id),
                ('state', '=', 'done')
            ])
            date_roles = []
            for rol in roles:
                date_roles.append((datetime.strptime(rol.date_from, "%Y-%m-%d")).date())
            date_roles = sorted(date_roles, reverse=True)
            rol = roles.filtered(
                lambda rol: (datetime.strptime(rol.date_from, "%Y-%m-%d")).year == date_roles[0].year
                            and (datetime.strptime(rol.date_from,  "%Y-%m-%d")).month ==  date_roles[0].month)
            self.last_salary = (float(self.employee.sueldo) / float(30)) * float(rol.dias_trabajados)
            self.pending_holidays = self.get_holidays(self.employee)

    employee = fields.Many2one('hr.employee', string='Empleado', domain=[('state_laboral', '=', 'activo')],
                               required=True)
    reason_of_exit = fields.Selection(REASON_OF_EXIT, string='Motivo de Salida', required=True, default='0')
    date_of_admission = fields.Date(related='employee.fecha_ingreso', string='Fecha de Ingreso')
    departure_date = fields.Date('Fecha de Salida', required=True)
    last_salary = fields.Float('Último Sueldo')
    monthly_benefits = fields.Selection(related='employee.acumula_beneficios', string='Acumula Beneficios?')
    pending_holidays = fields.Integer('Vacaciones sin Gozar (Días)')


class hr_employee(models.Model):
    _inherit = 'hr.employee'

    def action_view_settlement(self):
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('elitum_rrhh.eliterp_action_settlement_query')
        form_view_id = imd.xmlid_to_res_id('elitum_rrhh.eliterp_settlement_view_form')
        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'res_id': self.settlement_id.id,
            'views': [[form_view_id, 'form']],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }
        return result

    @api.onchange('birthday')
    def _onchange_birthday(self):
        if self.birthday:
            edad = (datetime.now().date() - datetime.strptime(self.birthday, '%Y-%m-%d').date()).days / 365
            self.edad = edad

    @api.onchange('user_id')
    def _onchange_user(self):
        dump = False

    def get_edad_empleado(self):
        for empleado in self:
            if (empleado.birthday):
                edad = (datetime.now().date() - datetime.strptime(empleado.birthday, '%Y-%m-%d').date()).days / 365
            else:
                edad = 0
            empleado.edad = edad

    @api.one
    def _get_tiempo_laboral(self):
        if not self.fecha_ingreso:
            self.tiempo_laboral = False
        else:
            # MARZ (Calculamos los días luego los meses, cuando sean 13 recibe los FR)
            day_ = 0.0328767  # Equivalencia en meses
            fecha_inicio = datetime.strptime(self.fecha_ingreso, '%Y-%m-%d').date()
            fecha_fin = datetime.today().date()
            days = abs(fecha_fin - fecha_inicio).days
            meses = round(days * day_, 0)
            if meses >= 13:
                self.tiempo_laboral = True

    def action_view_documentos(self):
        documentos_id = self.env['hr.employee.documentos'].search([('hr_employee_id', '=', self[0].id)])
        res = {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee.documentos',
            'view_mode': 'form',
            'view_type': 'form',
        }
        if documentos_id:
            res['res_id'] = documentos_id[0]
            res['context'] = "{}"
        else:
            res['context'] = "{'default_hr_employee_id': " + str(self[0].id) + "}"

        return res

    @api.onchange('nombres', 'apellidos')
    def _onchange_apellidos(self):
        value = {}
        if self.nombres and self.apellidos:
            value['name'] = self.apellidos + ' ' + self.nombres
            return {'value': value}

    # MARZ
    @api.depends('state_laboral')
    @api.onchange('fecha_salida')
    def onchange_fecha_salida(self):
        if self.fecha_salida:
            return self.update({'state_laboral': 'pasivo'})
        else:
            return self.update({'state_laboral': 'activo'})

    @api.depends('attendance_ids')
    def _compute_last_attendance_id(self):
        # Soló ELITUMDEVELOP
        for employee in self:
            employee.last_attendance_id = False

    @api.depends('attendance_ids')
    def _compute_attendance_state(self):
        ahora = datetime.now() - timedelta(hours=5)
        # Soló ELITUMDEVELOP
        state = 'checked_out'
        entradas = []
        for employee in self:
            for registro in employee.attendance_ids:
                object_datetime = datetime.strptime(registro.datetime_check, "%Y-%m-%d %H:%M:%S")
                object_datetime = object_datetime - timedelta(hours=5)
                if registro.type_check.code == 0 and ahora.date() == object_datetime.date():
                    entradas.append(registro.id)
                if len(entradas) > 0:
                    state = 'checked_in'
            employee.attendance_state = state

    historial_notas = fields.One2many('hr.employee.historial.notas', 'employee_id', 'Tipo de Notas')
    nombres = fields.Char('Nombres', required=True)
    apellidos = fields.Char('Apellidos', required=True)
    tiene_dispacidad = fields.Boolean('Tiene Discapacidad?')
    discapacidad_id = fields.Many2one('hr.employee.discapacidad', 'Discapacidad')
    discapacidad_grado = fields.Integer('Grado', size=3)
    discapacidad_tipo = fields.Char('Tipo')
    nivel_educacion = fields.Selection([('basico', u'Educación Basica'),
                                        ('bachiller', 'Bachiller'),
                                        ('tercer', 'Tercer Nivel'),
                                        ('postgrado', 'Postgrado')], u'Nivel de Educación')
    tipo_sangre = fields.Selection([('a_mas', 'A+'),
                                    ('a_menos', 'A-'),
                                    ('b_mas', 'B+'),
                                    ('b_menos', 'B-'),
                                    ('ab_mas', 'AB+'),
                                    ('ab_menos', 'AB-'),
                                    ('o_mas', 'O+'),
                                    ('o_menos', 'O-')], u'Tipo de Sangre')
    state_laboral = fields.Selection([('activo', 'Activo'),
                                      ('pasivo', 'Pasivo')], 'Estado', default='activo')
    fecha_ingreso = fields.Date('Fecha de Ingreso', required=True)
    sueldo = fields.Float('Sueldo', required=True)
    codigo_sectorial_id = fields.Many2one('hr.employee.codigo.sectorial', u'Código Sectorial')
    correo = fields.Char('Correo')
    extension = fields.Char('Extension')
    edad = fields.Integer('Edad', compute='get_edad_empleado')
    direccion = fields.Char(u'Dirección de Domicilio')
    telefono_personal = fields.Char(u'Teléfono Personal')
    conyugue = fields.Char(u'Cónyugue')
    identificacion_conyugue = fields.Char(u'Identificación')
    if_hijos = fields.Boolean('Tiene Hijos?')
    line_hijos = fields.One2many('hr.employee.hijos', 'employee_id', 'Hijos')
    nombre_contacto1 = fields.Char('Contacto')
    parentesco_contacto1 = fields.Char('Parentesco')
    telefono_contacto1 = fields.Char('Telefono')
    nombre_contacto2 = fields.Char('Contacto')
    parentesco_contacto2 = fields.Char('Parentesco')
    telefono_contacto2 = fields.Char('Telefono')
    type_bank_account = fields.Selection([('saving', 'Ahorro'), ('current', 'Corriente')], u'Tipo de Cuenta')
    number_bank = fields.Char('No. Cuenta')
    bank_id = fields.Many2one('res.bank', 'Banco')
    if_uniforme = fields.Boolean('Uniforme?')
    line_uniformes = fields.One2many('hr.employee.uniformes', 'employee_id', 'Uniformes')
    if_tarjeta_comisariato = fields.Boolean('Tarjeta Comisariato?')
    tarjeta_comisariato_cupo = fields.Float('Cupo')
    if_movil = fields.Boolean('Movil?')
    movil_operadora = fields.Selection(
        [('cnt', 'CNT'), ('movistar', 'MOVISTAR'), ('claro', 'CLARO'), ('tuenti', 'TUENTI')], 'Operadora')
    movil_plan = fields.Float('Plan')
    movil_monto_subsidio = fields.Float('Monto Subsidio')
    payroll_structure_id = fields.Many2one('hr.payroll.structure', 'Estructura Salarial', required=True)
    journal_id = fields.Many2one('account.journal', 'Diario Contable')
    no_carnet = fields.Char('No. Carnet')
    account_employee = fields.Many2one('account.account', string="Cuenta Nómina",
                                       domain=[('tipo_contable', '=', 'movimiento')])
    account_advance_payment = fields.Many2one('account.account', string="Cuenta Anticipo",
                                              domain=[('tipo_contable', '=', 'movimiento')])
    analytic_account_id = fields.Many2one('account.analytic.account', 'Centro de Costos')
    project_id = fields.Many2one('eliterp.project', 'Proyecto')
    numero_ausencias = fields.Integer('Ausencias', default=0)
    fecha_salida = fields.Date('Fecha de Salida')
    sexo = fields.Selection([('hombre', 'Hombre'), ('mujer', 'Mujer')], required=True)
    acumula_beneficios = fields.Selection([('si', 'Si'), ('no', 'No')], required=True)
    have_settlement = fields.Boolean('Tiene Finiquito?', default=False)
    settlement_id = fields.Many2one('eliterp.settlement', string='Finiquito')
    tiempo_laboral = fields.Boolean(compute='_get_tiempo_laboral')
    regla_fondo_reserva = fields.Boolean('Regla de Fondos de Reserva',
                                         default=False,
                                         help='Habilitar cuando el empleado tiene varios contratos')  # MARZ (Casos especiales antiguos contratos)
    # Soló ELITUMDEVELOP
    id_biometric = fields.Integer('Id de Biométrico', help='Debe ser el mismo de dispositivo relacionado al empleado')

    _sql_constraints = [
        ('rrhh_hr_employee_id_biometric_unique', 'unique (id_biometric)',
         "El Id de Biométrico debe ser único por Empleado")
    ]


class Holidays(models.Model):
    _inherit = 'hr.holidays'

    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
        ('validate', 'Approved')
    ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='draft',
        help="The status is set to 'To Submit', when a holiday request is created." +
             "\nThe status is 'To Approve', when holiday request is confirmed by user." +
             "\nThe status is 'Refused', when holiday request is refused by manager." +
             "\nThe status is 'Approved', when holiday request is approved by manager.")


# MARZ
class GastosDeduciblesEmpleado(models.Model):
    _name = 'eliterp.tabla.gastos.deducibles'

    _description = 'Tabla Gastos Deducibles Empleado'

    name = fields.Char('Nombre', required=True)
    valor = fields.Float('Valor', required=True)
    status = fields.Boolean('Activo?', default=True)
