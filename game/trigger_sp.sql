-- ===================================================================
-- TRIGGER 1: Validar Peso do Inventário ao Adicionar/Mover Itens
-- ===================================================================
-- DESCRIÇÃO: Antes de um item ser inserido ou atualizado, esta função
-- verifica se o peso do item, somado ao peso dos itens já existentes,
-- não ultrapassa a capacidade (Pods) do inventário de destino.
-- Se ultrapassar, a operação é cancelada com um erro.
-- ===================================================================

-- PASSO 1: A Função do Trigger
CREATE OR REPLACE FUNCTION func_check_inventory_weight()
RETURNS TRIGGER AS $$
DECLARE
    v_total_peso NUMERIC;
    v_max_pods INT;
BEGIN
    -- Se um item está sendo adicionado a um inventário
    IF NEW.id_inventario IS NOT NULL THEN
        -- Pega a capacidade máxima do inventário de destino
        SELECT pods INTO v_max_pods FROM inventario WHERE id_inventario = NEW.id_inventario;

        -- Calcula o peso total dos itens que já estão no inventário
        SELECT COALESCE(SUM(peso), 0) INTO v_total_peso FROM item WHERE id_inventario = NEW.id_inventario;

        -- Se o peso total + peso do novo item exceder a capacidade, lança um erro.
        IF (v_total_peso + NEW.peso) > v_max_pods THEN
            RAISE EXCEPTION 'Capacidade de peso (Pods) do inventário excedida! Operação cancelada.';
        END IF;
    END IF;

    -- Se a verificação passar, permite a operação
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- PASSO 2: A Declaração do Trigger na Tabela 'item'
CREATE TRIGGER trg_check_inventory_weight
BEFORE INSERT OR UPDATE ON item
FOR EACH ROW
EXECUTE FUNCTION func_check_inventory_weight();


-- ===================================================================
-- TRIGGER 2: Conceder XP ao Jogador Após Vitória
-- ===================================================================
-- DESCRIÇÃO: Após um registro de confronto ser inserido na tabela 'confronta',
-- este trigger verifica se o vencedor foi o jogador (vencedor = TRUE).
-- Se sim, ele busca o XP da criatura derrotada e atualiza o level do
-- personagem do jogador (a lógica de level up é simplificada aqui).
-- ===================================================================

-- PASSO 1: A Função do Trigger
CREATE OR REPLACE FUNCTION func_grant_xp_on_victory()
RETURNS TRIGGER AS $$
DECLARE
    v_xp_ganho INT;
    v_jogador_level_atual INT;
BEGIN
    -- Verifica se o confronto foi uma vitória para o jogador
    IF NEW.vencedor = TRUE THEN
        -- Pega o XP da criatura derrotada
        SELECT XP INTO v_xp_ganho FROM criatura WHERE ID_personagem = NEW.criatura_id;

        -- Pega o level atual do jogador
        SELECT level INTO v_jogador_level_atual FROM personagem WHERE ID_personagem = NEW.jogador_id;
        
        -- Atualiza o personagem do jogador com um novo level (lógica de exemplo: +1 level por vitória)
        UPDATE personagem
        SET level = v_jogador_level_atual + 1
        WHERE ID_personagem = NEW.jogador_id;

        -- Exibe uma notificação no console do banco (útil para debug)
        RAISE NOTICE 'Jogador ID % venceu! Ganhou % XP e subiu para o nível %.', 
                     NEW.jogador_id, v_xp_ganho, v_jogador_level_atual + 1;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- PASSO 2: A Declaração do Trigger na Tabela 'confronta'
CREATE TRIGGER trg_grant_xp_on_victory
AFTER INSERT ON confronta
FOR EACH ROW
EXECUTE FUNCTION func_grant_xp_on_victory();


-- ===================================================================
-- TRIGGER 3: Log de Alterações de Nível do Personagem
-- ===================================================================
-- DESCRIÇÃO: Cria uma tabela de log e um trigger que armazena
-- informações sobre qualquer alteração no 'level' de um personagem.
-- Útil para auditoria e para rastrear a progressão.
-- ===================================================================

