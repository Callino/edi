# © 2015-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def name_get(self):
        """Add amount_untaxed in name_get of invoices"""
        res = super(AccountInvoice, self).name_get()
        if self._context.get('invoice_show_amount'):
            new_res = []
            for (inv_id, name) in res:
                pre = post = ''
                inv = self.browse(inv_id)
                display_currency = inv.currency_id
                if display_currency.position == 'before':
                    pre = u'{symbol}\N{NO-BREAK SPACE}'.format(
                        symbol=display_currency.symbol or '')
                else:
                    post = u'\N{NO-BREAK SPACE}{symbol}'.format(
                        symbol=display_currency.symbol or '')
                name += _('Amount w/o tax: {pre}{0}{post}').format(
                    inv.amount_untaxed, pre=pre, post=post)
                new_res.append((inv_id, name))
            return new_res
        else:
            return res
