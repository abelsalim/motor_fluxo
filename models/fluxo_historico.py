from odoo import api, fields, models


class FluxoHistorico(models.Model):

    # --- Odoo Atributos ---

    _name = 'fluxo.historico'

    _description = 'Histórico Detalhado do Fluxo'

    _order = 'data_entrada desc'

    # --- Odoo Fields ---

    res_model = fields.Char(
        string='Modelo',
        required=True,
        index=True
    )

    res_id = fields.Integer(
        string='ID do Registro',
        required=True,
        index=True
    )

    etapa_id = fields.Many2one(
        comodel_name='fluxo.etapa',
        string='Etapa',
        required=True
    )

    usuario_id = fields.Many2one(
        comodel_name='res.users',
        string='Usuário',
        default=lambda self: self.env.user
    )

    empresa_id = fields.Many2one(
        comodel_name='res.company',
        string='Empresa',
        default=lambda self: self.env.company
    )

    data_entrada = fields.Datetime(
        string='Entrada',
        default=fields.Datetime.now
    )

    data_saida = fields.Datetime(
        string='Saída'
    )

    duracao_horas = fields.Float(
        string='Duração (h)',
        compute='_calcula_duracao',
        store=True
    )

    # --- Métodos Computados ---

    @api.depends('data_entrada', 'data_saida')
    def _calcula_duracao(self) -> None:

        for rec in self:
            if not rec.data_entrada or not rec.data_saida:
                rec.duracao_horas = 0.0

                continue

            delta = rec.data_saida - rec.data_entrada
            rec.duracao_horas = delta.total_seconds() / 3600.0

    # --- Métodos de Ação ---

    def acao_voltar_para_etapa(self) -> dict[str, str]:

        self.ensure_one()
        registro_pai = self.env[str(self.res_model)].browse(self.res_id)

        if registro_pai.exists():
            registro_pai.write({'etapa_id': self.etapa_id.id})

        return {'type': 'ir.actions.client', 'tag': 'reload'}
