
# DD - Dicionário de Dados

> "Um dicionário de dados é uma coleção de metadados que contém definições e representações de elementos de dados."

## Entidade: Personagem  

#### Descrição: Representa qualquer personagem do jogo, podendo ser controlado por um jogador ou ser um NPC (personagem não jogável).

#### Observação: 

| Nome Variável |     Tipo     |         Descrição          | Valores permitidos  | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------:  | :--------------------: | :------: | ----------------- |
| iD_Personagem |     INT      | Identificador do personagem|Inteiro positivo     |  Não                   |    PK    |                   |
| vida_Maxima   |     INT      | Valor máximo de vida       |    ≥ 0              |  Não                   |          |                   |
| mana_Maxima   |     INT      | Valor máximo de mana       |    ≥ 0              |	Sim                    |          |                   |
| habilidade    | VARCHAR(100) | Nome da habilidade         | Texto               | Sim                    |          |                   |
| hostilidade   | BOOLEAN      | Indica a hostilidade       | TRUE / FALSE        |  Não                   |          |                   |
| level         |    	INT      | Nível do personagem        |    ≥ 1              |  Não                   |          |                   |
| resistencias  |   	TEXT     | Resistências do personagem |Lista de resistências|  Sim                   |          |                   |
| dialogo       |     TEXT     | diálogo do personagem      |  Texto livre        | 	Sim                  |          |                   |

## Entidade: Jogador

#### Descrição: 

#### Observação: 

| Nome Variável  |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------:  | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| ID_Jogador     |    INT       |  Identificador do jogador  |Inteiro positivo    |        Não             |          |                   |
|tipo_equipamento| 	VARCHAR(50) |  Tipo de equipamento usado |   ****             |        Sim             |          |                   |
|  cenario       | 	VARCHAR(50) |  Nome do cenário           |   ****             |        Sim             |   PF     |                   | 
  



 
## Entidade: inventário 

#### Descrição: Armazena os itens que um jogador possui.

#### Observação: Relaciona-se com Jogador e pode conter múltiplos itens.

| Nome Variável |     Tipo     |         Descrição                   | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------:          | :----------------: | :--------------------: | :------: | ----------------- |
| ID_inventário |    	INT      |Identificador do inventário          |  Inteiro positivo  |      Não               |    PK    |                   |
| id_jogador    |     INT      |Jogador ao qual o inventário pertence| Inteiro positivo   |      Não               |          |                   |
|  Pods         |     FLOAT    |      ****                           |        ≥ 0         |      Sim               |    FK    |                   |

## Entidade: características  

#### Descrição: Atributos vinculados ao jogador.

#### Observação: Relaciona-se com Jogador.

| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| ID_Jogador    |     	INT    |Referência ao jogador       | 	Inteiro positivo |       	Não             |   FK     |                   |
| fogo          |     	INT    |elemento fogo               |        0 a 100     |        Sim             |          |                   |
| agua          |      	INT    |elemento água               |        0 a 100     |        Sim             |          |                   |
| terra         |      	INT    |elemento terra              |        0 a 100     |        Sim             |          |                   |
| ar            |       INT    |elemento ar                 |        0 a 100     |        Sim             |          |                   |



## Entidade:  Mago 
#### Descrição: Especialização de um jogador com poderes mágicos.

#### Observação: Herdada da entidade Jogador.

| Nome Variável   |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------:   | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| ID_Jogador      |    	INT      |Referência ao jogador mago  |Inteiro positivo    |   	Não                 |    FK    |                   |
| atq_Magico      |    	INT      |ataques mágicos             |  ≥ 0               |   	Não                 |          |                   |
| atq_MultElemento|BOOLEAN       |   ********                 |  TRUE / FALSE      |   	Sim                 |          |                   |




## Entidade:  Guerreiro
#### Descrição: 

#### Observação: 

| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Jogador   |              |                            |                    |                        |   FK     |                   |
|  atq_Fisico   |              |                            |                    |                        |          |                   |
|  bloquear_Dano|              |                            |                    |                        |          |                   |



 
## Entidade: Arqueiro
#### Descrição: 

#### Observação: 

| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| ID_Jogador    |              |                            |                    |                        |    FK    |                   |
|  atq_Preciso  |              |                            |                    |                        |          |                   |
|  atq_Rapido   |              |                            |                    |                        |          |                   |

## Entidade: Sacerdote
#### Descrição: 

#### Observação: 

| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| ID_Jogador    |              |                            |                    |                        |    FK    |                   |
|bencao_Cura    |              |                            |                    |                        |          |                   |
|atq_Especial   |              |                            |                    |                        |          |                   |


## Entidade: Criatura
#### Descrição: 

#### Observação: 

| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| ID_Criatura   |              |                            |                    |                        |    PK    |                   |
|  XP           |              |                            |                    |                        |          |                   |


## Entidade: Ork
#### Descrição: 

#### Observação: 
| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|ID_Criatura    |              |                            |                    |                        |    FK    |                   |
|Raiva          |              |                            |                    |                        |          |                   |


## Entidade: Goblin
#### Descrição: 

#### Observação: 
| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| ID_Criatura   |              |                            |                    |                        |  FK      |                   |
|Raiva          |              |                            |                    |                        |          |                   |
|furtividade    |              |                            |                    |                        |          |                   |
|roubo          |              |                            |                    |                        |          |                   |

## Entidade: NPC
#### Descrição: 

#### Observação: 
| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|    UniqueID   |              |                            |                    |                        |    PK    |                   |
|   quest       |              |                            |                    |                        |          |                   |
|  localizacao  |              |                            |                    |                        |          |                   |
|  horaAparicao |              |                            |                    |                        |          |                   |

## Entidade: Comerciante
#### Descrição: 

#### Observação: 

| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  venda_Item   |              |                            |                    |                        |          |                   |
| compra_Item   |              |                            |                    |                        |          |                   |

## Entidade: Guia
#### Descrição: 

#### Observação: 

| Nome Variável   |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------:   | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|custo_orientacao |              |                            |                    |                        |          |                   |


## Entidade: Item
#### Descrição: 

#### Observação: 
| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| ID_item       |              |                            |                    |                        |  PK      |                   |
| id_inventario |              |                            |                    |                        |  FK      |                   |
|  peso         |              |                            |                    |                        |          |                   |
| durabilidade  |              |                            |                    |                        |          |                   |        

## Entidade: Arma
#### Descrição: 

#### Observação: 
| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|    mãos       |              |                            |                    |                        |          |                   |
|   dano        |              |                            |                    |                        |          |                

## Entidade: Armadura
#### Descrição: 

#### Observação: 
| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  defesa       |              |                            |                    |                        |          |                   |

## Entidade: Batalha
#### Descrição: 

#### Observação: 
| Nome Variável  |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------:  | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| ID_batalha     |              |                            |                    |                        |   PK     |                   |
| Dano_Causado   |              |                            |                    |                        |          |                   |
|Controle_Dano   |              |                            |                    |                        |          |                   |
|Ambiente_Batalha|              |                            |                    |                        |          |                   |
| Dano_Sofrido   |              |                            |                    |                        |          |                   |


## Entidade:
#### Descrição: 

#### Observação: | Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|               |              |                            |                    |                        |          |                   |
|               |              |                            |                    |                        |          |                   |
