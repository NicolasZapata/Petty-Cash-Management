{
  'name': 'Petty Cash Management',
  'version': '1.0',
  'description': 'Petty Cash Management',
  'summary': '',
  'author': 'Grupo Quanam Colombia SAS',
  'website': 'grupoquanam.com.co',
  'license': 'LGPL-3',
  'category': '',
  'depends': [
    'hr',
    'hr_expense',
    'account',
    'mail'
  ],
  'data': [
    # Views
    'views/petty_cash_view.xml',
    'views/hr_expense_views.xml',
    # Security
    'security/ir.model.access.csv',
  ],
  # 'demo': [
  #   ''
  # ],
  'auto_install': False,
  'application': False,
  'assets': {
    'web.assets_backend': [
      'petty_cash_management/static/src/scss/petty_cash.scss'
    ]
  }
}