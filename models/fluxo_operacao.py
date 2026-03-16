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

    model_id = fields.Many2one(
        related='etapa_inicial_id.model_id',
        store=True
    )

    model_name = fields.Char(
        related='model_id.model',
        store=True,
        index=True
    )

    etapa_inicial_id = fields.Many2one(
        comodel_name='fluxo.etapa',
        string='Etapa Inicial',
        required=True,
        help=(
            "Ao selecionar esta operação, o registro irá automaticamente para "
            "esta etapa."
        )
    )
