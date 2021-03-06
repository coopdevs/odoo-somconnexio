{
    'name': "Odoo Som Connexió customizations",
    'version': '12.0.0.0.2',
    'depends': [
        'easy_my_coop_es',
        'easy_my_coop_sponsorship',
        'sale_management',
        'contract',
        'web_favicon',
        'web_responsive',
        'web_decimal_numpad_dot',
        'web_no_bubble',
        'web_searchbar_full_width',
    ],
    'author': "Coopdevs Treball SCCL",
    'website': 'https://coopdevs.org',
    'category': "Cooperative management",
    'description': """
    Odoo Som Connexió customizations.
    """,
    "license": "AGPL-3",
    'data': [
        'views/subscription_request_view.xml',
        'views/coop_agreement_view.xml',
        'views/res_partner_view.xml',
        'views/contract_view.xml',
        'views/contract_category_product_view.xml',
        'views/contract_category_service_technology_view.xml',
        'views/service_technology_service_supplier.xml',
        'views/product_pricelist_view.xml',
        'views/product_category_technology_supplier_view.xml',
        'views/menus.xml',
        'security/ir.model.access.csv',
        'data/contract_categories.xml',
        'data/product_categories.xml',
        'data/contract_category_product.xml',
        'data/service_technology.xml',
        'data/contract_category_service_technology.xml',
        'data/service_supplier.xml',
        'data/service_technology_service_supplier.xml',
        'data/product.category.technology.supplier.csv',
    ],
}
