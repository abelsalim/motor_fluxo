from odoo import fields, models


class FluxoEtapa(models.Model):

    # --- Odoo Atributos ---

    _name = 'fluxo.etapa'

    _description = 'Configuração da Etapa'

    _order = 'sequencia, id'

    # --- Odoo Fields ---

    name = fields.Char(
        string='Nome da Etapa',
        required=True,
        translate=True
    )

    sequencia = fields.Integer(
        string='Sequência',
        default=10
    )

    modelo_id = fields.Many2one(
        comodel_name='ir.model',
        string='Modelo Alvo',
        required=True,
        ondelete='cascade'
    )

    modelo_tecnico = fields.Char(
        related='modelo_id.model',
        string='Modelo Técnico',
        store=True,
        index=True
    )

    recolhido = fields.Boolean(
        string='Recolhido no Kanban?',
        default=False
    )

    etapa_final = fields.Boolean(
        string='Etapa de Conclusão?',
        help='Indica se o processo encerra aqui.'
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
        domain="[('modelo_id', '=', modelo_id)]"
    )

    obs = fields.Char(
        string='Observação'
    )
