import json

from decouple import config
import psycopg2

NAME = 'fidcCopobrasTesteLocal'
USER = config('DB_USER')
PASSWORD = config('DB_PASSWORD')
HOST = config('DB_HOST')
PORT = config('DB_PORT', default='5432')

connect = psycopg2.connect(
    host=HOST,
    database=NAME,
    user=USER,
    password=PASSWORD,
    port=PORT,
)
from decimal import Decimal
from datetime import date, datetime

connect.autocommit = True
cursor = connect.cursor()
def default_converter(obj):
    if isinstance(obj, (Decimal)):
        return float(obj)
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

try:
    print("Executando consulta para estoque...")
    cursor.execute("""
    
        with recursive
            a as (select ativo_id, sum(quantidade)
                from carteira
                where data_de_compra <= '2025-09-03'
                group by ativo_id
                having sum(quantidade) > 0.001),

            b as (select ativo_id, preco
                from cotacao
                where ativo_id in (select ativo_id from a)
                    and data = '2025-09-03'),


            entidade_hierarquia as (
                select id as original_id,
                    id as current_id,
                    father_id
                from entidade
                where entidade.id in (select entidade_destinatario_id
                                    from nf,
                                        nf_duplicata,
                                        ativo
                                    where ativo.id in (select ativo_id from a)
                                        and ativo.nf_duplicata_id = nf_duplicata.id
                                        and nf.id = nf_duplicata.nf_id)

                union all

                select eh.original_id,
                    e.id,
                    e.father_id
                from entidade_hierarquia eh
                        join entidade e on e.id = eh.father_id
                where eh.current_id != eh.father_id
            ),

            raiz_entidade as (select original_id,
                                    current_id as root_id
                            from entidade_hierarquia
                            where current_id = father_id
            )

            select 'COPOBRAS FIDC'         as fidc_nome,
                '57.182.898/0001-83'    as fidc_cnpj,
                x.ativo_id              as codigo_identificador_parcela,
                x.emitente_inscricao    as cedente,
                x.destinatario          as sacado,
                'PJ'                    as sacado_tipo,
                raiz.root_id            as sacado_grupo_economico,
                '2025-09-03'            as data_base,
                x.nf_emissao            as data_emissao,
                carteira.data_de_compra as data_aquisicao,
                x.duplitaca_vencimento  as data_vencimento,
                x.valor_de_compra       as valor_aquisicao,
                b.preco                 as valor_presente,
                x.duplicata_valor       as valor_nominal,
                'TODO'                  as valor_pdd,
                'duplicata'             as lastro,
                x.taxa_cessao           as taxa_cessao

            from (select a.ativo_id,
                        ativo.info ->> 'taxa'            as taxa_cessao,
                        ativo.info ->> 'valor_de_compra' as valor_de_compra,
                        nf_duplicata.numero              as duplitaca_numero,
                        nf_duplicata.vencimento          as duplitaca_vencimento,
                        nf_duplicata.valor               as duplicata_valor,
                        nf.numero                        as nf_numero,
                        nf.serie                         as nf_serie,
                        nf.data_emissao                  as nf_emissao,
                        destinatario.id                  as destinatario,
                        destinatario.inscricao           as destinatario_inscricao,
                        emitente.id                      as emitente,
                        emitente.inscricao               as emitente_inscricao

                from a,
                    ativo,
                    nf_duplicata,
                    nf,
                    entidade as emitente,
                    entidade as destinatario

                where a.ativo_id = ativo.id
                    and ativo.nf_duplicata_id = nf_duplicata.id
                    and nf_duplicata.nf_id = nf.id
                    and nf.entidade_destinatario_id = destinatario.id
                    and nf.entidade_emitente_id = emitente.id
                    and ativo.tipo = 'investimento') x
                    left join b on x.ativo_id = b.ativo_id
                    left join carteira on x.ativo_id = carteira.ativo_id and carteira.tipo = 'C'
                    left join raiz_entidade raiz on x.destinatario = raiz.original_id;                     
    """)

    # Pega os nomes das colunas para montar o dicionário
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    if results:
        # Montando o JSON no padrão que combinamos
        # Usamos o primeiro registro para pegar os dados do Fundo
        payload = {
            "ref_date": results[0]['data_base'],
            "fidc_cnpj": results[0]['fidc_cnpj'],
            "data": {
                "identificacao_fidc": {
                    "nome": results[0]['fidc_nome'],
                    "cnpj": results[0]['fidc_cnpj']
                },
                "ativos": []
            }
        }

        # Preenchendo a lista de ativos
        for row in results:
            ativo = {
                "codigo_identificador_parcela": row['codigo_identificador_parcela'],
                "cedente": row['cedente'],
                "sacado": {
                    "nome": row['sacado'],
                    "identificacao_codigo": row['sacado'], # ou ID se tiver
                    "tipo_pessoa": row['sacado_tipo'],
                    "grupo_economico": row['sacado_grupo_economico']
                },
                "datas": {
                    "data_base": row['data_base'],
                    "emissao": row['data_emissao'],
                    "aquisicao": row['data_aquisicao'],
                    "vencimento": row['data_vencimento']
                },
                "valores": {
                    "aquisicao": row['valor_aquisicao'],
                    "presente": row['valor_presente'],
                    "nominal": row['valor_nominal'],
                    "pdd": row['valor_pdd']
                },
                "lastro": {
                    "tipo": row['lastro'],
                    "documento": row['codigo_identificador_parcela']
                },
                "demais_informacoes": {
                    "taxa_cessao": row['taxa_cessao']
                }
            }
            payload["data"]["ativos"].append(ativo)

        # Print do JSON final (é isso que você vai enviar no request.post para a API)
        print(json.dumps(payload, indent=2, default=default_converter))
    
except Exception as e:
    print("Erro ao executar ALTER TABLE:", e)
finally:
    cursor.close()
    connect.close()