-- PASSO 1: Criar a tabela de log (se não existir)
CREATE TABLE IF NOT EXISTS log_personagem_level (
    id_log SERIAL PRIMARY KEY,
    id_personagem INT NOT NULL,
    level_antigo INT,
    level_novo INT,
    data_modificacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- PASSO 2: A Função do Trigger
CREATE OR REPLACE FUNCTION func_log_personagem_level_up()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se a coluna 'level' foi de fato alterada
    IF OLD.level IS DISTINCT FROM NEW.level THEN
        INSERT INTO log_personagem_level (id_personagem, level_antigo, level_novo)
        VALUES (OLD.ID_personagem, OLD.level, NEW.level);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- PASSO 3: A Declaração do Trigger na Tabela 'personagem'
CREATE TRIGGER trg_log_personagem_level_up
AFTER UPDATE ON personagem
FOR EACH ROW
EXECUTE FUNCTION func_log_personagem_level_up();


-- ===================================================================
-- STORED PROCEDURE 1: Executar uma Batalha Completa
-- ===================================================================
-- DESCRIÇÃO: Este procedimento executa uma sequência de batalha entre
-- um jogador e uma criatura. Ele simula o dano, determina um vencedor,
-- insere os resultados nas tabelas 'batalha' e 'confronta'.
-- ===================================================================

CREATE OR REPLACE PROCEDURE sp_executar_batalha(p_jogador_id INT, p_criatura_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_ataque_jogador INT;
    v_vida_criatura INT;
    v_dano_causado INT;
    v_vitoria BOOLEAN;
BEGIN
    -- Obter atributos de combate
    SELECT atq INTO v_ataque_jogador FROM skill WHERE ID_jogador = p_jogador_id;
    SELECT vida_maxima INTO v_vida_criatura FROM personagem WHERE ID_personagem = p_criatura_id;

    -- Lógica de batalha simplificada: Dano = ataque do jogador
    v_dano_causado := v_ataque_jogador;
    
    -- Determinar o vencedor
    IF v_dano_causado >= v_vida_criatura THEN
        v_vitoria := TRUE;
    ELSE
        v_vitoria := FALSE;
    END IF;

    -- Registrar o log da batalha
    INSERT INTO batalha (Dano_causado, Controle_Dano, Ambiente_batalha, Dano_sofrido)
    VALUES (v_dano_causado, 100, 'Campo Aberto', 0); -- Valores de exemplo

    -- Registrar o resultado do confronto (isso irá disparar o trigger de XP)
    INSERT INTO confronta (vencedor, criatura_id, jogador_id)
    VALUES (v_vitoria, p_criatura_id, p_jogador_id);

    COMMIT;
END;
$$;


-- ===================================================================
-- STORED PROCEDURE 2: Transferir Item Entre Personagens
-- ===================================================================
-- DESCRIÇÃO: Gerencia a transferência de um item do inventário de um
-- personagem (vendedor) para outro (comprador), validando a posse
-- do item e a capacidade do inventário do comprador.
-- ===================================================================

CREATE OR REPLACE PROCEDURE sp_transferir_item(p_item_id INT, p_vendedor_id INT, p_comprador_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_inventario_vendedor_id INT;
    v_inventario_comprador_id INT;
    v_item_inventario_atual INT;
BEGIN
    -- Pega os IDs dos inventários
    SELECT id_inventario INTO v_inventario_vendedor_id FROM inventario WHERE id_personagem = p_vendedor_id;
    SELECT id_inventario INTO v_inventario_comprador_id FROM inventario WHERE id_personagem = p_comprador_id;
    
    -- Pega o inventário atual do item
    SELECT id_inventario INTO v_item_inventario_atual FROM item WHERE id_item = p_item_id;

    -- Validação 1: O vendedor realmente possui o item?
    IF v_item_inventario_atual IS DISTINCT FROM v_inventario_vendedor_id THEN
        RAISE EXCEPTION 'O vendedor (ID: %) não possui o item (ID: %).', p_vendedor_id, p_item_id;
    END IF;

    -- Validação 2: O comprador tem um inventário?
    IF v_inventario_comprador_id IS NULL THEN
        RAISE EXCEPTION 'O comprador (ID: %) não possui um inventário.', p_comprador_id;
    END IF;

    -- Ação: Atualizar o item para o novo inventário.
    -- O trigger trg_check_inventory_weight será disparado automaticamente aqui para validar o peso.
    UPDATE item SET id_inventario = v_inventario_comprador_id WHERE id_item = p_item_id;

    RAISE NOTICE 'Item ID % transferido com sucesso do personagem % para o personagem %.', p_item_id, p_vendedor_id, p_comprador_id;
    
    COMMIT;
END;
$$;