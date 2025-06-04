-- Tabela Criatura
CREATE TABLE Criatura (
    ID_personagem SERIAL PRIMARY KEY,
    XP INTEGER
);

-- Tabela Ork
CREATE TABLE Ork (
    ID_personagem INTEGER PRIMARY KEY,
    Raiva INTEGER,
    FOREIGN KEY (ID_personagem) REFERENCES Criatura(ID_personagem)
);

-- Tabela Goblin
CREATE TABLE Goblin (
    ID_personagem INTEGER PRIMARY KEY,
    furtividade INTEGER,
    roubo INTEGER,
    FOREIGN KEY (ID_personagem) REFERENCES Criatura(ID_personagem)
);

-- Tabela Boss
CREATE TABLE Boss (
    ID_personagem INTEGER PRIMARY KEY,
    faseAtual INTEGER,
    imunidades TEXT,
    FOREIGN KEY (ID_personagem) REFERENCES Criatura(ID_personagem)
);


-- Tabela Confronta
CREATE TABLE Confronta (
    Unique_ID SERIAL PRIMARY KEY,
    vencedor BOOLEAN,
    criatura_id INTEGER,
    jogador_id INTEGER,
    FOREIGN KEY (criatura_id) REFERENCES Criatura(ID_personagem),
    FOREIGN KEY (jogador_id) REFERENCES Jogador(ID_jogador) -- Falta a tabela Jogador, que deve ser criada antes desta tabela
);

