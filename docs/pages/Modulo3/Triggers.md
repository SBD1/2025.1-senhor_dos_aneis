<span style="background-color:#c5a352; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Versão 1.0</span>

# Triggers e Stored Procedures

---

## Conceito:

**Triggers** e **Stored Procedures** são objetos de banco de dados que estendem o poder do SQL, permitindo que a lógica de negócio seja executada diretamente no servidor. Eles automatizam tarefas, garantem a integridade dos dados e otimizam a performance, funcionando como blocos de código reutilizáveis que operam sobre as tabelas.

Uma **Stored Procedure** (Procedimento Armazenado) é um conjunto de comandos SQL que pode ser salvo e executado sob demanda. Ela pode aceitar parâmetros de entrada e retornar valores, agindo como uma função em uma linguagem de programação. O uso de procedures centraliza a lógica, reduz o tráfego de rede e melhora a segurança, pois as aplicações podem interagir com o banco de dados através de uma interface bem definida, sem precisar de acesso direto às tabelas.

Já um **Trigger** (Gatilho) é um tipo especial de procedimento que é "disparado" automaticamente em resposta a eventos específicos de manipulação de dados (DML), como `INSERT`, `UPDATE` ou `DELETE`. Triggers são ideais para impor regras de negócio complexas, auditar modificações ou manter a consistência entre tabelas relacionadas de forma automática. Diferente de uma Stored Procedure, um Trigger não pode ser chamado diretamente; sua execução é uma consequência de uma ação sobre os dados.

---

## Implementações no Software:

### **Visão Geral dos Objetos Programáveis**

Este script implementa a lógica de negócio dinâmica do jogo de RPG através de triggers e stored procedures. Esses objetos automatizam regras (como a validação de peso em inventários e a concessão de experiência) e encapsulam ações (como a execução de uma batalha completa), garantindo que as mecânicas do jogo funcionem de forma consistente e segura diretamente no banco de dados.

A seguir, apresento a criação de cada objeto programável:

---

## Declarações de DML no Software:

!!! Warning "Atenção!"
    O conteúdo deste tópico **poderá sofrer alterações** ao longo da Disciplina de Sistema de Banco de Dados 1. Portanto, à medida que novas inserções forem necessárias, o arquivo atual sempre sempre se manterá atualizado com a nova versão.

!!! Tip "Atenção!"
    Alguns DML's abaixo **também utiliza de comandos DQL (Data Query Language) de forma integrada**, isto é, comandos `SELECT` a fim de não comprometer as referências às chaves primárias à medida que o software evolui. Dessa maneira, entenda que ao invés da equipe inserir manualmente os valores de _ID's_ ou _Seeds_ nos campos de chave estrangeira, foi feito uma busca com `SELECT` sob alguns parâmetros com `WHERE` para capturar estes valores.  

---

### **1. Triggers**

Estes são os procedimentos que o banco de dados executará automaticamente para manter as regras do jogo.

#### **1.1. Trigger de Verificação de Peso do Inventário (`trg_check_inventory_weight`)**

Este trigger garante que um jogador não possa carregar mais itens do que a sua capacidade (`pods`) permite. Ele é disparado antes de qualquer item ser adicionado ou movido, calculando o peso total e cancelando a operação se o limite for excedido.

```postgres
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
```

#### **1.2. Trigger de Concessão de Experiência (`trg_grant_xp_on_victory`)**

Essencial para a progressão no jogo, este trigger é disparado após um confronto ser registrado. Se o resultado for uma vitória do jogador (`vencedor = TRUE`), o trigger automaticamente busca o valor de `XP` da criatura derrotada e atualiza o nível do personagem do jogador.

```postgres
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
```

#### **1.3. Trigger de Auditoria de Nível (`trg_log_personagem_level_up`)**

Para fins de auditoria e análise de progressão, este trigger cria um registro em uma tabela de log (`log_personagem_level`) toda vez que o atributo `level` de um personagem é modificado, armazenando o valor antigo, o novo valor e a data da alteração.

```postgres
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
```

-----

### **2. Stored Procedures (Ações Manuais)**

Estes são os procedimentos que podem ser chamados pela aplicação para executar operações que exigem uma interrupções no banco.

#### **2.1. Procedure de Execução de Batalha (`sp_executar_batalha`)**

