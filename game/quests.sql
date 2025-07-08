-- ===================================================================
-- SISTEMA DE QUESTS APRIMORADO
-- Adiciona tabelas e funcionalidades para um sistema de missões completo
-- ===================================================================

-- Tabela de Quests
CREATE TABLE IF NOT EXISTS quest (
    id_quest SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    recompensa_xp INTEGER DEFAULT 0,
    recompensa_item VARCHAR(100),
    pre_requisito_level INTEGER DEFAULT 1,
    tipo_quest VARCHAR(50) DEFAULT 'Principal', -- Principal, Secundária, Diária
    status VARCHAR(20) DEFAULT 'Disponível', -- Disponível, Em Progresso, Completada
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- **ASSUNÇÃO/CORREÇÃO**: A tabela 'jogador' não foi fornecida, mas é referenciada.
-- Criei uma estrutura básica para 'jogador' e 'cenario' e 'inventario'
-- para que o script possa ser executado sem erros de referência.
-- Você precisará ajustar isso para a sua estrutura real.
CREATE TABLE IF NOT EXISTS jogador (
    ID_personagem SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    level INTEGER DEFAULT 1,
    xp INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_personagem INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (id_personagem) REFERENCES jogador(ID_personagem)
);

CREATE TABLE IF NOT EXISTS item (
    id_item SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    peso DECIMAL(5,2),
    durabilidade INTEGER,
    id_inventario INTEGER NOT NULL,
    FOREIGN KEY (id_inventario) REFERENCES inventario(id_inventario)
);


CREATE TABLE IF NOT EXISTS cenario (
    id_cenario SERIAL PRIMARY KEY,
    nome_cenario VARCHAR(100) NOT NULL
);

-- Tabela de Progresso de Quest do Jogador
CREATE TABLE IF NOT EXISTS quest_progresso (
    id_progresso SERIAL PRIMARY KEY,
    id_jogador INTEGER NOT NULL,
    id_quest INTEGER NOT NULL,
    progresso_atual INTEGER DEFAULT 0,
    progresso_maximo INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'Em Progresso',
    iniciado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completado_em TIMESTAMP NULL,
    FOREIGN KEY (id_jogador) REFERENCES jogador(ID_personagem),
    FOREIGN KEY (id_quest) REFERENCES quest(id_quest),
    UNIQUE(id_jogador, id_quest)
);

-- Tabela de Diários/Logs de Eventos
CREATE TABLE IF NOT EXISTS diario_eventos (
    id_evento SERIAL PRIMARY KEY,
    id_jogador INTEGER NOT NULL,
    tipo_evento VARCHAR(50) NOT NULL, -- Movimento, Batalha, Quest, Item, Interação
    descricao TEXT NOT NULL,
    cenario_id INTEGER,
    timestamp_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_jogador) REFERENCES jogador(ID_personagem),
    -- **CORREÇÃO**: Adicionado ON DELETE SET NULL para o cenario_id,
    -- caso o cenário seja removido, o log não perca a referência de jogador.
    FOREIGN KEY (cenario_id) REFERENCES cenario(id_cenario) ON DELETE SET NULL
);

-- ===================================================================
-- INSERIR QUESTS INICIAIS
-- ===================================================================

INSERT INTO quest (nome, descricao, recompensa_xp, recompensa_item, pre_requisito_level, tipo_quest) VALUES
('A Busca do Palantír', 'Encontre os três fragmentos do Palantír perdido espalhados pela Terra Média para ajudar na defesa contra as forças sombrias.', 1000, 'Palantír Restaurado', 1, 'Principal'),
('Defensor do Condado', 'Derrote 5 criaturas hostis para proteger as terras pacíficas dos Hobbits.', 500, 'Espada do Condado', 3, 'Secundária'),
('Explorador da Terra Média', 'Visite todos os 4 cenários principais para mapear a região.', 300, 'Mapa Élfico', 1, 'Secundária'),
('Caçador de Goblins', 'Elimine 3 Goblins que estão aterrorizando as estradas.', 400, 'Adaga Anti-Goblin', 5, 'Secundária'),
('O Chamado de Minas Tirith', 'Chegue a Minas Tirith e fale com o Senescente para receber uma missão especial.', 600, 'Anel de Gondor', 8, 'Principal');

-- **INSERÇÃO DE DADOS DE EXEMPLO**: Adicionado para tornar o script executável
-- e permitir testes das funcionalidades.
INSERT INTO jogador (nome, level, xp) VALUES
('Frodo Bolseiro', 1, 0),
('Aragorn', 7, 1500);

INSERT INTO inventario (id_personagem) VALUES
(1), (2);

INSERT INTO cenario (nome_cenario) VALUES
('O Condado'),
('Floresta de Fangorn'),
('Passo de Caradhras'),
('Minas Tirith');

