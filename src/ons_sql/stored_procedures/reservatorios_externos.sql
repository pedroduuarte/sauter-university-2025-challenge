-- código principal de transformação.

CREATE OR REPLACE PROCEDURE `canvas-provider-472313-n5.reservatorios_externos_dataset.reservatorios_externos`()
BEGIN
  DECLARE tabela_criada BOOL;

  -- Verifica se a tabela já existe
  SET tabela_criada = (
    SELECT COUNT(*) > 0
    FROM `canvas-provider-472313-n5.reservatorios_externos_dataset.INFORMATION_SCHEMA.TABLES`
    WHERE table_name = 'trusted_data'
  );

  -- Criação da tabela se não existir
  IF NOT tabela_criada THEN
    CREATE TABLE `canvas-provider-472313-n5.reservatorios_externos_dataset.trusted_data`
    PARTITION BY DATE_TRUNC(ear_data, MONTH)
    CLUSTER BY nome_bacia, nome_reservatorio AS
    WITH dados_tratados AS (
      SELECT DISTINCT
        SAFE.PARSE_DATE('%Y-%m-%d', TRIM(ear_data)) AS ear_data,
        UPPER(TRIM(nom_reservatorio)) AS nome_reservatorio,
        SAFE_CAST(NULLIF(TRIM(cod_resplanejamento), '') AS INT64) AS id_res_planejamento,
        UPPER(TRIM(tip_reservatorio)) AS tipo_reservatorio,
        UPPER(TRIM(nom_bacia)) AS nome_bacia,
        UPPER(TRIM(nom_ree)) AS nom_ree,
        UPPER(TRIM(id_subsistema)) AS id_subsistema,
        UPPER(TRIM(nom_subsistema)) AS nome_subsistema,
        UPPER(TRIM(id_subsistema_jusante)) AS id_subsistema_jusante,
        UPPER(TRIM(nom_subsistema_jusante)) AS nome_subsistema_jusante,
        SAFE_CAST(NULLIF(TRIM(ear_reservatorio_subsistema_proprio_mwmes), '') AS FLOAT64) AS ear_propria_mwmes,
        SAFE_CAST(NULLIF(TRIM(ear_reservatorio_subsistema_jusante_mwmes), '') AS FLOAT64) AS ear_jusante_mwmes,
        SAFE_CAST(NULLIF(TRIM(earmax_reservatorio_subsistema_proprio_mwmes), '') AS FLOAT64) AS ear_maxima_propria_mwmes,
        SAFE_CAST(NULLIF(TRIM(earmax_reservatorio_subsistema_jusante_mwmes), '') AS FLOAT64) AS ear_maxima_jusante_mwmes,
        SAFE_CAST(NULLIF(TRIM(ear_reservatorio_percentual), '') AS FLOAT64) AS ear_percentual,
        SAFE_CAST(NULLIF(TRIM(ear_total_mwmes), '') AS FLOAT64) AS ear_total_mwmes,
        SAFE_CAST(NULLIF(TRIM(ear_maxima_total_mwmes), '') AS FLOAT64) AS ear_maxima_total_mwmes,
        SAFE_CAST(NULLIF(TRIM(val_contribearbacia), '') AS FLOAT64) AS contribuicao_ear_bacia_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearmaxbacia), '') AS FLOAT64) AS contribuicao_ear_maxima_bacia_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearsubsistema), '') AS FLOAT64) AS contribuicao_ear_subsistema_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearmaxsubsistema), '') AS FLOAT64) AS contribuicao_ear_maxima_subsistema_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearsubsistemajusante), '') AS FLOAT64) AS contribuicao_ear_subsistema_jusante_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearmaxsubsistemajusante), '') AS FLOAT64) AS contribuicao_ear_maxima_subsistema_jusante_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearsin), '') AS FLOAT64) AS contribuicao_ear_sin_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearmaxsin), '') AS FLOAT64) AS contribuicao_ear_maxima_sin_percentual
      FROM `canvas-provider-472313-n5.reservatorios_externos_dataset.novos_dados_ons`
      WHERE ear_data IS NOT NULL
        AND nom_reservatorio IS NOT NULL
        AND cod_resplanejamento IS NOT NULL
    )
    SELECT * FROM dados_tratados;

  ELSE
    -- Inserção apenas dos novos registros que ainda não existem
    INSERT INTO `canvas-provider-472313-n5.reservatorios_externos_dataset.trusted_data`
    WITH dados_tratados AS (
      SELECT DISTINCT
        SAFE.PARSE_DATE('%Y-%m-%d', TRIM(ear_data)) AS ear_data,
        UPPER(TRIM(nom_reservatorio)) AS nome_reservatorio,
        SAFE_CAST(NULLIF(TRIM(cod_resplanejamento), '') AS INT64) AS id_res_planejamento,
        UPPER(TRIM(tip_reservatorio)) AS tipo_reservatorio,
        UPPER(TRIM(nom_bacia)) AS nome_bacia,
        UPPER(TRIM(nom_ree)) AS nom_ree,
        UPPER(TRIM(id_subsistema)) AS id_subsistema,
        UPPER(TRIM(nom_subsistema)) AS nome_subsistema,
        UPPER(TRIM(id_subsistema_jusante)) AS id_subsistema_jusante,
        UPPER(TRIM(nom_subsistema_jusante)) AS nome_subsistema_jusante,
        SAFE_CAST(NULLIF(TRIM(ear_reservatorio_subsistema_proprio_mwmes), '') AS FLOAT64) AS ear_propria_mwmes,
        SAFE_CAST(NULLIF(TRIM(ear_reservatorio_subsistema_jusante_mwmes), '') AS FLOAT64) AS ear_jusante_mwmes,
        SAFE_CAST(NULLIF(TRIM(earmax_reservatorio_subsistema_proprio_mwmes), '') AS FLOAT64) AS ear_maxima_propria_mwmes,
        SAFE_CAST(NULLIF(TRIM(earmax_reservatorio_subsistema_jusante_mwmes), '') AS FLOAT64) AS ear_maxima_jusante_mwmes,
        SAFE_CAST(NULLIF(TRIM(ear_reservatorio_percentual), '') AS FLOAT64) AS ear_percentual,
        SAFE_CAST(NULLIF(TRIM(ear_total_mwmes), '') AS FLOAT64) AS ear_total_mwmes,
        SAFE_CAST(NULLIF(TRIM(ear_maxima_total_mwmes), '') AS FLOAT64) AS ear_maxima_total_mwmes,
        SAFE_CAST(NULLIF(TRIM(val_contribearbacia), '') AS FLOAT64) AS contribuicao_ear_bacia_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearmaxbacia), '') AS FLOAT64) AS contribuicao_ear_maxima_bacia_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearsubsistema), '') AS FLOAT64) AS contribuicao_ear_subsistema_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearmaxsubsistema), '') AS FLOAT64) AS contribuicao_ear_maxima_subsistema_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearsubsistemajusante), '') AS FLOAT64) AS contribuicao_ear_subsistema_jusante_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearmaxsubsistemajusante), '') AS FLOAT64) AS contribuicao_ear_maxima_subsistema_jusante_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearsin), '') AS FLOAT64) AS contribuicao_ear_sin_percentual,
        SAFE_CAST(NULLIF(TRIM(val_contribearmaxsin), '') AS FLOAT64) AS contribuicao_ear_maxima_sin_percentual
      FROM `canvas-provider-472313-n5.reservatorios_externos_dataset.novos_dados_ons`
      WHERE ear_data IS NOT NULL
        AND nom_reservatorio IS NOT NULL
        AND cod_resplanejamento IS NOT NULL
    )
    SELECT d.*
    FROM dados_tratados d
    WHERE NOT EXISTS (
      SELECT 1
      FROM `canvas-provider-472313-n5.reservatorios_externos_dataset.trusted_data` t
      WHERE t.ear_data = d.ear_data
        AND t.nome_reservatorio = d.nome_reservatorio
        AND t.id_res_planejamento = d.id_res_planejamento
    );
  END IF;
END;
