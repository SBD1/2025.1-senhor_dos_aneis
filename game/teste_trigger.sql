/*******************************************************************
* *
* SCRIPT DE TESTE PARA TRIGGERS E STORED PROCEDURES        *
* Versão do Jogo: 1.0                      *
* *
* INSTRUÇÕES:                                                      *
* 1. Execute este script em um ambiente de teste com os dados      *
* iniciais (DML) já carregados.                                 *
* 2. O script usa um bloco de transação (BEGIN...ROLLBACK) para    *
* garantir que os dados não sejam alterados permanentemente.    *
* Para salvar os resultados, troque 'ROLLBACK' por 'COMMIT'.   *
* *
*******************************************************************/

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