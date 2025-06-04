CREATE TABLE batalha (
    ID_batalha SERIAL PRIMARY KEY,
    Dano_causado INTEGER NOT NULL,
    Controle_Dano INTEGER NOT NULL,
    Ambiente_batalha VARCHAR(100) NOT NULL,
    Dano_sofrido INTEGER NOT NULL
); 