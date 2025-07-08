-- Adicionar NPCs específicos para cada cenário
INSERT INTO personagem (nome, vida_maxima, mana_maxima, habilidade, dificuldade, level, resistencia, dialogo) VALUES 
('Samwise Gamgee', 120, 80, 'Lealdade', 'Normal', 8, 'Luz', 'Sr. Frodo não iria muito longe sem Sam!'),
('Gandalf, o Cinzento', 200, 300, 'Magia Branca', 'Difícil', 25, 'Fogo', 'Um mago nunca chega tarde, nem cedo. Chega exatamente quando pretende.'),
('Legolas', 150, 120, 'Arco Élfico', 'Normal', 15, 'Ar', 'Eles estão vindo...'),
('Gimli', 180, 100, 'Machado Anão', 'Normal', 14, 'Terra', 'E ainda assim você conta como apenas um!'),
('Aragorn', 200, 150, 'Espada de Gondor', 'Difícil', 20, 'Físico', 'Você tem minha espada.'),
('Boromir', 190, 120, 'Horn of Gondor', 'Normal', 18, 'Físico', 'Um não pode simplesmente caminhar para Mordor.'),
('Frodo Baggins', 100, 90, 'Portador do Anel', 'Difícil', 12, 'Luz', 'Vou levar o Anel para Mordor.'),
('Merry Brandybuck', 110, 85, 'Espada de Rohan', 'Normal', 9, 'Físico', 'Por Rohan!'),
('Pippin Took', 105, 80, 'Coragem Hobbit', 'Normal', 8, 'Físico', 'Que aventura!'),
('Galadriel', 250, 400, 'Poder Élfico', 'Difícil', 30, 'Luz', 'O espelho mostra muitas coisas...'),
('Elrond', 220, 350, 'Sabedoria Élfica', 'Difícil', 28, 'Luz', 'A escolha é sua, aventureiro.'),
('Théoden', 180, 120, 'Rei de Rohan', 'Normal', 22, 'Físico', 'Por Rohan e pelo Rei!'),
('Éowyn', 160, 100, 'Escudo-Maiden', 'Normal', 18, 'Físico', 'Não sou um homem!'),
('Faramir', 170, 130, 'Capitão de Gondor', 'Normal', 19, 'Físico', 'Gondor precisa de todos os heróis.'),
('Denethor', 150, 200, 'Senescal de Gondor', 'Difícil', 25, 'Fogo', 'A cidade está perdida...'),
('Treebeard', 300, 150, 'Ent', 'Difícil', 35, 'Terra', 'Hmm, um hobbit...'),
('Tom Bombadil', 500, 500, 'Mestre da Floresta', 'Difícil', 50, 'Luz', 'Hey dol! merry dol!'),
('Goldberry', 200, 300, 'Filha do Rio', 'Normal', 25, 'Água', 'Bem-vindo, viajante!'),
('Bilbo Baggins', 90, 100, 'Aventureiro Aposentado', 'Normal', 15, 'Luz', 'Há muito tempo atrás...'),
('Radagast', 180, 250, 'Mago Marrom', 'Normal', 20, 'Terra', 'Os animais me contam muitas coisas...')
ON CONFLICT DO NOTHING;

