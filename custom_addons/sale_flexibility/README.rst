Sales Flexibility Module
========================

This module provides enhanced flexibility for editing sales documents in Odoo before they are printed.

.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.en.html
.. image:: https://img.shields.io/badge/version-15.0.1.0.0-green.svg

Key Features
------------

* **Flexible Document Editing**: Edit invoice dates, partner information, and amounts before printing
* **Print Status Tracking**: Automatic tracking of document print status with `x_is_printed` field
* **Dynamic Field Editability**: Fields become read-only once documents are printed
* **Security Controls**: Role-based permissions for editing printed documents
* **Audit Trail**: Complete tracking of document changes through Odoo's chatter system

Supported Document Types
------------------------

* **Sales Orders**: Full editing flexibility before printing
* **Delivery Orders**: Editable shipping information until printed
* **Invoices**: Flexible invoice date and amount editing before printing

Business Benefits
-----------------

* **Increased Operational Flexibility**: Make last-minute changes without recreating documents
* **Reduced Errors**: Correct mistakes before final printing
* **Improved User Experience**: Sales teams can adjust documents as needed
* **Maintained Data Integrity**: Security controls prevent unauthorized changes

Security Features
-----------------

* **Role-Based Access Control**:
  - Sales Document Editor: Can edit printed sales orders
  - Accounting Document Editor: Can edit printed invoices
  - Stock Document Editor: Can edit printed delivery orders
  - Flexibility Administrator: Full control over all features

* **Data Validation**:
  - Prevents modification of critical fields in printed documents
  - Validates totals and amounts for posted documents
  - Maintains accounting integrity

Installation
------------

1. Copy the module to your Odoo addons directory
2. Update the addons list: ``./odoo-bin -u all --stop-after-init``
3. Install the module via Apps menu or command line:
   ``./odoo-bin -d your_database -i sale_flexibility``

Configuration
-------------

After installation, assign appropriate security groups to users:

* Go to Settings → Users & Companies → Users
* Edit user and select appropriate groups under "Sales Flexibility" category

Usage
-----

**For Regular Users:**
1. Create or edit sales documents as usual
2. Make any necessary changes before printing
3. Once printed, fields become read-only automatically

**For Document Editors:**
1. Users with editor permissions can modify printed documents
2. Changes are tracked in the document's chatter
3. Full audit trail is maintained

**For Administrators:**
1. Configure user permissions through security groups
2. Monitor document changes through audit trails
3. Manage document editing policies

Technical Details
-----------------

**Model Inheritance:**
- ``sale.order``: Added ``x_is_printed`` field and validation
- ``stock.picking``: Added ``x_is_printed`` field and validation
- ``account.move``: Added ``x_is_printed`` field and validation

**Field Behavior:**
- ``x_is_printed``: Boolean field, default False, set to True on print
- Dynamic readonly attributes based on print status
- Tracking enabled for audit purposes

**Security Rules:**
- Record rules prevent editing printed documents without permissions
- Group-based access control for different document types
- Validation constraints maintain data integrity

Troubleshooting
---------------

**Common Issues:**

1. **Cannot edit printed documents**: Ensure user has appropriate security group
2. **Fields still read-only after permissions granted**: Clear cache and refresh browser
3. **Print status not updating**: Check that print actions are being overridden correctly

**Support:**
For technical support or questions, please contact your system administrator.

Changelog
---------

**Version 15.0.1.0.0**
- Initial release
- Basic functionality for Sales Orders, Delivery Orders, and Invoices
- Security groups and validation rules
- Print status tracking
- Dynamic field editability

License
-------

This module is licensed under LGPL-3.

Author
------

Your Company
Website: https://www.yourcompany.com

Maintainer
----------

Your Company Support Team