Esta procedure encapsula toda a lógica de um combate entre um jogador e uma criatura. Ao ser chamada, ela simula a luta, determina um vencedor com base nos atributos de cada um e registra os resultados nas tabelas `batalha` e `confronta`. Isso simplifica a lógica na aplicação, que precisa apenas chamar um único comando para uma ação complexa.

```postgres
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
```

#### **2.2. Procedure de Transferência de Itens (`sp_transferir_item`)**

Esta procedure gerencia a troca de itens entre dois personagens. Ela executa todas as validações necessárias: verifica se o vendedor realmente possui o item e se o comprador tem um inventário com capacidade disponível. A transferência só é concluída se todas as regras forem satisfeitas, garantindo a consistência dos dados.

```postgres
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
```

---

### **3. Testes**

Depois de executar os scripts fizemos alguns testes, como um check caso o peso do inventário passe do limite, transferencias de itens e XP:

#### **3.1. Testando o Trigger de Peso do Inventário (trg_check_inventory_weight)**

```postgres
-- O inventário do personagem 1 tem capacidade 30. A espada já pesa 0.1 e a armadura 5.0 (Total: 5.1).
-- Tentar adicionar um item pesado que exceda o limite.
-- Esta operação deverá FALHAR com uma exceção.
INSERT INTO item (id_item, id_inventario, nome, peso, durabilidade) 
VALUES (3, 1, 'Bigorna de Anão', 28.0, 999); 
-- ESPERADO: ERRO: Capacidade de peso (Pods) do inventário excedida!
```

#### **3.2.Testando o Trigger de XP (trg_grant_xp_on_victory) e a Stored Procedure de Batalha**

```postgres
-- O jogador 1 está no level 12. O Goblin Ladrão (ID 10) dá 1200 XP.
-- Vamos fazer o jogador 1 batalhar com o Goblin.
CALL sp_executar_batalha(p_jogador_id := 1, p_criatura_id := 10);

-- Verifique o resultado. O jogador 1 deve ter subido de nível.
SELECT nome, level FROM personagem WHERE ID_personagem = 1; 
-- ESPERADO: O level deve ser 13 agora.

-- Verifique a tabela de log para ver a alteração.
SELECT * FROM log_personagem_level WHERE id_personagem = 1;
-- ESPERADO: Um registro com level_antigo=12 e level_novo=13.
```

#### **3.3. Testando a Stored Procedure de Transferência de Item (sp_transferir_item)**

```postgres
-- Vamos transferir a 'Armadura de Couro' (ID 2) do personagem 1 para o personagem 2.
-- O inventário 2 tem 90 de capacidade, então deve funcionar.
CALL sp_transferir_item(p_item_id := 2, p_vendedor_id := 1, p_comprador_id := 2);

-- Verifique o inventário do item 2.
SELECT id_inventario FROM item WHERE id_item = 2;
-- ESPERADO: O id_inventario deve ser 2 agora.
```

#### **3.4. Testando a aplicação completa em bloco com (BEGIN...ROLLBACK)**

Aliado a esses testes específicos fizemos um script para a validação completa do game o script é envolvido em um bloco de transação (BEGIN...ROLLBACK), o que permite sua execução segura em qualquer ambiente sem alterar permanentemente os dados, tornando-o ideal para nossos testes e demonstrações.