-- Adicionar criaturas específicas para cada cenário
INSERT INTO personagem (nome, vida_maxima, mana_maxima, habilidade, dificuldade, level, resistencia, dialogo) VALUES 
('Lobo Sombrio', 80, 50, 'Caça Noturna', 'Normal', 5, 'Sombra', 'Uivo sinistro...'),
('Aranha Gigante', 120, 30, 'Tecelã de Seda', 'Normal', 8, 'Veneno', 'Ssss... presa...'),
('Orc Guerreiro', 100, 60, 'Combate Brutal', 'Normal', 7, 'Físico', 'Grrr... matar!'),
('Troll das Montanhas', 200, 40, 'Força Bruta', 'Difícil', 12, 'Pedra', 'Que cheiro de hobbit...'),
('Nazgûl', 150, 200, 'Terror Sombrio', 'Difícil', 20, 'Sombra', 'Ssss... o anel...'),
('Balrog', 300, 250, 'Demônio Antigo', 'Difícil', 25, 'Fogo', 'Você não pode passar!'),
('Dragão de Gelo', 250, 180, 'Sopro Congelante', 'Difícil', 22, 'Gelo', 'Mortais...'),
('Goblin Arqueiro', 70, 40, 'Tiro Preciso', 'Normal', 6, 'Ar', 'Tchak!'),
('Warg', 90, 30, 'Caçador em Matilha', 'Normal', 6, 'Sombra', 'Auuuu!'),
('Cave Troll', 180, 50, 'Destruidor', 'Normal', 10, 'Pedra', 'Smash!'),
('Haradrim', 85, 60, 'Guerreiro do Sul', 'Normal', 7, 'Físico', 'Por Sauron!'),
('Uruk-hai', 110, 70, 'Elite Orc', 'Normal', 9, 'Físico', 'Matar todos!'),
('Múmia Antiga', 95, 120, 'Maldição Eterna', 'Normal', 8, 'Sombra', 'Mmm... sangue...'),
('Esqueleto Guerreiro', 60, 80, 'Lâmina Óssea', 'Normal', 5, 'Sombra', 'Clank...'),
('Fantasma do Pântano', 70, 150, 'Assombração', 'Normal', 6, 'Sombra', 'Ooooh...'),
('Golem de Pedra', 160, 100, 'Guardião Antigo', 'Normal', 11, 'Pedra', 'Grunt...'),
('Basilisco', 140, 90, 'Olhar Mortal', 'Difícil', 15, 'Veneno', 'Ssss...'),
('Hidra', 200, 120, 'Múltiplas Cabeças', 'Difícil', 18, 'Água', 'Hssss...'),
('Minotauro', 130, 80, 'Fúria Selvagem', 'Normal', 10, 'Físico', 'Muuu!'),
('Quimera', 180, 150, 'Bestas Múltiplas', 'Difícil', 16, 'Fogo', 'Raaaar!')
ON CONFLICT DO NOTHING;

-- Associar NPCs aos cenários
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

-- Pântano dos Mortos (5)
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

-- Associar criaturas aos cenários
INSERT INTO cenario_criatura (id_cenario, id_personagem) VALUES 
-- O Condado (1) - criaturas mais fracas
(1, (SELECT ID_personagem FROM personagem WHERE nome = 'Lobo Sombrio')),
(1, (SELECT ID_personagem FROM personagem WHERE nome = 'Goblin Arqueiro')),

-- Floresta Sombria (2) - criaturas da floresta
(2, (SELECT ID_personagem FROM personagem WHERE nome = 'Aranha Gigante')),
(2, (SELECT ID_personagem FROM personagem WHERE nome = 'Warg')),
(2, (SELECT ID_personagem FROM personagem WHERE nome = 'Basilisco')),

-- Montanhas Nebulosas (3) - criaturas das montanhas
(3, (SELECT ID_personagem FROM personagem WHERE nome = 'Troll das Montanhas')),
(3, (SELECT ID_personagem FROM personagem WHERE nome = 'Dragão de Gelo')),
(3, (SELECT ID_personagem FROM personagem WHERE nome = 'Golem de Pedra')),

-- Ruínas de Osgiliath (4) - criaturas sombrias
(4, (SELECT ID_personagem FROM personagem WHERE nome = 'Nazgûl')),
(4, (SELECT ID_personagem FROM personagem WHERE nome = 'Esqueleto Guerreiro')),
(4, (SELECT ID_personagem FROM personagem WHERE nome = 'Múmia Antiga')),

-- Pântano dos Mortos (5) - criaturas do pântano
(5, (SELECT ID_personagem FROM personagem WHERE nome = 'Fantasma do Pântano')),
(5, (SELECT ID_personagem FROM personagem WHERE nome = 'Hidra')),

-- Minas de Moria (6) - criaturas das profundezas
(6, (SELECT ID_personagem FROM personagem WHERE nome = 'Balrog')),
(6, (SELECT ID_personagem FROM personagem WHERE nome = 'Cave Troll')),
(6, (SELECT ID_personagem FROM personagem WHERE nome = 'Goblin Arqueiro')),

-- Colinas do Vento (7) - criaturas das planícies
(7, (SELECT ID_personagem FROM personagem WHERE nome = 'Orc Guerreiro')),
(7, (SELECT ID_personagem FROM personagem WHERE nome = 'Uruk-hai')),
(7, (SELECT ID_personagem FROM personagem WHERE nome = 'Warg')),

-- Porto Cinzento (8) - criaturas marítimas
(8, (SELECT ID_personagem FROM personagem WHERE nome = 'Quimera')),
(8, (SELECT ID_personagem FROM personagem WHERE nome = 'Minotauro'))
ON CONFLICT DO NOTHING;

