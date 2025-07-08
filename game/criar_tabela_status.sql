-- Script para criar a tabela jogador_status
-- Esta tabela armazena a vida e mana atuais do jogador

-- Criar a tabela jogador_status
CREATE TABLE IF NOT EXISTS jogador_status (
    id_jogador INTEGER PRIMARY KEY,
    vida_atual INTEGER NOT NULL DEFAULT 100,
    mana_atual INTEGER NOT NULL DEFAULT 100,
    FOREIGN KEY (id_jogador) REFERENCES jogador(ID_personagem) ON DELETE CASCADE
);

-- Inserir registros iniciais para jogadores existentes
-- Isso garante que todos os jogadores tenham vida e mana atuais
INSERT INTO jogador_status (id_jogador, vida_atual, mana_atual)
SELECT 
    j.ID_personagem,
    p.vida_maxima,
    p.mana_maxima
FROM jogador j
JOIN personagem p ON j.ID_personagem = p.ID_personagem
WHERE NOT EXISTS (
    SELECT 1 FROM jogador_status js WHERE js.id_jogador = j.ID_personagem
);

-- Mostrar quantos registros foram criados
SELECT COUNT(*) as jogadores_com_status FROM jogador_status; 