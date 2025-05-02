
# DD - Dicionário de Dados

> "Um dicionário de dados é uma coleção de metadados que contém definições e representações de elementos de dados."

## Entidade: Personagem  

#### Descrição: 

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
| ID_Jogador     |              |                            |                    |                        |          |                   |
|tipo_equipamento|              |                            |                    |                        |          |                   |
|  cenario       |              |                            |                    |                        |   PF     |                   | 
  



 
## Entidade: inventário 

#### Descrição: 

#### Observação: 

| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| ID_inventário |              |                            |                    |                        |    PK    |                   |
| id_jogador    |              |                            |                    |                        |          |                   |
|  Pods         |              |                            |                    |                        |    FK    |                   |

## Entidade: características  

#### Descrição: 

#### Observação: 

| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|   ID_Jogador  |              |                            |                    |                        |   FK     |                   |
| fogo          |              |                            |                    |                        |          |                   |
| agua          |              |                            |                    |                        |          |                   |
| terra         |              |                            |                    |                        |          |                   |
| ar            |              |                            |                    |                        |          |                   |



## Entidade:  Mago 
#### Descrição: 

#### Observação: 

| Nome Variável   |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------:   | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| ID_Jogador      |              |                            |                    |                        |    FK    |                   |
| atq_Magico      |              |                            |                    |                        |          |                   |
| atq_MultElemento|              |                            |                    |                        |          |                   |




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
