-- Limpar dados existentes
DELETE FROM confronta;
DELETE FROM batalha;
DELETE FROM skill;
DELETE FROM caracteristicas;
DELETE FROM guerreiro;
DELETE FROM sacerdote;
DELETE FROM mago;
DELETE FROM arqueiro;
DELETE FROM arma;
DELETE FROM armadura;
DELETE FROM item;
DELETE FROM inventario;
DELETE FROM jogador;
DELETE FROM boss;
DELETE FROM ork;
DELETE FROM criatura;
DELETE FROM comerciante;
DELETE FROM npc;
DELETE FROM personagem;
DELETE FROM cenario;

-- ============================================
-- CENÁRIOS DO JOGO
-- ============================================
INSERT INTO cenario (id_cenario, norte_id, leste_id, oeste_id, sul_id, sol, chuva, noite, dia) VALUES
(1, NULL, 2, NULL, NULL, 'Claro', 'Sem chuva', 'Estrelas brilhantes', 'Amanhecer dourado'), -- Acampamento Élfico
(2, NULL, 3, 1, NULL, 'Nublado', 'Garoa leve', 'Neblina densa', 'Cinzento'), -- Estrada para Eregion  
(3, NULL, 4, 2, NULL, 'Sombrio', 'Chuva forte', 'Escuridão total', 'Penumbra'), -- Portões de Ost-in-Edhil
(4, 5, 6, 3, 7, 'Ausente', 'Tempestade', 'Trevas antigas', 'Luz fantasmagórica'), -- Salões das Forjas (centro)
(5, NULL, NULL, NULL, 4, 'Fogo interno', 'Vapor', 'Brasas vermelhas', 'Chamas dançantes'), -- Forja Principal
(6, NULL, NULL, 4, NULL, 'Reflexos', 'Umidade', 'Sombras móveis', 'Espelhos brilhantes'), -- Câmara dos Segredos
(7, NULL, NULL, NULL, 4, 'Vento forte', 'Rajadas', 'Lua pálida', 'Vista panorâmica'); -- Torre do Observatório

-- ============================================
-- PERSONAGENS DO JOGO
-- ============================================
INSERT INTO personagem (nome, vida_maxima, mana_maxima, habilidade, dificuldade, level, resistencia, dialogo) VALUES
-- NPCs do Acampamento Élfico
('Erestor, Lorde Élfico', 150, 200, 'Liderança Élfica', 'Média', 20, 'Sombras', 'Aventureiro, ouvi rumores sobre anéis perdidos em Eregion. Você aceita esta missão perigosa?'),
('Lindir, o Curandeiro', 120, 180, 'Cura Élfica', 'Fácil', 15, 'Veneno', 'Minhas poções podem salvar sua vida nas ruínas sombrias. Leve algumas!'),
('Glorfindel, o Mercador', 140, 100, 'Comércio de Armas', 'Fácil', 18, 'Medo', 'Armas élficas são sua melhor defesa contra os horrores de Eregion.'),

-- Criaturas Inimigas
('Lobo Selvagem', 45, 10, 'Mordida Feroz', 'Fácil', 3, 'Frio', 'AUUUU!'),
('Orc Errante', 80, 30, 'Brutalidade', 'Média', 6, 'Dor', 'Carne fresca para a horda!'),
('Espectro Élfico', 90, 120, 'Lamento Fantasma', 'Média', 8, 'Físico', 'Nossos segredos... não devem... ser revelados...'),
('Balrog Menor', 300, 200, 'Fogo das Profundezas', 'Difícil', 15, 'Fogo,Físico', 'Você não passará!'),
('Sombra Antiga', 60, 80, 'Drenar Energia', 'Média', 7, 'Luz', '...sussurros incompreensíveis...'),
('Nazgûl Menor', 250, 150, 'Terror Negro', 'Difícil', 12, 'Frio,Medo', 'Os anéis... são nossos... por direito...'),
('Capitão Nazgûl', 400, 250, 'Grito da Morte', 'Extrema', 18, 'Fogo,Físico,Medo', 'Entreguem os anéis... ou pereçam na escuridão eterna!');

-- Definir especializações dos NPCs
INSERT INTO npc (ID_personagem, quest, localizacao, hora_aparicao) VALUES
(1, 'Recupere os três anéis perdidos de Eregion antes que caiam nas mãos do Inimigo', 'Acampamento Élfico', '06:00:00');

INSERT INTO comerciante (ID_personagem, venda_item, compra_item) VALUES
(2, 'Poção de Cura Élfica, Pão Lembas, Água Abençoada', 'Itens raros, Materiais mágicos'),
(3, 'Espada Élfica, Armadura de Mithril, Escudo de Gondolin', 'Armas quebradas, Materiais de forja');

-- Definir criaturas
INSERT INTO criatura (ID_personagem, XP) VALUES
(4, 150), (5, 400), (6, 500), (7, 2000), (8, 350), (9, 1500), (10, 5000);

INSERT INTO ork (ID_personagem, Raiva) VALUES (5, 85);
INSERT INTO boss (ID_personagem, faseAtual, imunidades) VALUES 
(7, 1, 'fogo,calor'),
(9, 1, 'físico,luz'), 
(10, 3, 'frio,medo,sombras');

-- ============================================
-- INVENTÁRIOS E ITENS
-- ============================================
INSERT INTO inventario (id_personagem, pods) VALUES
(2, 100), -- Lindir
(3, 150); -- Glorfindel

-- Itens disponíveis para compra
INSERT INTO item (nome, peso, durabilidade, id_inventario) VALUES
('Poção de Cura Élfica', 0.5, 1, 1),
('Pão Lembas', 0.2, 5, 1),
('Água Abençoada', 1.0, 3, 1),
('Espada Élfica', 2.5, 500, 2),
('Armadura de Mithril', 8.0, 1000, 2),
('Escudo de Gondolin', 4.0, 600, 2);

INSERT INTO arma (id_item, mãos, dano) VALUES
(4, 1, 75); -- Espada Élfica

INSERT INTO armadura (id_item, defesa) VALUES
(5, 120), -- Armadura de Mithril
(6, 80);  -- Escudo de Gondolin

-- Anéis Mágicos (encontrados no jogo)
INSERT INTO item (nome, peso, durabilidade, id_inventario) VALUES
('Anel da Proteção', 0.1, 999, NULL),
('Anel da Invisibilidade Menor', 0.1, 999, NULL),
('Anel da Compreensão', 0.1, 999, NULL);