-- Adicionar NPCs às tabelas específicas
INSERT INTO guia (ID_personagem, custo_orientacao) VALUES 
((SELECT ID_personagem FROM personagem WHERE nome = 'Gandalf, o Cinzento'), 5),
((SELECT ID_personagem FROM personagem WHERE nome = 'Aragorn'), 3),
((SELECT ID_personagem FROM personagem WHERE nome = 'Elrond'), 10),
((SELECT ID_personagem FROM personagem WHERE nome = 'Radagast'), 2)
ON CONFLICT DO NOTHING;

INSERT INTO comerciante (ID_personagem, venda_item, compra_item) VALUES 
((SELECT ID_personagem FROM personagem WHERE nome = 'Samwise Gamgee'), 'Poção de Cura, Pão de Lemba, Erva Medicinal', 'Moeda de Ouro, Cristal Sombrio'),
((SELECT ID_personagem FROM personagem WHERE nome = 'Gimli'), 'Adaga de Ferro, Machado de Batalha, Armadura de Ferro', 'Ferro das Montanhas, Gema Congelada'),
((SELECT ID_personagem FROM personagem WHERE nome = 'Legolas'), 'Arco Élfico, Flechas Mágicas, Poção de Mana', 'Madeira Élfica, Cristal Sombrio'),
((SELECT ID_personagem FROM personagem WHERE nome = 'Galadriel'), 'Anel de Proteção, Poção de Invisibilidade, Pergaminho Antigo', 'Fragmento do Palantír, Pedra do Rei')
ON CONFLICT DO NOTHING;

INSERT INTO npc (ID_personagem, quest, localizacao) VALUES 
((SELECT ID_personagem FROM personagem WHERE nome = 'Frodo Baggins'), 'Ajude a proteger o Condado dos perigos que se aproximam', 'O Condado'),
((SELECT ID_personagem FROM personagem WHERE nome = 'Boromir'), 'Gondor precisa de heróis para defender Osgiliath', 'Ruínas de Osgiliath'),
((SELECT ID_personagem FROM personagem WHERE nome = 'Théoden'), 'Rohan enfrenta ameaças das planícies', 'Colinas do Vento'),
((SELECT ID_personagem FROM personagem WHERE nome = 'Treebeard'), 'A floresta anciã precisa de proteção', 'Floresta Sombria')
ON CONFLICT DO NOTHING;

-- Adicionar criaturas à tabela de criaturas
INSERT INTO criatura (ID_personagem, XP) VALUES 
((SELECT ID_personagem FROM personagem WHERE nome = 'Lobo Sombrio'), 50),
((SELECT ID_personagem FROM personagem WHERE nome = 'Aranha Gigante'), 80),
((SELECT ID_personagem FROM personagem WHERE nome = 'Orc Guerreiro'), 70),
((SELECT ID_personagem FROM personagem WHERE nome = 'Troll das Montanhas'), 150),
((SELECT ID_personagem FROM personagem WHERE nome = 'Nazgûl'), 200),
((SELECT ID_personagem FROM personagem WHERE nome = 'Balrog'), 300),
((SELECT ID_personagem FROM personagem WHERE nome = 'Dragão de Gelo'), 250),
((SELECT ID_personagem FROM personagem WHERE nome = 'Goblin Arqueiro'), 60),
((SELECT ID_personagem FROM personagem WHERE nome = 'Warg'), 65),
((SELECT ID_personagem FROM personagem WHERE nome = 'Cave Troll'), 120),
((SELECT ID_personagem FROM personagem WHERE nome = 'Haradrim'), 75),
((SELECT ID_personagem FROM personagem WHERE nome = 'Uruk-hai'), 90),
((SELECT ID_personagem FROM personagem WHERE nome = 'Múmia Antiga'), 85),
((SELECT ID_personagem FROM personagem WHERE nome = 'Esqueleto Guerreiro'), 45),
((SELECT ID_personagem FROM personagem WHERE nome = 'Fantasma do Pântano'), 70),
((SELECT ID_personagem FROM personagem WHERE nome = 'Golem de Pedra'), 110),
((SELECT ID_personagem FROM personagem WHERE nome = 'Basilisco'), 130),
((SELECT ID_personagem FROM personagem WHERE nome = 'Hidra'), 180),
((SELECT ID_personagem FROM personagem WHERE nome = 'Minotauro'), 100),
((SELECT ID_personagem FROM personagem WHERE nome = 'Quimera'), 160)
ON CONFLICT DO NOTHING; 