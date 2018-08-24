# -*- coding: utf-8 -*-
# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api
import logging

logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def render_qweb_pdf(self, res_ids=None, data=None):
        """We go through that method when the PDF is generated for the 1st
        time and also when it is read from the attachment.
        This method is specific to QWeb"""
        pdf_content = super(IrActionsReport, self).render_qweb_pdf(
            res_ids, data)
        invoice_reports = [
            'account.report_invoice',
            'account.account_invoice_report_duplicate_main']
        if (
                len(self) == 1 and
                self.report_name in invoice_reports and
                len(res_ids) == 1 and
                not self._context.get('no_embedded_ubl_xml')):
            invoice = self.env['account.invoice'].browse(res_ids[0])
            pdf_content = invoice.embed_ubl_xml_in_pdf(pdf_content=pdf_content)
        return pdf_content
