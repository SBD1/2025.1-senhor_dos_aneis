-- Script para atualizar comerciantes com mais itens
-- Isso torna o sistema de comércio mais interessante

-- Atualizar comerciantes existentes com mais itens
UPDATE comerciante 
SET venda_item = 'Poção de Cura, Poção de Mana, Adaga de Ferro, Espada de Ferro, Armadura de Couro, Escudo de Madeira, Anel de Proteção, Cajado Mágico, Arco Élfico, Bastão Sagrado, Capacete de Ferro, Botas de Couro, Pergaminho Antigo, Runa de Proteção',
    compra_item = 'Fragmento do Palantír, Cristal Sombrio, Gema Congelada, Osso de Dragão, Fragmento Antigo, Runa Perdida, Pedra do Rei, Pele de Lobo, Ferro das Montanhas, Madeira Élfica, Erva Medicinal, Pão de Lemba'
WHERE ID_personagem IN (
    SELECT ID_personagem FROM comerciante
);

-- Verificar se há comerciantes sem itens e adicionar itens padrão
INSERT INTO comerciante (ID_personagem, venda_item, compra_item)
SELECT p.ID_personagem, 
       'Poção de Cura, Poção de Mana, Adaga de Ferro, Espada de Ferro, Armadura de Couro, Escudo de Madeira, Anel de Proteção, Cajado Mágico, Arco Élfico, Bastão Sagrado, Capacete de Ferro, Botas de Couro, Pergaminho Antigo, Runa de Proteção',
       'Fragmento do Palantír, Cristal Sombrio, Gema Congelada, Osso de Dragão, Fragmento Antigo, Runa Perdida, Pedra do Rei, Pele de Lobo, Ferro das Montanhas, Madeira Élfica, Erva Medicinal, Pão de Lemba'
FROM personagem p
WHERE EXISTS (
    SELECT 1 FROM cenario_npc cn 
    WHERE cn.id_personagem = p.ID_personagem 
    AND cn.id_cenario IN (1, 2, 3, 4, 5, 6, 7, 8)
)
AND NOT EXISTS (
    SELECT 1 FROM comerciante c WHERE c.ID_personagem = p.ID_personagem
)
AND p.nome LIKE '%Comerciante%' OR p.nome LIKE '%Mercador%' OR p.nome LIKE '%Vendedor%';

-- Mostrar estatísticas dos comerciantes
SELECT 
    p.nome as comerciante,
    c.venda_item as itens_venda,
    c.compra_item as itens_compra
FROM comerciante c
JOIN personagem p ON c.ID_personagem = p.ID_personagem
ORDER BY p.nome; 