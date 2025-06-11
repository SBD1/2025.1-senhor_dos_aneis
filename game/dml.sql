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


INSERT INTO Inventario (ID_Inventario, ID_personagem, Poder)
VALUES 
    (1, 1, 30),   -- Frodo
    (2, 2, 90);   -- Aragorn


INSERT INTO Item (ID_Item, ID_Inventario, peso, durabilidade)
VALUES 
    (14, 1, 0.1, 250),   -- O Um Anel (Frodo)
    (102, 2, 4.5, 200),  -- Espada Andúril (Aragorn)
    (143, 1, 2.0, 100);  -- Cota de Mithril (Frodo)

INSERT INTO Arma (ID_item, dano, delay)
VALUES 
    (102, 50, 1.2),   -- Andúril
    (14, 25, 0.8);    -- Ferroada (Sting)

INSERT INTO Armadura (ID_item, defesa)
VALUES 
    (143, 95);   -- Cota de Mithril (alta defesa)
