# DD - Dicionário de Dados

> Um Dicionário de Dados (DD) é um documento que descreve detalhadamente todos os dados usados em um sistema ou banco de dados.

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
|     Pods      | FLOAT |       Capacidade do inventário        |        ≥ 0         |          Sim           |    FK    |                   |

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

#### Descrição: Classe especializada em combate corpo a corpo com alta resistência física.

#### Observação: Herdada da entidade Jogador.

| Nome Variável | Tipo |             Descrição              | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :--------------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Jogador   | INT  | Identificador do jogador guerreiro |  Inteiro positivo  |          Não           |    FK    |                   |
|  atq_Fisico   | INT  |       Força de ataque físico       |        ≥ 0         |          Não           |          |                   |
| bloquear_Dano | INT  |    Capacidade de bloquear dano     |      0 a 100       |          Sim           |          |                   |

## Entidade: Arqueiro

#### Descrição: Especialização de um jogador com foco em ataques à distância e precisão.

#### Observação: Herda de Jogador.

| Nome Variável | Tipo |           Descrição            | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :----------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Jogador   | INT  | Referência ao jogador arqueiro |  Inteiro positivo  |          Não           |    FK    |                   |
|  atq_Preciso  | INT  |      Precisão dos ataques      |      0 a 100       |          Sim           |          |                   |
|  atq_Rapido   | INT  |     Velocidade dos ataques     |        ≥ 0         |          Sim           |          |                   |

## Entidade: Sacerdote

#### Descrição: Especialização de um jogador com foco em cura e suporte.

#### Observação: Herdada da entidade Jogador.

| Nome Variável | Tipo |            Descrição            | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :-----------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Jogador   | INT  | Referência ao jogador sacerdote |  Inteiro positivo  |          Não           |    FK    |                   |
|  bencao_Cura  | INT  |          Poder de cura          |        ≥ 0         |          Sim           |          |                   |
| atq_Especial  | INT  |     Dano de ataque especial     |        ≥ 0         |          Sim           |          |                   |

## Entidade: Criatura

#### Descrição: Representa os monstros e criaturas do jogo que podem ser enfrentados.

| Nome Variável | Tipo |              Descrição              | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :---------------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Criatura  | INT  |   Identificador único da criatura   |  Inteiro positivo  |          Não           |    PK    |                   |
|      XP       | INT  | Experiência concedida ao derrotá-la |        ≥ 0         |          Não           |          |                   |

| Nome Variável | Tipo |          Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :-------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Criatura  | INT  |  Identificador da criatura  |  Inteiro positivo  |          Não           |    PK    |                   |
|      XP       | INT  | Pontos de experiência dados |        ≥ 0         |          Não           |          |                   |

## Entidade: Ork

#### Descrição: Tipo específico de criatura com características próprias.

#### Observação:

| Nome Variável | Tipo |       Descrição       | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :-------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Criatura  | INT  | Referência à criatura |  Inteiro positivo  |          Não           |    FK    |                   |
|     Raiva     | INT  | Grau de agressividade |      0 a 100       |          Sim           |          |                   |

## Entidade: Goblin

#### Descrição: Tipo específico de criatura com habilidades furtivas.

#### Observação:

| Nome Variável | Tipo |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  ID_Criatura  | INT  | Referência à criatura base |  Inteiro positivo  |          Não           |    FK    |                   |
|     Raiva     | INT  |   Grau de agressividade    |      0 a 100       |          Sim           |          |                   |
|  furtividade  | INT  |    Nível de furtividade    |      0 a 100       |          Sim           |          |                   |
|     roubo     | INT  |    Capacidade de roubo     |      0 a 100       |          Sim           |          |                   |

## Entidade: NPC

#### Descrição: Personagens não jogáveis que interagem com o jogador.

#### Observação: Personagens que fornecem missões e interações no jogo.

| Nome Variável |     Tipo     |         Descrição          | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :----------: | :------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|   UniqueID    |     INT      | Identificador único do NPC |  Inteiro positivo  |          Não           |    PK    |                   |
|     quest     | VARCHAR(100) |     Missão disponível      |       Texto        |          Sim           |          |                   |
|  localizacao  | VARCHAR(100) |      Posição no mapa       |       Texto        |          Não           |          |                   |
| horaAparicao  |  TIMESTAMP   |   Horário de surgimento    | Formato timestamp  |          Sim           |          |                   |

## Entidade: Comerciante

#### Descrição: NPC especializado em comércio de itens.

#### Observação: Herdada da entidade NPC.

| Nome Variável |  Tipo   |     Descrição      | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :-----: | :----------------: | :----------------: | :--------------------: | :------: | ----------------- |
|  venda_Item   | BOOLEAN | Pode vender itens? |    TRUE / FALSE    |          Não           |          |                   |
|  compra_Item  | BOOLEAN | Pode vender itens? |    TRUE / FALSE    |          Não           |          |                   |

## Entidade: Guia

#### Descrição: NPC que fornece orientações aos jogadores.

#### Observação:

|  Nome Variável   | Tipo |           Descrição           | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :--------------: | :--: | :---------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
| custo_orientacao | INT  | Custo para receber orientação |        ≥ 0         |          Não           |          |                   |

## Entidade: Item

#### Descrição: Objeto armazenável no inventário do jogador.

#### Observação:

| Nome Variável | Tipo  |            Descrição            | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :---: | :-----------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|    ID_item    |  INT  |      Identificador do item      |  Inteiro positivo  |          Não           |    PK    |                   |
| id_inventario |  INT  |   Inventário ao qual pertence   |  Inteiro positivo  |          Não           |    FK    |                   |
|     peso      | FLOAT |          Peso do item           |        ≥ 0         |          Não           |          |                   |
| durabilidade  |  INT  | Número de usos antes de quebrar |        ≥ 0         |          Sim           |          |                   |

## Entidade: Arma

#### Descrição: : Item ofensivo usado em batalha.

#### Observação: Herda de Item.

| Nome Variável | Tipo |  Descrição   | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :----------: | :----------------: | :--------------------: | :------: | ----------------- |
|     mãos      | INT  |              |       1 ou 2       |          Não           |          |                   |
|     dano      | INT  | Dano causado |        ≥ 0         |          Não           |          |                   |

## Entidade: Armadura

#### Descrição: Item defensivo que reduz dano.

#### Observação:

| Nome Variável | Tipo |       Descrição        | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :-----------: | :--: | :--------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|    defesa     | INT  | Capacidade de proteção |        ≥ 0         |          Não           |          |                   |

## Entidade: Batalha

#### Descrição: Representa um combate entre personagens e criaturas.

#### Observação:

Pode ocorrer em ambientes diversos.

|  Nome Variável   |    Tipo     |            Descrição             | Valores permitidos | Permite valores nulos? | É chave? | Outras Restrições |
| :--------------: | :---------: | :------------------------------: | :----------------: | :--------------------: | :------: | ----------------- |
|    ID_batalha    |     INT     |     Identificador da batalha     |  Inteiro positivo  |          Não           |    PK    |                   |
|   Dano_Causado   |     INT     |       Dano total infligido       |        ≥ 0         |          Não           |          |                   |
|  Controle_Dano   | VARCHAR(50) |         controle de dano         |       Texto        |          Sim           |          |                   |
| Ambiente_Batalha | VARCHAR(50) | Ambiente onde ocorreu a batalha  |       Texto        |          Sim           |          |                   |
|   Dano_Sofrido   |     INT     | Dano total recebido pelo jogador |        ≥ 0         |          Não           |          |                   |
