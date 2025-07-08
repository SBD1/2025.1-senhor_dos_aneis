-- Adicionar NPCs aos cenários
INSERT INTO cenario_npc (id_cenario, id_personagem) VALUES 
-- O Condado (1)
(1, (SELECT ID_personagem FROM personagem WHERE nome = 'Samwise Gamgee')),
(1, (SELECT ID_personagem FROM personagem WHERE nome = 'Frodo Baggins')),
(1, (SELECT ID_personagem FROM personagem WHERE nome = 'Merry Brandybuck')),
(1, (SELECT ID_personagem FROM personagem WHERE nome = 'Pippin Took')),
(1, (SELECT ID_personagem FROM personagem WHERE nome = 'Bilbo Baggins')),

-- Floresta Sombria (2)
(2, (SELECT ID_personagem FROM personagem WHERE nome = 'Legolas')),
(2, (SELECT ID_personagem FROM personagem WHERE nome = 'Gimli')),
(2, (SELECT ID_personagem FROM personagem WHERE nome = 'Treebeard')),
(2, (SELECT ID_personagem FROM personagem WHERE nome = 'Tom Bombadil')),
(2, (SELECT ID_personagem FROM personagem WHERE nome = 'Goldberry')),

-- Montanhas Nebulosas (3)
(3, (SELECT ID_personagem FROM personagem WHERE nome = 'Gandalf, o Cinzento')),
(3, (SELECT ID_personagem FROM personagem WHERE nome = 'Aragorn')),
(3, (SELECT ID_personagem FROM personagem WHERE nome = 'Radagast')),

-- Ruínas de Osgiliath (4)
(4, (SELECT ID_personagem FROM personagem WHERE nome = 'Boromir')),
(4, (SELECT ID_personagem FROM personagem WHERE nome = 'Faramir')),
(4, (SELECT ID_personagem FROM personagem WHERE nome = 'Denethor')),

-- Pântano dos Mortos (5) - já tem Gollum
(5, (SELECT ID_personagem FROM personagem WHERE nome = 'Gollum')),

-- Minas de Moria (6)
(6, (SELECT ID_personagem FROM personagem WHERE nome = 'Gimli')),

-- Colinas do Vento (7)
(7, (SELECT ID_personagem FROM personagem WHERE nome = 'Théoden')),
(7, (SELECT ID_personagem FROM personagem WHERE nome = 'Éowyn')),

-- Porto Cinzento (8)
(8, (SELECT ID_personagem FROM personagem WHERE nome = 'Galadriel')),
(8, (SELECT ID_personagem FROM personagem WHERE nome = 'Elrond'))
ON CONFLICT DO NOTHING; 