-- ===================================================================
-- TRIGGERS E STORED PROCEDURES PARA QUEST SYSTEM
-- ===================================================================

-- Função para automaticamente iniciar quests quando jogador atinge level necessário
CREATE OR REPLACE FUNCTION auto_iniciar_quests()
RETURNS TRIGGER AS $$
DECLARE
    quest_record RECORD;
BEGIN
    -- Verifica se o level foi aumentado
    IF NEW.level > OLD.level THEN
        -- Busca quests disponíveis para o novo level
        FOR quest_record IN
            SELECT id_quest, nome, tipo_quest FROM quest
            WHERE pre_requisito_level <= NEW.level
            AND status = 'Disponível'
            AND id_quest NOT IN (
                SELECT id_quest FROM quest_progresso
                WHERE id_jogador = NEW.ID_personagem
            )
        LOOP
            -- Inicia automaticamente quests principais
            -- **CORREÇÃO**: A verificação de 'tipo_quest' já está na query do loop,
            -- então a subquery 'EXISTS' é redundante e pode ser simplificada.
            IF quest_record.tipo_quest = 'Principal' THEN
                INSERT INTO quest_progresso (
                    id_jogador, id_quest, progresso_atual, progresso_maximo
                )
                VALUES (
                    NEW.ID_personagem,
                    quest_record.id_quest,
                    0,
                    CASE quest_record.id_quest
                        WHEN 1 THEN 3  -- Palantír - 3 fragmentos
                        WHEN 5 THEN 1  -- Minas Tirith - 1 visita
                        ELSE 1
                    END
                );

                -- Log do evento
                INSERT INTO diario_eventos (
                    id_jogador, tipo_evento, descricao
                )
                VALUES (
                    NEW.ID_personagem,
                    'Quest',
                    'Nova quest iniciada: ' || quest_record.nome
                );
            END IF;
        END LOOP;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_auto_iniciar_quests
AFTER UPDATE OF level ON jogador -- 
FOR EACH ROW
EXECUTE FUNCTION auto_iniciar_quests(); -- **CORREÇÃO**: Referência à função sem parênteses

