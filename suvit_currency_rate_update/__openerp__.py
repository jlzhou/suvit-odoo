# -*- coding: utf-8 -*-
{
    'name': 'Сувит. Обновление курса валют',
    'version': '0.0.1',
    'category': 'Suvit',
    'complexity': 'easy',
    'description': """
TODO
    """,
    'author': 'Suvit LLC',
    'depends': [
        'currency_rate_update',
    ],
    'init': [
    ],
    'data': [
        'views/menu.xml',
        'migrations/data/0001_currency_rate_update.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'external_dependencies' : {
        'python' : ['xmltodict'],
    }
}