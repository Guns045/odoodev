#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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
        return super(SaleOrder, self).create(vals)

    def write(self, vals):
        # Check if user has permission to edit printed documents
        for record in self:
            if record.x_is_printed and not self.env.user.has_group('sale_flexibility.group_sales_document_editor'):
                # Check if critical fields are being changed
                critical_fields = [
                    'partner_id', 'partner_shipping_id', 'pricelist_id',
                    'payment_term_id', 'currency_id', 'order_line'
                ]

                for field in critical_fields:
                    if field in vals:
                        old_value = getattr(record, field)
                        new_value = vals[field]

                        # For order_line, check if it's being modified
                        if field == 'order_line' and isinstance(new_value, list):
                            if any(command[0] in (0, 1, 2, 3, 4, 5, 6) for command in new_value):
                                raise ValidationError(
                                    _("You cannot modify the order lines of a printed sales order. "
                                      "Contact your administrator if you need to make changes to document '%s'.")
                                    % record.name
                                )
                        elif old_value != new_value:
                            raise ValidationError(
                                _("You cannot modify the '%s' field of a printed sales order. "
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

        return super(SaleOrder, self).write(vals)

    def action_quotation_send(self):
        """Override to set printed flag when sending quotation"""
        result = super(SaleOrder, self).action_quotation_send()
        if self.state in ['sale', 'done']:
            self.x_is_printed = True
            self.message_post(
                body=_("Document marked as printed when sent to customer."),
                message_type='notification'
            )
        return result

    def action_print_quotation(self):
        """Override to set printed flag when printing quotation"""
        result = super(SaleOrder, self).action_print_quotation()
        self.x_is_printed = True
        self.message_post(
            body=_("Document marked as printed when quotation was printed."),
            message_type='notification'
        )
        return result

    def action_confirm(self):
        """Add validation when confirming printed orders"""
        if self.x_is_printed and not self.env.user.has_group('sale_flexibility.group_sales_document_editor'):
            raise UserError(
                _("You cannot confirm a printed sales order without proper permissions. "
                  "Please contact your administrator.")
            )
        return super(SaleOrder, self).action_confirm()

    @api.constrains('amount_total', 'order_line')
    def _check_valid_amounts(self):
        """Validate that totals are correct for printed documents"""
        for order in self:
            if order.x_is_printed and order.state in ['sale', 'done']:
                # Recalculate to ensure totals are correct
                calculated_total = sum(line.price_total for line in order.order_line)
                if abs(order.amount_total - calculated_total) > 0.01:
                    raise ValidationError(
                        _("The total amount does not match the sum of order lines. "
                          "Please recalculate the totals for document '%s'.") % order.name
                    )