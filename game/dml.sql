-- Inserindo dados na tabela batalha
INSERT INTO batalha (Dano_causado, Controle_Dano, Ambiente_batalha, Dano_sofrido) VALUES
(100, 80, 'Floresta de Fangorn', 50),
(150, 90, 'Moria', 75),
(200, 95, 'Portão Negro de Mordor', 120),
(80, 70, 'Rohan', 40),
(120, 85, 'Gondor', 60); 

-- Inserção de dados na tabela Jogador
INSERT INTO jogador (ID_personagem, cenario, tipo_equipamento) VALUES
(1, 1, 'Espada'),
(2, 1, 'Cajado'),
(3, 2, 'Arco');

-- Inserção de dados na tabela Skill
INSERT INTO skill (ID_jogador, atq) VALUES
(1, 100),
(2, 80),
(3, 90);

-- Inserção de dados na tabela Caracteristicas
INSERT INTO caracteristicas (ID_jogador, fogo, agua, terra, ar) VALUES
(1, 50, 30, 40, 20),
(2, 70, 50, 30, 40),
(3, 40, 60, 30, 50); 


INSERT INTO Inventario (ID_Inventario, ID_personagem, Pods)
VALUES 
    (1, 1, 30),   
    (2, 2, 90);   


INSERT INTO Item (ID_Item, ID_Inventario, peso, durabilidade)
VALUES 
    (1, 1, 0.1, 250),   
    (2, 2, 4.5, 200),  
    (3, 1, 2.0, 100);  

INSERT INTO Arma (ID_item, dano)
VALUES 
    (1, 50),   
    (2, 25);   

INSERT INTO Armadura (ID_item, defesa)
VALUES 
    (1, 95);   


-- Felipe

-- Inserindo dados na tabela base Personagem
-- (Assumindo que o SERIAL vai gerar os IDs 1, 2, 3 e 4)
INSERT INTO Personagem (nome, vida_maxima, mana_maxima, habilidade, dificuldade, level, resistencia, dialogo) VALUES
('Roric, o Guia', 100, 150, 'Navegação', 'Normal', 12, 'Gelo', 'Olá, viajante! Posso te ajudar a encontrar seu destino por algumas moedas.'),
('Borgar, o Mercador', 150, 50, 'Comércio', 'Fácil', 18, 'Nenhuma', 'Tenho os melhores itens deste lado da montanha! Dê uma olhada.'),
('Lord Valerius', 120, 120, 'Liderança', 'Difícil', 25, 'Persuasão', 'Bem-vindo ao meu domínio. Cumpra uma tarefa para mim e será recompensado.'),
('Elara, a Cidadã', 80, 80, 'Culinária', 'Fácil', 5, 'Nenhuma', 'Um belo dia para um passeio na praça, não acha?');


-- Inserindo dados nas tabelas especializadas usando os IDs correspondentes

-- Roric (ID 1) é um Guia
INSERT INTO Guia (ID_personagem, custo_orientacao) VALUES
(1, 75.50);

-- Borgar (ID 2) é um Comerciante
INSERT INTO Comerciante (ID_personagem, venda_item, compra_item) VALUES
(2, 'Poções de cura, Adagas de ferro', 'Ervas raras, Peles de lobo');

-- Lord Valerius (ID 3) é um NPC que oferece uma quest
INSERT INTO NPC (ID_personagem, quest, localizacao, hora_aparicao) VALUES
(3, 'Derrote o líder dos goblins na floresta sombria.', 'Sala do Trono do Castelo', '14:00:00');

-- Gabriel

- Inserindo Criaturas
INSERT INTO Criatura (XP) VALUES (1500); -- ID 1
INSERT INTO Criatura (XP) VALUES (1200); -- ID 2
INSERT INTO Criatura (XP) VALUES (5000); -- ID 3
INSERT INTO Criatura (XP) VALUES (1000); -- ID 4 (Jogador)

-- Inserindo Ork (referencia ID 1)
INSERT INTO Ork (ID_personagem, Raiva) VALUES (1, 90);

-- Inserindo Goblin (referencia ID 2)
INSERT INTO Goblin (ID_personagem, furtividade, roubo) VALUES (2, 75, 40);

-- Inserindo Boss (referencia ID 3)
INSERT INTO Boss (ID_personagem, faseAtual, imunidades) VALUES (3, 2, 'fogo,veneno');