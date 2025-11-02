#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

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
        return super(StockPicking, self).create(vals)

    def write(self, vals):
        # Check if user has permission to edit printed documents
        for record in self:
            if record.x_is_printed and not self.env.user.has_group('sale_flexibility.group_stock_document_editor'):
                # Check if critical fields are being changed
                critical_fields = [
                    'partner_id', 'location_id', 'location_dest_id', 'origin',
                    'scheduled_date', 'priority', 'move_ids_without_package'
                ]

                for field in critical_fields:
                    if field in vals:
                        old_value = getattr(record, field)
                        new_value = vals[field]

                        # For move_ids_without_package, check if it's being modified
                        if field == 'move_ids_without_package' and isinstance(new_value, list):
                            if any(command[0] in (0, 1, 2, 3, 4, 5, 6) for command in new_value):
                                raise ValidationError(
                                    _("You cannot modify the stock moves of a printed delivery order. "
                                      "Contact your administrator if you need to make changes to document '%s'.")
                                    % record.name
                                )
                        elif old_value != new_value:
                            raise ValidationError(
                                _("You cannot modify the '%s' field of a printed delivery order. "
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

        return super(StockPicking, self).write(vals)

    def action_print_delivery_slip(self):
        """Override to set printed flag when printing delivery slip"""
        result = super(StockPicking, self).action_print_delivery_slip()
        self.x_is_printed = True
        self.message_post(
            body=_("Document marked as printed when delivery slip was printed."),
            message_type='notification'
        )
        return result

    def do_print_picking(self):
        """Override to set printed flag when doing picking operations"""
        result = super(StockPicking, self).do_print_picking()
        self.x_is_printed = True
        self.message_post(
            body=_("Document marked as printed when picking operations were printed."),
            message_type='notification'
        )
        return result

    def action_validate(self):
        """Add validation when validating printed delivery orders"""
        if self.x_is_printed and not self.env.user.has_group('sale_flexibility.group_stock_document_editor'):
            raise UserError(
                _("You cannot validate a printed delivery order without proper permissions. "
                  "Please contact your administrator.")
            )
        return super(StockPicking, self).action_validate()

    def button_validate(self):
        """Override button_validate for consistency"""
        return self.action_validate()