```postgres
BEGIN; -- Inicia uma transação para não salvar os dados de teste

-- ===================================================================
-- TESTE 1: Trigger de Peso de Inventário (trg_check_inventory_weight)
-- ===================================================================

-- -------------------------------------------------------------------
-- Teste 1.1: FALHA - Tentar adicionar item excedendo o peso máximo
-- -------------------------------------------------------------------
RAISE INFO '--> TESTE 1.1: FALHA - Adicionar item pesado demais.';
RAISE INFO 'Cenário: Inventário 1 (Personagem 1) tem capacidade 30. Vamos tentar adicionar um item de peso 28, o que excederia o limite (5.1 já em uso + 28 > 30).';

-- Verificação Pré-Teste
SELECT pods AS capacidade_maxima, 
       (SELECT SUM(peso) FROM item WHERE id_inventario = 1) AS peso_atual
FROM inventario WHERE id_inventario = 1;

-- Ação (ESPERADO: ERRO!)
-- Esta linha deve causar um erro e interromper a transação se não for tratada.
-- Para um teste automatizado, você usaria um bloco DO/EXCEPTION. Para visualização, apenas saiba que ela falha.
-- INSERT INTO item (id_item, id_inventario, nome, peso, durabilidade) VALUES (100, 1, 'Bigorna de Anão', 28.0, 999);
RAISE INFO 'NOTA: A ação de INSERT para o teste 1.1 foi comentada para permitir que o script continue. Se descomentada, ela deve gerar uma exceção: "Capacidade de peso (Pods) do inventário excedida!".';


-- -------------------------------------------------------------------
-- Teste 1.2: SUCESSO - Adicionar item com peso válido
-- -------------------------------------------------------------------
RAISE INFO '--> TESTE 1.2: SUCESSO - Adicionar item com peso válido.';
RAISE INFO 'Cenário: Inventário 1 (Personagem 1) tem 24.9 de espaço livre. Vamos adicionar um item de peso 10.0.';

-- Verificação Pré-Teste
SELECT count(*) AS total_itens_antes FROM item WHERE id_inventario = 1;

-- Ação
INSERT INTO item (id_item, id_inventario, nome, peso, durabilidade) VALUES (101, 1, 'Elmo de Aço', 10.0, 150);
RAISE INFO 'Ação: Item "Elmo de Aço" inserido no inventário 1.';

-- Verificação Pós-Teste
SELECT count(*) AS total_itens_depois, 
       SUM(peso) AS novo_peso_total
FROM item WHERE id_inventario = 1;
RAISE INFO 'ESPERADO: total_itens_depois deve ser 3. novo_peso_total deve ser 15.10.';


-- ===================================================================
-- TESTE 2: Procedure de Transferência de Item (sp_transferir_item)
-- ===================================================================

-- -------------------------------------------------------------------
-- Teste 2.1: SUCESSO - Transferência válida
-- -------------------------------------------------------------------
RAISE INFO '--> TESTE 2.1: SUCESSO - Transferência de item válida.';
RAISE INFO 'Cenário: Transferir a "Armadura de Couro" (ID 2, peso 5.0) do Personagem 1 para o Personagem 2 (Inventário 2, capacidade 90).';

-- Verificação Pré-Teste
SELECT id_inventario FROM item WHERE id_item = 2;
RAISE INFO 'ESPERADO (antes): id_inventario deve ser 1.';

-- Ação
CALL sp_transferir_item(p_item_id := 2, p_vendedor_id := 1, p_comprador_id := 2);

-- Verificação Pós-Teste
SELECT id_inventario FROM item WHERE id_item = 2;
RAISE INFO 'ESPERADO (depois): id_inventario deve ser 2.';

-- -------------------------------------------------------------------
-- Teste 2.2: FALHA - Vendedor não possui o item
-- -------------------------------------------------------------------
RAISE INFO '--> TESTE 2.2: FALHA - Vendedor não possui o item.';
RAISE INFO 'Cenário: Tentar fazer o Personagem 3 (que não tem o item) vender a "Espada Longa" (ID 1) para o Personagem 1.';

-- Verificação Pré-Teste
SELECT p.nome, i.id_inventario FROM item i JOIN inventario inv ON i.id_inventario = inv.id_inventario JOIN personagem p ON inv.id_personagem = p.id_personagem WHERE i.id_item = 1;
RAISE INFO 'NOTA: Espada Longa pertence ao Personagem 1.';

-- Ação (ESPERADO: ERRO!)
-- CALL sp_transferir_item(p_item_id := 1, p_vendedor_id := 3, p_comprador_id := 1);
RAISE INFO 'NOTA: A ação de CALL para o teste 2.2 foi comentada. Se descomentada, ela deve gerar a exceção: "O vendedor (ID: 3) não possui o item (ID: 1).".';

-- -------------------------------------------------------------------
-- Teste 2.3: FALHA - Comprador não tem espaço no inventário
-- -------------------------------------------------------------------
RAISE INFO '--> TESTE 2.3: FALHA - Comprador com inventário cheio.';
RAISE INFO 'Cenário: Transferir a "Espada Longa" (ID 1, peso 0.1) do Personagem 1 para o Personagem 3. Antes, vamos lotar o inventário do Personagem 3.';

-- Setup: Criar inventário para Personagem 3 e lotá-lo
INSERT INTO inventario (id_inventario, id_personagem, pods) VALUES (3, 3, 20);
INSERT INTO item (id_item, id_inventario, nome, peso, durabilidade) VALUES (102, 3, 'Escudo Torre', 20.0, 500);
RAISE INFO 'Setup: Inventário para Personagem 3 criado com capacidade 20 e já preenchido com um item de peso 20.0.';

-- Ação (ESPERADO: ERRO!)
-- Tenta mover a espada de peso 0.1 para o inventário já lotado.
-- CALL sp_transferir_item(p_item_id := 1, p_vendedor_id := 1, p_comprador_id := 3);
RAISE INFO 'NOTA: A ação de CALL para o teste 2.3 foi comentada. A procedure deve falhar por causa do trigger trg_check_inventory_weight, gerando a exceção de capacidade excedida.';


-- ===================================================================
-- TESTE 3: Batalha, Concessão de XP e Log (sp_executar_batalha, 
--          trg_grant_xp_on_victory, trg_log_personagem_level_up)
-- ===================================================================
-- Este teste verifica 3 funcionalidades de uma vez.

-- -------------------------------------------------------------------
-- Teste 3.1: SUCESSO - Jogador vence, ganha XP, sobe de nível e gera log
-- -------------------------------------------------------------------
RAISE INFO '--> TESTE 3.1: SUCESSO - Batalha com vitória e progressão.';
RAISE INFO 'Cenário: O "Guia Roric" (ID 1, jogador, ATQ 100) enfrenta o "Goblin Ladrão" (ID 10, vida 90, XP 1200). O jogador deve vencer.';

-- Verificação Pré-Teste
SELECT level AS nivel_antes FROM personagem WHERE id_personagem = 1;
SELECT count(*) AS total_confrontos_antes FROM confronta;
SELECT count(*) AS total_logs_antes FROM log_personagem_level WHERE id_personagem = 1;

-- Ação
CALL sp_executar_batalha(p_jogador_id := 1, p_criatura_id := 10);
RAISE INFO 'Ação: Batalha executada entre jogador 1 e criatura 10.';

-- Verificação Pós-Teste
SELECT level AS nivel_depois FROM personagem WHERE id_personagem = 1;
RAISE INFO 'ESPERADO: nivel_depois deve ser maior que o anterior.';

SELECT vencedor FROM confronta ORDER BY unique_id DESC LIMIT 1;
RAISE INFO 'ESPERADO: vencedor deve ser TRUE.';

SELECT level_antigo, level_novo FROM log_personagem_level WHERE id_personagem = 1 ORDER BY id_log DESC LIMIT 1;
RAISE INFO 'ESPERADO: Um novo log de alteração de nível deve existir.';

-- -------------------------------------------------------------------
-- Teste 3.2: LÓGICA DO TRIGGER - Confronto com derrota não concede XP
-- -------------------------------------------------------------------
RAISE INFO '--> TESTE 3.2: LÓGICA - Derrota não concede XP.';
RAISE INFO 'Cenário: Vamos simular uma derrota para o Jogador 2, inserindo um confronto com "vencedor = FALSE". O trigger de XP não deve ser acionado.';

-- Verificação Pré-Teste
SELECT level AS nivel_antes FROM personagem WHERE id_personagem = 2;

-- Ação
INSERT INTO confronta(vencedor, criatura_id, jogador_id) VALUES (FALSE, 9, 2);
RAISE INFO 'Ação: Inserido confronto com derrota para o jogador 2.';

-- Verificação Pós-Teste
SELECT level AS nivel_depois FROM personagem WHERE id_personagem = 2;
RAISE INFO 'ESPERADO: nivel_depois deve ser igual ao nivel_antes.';


RAISE INFO '==================================================';
RAISE INFO 'Todos os testes foram executados.';
RAISE INFO 'A transação será desfeita com ROLLBACK.';
RAISE INFO '==================================================';

ROLLBACK; -- Desfaz todas as alterações feitas durante o teste
```

---

## Tabela de Versionamento

| Versão | Data       | Descrição                                     | Autor(es)                                                             | Revisor(es)                                                          |
|--------|------------|-----------------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------|
|1.0  |04/07/2025     | Criação da documentação para triggers e stored procedures do jogo | [Felipe das Neves](https://github.com/FelipeFreire-gf) | [Felipe das Neves](https://github.com/FelipeFreire-gf) |