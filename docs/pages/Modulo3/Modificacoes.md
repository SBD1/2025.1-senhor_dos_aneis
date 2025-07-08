# Atualizações feitas no trabalho

## Atualizações feitas no DDL
> Adicionamos mais cenários para melhorar a experiência do jogador, expandindo significativamente o mundo disponível para exploração. Os novos ambientes incluem:

# Novos arquivos criados para o jogo 
## Arquivo: quests.sql 
> Objetivo: Implementar uma mecânica de missões em um jogo RPG, incluindo o cadastro de quests com recompensas e pré-requisitos, o controle de progresso individual do jogador, a atribuição automática de missões conforme o nível, a conclusão com ganhos de experiência e itens, o registro de eventos relevantes como movimentações e ações, e o uso de triggers e stored procedures para automatizar essa lógica no banco de dados.

??? info "_1. quests.sql  "
 ```Postgres
-- ===================================================================
-- SISTEMA DE QUESTS APRIMORADO
-- Adiciona tabelas e funcionalidades para um sistema de missões completo
-- ===================================================================

-- Tabela de Quests
CREATE TABLE IF NOT EXISTS quest (
    id_quest SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    recompensa_xp INTEGER DEFAULT 0,
    recompensa_item VARCHAR(100),
    pre_requisito_level INTEGER DEFAULT 1,
    tipo_quest VARCHAR(50) DEFAULT 'Principal', -- Principal, Secundária, Diária
    status VARCHAR(20) DEFAULT 'Disponível', -- Disponível, Em Progresso, Completada
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- **ASSUNÇÃO/CORREÇÃO**: A tabela 'jogador' não foi fornecida, mas é referenciada.
-- Criei uma estrutura básica para 'jogador' e 'cenario' e 'inventario'
-- para que o script possa ser executado sem erros de referência.
-- Você precisará ajustar isso para a sua estrutura real.
CREATE TABLE IF NOT EXISTS jogador (
    ID_personagem SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    level INTEGER DEFAULT 1,
    xp INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_personagem INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (id_personagem) REFERENCES jogador(ID_personagem)
);

CREATE TABLE IF NOT EXISTS item (
    id_item SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    peso DECIMAL(5,2),
    durabilidade INTEGER,
    id_inventario INTEGER NOT NULL,
    FOREIGN KEY (id_inventario) REFERENCES inventario(id_inventario)
);


CREATE TABLE IF NOT EXISTS cenario (
    id_cenario SERIAL PRIMARY KEY,
    nome_cenario VARCHAR(100) NOT NULL
);

-- Tabela de Progresso de Quest do Jogador
CREATE TABLE IF NOT EXISTS quest_progresso (
    id_progresso SERIAL PRIMARY KEY,
    id_jogador INTEGER NOT NULL,
    id_quest INTEGER NOT NULL,
    progresso_atual INTEGER DEFAULT 0,
    progresso_maximo INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'Em Progresso',
    iniciado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completado_em TIMESTAMP NULL,
    FOREIGN KEY (id_jogador) REFERENCES jogador(ID_personagem),
    FOREIGN KEY (id_quest) REFERENCES quest(id_quest),
    UNIQUE(id_jogador, id_quest)
);

-- Tabela de Diários/Logs de Eventos
CREATE TABLE IF NOT EXISTS diario_eventos (
    id_evento SERIAL PRIMARY KEY,
    id_jogador INTEGER NOT NULL,
    tipo_evento VARCHAR(50) NOT NULL, -- Movimento, Batalha, Quest, Item, Interação
    descricao TEXT NOT NULL,
    cenario_id INTEGER,
    timestamp_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_jogador) REFERENCES jogador(ID_personagem),
    -- **CORREÇÃO**: Adicionado ON DELETE SET NULL para o cenario_id,
    -- caso o cenário seja removido, o log não perca a referência de jogador.
    FOREIGN KEY (cenario_id) REFERENCES cenario(id_cenario) ON DELETE SET NULL
);

-- ===================================================================
-- INSERIR QUESTS INICIAIS
-- ===================================================================

INSERT INTO quest (nome, descricao, recompensa_xp, recompensa_item, pre_requisito_level, tipo_quest) VALUES
('A Busca do Palantír', 'Encontre os três fragmentos do Palantír perdido espalhados pela Terra Média para ajudar na defesa contra as forças sombrias.', 1000, 'Palantír Restaurado', 1, 'Principal'),
('Defensor do Condado', 'Derrote 5 criaturas hostis para proteger as terras pacíficas dos Hobbits.', 500, 'Espada do Condado', 3, 'Secundária'),
('Explorador da Terra Média', 'Visite todos os 4 cenários principais para mapear a região.', 300, 'Mapa Élfico', 1, 'Secundária'),
('Caçador de Goblins', 'Elimine 3 Goblins que estão aterrorizando as estradas.', 400, 'Adaga Anti-Goblin', 5, 'Secundária'),
('O Chamado de Minas Tirith', 'Chegue a Minas Tirith e fale com o Senescente para receber uma missão especial.', 600, 'Anel de Gondor', 8, 'Principal');

-- **INSERÇÃO DE DADOS DE EXEMPLO**: Adicionado para tornar o script executável
-- e permitir testes das funcionalidades.
INSERT INTO jogador (nome, level, xp) VALUES
('Frodo Bolseiro', 1,
```


## Docker
 > Adicionamos suporte para containerização do projeto.
