{
    'name': 'estate_account',
    'version': '1.0',
    'depends': ['base', 'estate', 'account'],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_account_menu.xml',
    ]
}