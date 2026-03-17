from typing import Self

from odoo import fields, models


class FluxoEtapa(models.Model):

    # --- Odoo Atributos ---

    _name = 'fluxo.etapa'
    _description = 'Configuração da Etapa'
    _order = 'sequencia, id'
    _rec_name = 'nome'

    # --- Odoo Fields ---

    nome = fields.Char(
        string='Etapa',
        required=True,
        translate=True
    )

    sequencia = fields.Integer(
        string='Sequência',
        default=10
    )

    model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Modelo Alvo',
        required=True,
        ondelete='cascade'
    )

    model_name = fields.Char(
        related='model_id.model',
        string='Modelo Técnico',
        store=True,
        index=True
    )

    etapa_conclusao = fields.Boolean(
        string='Etapa de Conclusão?',
        help='Indica se o processo encerra aqui.'
    )

    etapa_cancelamento = fields.Boolean(
        string='Etapa de Cancelamento?',
        help='Indica se o processo foi cancelado aqui.'
    )

    grupos_permitidos_ids = fields.Many2many(
        comodel_name='res.groups', 
        string='Grupos Permitidos',
        help='Se vazio, todos podem mover para esta etapa.'
    )

    codigo_antes = fields.Text(
        string='Python: Antes de Entrar',
        help=(
            "Execute validações aqui. Use 'registro' para acessar o objeto.'"
            "\nEx: if registro.valor < 0: raise UserError('Erro')"
        )
    )

    codigo_depois = fields.Text(
        string='Python: Depois de Entrar',
        help=(
            "Execute ações pós-gravação.\nEx: registro.message_post"
            "(body='Mudou!')"
        )
    )

    proxima_etapa_ids = fields.Many2many(
        comodel_name='fluxo.etapa',
        relation='fluxo_etapa_proxima_rel',
        column1='etapa_atual_id',
        column2='proxima_etapa_id',
        string='Próximas Etapas Permitidas',
        domain="[('model_id', '=', model_id)]"
    )

    obs = fields.Char(
        string='Observação'
    )

    # --- SQL Constraints ---

    _sql_constraints = [
        (
            'nome_uniq',
            'unique (nome)',
            'Já existe uma etapa com este nome!'
        )
    ]

    # --- Métodos  Odoo Core ---

    def copy(self: Self, default: dict | None = None) -> Self:

        default = dict(default or {})

        if 'nome' not in default:
            default['nome'] = f"{self.nome} (Cópia)"

        return super().copy(default)
