-- Função para mover personagem
CREATE OR REPLACE FUNCTION mover_jogador(p_jogador_id INT, p_direcao VARCHAR(10))
RETURNS VARCHAR(200) AS $$
DECLARE
    v_cenario_atual INT;
    v_novo_cenario INT;
    v_descricao TEXT;
BEGIN
    -- Pegar cenário atual
    SELECT cenario INTO v_cenario_atual FROM jogador WHERE ID_personagem = p_jogador_id;
    
    -- Determinar novo cenário baseado na direção
    CASE p_direcao
        WHEN 'norte' THEN
            SELECT norte_id INTO v_novo_cenario FROM cenario WHERE id_cenario = v_cenario_atual;
        WHEN 'sul' THEN
            SELECT sul_id INTO v_novo_cenario FROM cenario WHERE id_cenario = v_cenario_atual;
        WHEN 'leste' THEN
            SELECT leste_id INTO v_novo_cenario FROM cenario WHERE id_cenario = v_cenario_atual;
        WHEN 'oeste' THEN
            SELECT oeste_id INTO v_novo_cenario FROM cenario WHERE id_cenario = v_cenario_atual;
    END CASE;
    
    -- Verificar se movimento é válido
    IF v_novo_cenario IS NULL THEN
        RETURN 'Não há caminho nesta direção.';
    END IF;
    
    -- Atualizar posição do jogador
    UPDATE jogador SET cenario = v_novo_cenario WHERE ID_personagem = p_jogador_id;
    
    -- Retornar descrição do novo local
    SELECT CONCAT('Você chegou ao cenário ', v_novo_cenario, '. Clima: ', sol) 
    INTO v_descricao FROM cenario WHERE id_cenario = v_novo_cenario;
    
    RETURN v_descricao;
END;
$$ LANGUAGE plpgsql;

-- Procedure para batalha completa
CREATE OR REPLACE PROCEDURE batalha_completa(p_jogador_id INT, p_criatura_id INT)
LANGUAGE plpgsql AS $$
DECLARE
    v_classe_jogador VARCHAR(20);
    v_ataque_base INT;
    v_ataque_especial INT;
    v_vida_criatura INT;
    v_resistencia_criatura VARCHAR(255);
    v_dano_final INT;
    v_vitoria BOOLEAN;
    v_ambiente VARCHAR(100);
BEGIN
    -- Determinar classe do jogador e ataques
    IF EXISTS(SELECT 1 FROM guerreiro WHERE id_personagem = p_jogador_id) THEN
        SELECT atq_Fisico INTO v_ataque_especial FROM guerreiro WHERE id_personagem = p_jogador_id;
        v_classe_jogador := 'Guerreiro';
    ELSIF EXISTS(SELECT 1 FROM mago WHERE id_personagem = p_jogador_id) THEN
        SELECT atq_Magico INTO v_ataque_especial FROM mago WHERE id_personagem = p_jogador_id;
        v_classe_jogador := 'Mago';
    ELSIF EXISTS(SELECT 1 FROM sacerdote WHERE id_personagem = p_jogador_id) THEN
        SELECT atq_Especial INTO v_ataque_especial FROM sacerdote WHERE id_personagem = p_jogador_id;
        v_classe_jogador := 'Sacerdote';
    ELSIF EXISTS(SELECT 1 FROM arqueiro WHERE id_personagem = p_jogador_id) THEN
        SELECT atq_Preciso INTO v_ataque_especial FROM arqueiro WHERE id_personagem = p_jogador_id;
        v_classe_jogador := 'Arqueiro';
    END IF;
    
    -- Pegar ataque base e vida da criatura
    SELECT s.atq INTO v_ataque_base FROM skill s WHERE s.ID_jogador = p_jogador_id;
    SELECT vida_maxima, resistencia INTO v_vida_criatura, v_resistencia_criatura 
    FROM personagem WHERE ID_personagem = p_criatura_id;
    
    -- Calcular dano (base + especialização)
    v_dano_final := v_ataque_base + v_ataque_especial;
    
    -- Aplicar modificadores baseados em resistências
    IF v_resistencia_criatura LIKE '%Físico%' AND v_classe_jogador = 'Guerreiro' THEN
        v_dano_final := v_dano_final / 2;
    ELSIF v_resistencia_criatura LIKE '%Fogo%' AND v_classe_jogador = 'Mago' THEN
        v_dano_final := v_dano_final / 2;
    END IF;
    
    -- Determinar ambiente baseado no cenário atual
    SELECT CASE 
        WHEN cenario = 1 THEN 'Acampamento Élfico'
        WHEN cenario = 2 THEN 'Estrada Perigosa'
        WHEN cenario = 3 THEN 'Portões Sombrios'
        WHEN cenario = 4 THEN 'Salões Ancestrais'
        WHEN cenario = 5 THEN 'Forja Flamejante'
        WHEN cenario = 6 THEN 'Câmara de Espelhos'
        WHEN cenario = 7 THEN 'Torre dos Ventos'
        ELSE 'Local Desconhecido'
    END INTO v_ambiente
    FROM jogador WHERE ID_personagem = p_jogador_id;
    
    -- Determinar vitória
    v_vitoria := v_dano_final >= v_vida_criatura;
    
    -- Registrar batalha
    INSERT INTO batalha (Dano_causado, Controle_Dano, Ambiente_batalha, Dano_sofrido)
    VALUES (v_dano_final, 100, v_ambiente, CASE WHEN v_vitoria THEN 0 ELSE 30 END);
    
    -- Registrar confronto
    INSERT INTO confronta (vencedor, criatura_id, jogador_id)
    VALUES (v_vitoria, p_criatura_id, p_jogador_id);
END;
$$;

-- Verificar se jogador coletou todos os anéis
CREATE OR REPLACE FUNCTION verificar_vitoria(p_jogador_id INT)
RETURNS BOOLEAN AS $$
DECLARE
    v_aneis_coletados INT;
BEGIN
    SELECT COUNT(*) INTO v_aneis_coletados
    FROM item i
    JOIN inventario inv ON i.id_inventario = inv.id_inventario
    WHERE inv.id_personagem = p_jogador_id
    AND i.nome IN ('Anel da Proteção', 'Anel da Invisibilidade Menor', 'Anel da Compreensão');
    
    RETURN v_aneis_coletados = 3;
END;
$$ LANGUAGE plpgsql;
