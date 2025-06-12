
-- Listar inventário de cada jogador
SELECT i.id_inventario, p.nome AS jogador, i.pods
FROM inventario i
JOIN jogador j ON i.id_jogador = j.id_jogador
JOIN personagem p ON j.id_personagem = p.id_personagem;
