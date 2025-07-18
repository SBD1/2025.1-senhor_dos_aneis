<span style="background-color:#c5a352; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Versão 1.0</span>

# Data Manipulation Language

## Conceito:

A Data Manipulation Language (DML), ou Linguagem de Manipulação de Dados, é a parte do SQL responsável por lidar diretamente com os dados armazenados nas estruturas definidas pela DDL. Enquanto a DDL define "onde" os dados vão ficar, a DML atua sobre "quais" dados vão ocupar esses espaços e "como" serão manipulados. Com comandos como `SELECT`, `INSERT`, `UPDATE` e `DELETE`, a DML permite consultar, adicionar, modificar e remover registros dentro das tabelas do banco de dados.

Ao contrário dos comandos DDL, que geralmente afetam a estrutura do banco de forma permanente, os comandos DML operam sobre os dados em si e podem ser revertidos com o uso de transações (`BEGIN`, `COMMIT`, `ROLLBACK`). Isso garante maior controle sobre as operações, especialmente em aplicações que exigem consistência e segurança na manipulação de dados.

---
## Declarações de DML no Software:

!!! Warning "Atenção!"
    O conteúdo deste tópico **poderá sofrer alterações** ao longo da Disciplina de Sistema de Banco de Dados 1. Portanto, à medida que novas inserções forem necessárias, o arquivo atual sempre sempre se manterá atualizado com a nova versão.

!!! Tip "Atenção!"
    Alguns DML's abaixo **também utiliza de comandos DQL (Data Query Language) de forma integrada**, isto é, comandos `SELECT` a fim de não comprometer as referências às chaves primárias à medida que o software evolui. Dessa maneira, entenda que ao invés da equipe inserir manualmente os valores de _ID's_ ou _Seeds_ nos campos de chave estrangeira, foi feito uma busca com `SELECT` sob alguns parâmetros com `WHERE` para capturar estes valores.  


??? info "_1. Personagens Base_ INSERT's"

    ```Postgres
    -- ============================================
    -- 1. TODOS OS PERSONAGENS BASE
    -- ============================================
    INSERT INTO personagem (nome, vida_maxima, mana_maxima, habilidade, dificuldade, level, resistencia, dialogo) VALUES
    ('Roric, o Guia', 100, 150, 'Navegação', 'Normal', 12, 'Gelo', 'Olá, viajante! Posso te ajudar a encontrar seu destino por algumas moedas.'), -- ID 1
    ('Borgar, o Mercador', 150, 50, 'Comércio', 'Fácil', 18, 'Nenhuma', 'Tenho os melhores itens deste lado da montanha! Dê uma olhada.'), -- ID 2
    ('Lord Valerius', 120, 120, 'Liderança', 'Difícil', 25, 'Persuasão', 'Bem-vindo ao meu domínio. Cumpra uma tarefa para mim e será recompensado.'), -- ID 3
    ('Elara, a Cidadã', 80, 80, 'Culinária', 'Fácil', 5, 'Nenhuma', 'Um belo dia para um passeio na praça, não acha?'), -- ID 4
    ('Aeldrin, o Mago', 90, 200, 'Feitiçaria', 'Média', 14, 'Fogo', 'O conhecimento está nas runas antigas.'), -- ID 5
    ('Thalas, o Invocador', 100, 180, 'Invocação', 'Alta', 16, 'Sombras', 'O mundo espiritual é volátil.'), -- ID 6
    ('Lira, a Arqueira', 85, 110, 'Precisão', 'Normal', 13, 'Ar', 'Nada escapa dos meus olhos.'), -- ID 7
    ('Kira, a Caçadora', 90, 100, 'Furtividade', 'Difícil', 15, 'Vento', 'Eu vejo o que os outros não enxergam.'), -- ID 8
    ('Ork Bruto', 200, 20, 'Força Bruta', 'Média', 10, 'Físico', 'GRRRR!'), -- ID 9
    ('Goblin Ladrão', 90, 60, 'Roubo', 'Fácil', 7, 'Furtividade', 'Hehe, peguei seu ouro!'), -- ID 10
    ('Rei Demônio', 500, 250, 'Magia Negra', 'Extrema', 20, 'Fogo', 'Você jamais sairá vivo daqui!'); -- ID 11
    ```

??? info "_2. Especializações de NPCs_ INSERT's"

    ```Postgres
    -- ============================================
    -- 2. ESPECIALIZAÇÕES DE PERSONAGEM (NPCs)
    -- ============================================
    INSERT INTO guia (ID_personagem, custo_orientacao) VALUES (1, 75.50);

    INSERT INTO comerciante (ID_personagem, venda_item, compra_item) VALUES 
    (2, 'Poções de cura, Adagas de ferro', 'Ervas raras, Peles de lobo');

    INSERT INTO npc (ID_personagem, quest, localizacao, hora_aparicao) VALUES 
    (3, 'Derrote o líder dos goblins na floresta sombria.', 'Sala do Trono do Castelo', '14:00:00');
    ```

