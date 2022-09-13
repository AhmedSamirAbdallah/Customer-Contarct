# -*- coding: utf-8 -*-
{
    'name': 'Customer Contract',
    'summary': '',
    'depends': ['base','contacts','sale'],
    'author': 'Ahmed Samir',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/inherited_partner_view.xml',
        'views/customer_contract_view.xml',
        'report/report_view.xml',
        'report/sale_template.xml',
        'data/cron.xml',
    ],
    'demo': [
    ],
    'application': True,
}
