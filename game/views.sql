/*******************************************************************
*
* ARQUIVO: views.sql
* PROJETO: Jogo de RPG - Banco de Dados
* VERSÃO: 1.0
* DATA: 04 de Julho de 2025
*
* DESCRIÇÃO:
* Este script contém a criação de todas as Views (visões)
* utilizadas para simplificar as consultas e abstrair a
* complexidade do banco de dados do jogo.
*
*******************************************************************/

-- ===================================================================
-- VIEW 1: vw_detalhes_jogador
-- DESCRIÇÃO: Consolida todas as informações de um jogador em uma
--            única ficha, incluindo stats, classe e localização.
-- ===================================================================
CREATE OR REPLACE VIEW vw_detalhes_jogador AS
SELECT
    p.id_personagem,
    p.nome,
    p.level,
    p.vida_maxima,
    p.mana_maxima,
    p.habilidade,
    p.resistencia,
    j.tipo_equipamento,
    s.atq AS ataque,
    c.fogo,
    c.agua,
    c.terra,
    c.ar,
    cen.id_cenario AS cenario_atual_id,
    cen.sol AS clima_cenario_atual
FROM
    personagem p
    INNER JOIN jogador j ON p.id_personagem = j.id_personagem
    LEFT JOIN skill s ON j.id_personagem = s.id_jogador
    LEFT JOIN caracteristicas c ON j.id_personagem = c.id_jogador
    LEFT JOIN cenario cen ON j.cenario = cen.id_cenario;


-- ===================================================================
-- VIEW 2: vw_itens_completos
-- DESCRIÇÃO: Unifica os dados de item, arma e armadura, informando
--            também o personagem que possui cada item.
-- ===================================================================
CREATE OR REPLACE VIEW vw_itens_completos AS
SELECT
    i.id_item,
    i.nome AS nome_item,
    i.peso,
    i.durabilidade,
    a.dano,
    a.mãos,
    ar.defesa,
    p.id_personagem AS dono_id,
    p.nome AS dono_nome,
    CASE
        WHEN a.id_item IS NOT NULL THEN 'Arma'
        WHEN ar.id_item IS NOT NULL THEN 'Armadura'
        ELSE 'Item Comum'
    END AS tipo_de_item
FROM
    item i
    LEFT JOIN arma a ON i.id_item = a.id_item
    LEFT JOIN armadura ar ON i.id_item = ar.id_item
    LEFT JOIN inventario inv ON i.id_inventario = inv.id_inventario
    LEFT JOIN personagem p ON inv.id_personagem = p.id_personagem;


-- ===================================================================
-- VIEW 3: vw_historico_confrontos
-- DESCRIÇÃO: Transforma o log de confrontos em um histórico legível,
--            substituindo IDs por nomes e formatando o resultado.
-- ===================================================================
CREATE OR REPLACE VIEW vw_historico_confrontos AS
SELECT
    c.unique_id,
    jog_p.nome AS nome_jogador,
    cria_p.nome AS nome_criatura,
    CASE
        WHEN c.vencedor = TRUE THEN 'Vitória do Jogador'
        WHEN c.vencedor = FALSE THEN 'Vitória da Criatura'
        ELSE 'Indefinido'
    END AS resultado
FROM
    confronta c
    LEFT JOIN jogador jog ON c.jogador_id = jog.id_personagem
    LEFT JOIN personagem jog_p ON jog.id_personagem = jog_p.id_personagem
    LEFT JOIN criatura cria ON c.criatura_id = cria.id_personagem
    LEFT JOIN personagem cria_p ON cria.id_personagem = cria_p.id_personagem;


-- ===================================================================
-- VIEW 4: vw_informacoes_npcs
-- DESCRIÇÃO: Agrupa todos os tipos de NPCs (Guias, Comerciantes, etc)
--            em uma única visão para facilitar a consulta de suas
--            funções, ofertas e localizações.
-- ===================================================================
CREATE OR REPLACE VIEW vw_informacoes_npcs AS
SELECT
    p.id_personagem,
    p.nome,
    p.level,
    p.dialogo,
    n.localizacao,
    n.quest,
    n.hora_aparicao,
    co.venda_item,
    co.compra_item,
    g.custo_orientacao,
    CASE
        WHEN g.id_personagem IS NOT NULL THEN 'Guia'
        WHEN co.id_personagem IS NOT NULL THEN 'Comerciante'
        WHEN n.id_personagem IS NOT NULL THEN 'NPC de Quest'
        ELSE 'NPC Comum'
    END AS tipo_npc
FROM
    personagem p
    INNER JOIN npc n ON p.id_personagem = n.id_personagem
    LEFT JOIN comerciante co ON p.id_personagem = co.id_personagem
    LEFT JOIN guia g ON p.id_personagem = g.id_personagem;
