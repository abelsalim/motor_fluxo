from odoo import fields, models


class FluxoOperacao(models.Model):

    # --- Odoo Atributos ---

    _name = 'fluxo.operacao'
    _description = 'Operação do Fluxo (Template)'
    _order = 'name'

    # --- Odoo Fields ---

    name = fields.Char(
        string='Nome da Operação',
        required=True,
        translate=True
    )

    modelo_id = fields.Many2one(
        comodel_name='ir.model',
        string='Modelo Alvo',
        required=True,
        ondelete='cascade'
    )

    modelo_tecnico = fields.Char(
        related='modelo_id.model',
        store=True,
        index=True
    )

    etapa_inicial_id = fields.Many2one(
        'fluxo.etapa', 
        string='Etapa Inicial',
        required=True,
        domain="[('modelo_id', '=', modelo_id)]",
        help=(
            "Ao selecionar esta operação, o registro irá automaticamente para "
            "esta etapa."
        )
    )
