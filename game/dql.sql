-- ==========================
-- 1. Consultas na tabela personagem
-- ==========================
SELECT * FROM personagem;

-- Personagens com vida máxima acima de 100 e nível maior que 10
SELECT nome, vida_maxima, level
FROM personagem
WHERE vida_maxima > 100 AND level > 10
ORDER BY level DESC;

-- ==========================
-- 2. Consultas na tabela cenario com relações
-- ==========================
SELECT 
    c.id_cenario,
    c.sol,
    c.chuva,
    c.noite,
    c.dia,
    norte.sol AS sol_norte,
    leste.sol AS sol_leste,
    oeste.sol AS sol_oeste,
    sul.sol AS sol_sul
FROM cenario c
LEFT JOIN cenario norte ON c.norte_id = norte.id_cenario
LEFT JOIN cenario leste ON c.leste_id = leste.id_cenario
LEFT JOIN cenario oeste ON c.oeste_id = oeste.id_cenario
LEFT JOIN cenario sul ON c.sul_id = sul.id_cenario;

-- ==========================
-- 3. Consultas na tabela jogador com dados de personagem e cenário
-- ==========================
SELECT
    j.ID_personagem,
    p.nome AS nome_personagem,
    j.tipo_equipamento,
    c.id_cenario,
    c.sol,
    c.dia
FROM jogador j
INNER JOIN personagem p ON j.ID_personagem = p.ID_personagem
INNER JOIN cenario c ON j.cenario = c.id_cenario;

-- ==========================
-- 4. Consultas na tabela inventario com itens e personagem
-- ==========================
SELECT 
    i.id_inventario,
    i.id_personagem,
    p.nome AS nome_personagem,
    i.pods,
    it.id_item,
    it.nome AS nome_item,
    it.peso,
    it.durabilidade
FROM inventario i
INNER JOIN personagem p ON i.id_personagem = p.ID_personagem
LEFT JOIN item it ON it.id_inventario = i.id_inventario;

-- ==========================
-- 5. Consultas na tabela item com armas e armaduras
-- ==========================
SELECT 
    it.id_item,
    it.nome,
    it.peso,
    it.durabilidade,
    a.mãos,
    a.dano,
    ar.defesa
FROM item it
LEFT JOIN arma a ON it.id_item = a.id_item
LEFT JOIN armadura ar ON it.id_item = ar.id_item;

-- ==========================
-- 6. Consultas nas especializações de personagem
-- ==========================
-- Guia com custo de orientação e personagem
SELECT 
    g.ID_personagem,
    p.nome,
    g.custo_orientacao
FROM guia g
INNER JOIN personagem p ON g.ID_personagem = p.ID_personagem;

-- Comerciante com itens que compra e vende
SELECT 
    c.ID_personagem,
    p.nome,
    c.venda_item,
    c.compra_item
FROM comerciante c
INNER JOIN personagem p ON c.ID_personagem = p.ID_personagem;

-- NPC com quests e horários
SELECT 
    n.ID_personagem,
    p.nome,
    n.quest,
    n.localizacao,
    n.hora_aparicao
FROM npc n
INNER JOIN personagem p ON n.ID_personagem = p.ID_personagem;

-- ==========================
-- 7. Consultas em criaturas e especializações
-- ==========================
-- Criaturas com XP e dados de personagem
SELECT 
    cr.ID_personagem,
    p.nome,
    cr.XP
FROM criatura cr
INNER JOIN personagem p ON cr.ID_personagem = p.ID_personagem;

-- Orks com Raiva
SELECT 
    o.ID_personagem,
    p.nome,
    o.Raiva
FROM ork o
INNER JOIN criatura cr ON o.ID_personagem = cr.ID_personagem
INNER JOIN personagem p ON o.ID_personagem = p.ID_personagem;

-- Goblins com furtividade e roubo
SELECT 
    g.ID_personagem,
    p.nome,
    g.furtividade,
    g.roubo
FROM goblin g
INNER JOIN criatura cr ON g.ID_personagem = cr.ID_personagem
INNER JOIN personagem p ON g.ID_personagem = p.ID_personagem;

-- Boss com fase atual e imunidades
SELECT 
    b.ID_personagem,
    p.nome,
    b.faseAtual,
    b.imunidades
FROM boss b
INNER JOIN criatura cr ON b.ID_personagem = cr.ID_personagem
INNER JOIN personagem p ON b.ID_personagem = p.ID_personagem;

-- ==========================
-- 8. Consultas na tabela confronta com resultado de batalha
-- ==========================
SELECT
    con.Unique_ID,
    con.vencedor,
    cri.ID_personagem AS criatura_id,
    cri2.nome AS nome_criatura,
    jog.ID_personagem AS jogador_id,
    jog2.nome AS nome_jogador
FROM confronta con
LEFT JOIN criatura cri ON con.criatura_id = cri.ID_personagem
LEFT JOIN personagem cri2 ON cri.ID_personagem = cri2.ID_personagem
LEFT JOIN jogador jog ON con.jogador_id = jog.ID_personagem
LEFT JOIN personagem jog2 ON jog.ID_personagem = jog2.ID_personagem;

-- ==========================
-- 9. Consultas na tabela batalha
-- ==========================
SELECT *
FROM batalha;

-- Média de dano causado e sofrido por ambiente
SELECT 
    Ambiente_batalha,
    AVG(Dano_causado) AS media_dano_causado,
    AVG(Dano_sofrido) AS media_dano_sofrido
FROM batalha
GROUP BY Ambiente_batalha
ORDER BY media_dano_causado DESC;

-- ==========================
-- 10. Consultas em skill e caracteristicas do jogador
-- ==========================
SELECT 
    s.ID_jogador,
    p.nome,
    s.atq
FROM skill s
INNER JOIN jogador j ON s.ID_jogador = j.ID_personagem
INNER JOIN personagem p ON j.ID_personagem = p.ID_personagem;

SELECT 
    c.ID_jogador,
    p.nome,
    c.fogo,
    c.agua,
    c.terra,
    c.ar
FROM caracteristicas c
INNER JOIN jogador j ON c.ID_jogador = j.ID_personagem
INNER JOIN personagem p ON j.ID_personagem = p.ID_personagem;

-- ==========================
-- 11. Consultas em classes de personagem especializadas
-- ==========================
SELECT 
    gw.id_personagem,
    p.nome,
    gw.atq_Fisico,
    gw.bloquear_Dano
FROM guerreiro gw
INNER JOIN personagem p ON gw.id_personagem = p.ID_personagem;

SELECT 
    sc.id_personagem,
    p.nome,
    sc.bencao_Cura,
    sc.atq_Especial
FROM sacerdote sc
INNER JOIN personagem p ON sc.id_personagem = p.ID_personagem;

SELECT 
    mg.id_personagem,
    p.nome,
    mg.atq_Magico,
    mg.atq_MultiElemento
FROM mago mg
INNER JOIN personagem p ON mg.id_personagem = p.ID_personagem;

SELECT 
    ar.id_personagem,
    p.nome,
    ar.atq_Preciso,
    ar.atq_Rapido
FROM arqueiro ar
INNER JOIN personagem p ON ar.id_personagem = p.ID_personagem;

