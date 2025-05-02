# DD - Dicionário de Dados

> "Um dicionário de dados é uma coleção de metadados que contém definições e representações de elementos de dados."

## Entidade: Personagem

#### Descrição: Representa qualquer personagem do jogo, podendo ser controlado por um jogador ou ser um NPC (personagem não jogável).

#### Observação:

| Nome Variável |     Tipo     |          Descrição          |  Valores permitidos   | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :-------------------------: | :-------------------: | :--------------------: | :------: | ----------------- |
| iD_Personagem |     INT      | Identificador do personagem |   Inteiro positivo    |          Não           |    PK    |                   |
|  vida_Maxima  |     INT      |    Valor máximo de vida     |          ≥ 0          |          Não           |          |                   |
|  mana_Maxima  |     INT      |    Valor máximo de mana     |          ≥ 0          |          Sim           |          |                   |
|  habilidade   | VARCHAR(100) |     Nome da habilidade      |         Texto         |          Sim           |          |                   |
|  hostilidade  |   BOOLEAN    |    Indica a hostilidade     |     TRUE / FALSE      |          Não           |          |                   |
|     level     |     INT      |     Nível do personagem     |          ≥ 1          |          Não           |          |                   |
| resistencias  |     TEXT     | Resistências do personagem  | Lista de resistências |          Sim           |          |                   |
|    dialogo    |     TEXT     |    diálogo do personagem    |      Texto livre      |          Sim           |          |                   |

## Entidade: Jogador

#### Descrição:

#### Observação:

|  Nome Variável   |    Tipo     |         Descrição         | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :--------------: | :---------: | :-----------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|    ID_Jogador    |     INT     | Identificador do jogador  |  Inteiro positivo  |          Não           |          |                   |
| tipo_equipamento | VARCHAR(50) | Tipo de equipamento usado |      \*\*\*\*      |          Sim           |          |                   |
|     cenario      | VARCHAR(50) |      Nome do cenário      |      \*\*\*\*      |          Sim           |    PF    |                   |

## Entidade: inventário

#### Descrição: Armazena os itens que um jogador possui.

#### Observação: Relaciona-se com Jogador e pode conter múltiplos itens.

| Nome Variável | Tipo  |               Descrição               | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :---: | :-----------------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| ID_inventário |  INT  |      Identificador do inventário      |  Inteiro positivo  |          Não           |    PK    |                   |
|  id_jogador   |  INT  | Jogador ao qual o inventário pertence |  Inteiro positivo  |          Não           |          |                   |
|     Pods      | FLOAT |               \*\*\*\*                |        ≥ 0         |          Sim           |    FK    |                   |

## Entidade: características

#### Descrição: Atributos vinculados ao jogador.

#### Observação: Relaciona-se com Jogador.

| Nome Variável | Tipo |       Descrição       | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :-------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Jogador   | INT  | Referência ao jogador |  Inteiro positivo  |          Não           |    FK    |                   |
|     fogo      | INT  |     elemento fogo     |      0 a 100       |          Sim           |          |                   |
|     agua      | INT  |     elemento água     |      0 a 100       |          Sim           |          |                   |
|     terra     | INT  |    elemento terra     |      0 a 100       |          Sim           |          |                   |
|      ar       | INT  |      elemento ar      |      0 a 100       |          Sim           |          |                   |

## Entidade: Mago

#### Descrição: Especialização de um jogador com poderes mágicos.

#### Observação: Herdada da entidade Jogador.

|  Nome Variável   |  Tipo   |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :--------------: | :-----: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|    ID_Jogador    |   INT   | Referência ao jogador mago |  Inteiro positivo  |          Não           |    FK    |                   |
|    atq_Magico    |   INT   |      ataques mágicos       |        ≥ 0         |          Não           |          |                   |
| atq_MultElemento | BOOLEAN |        **\*\*\*\***        |    TRUE / FALSE    |          Sim           |          |                   |

## Entidade: Guerreiro

#### Descrição: Especialização de um jogador com foco em combate corpo a corpo e defesa física.

#### Observação: Herdada da entidade Jogador.

| Nome Variável |  Tipo   |            Descrição            | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :-----: | :-----------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Jogador   |   INT   | Referência ao jogador guerreiro |  Inteiro positivo  |          Não           |    FK    |                   |
|  atq_Fisico   |   INT   |     Poder de ataque físico      |        ≥ 0         |          Não           |          |                   |
| bloquear_Dano | BOOLEAN |   Capacidade de bloquear dano   |    TRUE / FALSE    |          Sim           |          |                   |

## Entidade: Arqueiro

#### Descrição: Especialização de um jogador com foco em ataques à distância e precisão.

#### Observação: Herdada da entidade Jogador.

| Nome Variável |  Tipo   |           Descrição            | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :-----: | :----------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Jogador   |   INT   | Referência ao jogador arqueiro |  Inteiro positivo  |          Não           |    FK    |                   |
|  atq_Preciso  |   INT   |    Poder de ataque preciso     |        ≥ 0         |          Não           |          |                   |
|  atq_Rapido   | BOOLEAN |  Capacidade de ataque rápido   |    TRUE / FALSE    |          Sim           |          |                   |

## Entidade: Sacerdote

#### Descrição: Especialização de um jogador com foco em cura e suporte.

#### Observação: Herdada da entidade Jogador.

