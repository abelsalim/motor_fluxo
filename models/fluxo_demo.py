from odoo import models, fields


class FluxoDemoTarefa(models.Model):

    # --- Odoo Atributos ---

    _name = 'fluxo.demo.tarefa'

    _description = 'Tarefa de Demonstração do Fluxo'

    _inherit = ['fluxo.base']

    # --- Odoo Fields ---

    name = fields.Char(
        string='Título da Tarefa',
        required=True
    )

    descricao = fields.Text(
        string='Descrição'
    )

    prioridade = fields.Selection(
        [
            ('0', 'Normal'),
            ('1', 'Alta'),
            ('2', 'Urgente')
        ],
        string='Prioridade',
        default='0',
        widget='priority'
    )
