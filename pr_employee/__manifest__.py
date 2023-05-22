{
    'name': "Project Employee",
    'version': '1.0.0',
    'category': 'Project Management',
    'author': "Med Fares",
    'summary': 'Project Employee system',
    'description': """ Project Employee System """,
    'depends': ['hr', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
    ],
    'demo': [],

    'auto-install': False,
    'installable': True,
    'license': 'LGPL-3',
    'application': True,
}
