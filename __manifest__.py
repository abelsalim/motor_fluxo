# -*- coding: utf-8 -*-
{
    'name': "Motor de Fluxos",
    'summary': "Gerenciamento de Etapas, Operações e Histórico Dinâmico",
    'description': """
        Motor base para criação de workflows sem desenvolvimento (No-Code).
        Adiciona capacidades de:
        - Etapas configuráveis por modelo.
        - Operações que definem o início do fluxo.
        - Histórico automático com botão de retrocesso.
        - Automação via Python (antes/depois da etapa).
    """,
    'author': "Abel Salim",
    'category': 'Technical/Workflow',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        # Menu Root
        'views/fluxo_menus.xml',

        # Views
        'views/fluxo_etapa_views.xml',
        'views/fluxo_operacao_views.xml',
        'views/fluxo_demo_views.xml',
        # 'views/fluxo_historico_views.xml'
    ],
    'application': True,
    'installable': True,
}