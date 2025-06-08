CREATE TABLE batalha (
    ID_batalha SERIAL PRIMARY KEY,
    Dano_causado INTEGER NOT NULL,
    Controle_Dano INTEGER NOT NULL,
    Ambiente_batalha VARCHAR(100) NOT NULL,
    Dano_sofrido INTEGER NOT NULL
); 

-- Criação da tabela Skill
CREATE TABLE skill (
    ID_jogador INTEGER PRIMARY KEY,
    atq INTEGER NOT NULL,
    FOREIGN KEY (ID_jogador) REFERENCES jogador(ID_personagem)
);

-- Criação da tabela Caracteristicas
CREATE TABLE caracteristicas (
    ID_jogador INTEGER PRIMARY KEY,
    fogo INTEGER NOT NULL,
    agua INTEGER NOT NULL,
    terra INTEGER NOT NULL,
    ar INTEGER NOT NULL,
    FOREIGN KEY (ID_jogador) REFERENCES jogador(ID_personagem)
);

-- Criação da tabela Jogador
CREATE TABLE jogador (
    ID_personagem INTEGER PRIMARY KEY,
    cenario INTEGER NOT NULL,
    tipo_equipamento VARCHAR(50) NOT NULL,
    FOREIGN KEY (ID_personagem) REFERENCES personagem(ID_personagem),
    FOREIGN KEY (cenario) REFERENCES cenario(ID_cenario)
); 