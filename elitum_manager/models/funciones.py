# -*- encoding: utf-8 -*-
#########################################################################
# Copyright (C) 2016 Ing. Harry Alvarez, Elitum Group                   #
#                                                                       #
#This program is free software: you can redistribute it and/or modify   #
#it under the terms of the GNU General Public License as published by   #
#the Free Software Foundation, either version 3 of the License, or      #
#(at your option) any later version.                                    #
#                                                                       #
#This program is distributed in the hope that it will be useful,        #
#but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#GNU General Public License for more details.                           #
#                                                                       #
#You should have received a copy of the GNU General Public License      #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#########################################################################


from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError,except_orm, RedirectWarning, ValidationError
import math

UNIDADES = (
    '', 'Un ', 'Dos ', 'Tres ', 'Cuatro ', 'Cinco ', 'Seis ', 'Siete ', 'Ocho ', 'Nueve ', 'Diez ', 'Once ',
    'Doce ',
    'Trece ', 'Catorce ', 'Quince ', 'Dieciséis ', 'Diecisiete ', 'Dieciocho ', 'Diecinueve ', 'Veinte ')
DECENAS = ('Veinti', 'Treinta ', 'Cuarenta ', 'Cincuenta ', 'Sesenta ', 'Setenta ', 'Ochenta ', 'Noventa ', 'Cien ')
CENTENAS = (
    'Ciento ', 'Doscientos ', 'Trescientos ', 'Cuatrocientos ', 'Quinientos ', 'Seiscientos ', 'Setecientos ',
    'Ochocientos ', 'Novecientos ')

TOTALES = []

class EliterpFunciones(models.TransientModel):

    _name = 'eliterp.funciones'

    def validar_periodo(self,fecha):
        '''Función para validar Fecha de Documento'''
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
        periodo = self.env['account.period'].search([('name','=',fecha.year)])
        if len(periodo)==0:
            raise except_orm("Error", "No hay ningún Período Contable")
        periodo_contable = periodo.lineas_periodo.filtered(lambda x: x.code == fecha.month)
        if len(periodo_contable)==0:
            raise except_orm("Error", "No hay ningún Período Contable")
        fecha_actual= fields.Date.today()
        if datetime.strptime(fecha_actual, "%Y-%m-%d")<datetime.strptime(periodo_contable.fecha_inicio, "%Y-%m-%d"):
            raise except_orm("Error", "La Fecha del registro está fuera del rango del Período")
        if datetime.strptime(fecha_actual, "%Y-%m-%d")>datetime.strptime(periodo_contable.fecha_cierre, "%Y-%m-%d"):
            raise except_orm("Error", "El Período Contable está Cerrado")

    def _get_month_name(self, mes):
        if mes == 1:
            return "Enero"
        if mes == 2:
            return "Febrero"
        if mes == 3:
            return "Marzo"
        if mes == 4:
            return "Abril"
        if mes == 5:
            return "Mayo"
        if mes == 6:
            return "Junio"
        if mes == 7:
            return "Julio"
        if mes == 8:
            return "Agosto"
        if mes == 9:
            return "Septiembre"
        if mes == 10:
            return "Octubre"
        if mes == 11:
            return "Noviembre"
        if mes == 12:
            return "Diciembre"

    def __convertNumber(self, n):
        output = ''
        if (n == '100'):
            output = "Cien "
        elif (n[0] != '0'):
            output = CENTENAS[int(n[0]) - 1]
        k = int(n[1:])
        if (k <= 20):
            output += UNIDADES[k]
        else:
            if ((k > 30) & (n[2] != '0')):
                output += '%sy %s' % (DECENAS[int(n[1]) - 2], UNIDADES[int(n[2])])
            else:
                output += '%s%s' % (DECENAS[int(n[1]) - 2], UNIDADES[int(n[2])])
        return output

    def Numero_a_Texto(self, number_in):
        convertido = ''
        number_str = str(number_in) if (type(number_in) != 'str') else number_in
        number_str = number_str.zfill(9)
        millones, miles, cientos = number_str[:3], number_str[3:6], number_str[6:]
        if (millones):
            if (millones == '001'):
                convertido += 'Un Millon '
            elif (int(millones) > 0):
                convertido += '%sMillones ' % self.__convertNumber(millones)
        if (miles):
            if (miles == '001'):
                convertido += 'Mil '
            elif (int(miles) > 0):
                convertido += '%sMil ' % self.__convertNumber(miles)
        if (cientos):
            if (cientos == '001'):
                convertido += 'Un '
            elif (int(cientos) > 0):
                convertido += '%s ' % self.__convertNumber(cientos)
        return convertido

    def get_amount_to_word(self, j):
        try:
            Arreglo1 = str(j).split(',')
            Arreglo2 = str(j).split('.')
            if (len(Arreglo1) > len(Arreglo2) or len(Arreglo1) == len(Arreglo2)):
                Arreglo = Arreglo1
            else:
                Arreglo = Arreglo2

            if (len(Arreglo) == 2):
                whole = math.floor(j)
                frac = j - whole
                num = str("{0:.2f}".format(frac))[2:]
                return (self.Numero_a_Texto(Arreglo[0]) + 'con ' + num + "/100").capitalize()
            elif (len(Arreglo) == 1):
                return (self.Numero_a_Texto(Arreglo[0]) + 'con ' + '00/100').capitalize()
        except ValueError:
            return "Cero"

    def get_date_format_invoice(self, date):
        mes = self._get_month_name(int(date[5:7]))
        return '%s de %s de %s' % (date[8:], mes, date[:4])