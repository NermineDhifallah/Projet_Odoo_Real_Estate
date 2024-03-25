{
    'name' : "Real Estate",
    'author': 'Nermine Dhifallah',
    'category': '',
    'version' : '17.0.0.1.0',
    'depends':['base',
               'mail',
               ],
    'data':[
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'reports/property_report.xml',

    ],
    "assets":{
      'web.assets_backend': ['app_one\static\src\css\property.css']
    },
    'application': True,
}
