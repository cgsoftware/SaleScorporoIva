# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from tools.translate import _
import decimal_precision as dp
from osv import fields, osv

#
# Dimensions Definition
#
class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    
    _columns = {
                'price_unit_vat': fields.float('Prezzo Ivato', required=False, digits_compute= dp.get_precision('Sale Price'), readonly=True, states={'draft': [('readonly', False)]}),
                }

    def scorporo(self,cr, uid, ids, price_unit,tax_id,price_unit_vat): 
            #import pdb;pdb.set_trace()
            v = {}
            if price_unit_vat<>0:
              if tax_id:
                taxes = self.pool.get('account.tax').browse(cr,uid,tax_id[0][2])[0]
                v['price_unit'] = price_unit_vat/(1+taxes.amount)
                
            else:
                v['price_unit'] = price_unit
            return {'value': v}
          
    def aggiunge_iva(self,cr, uid, ids, price_unit,tax_id,price_unit_vat):
        v = {}
        if price_unit<>0:
          if tax_id:
                taxes = self.pool.get('account.tax').browse(cr,uid,tax_id[0][2])[0]
                v['price_unit_vat'] = price_unit*(1+taxes.amount)
          else:
                v['price_unit_vat'] = price_unit_vat
          return {'value': v}
          
          
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
      result = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, packaging, fiscal_position, flag)
      #import pdb;pdb.set_trace()
      if result['value'].get('price_unit',False):
        if result['value'].get('tax_id',False):
          tax_id = result['value']['tax_id']
          taxes = self.pool.get('account.tax').browse(cr,uid,tax_id)[0]
          result['value']['price_unit_vat'] = result['value']['price_unit']*(1+taxes.amount)
      return result
        
sale_order_line()