??? info "_3. Criaturas_ INSERT's"

    ```Postgres
    -- ============================================
    -- 3. CRIATURAS
    -- ============================================
    INSERT INTO criatura (ID_personagem, XP) VALUES 
    (9, 1500),
    (10, 1200),
    (11, 5000);

    INSERT INTO ork (ID_personagem, Raiva) VALUES (9, 90);

    INSERT INTO goblin (ID_personagem, furtividade, roubo) VALUES (10, 75, 40);

    INSERT INTO boss (ID_personagem, faseAtual, imunidades) VALUES (11, 2, 'fogo,veneno');
    ```

??? info "_4. Cenários_ INSERT's"

    ```Postgres
    -- ============================================
    -- 4. CENÁRIOS
    -- ============================================
    INSERT INTO cenario (norte_id, leste_id, oeste_id, sul_id, sol, chuva, noite, dia) VALUES
    (NULL, 2, NULL, 3, 'Ensolarado', 'Sem chuva', 'Lua cheia', 'Claro'), -- ID 1
    (NULL, NULL, 1, 4, 'Nublado', 'Chuva fraca', 'Escuro', 'Parcialmente nublado'), -- ID 2
    (1, 4, NULL, NULL, 'Sol forte', 'Tempestade', 'Estrelado', 'Brilhante'), -- ID 3
    (3, NULL, 2, NULL, 'Pôr do sol', 'Garoa', 'Neblina', 'Amanhecer'); -- ID 4
    ```

??? info "_5. Jogadores_ INSERT's"

    ```Postgres
    -- ============================================
    -- 5. JOGADORES
    -- ============================================
    INSERT INTO jogador (ID_personagem, cenario, tipo_equipamento) VALUES
    (1, 1, 'Espada'),
    (2, 1, 'Cajado'),
    (3, 2, 'Arco');

    INSERT INTO skill (ID_jogador, atq) VALUES
    (1, 100), (2, 80), (3, 90);

    INSERT INTO caracteristicas (ID_jogador, fogo, agua, terra, ar) VALUES
    (1, 50, 30, 40, 20),
    (2, 70, 50, 30, 40),
    (3, 40, 60, 30, 50);
    ```

??? info "_6. Inventário e Itens_ INSERT's"

    ```Postgres
    -- ============================================
    -- 6. INVENTÁRIO E ITENS
    -- ============================================
    INSERT INTO inventario (ID_inventario, ID_personagem, Pods) VALUES 
    (1, 1, 30),
    (2, 2, 90);

    INSERT INTO item (ID_item, ID_inventario, nome, peso, durabilidade)
    VALUES (1, 1, 'Espada Longa', 0.1, 250);

    INSERT INTO arma (ID_item, mãos, dano) VALUES (1, 1, 50);

    -- NOTA: O mesmo item não pode ser arma E armadura. Vou criar um item separado para armadura
    INSERT INTO item (ID_item, ID_inventario, nome, peso, durabilidade)
    VALUES (2, 1, 'Armadura de Couro', 5.0, 200);

    INSERT INTO armadura (ID_item, defesa) VALUES (2, 95);
    ```

??? info "_7. Classes de Personagem_ INSERT's"

    ```Postgres
    -- ============================================
    -- 7. CLASSES DE PERSONAGEM
    -- ============================================
    INSERT INTO guerreiro (ID_personagem, atq_Fisico, bloquear_Dano) VALUES
    (1, 85, 70),
    (2, 92, 65);

    INSERT INTO sacerdote (ID_personagem, bencao_Cura, atq_Especial) VALUES
    (3, 90, 45),
    (4, 85, 50);

    INSERT INTO mago (ID_personagem, atq_Magico, atq_MultiElemento) VALUES
    (5, 95, 80),
    (6, 88, 75);

    INSERT INTO arqueiro (ID_personagem, atq_Preciso, atq_Rapido) VALUES
    (7, 90, 85),
    (8, 87, 90);
    ```

??? info "_8. Batalhas_ INSERT's"

    ```Postgres
    -- ============================================
    -- 8. BATALHAS
    -- ============================================
    INSERT INTO batalha (Dano_causado, Controle_Dano, Ambiente_batalha, Dano_sofrido) VALUES
    (100, 80, 'Floresta de Fangorn', 50),
    (150, 90, 'Moria', 75),
    (200, 95, 'Portão Negro de Mordor', 120),
    (80, 70, 'Rohan', 40),
    (120, 85, 'Gondor', 60);
    ```

??? info "_9. Confrontos_ INSERT's"

    ```Postgres
    -- ============================================
    -- 9. CONFRONTOS
    -- ============================================
    INSERT INTO confronta (vencedor, criatura_id, jogador_id) VALUES
    (TRUE, 9, 1),
    (FALSE, 10, 2),
    (TRUE, 11, 3);
    ```

---

## Tabela de Versionamento

| Versão | Data       | Descrição                                     | Autor(es)                                                             | Revisor(es)                                                          |
|--------|------------|-----------------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------|
|1.0  |15/06/2025     | Todos os integrantes desenvolveram esse artefato | Todos os Integrantes |Todos os Integrantes|