#!/usr/bin/env python3
# -*- coding: utf-8 -*-

{
    'name': 'Sales Flexibility Module',
    'version': '15.0.1.0.0',
    'category': 'Sales',
    'summary': 'Flexible editing for sales documents before printing',
    'description': """
Sales Document Flexibility Module
=================================

This module provides enhanced flexibility for editing sales documents before they are printed.

Key Features:
* Allow editing of invoice dates, partner information, and amounts before printing
* Maintain data integrity with print status tracking
* Dynamic field editability based on print status
* Support for Sales Orders, Delivery Orders, and Invoices

Business Benefits:
* Increased operational flexibility
* Reduced errors due to last-minute changes
* Improved user experience for sales teams
* Maintained audit trail with print tracking

Technical Implementation:
* Inherits standard Odoo models (sale.order, stock.picking, account.move)
* Adds print status tracking with x_is_printed field
* Dynamic readonly attributes based on print status
* Security controls for authorized editing

Installation:
* Install via Apps menu or command line
* Requires proper user permissions for document editing
* Compatible with standard Odoo Sales and Accounting workflows

Support:
* Compatible with Odoo Community and Enterprise editions
* Tested with Odoo version 15.0+
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'sale_management',
        'stock',
        'account',
        'base',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/account_move_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 100,
    'images': ['static/description/main.png'],
}