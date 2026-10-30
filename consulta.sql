with h as (
  select codigo_loja, venda, pedidos,
         coalesce(ifood,0)+coalesce(food99,0)+coalesce(outros_canais,0) deliv,
         coalesce(ultima_venda::time, (coletado_em at time zone 'America/Sao_Paulo')::time) corte_t,
         coletado_em at time zone 'America/Sao_Paulo' col
  from hoje_loja),
hm as (select codigo_loja, extract(hour from corte_t)*60+extract(minute from corte_t) m from h),
w as (select v.codigo_loja, v.data, v.valor,
        split_part(v.faixa,':',1)::int*60+split_part(v.faixa,':',2)::int ini
      from venda_meia_hora v
      where v.data in ('2026-08-30','2026-09-30','2026-10-23','2026-10-16','2026-10-09','2026-10-02')),
x as (select w.*, case when ini<300 then 0 when ini+30<=hm.m then 1 when ini<hm.m then (hm.m-ini)/30.0 else 0 end f
      from w join hm using(codigo_loja)),
d as (select codigo_loja, data, sum(valor*f) ate, sum(valor) tot from x group by 1,2),
p as (select codigo_loja,
        sum(ate) filter (where data in ('2026-08-30','2026-09-30'))/nullif(sum(tot) filter (where data in ('2026-08-30','2026-09-30')),0) p30,
        sum(ate) filter (where extract(dow from data)=5)/nullif(sum(tot) filter (where extract(dow from data)=5),0) psex,
        max(ate) filter (where data='2026-09-30') ate_set,
        max(ate) filter (where data='2026-10-23') ate23
      from d group by 1)
select h.codigo_loja, round(h.venda,2) venda, round(h.deliv,2) deliv, h.pedidos,
       round(coalesce(p.p30,p.psex),5) pct, round(p.ate_set,2) ate_set, round(p.ate23,2) ate23,
       (select to_char(percentile_disc(0.5) within group (order by corte_t),'HH24"h"MI') from h) corte,
       (select to_char(max(col),'HH24"h"MI') from h) atualizado
from h left join p using(codigo_loja)
order by 1
