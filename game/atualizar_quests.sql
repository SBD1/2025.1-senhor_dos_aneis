-- ===================================================================
-- ATUALIZAÇÃO DO SISTEMA DE QUESTS
-- Adiciona suporte para quests dinâmicas dos NPCs
-- ===================================================================

-- Adicionar coluna quest_dinamica se não existir
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'quest' AND column_name = 'quest_dinamica'
    ) THEN
        ALTER TABLE quest ADD COLUMN quest_dinamica BOOLEAN DEFAULT FALSE;
        RAISE NOTICE 'Coluna quest_dinamica adicionada à tabela quest';
    ELSE
        RAISE NOTICE 'Coluna quest_dinamica já existe na tabela quest';
    END IF;
END $$;

-- Atualizar quests existentes para marcar como não dinâmicas
UPDATE quest SET quest_dinamica = FALSE WHERE quest_dinamica IS NULL;

-- Verificar se as quests dinâmicas já existem e criar se necessário
INSERT INTO quest (nome, descricao, recompensa_xp, recompensa_item, pre_requisito_level, tipo_quest, quest_dinamica) 
SELECT * FROM (VALUES
    ('Ajude a proteger o Condado dos perigos que se aproximam', 'Missão de Frodo Baggins para proteger o Condado', 120, 'Escudo do Condado', 1, 'NPC', TRUE),
    ('Gondor precisa de heróis para defender Osgiliath', 'Missão de Boromir para defender Osgiliath', 200, 'Espada de Gondor', 1, 'NPC', TRUE),
    ('Rohan enfrenta ameaças das planícies', 'Missão de Théoden para proteger Rohan', 180, 'Lança de Rohan', 1, 'NPC', TRUE),
    ('A floresta anciã precisa de proteção', 'Missão de Treebeard para proteger a floresta', 160, 'Bastão da Floresta', 1, 'NPC', TRUE)
) AS v(nome, descricao, recompensa_xp, recompensa_item, pre_requisito_level, tipo_quest, quest_dinamica)
WHERE NOT EXISTS (
    SELECT 1 FROM quest WHERE quest.nome = v.nome
);

-- Verificar se a tabela quest_progresso tem a constraint UNIQUE
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE table_name = 'quest_progresso' 
        AND constraint_name = 'quest_progresso_id_jogador_id_quest_key'
    ) THEN
        ALTER TABLE quest_progresso ADD CONSTRAINT quest_progresso_id_jogador_id_quest_key 
        UNIQUE (id_jogador, id_quest);
        RAISE NOTICE 'Constraint UNIQUE adicionada à tabela quest_progresso';
    ELSE
        RAISE NOTICE 'Constraint UNIQUE já existe na tabela quest_progresso';
    END IF;
END $$;

-- Mostrar status das quests
SELECT 
    nome,
    tipo_quest,
    quest_dinamica,
    recompensa_xp,
    recompensa_item
FROM quest 
ORDER BY quest_dinamica DESC, tipo_quest, nome;

-- Mensagem de sucesso
DO $$
BEGIN
    RAISE NOTICE 'Sistema de quests dinâmicas atualizado com sucesso!';
END $$; 