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
