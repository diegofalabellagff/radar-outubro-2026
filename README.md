# Radar Dia 30 · outubro 2026

Parcial de venda do Dia 30 (30/10/2026) das lojas do Grupo Fresh Food contra a meta do GFF, por loja e supervisor.

- `index.html`: o painel publicado (gerado, não editar à mão).
- `consulta.sql`: consulta rodada no Atlas (ferramenta `consultar_sql`) a cada atualização.
- `metas.json`: metas do dia 30 por loja e supervisor, dos PDFs de meta. Catalão = Caiçaras no Atlas (código 7950). Serra sem meta.
- `template.html`: layout do painel, com os marcadores `__DATA__`, `__CORTE__`, `__ATUALIZADO__` e `__SEMDELIV__`.
- `gen.py`: `python3 gen.py dados.json` gera o `index.html` a partir do resultado da consulta.

Uma tarefa agendada roda de hora em hora no dia 30, das 15h50 às 23h50, e atualiza o `index.html`.
