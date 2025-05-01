
# DD - Dicionário de Dados

> "Um dicionário de dados é uma coleção de nomes, atributos e definições sobre elementos de dados que estão sendo usados ​​em seu estudo.
## Entidade: Personagem


| Campo         | Tipo         | Chave   | Nulo? | Descrição                                  |
|---------------|--------------|---------|-------|---------------------------------------------|
| id_personagem | INT          | PK      | NÃO   | Identificador único do personagem           |
| classe        | VARCHAR(50)  |         | SIM   | Classe geral do personagem                  |
| vida_maxima   | INT          |         | SIM   | Vida máxima                                 |
| mana_maxima   | INT          |         | SIM   | Mana máxima                                 |
| habilidade    | TEXT         |         | SIM   | Habilidade especial                         |
| hostilidade   | BOOLEAN      |         | SIM   | Indica se é hostil                          |
| level         | INT          |         | SIM   | Nível do personagem                         |
| dialogo       | TEXT         |         | SIM   | Fala ou frase característica                |
| resistencias  | TEXT         |         | SIM   | Resistência a ataques ou elementos          |
