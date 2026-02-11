from __future__ import annotations
from typing import Any, cast, Literal, TYPE_CHECKING

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


if TYPE_CHECKING:
    from .fluxo_etapa import FluxoEtapa
    from .fluxo_operacao import FluxoOperacao


class FluxoBase(models.AbstractModel):

    # --- Odoo Atributos ---

    _name = 'fluxo.base'

    _description = 'Base Abstrata para Workflow'

    # --- Odoo Fields ---

    operacao_id = fields.Many2one(
        comodel_name='fluxo.operacao',
        string='Operação',
        # domain=lambda self: [('modelo_tecnico', '=', self._name)],
        tracking=True, index=True
    )

    etapa_id = fields.Many2one(
        comodel_name='fluxo.etapa',
        string='Etapa Atual',
        # domain=lambda self: [('modelo_tecnico', '=', self._name)],
        tracking=True, index=True, copy=False,
        group_expand='_agrupar_etapas_kanban'
    )

    etapas_disponiveis_ids = fields.Many2many(
        'fluxo.etapa', 
        compute='_compute_etapas_disponiveis'
    )

    historico_ids = fields.One2many(
        comodel_name='fluxo.historico',
        compute='_computar_historico',
        string='Histórico'
    )

    # --- Métodos Odoo Core ---

    def write(self, vals: dict[str, Any]) -> Literal[True]:

        if 'etapa_id' in vals:
            nova_etapa = cast(
                'FluxoEtapa', self.env['fluxo.etapa'].browse(vals['etapa_id'])
            )

            for rec in self:
                if nova_etapa.grupos_permitidos_ids:
                    grupos_usuario = getattr(self.env.user, 'groups_id')

                    if not (grupos_usuario & nova_etapa.grupos_permitidos_ids):
                        raise UserError(
                            ("Permissão negada para mover para: %s")
                            % nova_etapa.name
                        )

                if nova_etapa.codigo_antes:
                    self._executar_python(nova_etapa.codigo_antes, rec)

                self._fechar_log_historico(rec)

        res = super(FluxoBase, self).write(vals)

        if 'etapa_id' in vals:
            nova_etapa = cast(
                'FluxoEtapa', self.env['fluxo.etapa'].browse(vals['etapa_id'])
            )

            for rec in self:
                self._criar_log_historico(rec, vals['etapa_id'])

                if nova_etapa.codigo_depois:
                    self._executar_python(nova_etapa.codigo_depois, rec)

        return res

    @api.model_create_multi
    def create(self, vals_list: list[dict[str, Any]]) -> FluxoBase:

        for vals in vals_list:
            if vals.get('operacao_id') and not vals.get('etapa_id'):
                operacao = cast(
                    'FluxoOperacao', 
                    self.env['fluxo.operacao'].browse(vals['operacao_id'])
                )

                if not operacao.etapa_inicial_id:
                    continue

                vals['etapa_id'] = operacao.etapa_inicial_id.id

        registros = super().create(vals_list)

        for rec in registros:
            etapa_atual = cast('FluxoEtapa', rec.etapa_id)

            if etapa_atual:
                self._criar_log_historico(rec, etapa_atual.id)

        return registros

    # --- Métodos Computados ---

    def _computar_historico(self) -> None:
        for rec in self:
            rec.historico_ids = self.env['fluxo.historico'].search([
                ('res_model', '=', rec._name),
                ('res_id', '=', rec.id)
            ], order='data_entrada desc')

    # --- Métodos Depends ---

    @api.depends('etapa_id', 'operacao_id')
    def _compute_etapas_disponiveis(self):

        for rec in self:
            if rec.etapa_id:
                rec.etapas_disponiveis_ids = (
                    rec.etapa_id.proxima_etapa_ids | rec.etapa_id
                )

            elif rec.operacao_id and rec.operacao_id.etapa_inicial_id:
                rec.etapas_disponiveis_ids = rec.operacao_id.etapa_inicial_id

            else:
                rec.etapas_disponiveis_ids = False

    # --- Métodos Onchange ---

    @api.onchange('operacao_id')
    def _onchange_ao_mudar_operacao(self) -> None:

        operacao = cast('FluxoOperacao', self.operacao_id)
        if operacao and operacao.etapa_inicial_id:
            self.etapa_id = operacao.etapa_inicial_id

    # --- Métodos de Hook de Interface ---

    @api.model
    def _agrupar_etapas_kanban(self, stages, domain, order) -> models.BaseModel:
        return (
            self.env['fluxo.etapa']
            .search([('modelo_tecnico', '=', self._name)], order=order)
        )

    # --- Treatments Methods ---

    def _executar_python(self, codigo, registro) -> None:

        local_dict = {
            'registro': registro,
            'env': self.env,
            'UserError': UserError,
            'datetime': fields.Datetime
        }

        try:
            safe_eval(codigo, local_dict, mode="exec")

        except Exception as e:
            raise UserError("Erro na automação de etapa: %s" % str(e))

    def _criar_log_historico(self, registro, etapa_id) -> None:

        self.env['fluxo.historico'].create({
            'res_model': registro._name,
            'res_id': registro.id,
            'etapa_id': etapa_id,
            'data_entrada': fields.Datetime.now()
        })

    def _fechar_log_historico(self, registro) -> None:

        ultimo = self.env['fluxo.historico'].search([
            ('res_model', '=', registro._name),
            ('res_id', '=', registro.id),
            ('data_saida', '=', False)
        ], limit=1, order='data_entrada desc')

        if not ultimo:
            return

        ultimo.write({'data_saida': fields.Datetime.now()})
