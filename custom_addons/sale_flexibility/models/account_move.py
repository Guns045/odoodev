#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_is_printed = fields.Boolean(
        string='Is Printed',
        default=False,
        help='Indicates if this document has been printed. Once printed, fields become read-only.',
        copy=False,
        tracking=True,
    )

    @api.model
    def create(self, vals):
        if 'x_is_printed' not in vals:
            vals['x_is_printed'] = False
        return super(AccountMove, self).create(vals)

    def write(self, vals):
        # Check if user has permission to edit printed documents
        for record in self:
            if record.x_is_printed and not self.env.user.has_group('sale_flexibility.group_accounting_document_editor'):
                # Check if critical fields are being changed
                critical_fields = [
                    'partner_id', 'journal_id', 'currency_id', 'invoice_payment_term_id',
                    'invoice_date', 'invoice_date_due', 'invoice_line_ids'
                ]

                for field in critical_fields:
                    if field in vals:
                        old_value = getattr(record, field)
                        new_value = vals[field]

                        # For invoice_line_ids, check if it's being modified
                        if field == 'invoice_line_ids' and isinstance(new_value, list):
                            if any(command[0] in (0, 1, 2, 3, 4, 5, 6) for command in new_value):
                                raise ValidationError(
                                    _("You cannot modify the invoice lines of a printed invoice. "
                                      "Contact your administrator if you need to make changes to document '%s'.")
                                    % record.name
                                )
                        elif old_value != new_value:
                            raise ValidationError(
                                _("You cannot modify the '%s' field of a printed invoice. "
                                  "Contact your administrator if you need to make changes to document '%s'.")
                                % (field, record.name)
                            )

        # Prevent changing x_is_printed to False if it's already True
        if 'x_is_printed' in vals and vals['x_is_printed'] is False:
            for record in self:
                if record.x_is_printed is True:
                    # Prevent unmarking as printed
                    vals['x_is_printed'] = True
                    break

        return super(AccountMove, self).write(vals)

    def action_invoice_print(self):
        """Override to set printed flag when printing invoice"""
        result = super(AccountMove, self).action_invoice_print()
        self.x_is_printed = True
        self.message_post(
            body=_("Document marked as printed when invoice was printed."),
            message_type='notification'
        )
        return result

    def action_print_invoice(self):
        """Override to set printed flag when printing invoice (alternative method)"""
        result = super(AccountMove, self).action_print_invoice()
        self.x_is_printed = True
        self.message_post(
            body=_("Document marked as printed when invoice was printed."),
            message_type='notification'
        )
        return result

    def invoice_print(self):
        """Override to set printed flag when using direct print method"""
        result = super(AccountMove, self).invoice_print()
        self.x_is_printed = True
        self.message_post(
            body=_("Document marked as printed when invoice was printed."),
            message_type='notification'
        )
        return result

    def action_post(self):
        """Add validation when posting printed invoices"""
        if self.x_is_printed and not self.env.user.has_group('sale_flexibility.group_accounting_document_editor'):
            raise UserError(
                _("You cannot post a printed invoice without proper permissions. "
                  "Please contact your administrator.")
            )
        return super(AccountMove, self).action_post()

    @api.constrains('amount_total', 'invoice_line_ids')
    def _check_valid_amounts(self):
        """Validate that totals are correct for printed documents"""
        for move in self:
            if move.x_is_printed and move.state == 'posted':
                # For posted invoices, ensure amounts match
                calculated_total = sum(line.price_subtotal for line in move.invoice_line_ids)
                if abs(move.amount_untaxed - calculated_total) > 0.01:
                    raise ValidationError(
                        _("The untaxed amount does not match the sum of invoice lines. "
                          "Please recalculate the totals for document '%s'.") % move.name
                    )