| Nome Variável |  Tipo   |            Descrição            | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :-----: | :-----------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Jogador   |   INT   | Referência ao jogador sacerdote |  Inteiro positivo  |          Não           |    FK    |                   |
|  bencao_Cura  |   INT   |          Poder de cura          |        ≥ 0         |          Não           |          |                   |
| atq_Especial  | BOOLEAN |  Habilidade de ataque especial  |    TRUE / FALSE    |          Sim           |          |                   |

## Entidade: Criatura

#### Descrição: Representa os monstros e criaturas do jogo que podem ser enfrentados.

#### Observação: Entidade que representa inimigos não jogáveis.

| Nome Variável | Tipo |          Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :-------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Criatura  | INT  |  Identificador da criatura  |  Inteiro positivo  |          Não           |    PK    |                   |
|      XP       | INT  | Pontos de experiência dados |        ≥ 0         |          Não           |          |                   |

## Entidade: Ork

#### Descrição: Tipo específico de criatura com características próprias.

#### Observação: Herdada da entidade Criatura.

| Nome Variável | Tipo |         Descrição         | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :-----------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Criatura  | INT  | Referência à criatura Ork |  Inteiro positivo  |          Não           |    FK    |                   |
|     Raiva     | INT  |   Nível de raiva do Ork   |      0 a 100       |          Não           |          |                   |

## Entidade: Goblin

#### Descrição: Tipo específico de criatura com habilidades furtivas.

#### Observação: Herdada da entidade Criatura.

| Nome Variável |  Tipo   |          Descrição           | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :-----: | :--------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Criatura  |   INT   | Referência à criatura Goblin |  Inteiro positivo  |          Não           |    FK    |                   |
|  furtividade  |   INT   |     Nível de furtividade     |      0 a 100       |          Não           |          |                   |
|     roubo     | BOOLEAN |  Capacidade de roubar itens  |    TRUE / FALSE    |          Sim           |          |                   |

## Entidade: NPC

#### Descrição: Personagens não jogáveis que interagem com o jogador.

#### Observação: Personagens que fornecem missões e interações no jogo.

| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|   UniqueID    |     INT      | Identificador único do NPC |  Inteiro positivo  |          Não           |    PK    |                   |
|     quest     |     TEXT     | Missão oferecida pelo NPC  |    Texto livre     |          Sim           |          |                   |
|  localizacao  | VARCHAR(100) | Localização do NPC no mapa |       Texto        |          Não           |          |                   |
| horaAparicao  |  TIMESTAMP   | Horário que o NPC aparece  | Formato timestamp  |          Sim           |          |                   |

## Entidade: Comerciante

#### Descrição: NPC especializado em comércio de itens.

#### Observação: Herdada da entidade NPC.

| Nome Variável |  Tipo   |          Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :-----: | :-------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  venda_Item   | BOOLEAN | Capacidade de vender itens  |    TRUE / FALSE    |          Não           |          |                   |
|  compra_Item  | BOOLEAN | Capacidade de comprar itens |    TRUE / FALSE    |          Não           |          |                   |

## Entidade: Guia

#### Descrição: NPC que fornece orientações aos jogadores.

#### Observação: Herdada da entidade NPC.

|  Nome Variável   | Tipo |           Descrição           | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :--------------: | :--: | :---------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| custo_orientacao | INT  | Custo para receber orientação |        ≥ 0         |          Não           |          |                   |

## Entidade: Item

#### Descrição: Objetos que podem ser coletados e utilizados no jogo.

#### Observação: Itens que podem ser equipados ou utilizados pelos jogadores.

| Nome Variável | Tipo  |          Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :---: | :-------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|    ID_item    |  INT  | Identificador único do item |  Inteiro positivo  |          Não           |    PK    |                   |
| id_inventario |  INT  |  Referência ao inventário   |  Inteiro positivo  |          Sim           |    FK    |                   |
|     peso      | FLOAT |        Peso do item         |        > 0         |          Não           |          |                   |
| durabilidade  |  INT  |    Durabilidade do item     |      0 a 100       |          Não           |          |                   |

## Entidade: Arma

#### Descrição: Item específico para combate.

#### Observação: Herdada da entidade Item.

| Nome Variável | Tipo |           Descrição            | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :----------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|     mãos      | INT  | Quantidade de mãos necessárias |       1 ou 2       |          Não           |          |                   |
|     dano      | INT  |     Dano causado pela arma     |        ≥ 0         |          Não           |          |                   |

## Entidade: Armadura

#### Descrição: Item específico para defesa.

#### Observação: Herdada da entidade Item.

| Nome Variável | Tipo |          Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :-------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|    defesa     | INT  | Valor de defesa da armadura |        ≥ 0         |          Não           |          |                   |

## Entidade: Batalha

#### Descrição: Registro dos combates entre personagens.

#### Observação: Armazena informações sobre as batalhas no jogo.

|  Nome Variável   |    Tipo     |          Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :--------------: | :---------: | :-------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|    ID_batalha    |     INT     |  Identificador da batalha   |  Inteiro positivo  |          Não           |    PK    |                   |
|   Dano_Causado   |     INT     |     Dano total causado      |        ≥ 0         |          Não           |          |                   |
|  Controle_Dano   |   BOOLEAN   |   Controle de dano ativo    |    TRUE / FALSE    |          Não           |          |                   |
| Ambiente_Batalha | VARCHAR(50) | Local onde ocorre a batalha |       Texto        |          Não           |          |                   |
|   Dano_Sofrido   |     INT     |     Dano total recebido     |        ≥ 0         |          Não           |          |                   |

## Entidade:

#### Descrição:

#### Observação: | Nome Variável | Tipo | Descrição | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |

| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| | | | | | | |
| | | | | | | |