-- Stored Procedure para completar quest
CREATE OR REPLACE PROCEDURE sp_completar_quest(p_jogador_id INT, p_quest_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_recompensa_xp INT;
    v_recompensa_item VARCHAR(100);
    v_inventario_id INT;
    v_quest_nome VARCHAR(100); -- Adicionado para o log
    v_current_xp INT;
    v_current_level INT;
    v_xp_needed_for_next_level INT;
BEGIN
    -- Buscar recompensas da quest e nome da quest
    SELECT recompensa_xp, recompensa_item, nome INTO v_recompensa_xp, v_recompensa_item, v_quest_nome
    FROM quest WHERE id_quest = p_quest_id;

    -- Marcar quest como completada
    UPDATE quest_progresso
    SET status = 'Completada', completado_em = CURRENT_TIMESTAMP
    WHERE id_jogador = p_jogador_id AND id_quest = p_quest_id AND status = 'Em Progresso';

    -- Se a quest já estiver completada ou não estiver em progresso, não fazer nada (opcional)
    IF NOT FOUND THEN
        RAISE NOTICE 'Quest ID % for Player ID % is not in "Em Progresso" status or does not exist.', p_quest_id, p_jogador_id;
        RETURN; -- Sai da procedure
    END IF;

    -- Dar XP (e aumentar level automaticamente)
    SELECT xp, level INTO v_current_xp, v_current_level FROM jogador WHERE ID_personagem = p_jogador_id;

    v_current_xp := v_current_xp + v_recompensa_xp;

    -- **MELHORIA**: Lógica de level-up mais robusta
    -- Supondo que XP necessário para próximo nível = level * 500
    v_xp_needed_for_next_level := v_current_level * 500;

    WHILE v_current_xp >= v_xp_needed_for_next_level LOOP
        v_current_level := v_current_level + 1;
        v_current_xp := v_current_xp - v_xp_needed_for_next_level;
        v_xp_needed_for_next_level := v_current_level * 500; -- Recalcula para o novo nível
        RAISE NOTICE 'Jogador % subiu para o Nível %!', p_jogador_id, v_current_level;
    END LOOP;

    UPDATE jogador
    SET xp = v_current_xp, level = v_current_level
    WHERE ID_personagem = p_jogador_id;

    -- Adicionar item de recompensa se houver
    IF v_recompensa_item IS NOT NULL THEN
        SELECT id_inventario INTO v_inventario_id
        FROM inventario WHERE id_personagem = p_jogador_id;

        -- **CORREÇÃO**: Verificar se o inventário existe
        IF v_inventario_id IS NOT NULL THEN
            INSERT INTO item (nome, peso, durabilidade, id_inventario)
            VALUES (v_recompensa_item, 1.0, 999, v_inventario_id);
        ELSE
            RAISE WARNING 'Inventário não encontrado para o jogador %.', p_jogador_id;
        END IF;
    END IF;

    -- Log do evento
    INSERT INTO diario_eventos (id_jogador, tipo_evento, descricao)
    VALUES (p_jogador_id, 'Quest', 'Quest completada: ' || v_quest_nome);

    -- **CORREÇÃO**: COMMIT não é usado diretamente dentro de procedures no PostgreSQL.
    -- A transação é gerenciada externamente ou por blocos explícitos (BEGIN/END).
    -- Removido 'COMMIT;'
END;
$$;

-- Stored Procedure para atualizar progresso de quest
CREATE OR REPLACE PROCEDURE sp_atualizar_progresso_quest(
    p_jogador_id INT,
    p_quest_id INT,
    p_incremento INT DEFAULT 1
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_progresso_atual INT;
    v_progresso_maximo INT;
    v_current_status VARCHAR(20);
BEGIN
    -- Buscar progresso atual e status
    SELECT progresso_atual, progresso_maximo, status INTO v_progresso_atual, v_progresso_maximo, v_current_status
    FROM quest_progresso
    WHERE id_jogador = p_jogador_id AND id_quest = p_quest_id;

    -- **CORREÇÃO**: Verificar se a quest existe para o jogador e está em progresso
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Quest ID % for Player ID % not found or not initiated.', p_quest_id, p_jogador_id;
    END IF;

    IF v_current_status = 'Completada' THEN
        RAISE NOTICE 'Quest ID % for Player ID % is already completed.', p_quest_id, p_jogador_id;
        RETURN;
    END IF;

    -- Atualizar progresso
    UPDATE quest_progresso
    SET progresso_atual = LEAST(progresso_atual + p_incremento, progresso_maximo)
    WHERE id_jogador = p_jogador_id AND id_quest = p_quest_id;

    -- Verificar se quest foi completada
    -- **CORREÇÃO**: Usar o progresso ATUALIZADO da tabela
    SELECT progresso_atual INTO v_progresso_atual
    FROM quest_progresso
    WHERE id_jogador = p_jogador_id AND id_quest = p_quest_id;

    IF v_progresso_atual >= v_progresso_maximo THEN
        CALL sp_completar_quest(p_jogador_id, p_quest_id);
    END IF;

    -- **CORREÇÃO**: COMMIT não é usado diretamente dentro de procedures no PostgreSQL.
    -- Removido 'COMMIT;'
END;
$$;

-- Trigger para loggar movimentos do jogador
CREATE OR REPLACE FUNCTION func_log_movimento()
RETURNS TRIGGER AS $$
DECLARE
    v_cenario_nome VARCHAR(100);
BEGIN
    -- Buscar nome do cenário
    -- **CORREÇÃO**: OLD.cenario não existe na tabela 'personagem',
    -- assume-se que 'cenario' é uma coluna em 'jogador' ou que 'NEW.cenario_id' é usado.
    -- Ajustei para assumir que a tabela 'jogador' tem uma coluna 'id_cenario_atual'.
    -- Se 'cenario' for o ID do cenário na tabela 'jogador', então o uso de 'NEW.cenario' está correto para obter o ID.
    -- Adicionei um SELECT para obter o nome do cenário a partir do ID.
    SELECT nome_cenario INTO v_cenario_nome FROM cenario WHERE id_cenario = NEW.id_cenario_atual;

    -- **CORREÇÃO**: As condições CASE são desnecessárias se você já está buscando o nome do cenário.
    -- Se o cenário não for encontrado, 'v_cenario_nome' será NULL.

    INSERT INTO diario_eventos (
        id_jogador,
        tipo_evento,
        descricao,
        cenario_id -- Corrigido para usar a coluna cenario_id
    )
    VALUES (
        NEW.ID_personagem,
        'Movimento',
        'Jogador moveu-se para: ' || COALESCE(v_cenario_nome, 'Cenário Desconhecido'),
        NEW.id_cenario_atual -- Corrigido para usar a coluna cenario_id do jogador
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- **ASSUNÇÃO/CORREÇÃO**: Adicionei a coluna 'id_cenario_atual' à tabela 'jogador'
-- para que o trigger de movimento tenha um campo para monitorar.
ALTER TABLE jogador ADD COLUMN IF NOT EXISTS id_cenario_atual INTEGER REFERENCES cenario(id_cenario);

CREATE TRIGGER trg_log_movimento
AFTER UPDATE OF id_cenario_atual ON jogador -- Trigger quando a coluna de cenário do jogador é atualizada
FOR EACH ROW
WHEN (NEW.id_cenario_atual IS DISTINCT FROM OLD.id_cenario_atual) -- Garante que só dispara se o cenário realmente mudar
EXECUTE FUNCTION func_log_movimento();