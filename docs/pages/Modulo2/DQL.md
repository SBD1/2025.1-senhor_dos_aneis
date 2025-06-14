<span style="background-color:#1ec68e; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Versão 1.0</span>

# Data Query Language

## Conceito:

A Data Query Language (DQL), ou Linguagem de Consulta de Dados, é um subconjunto do SQL voltado especificamente para a recuperação de informações armazenadas no banco de dados. Seu principal comando é o `SELECT`, que permite realizar consultas para buscar dados com base em critérios definidos, podendo incluir filtros, ordenações, agrupamentos e junções entre tabelas. A DQL é essencial para exibir os dados de forma útil e significativa dentro das aplicações, como páginas de perfil, dashboards, rankings ou qualquer tela que dependa de dados dinâmicos.

Apesar de possuir apenas um comando principal, a DQL é extremamente poderosa quando combinada com cláusulas como `WHERE`, `JOIN`, `GROUP BY`, `HAVING` e `ORDER BY`. Essas cláusulas aumentam a flexibilidade e a precisão das consultas, permitindo desde buscas simples até relatórios complexos.

---
## Declarações DQL essenciais para funcionamento do jogo:

### 1. Busca pelos dados do Jogador:
Vamos supor que um usuário novo acessou o jogo e, no momento da criação do seu jogador, o chamou de _'Will'_. Para que seja obtida todos os dados deste jogador, podemos realizar a seguinte consulta:

```Postgres
SELECT * FROM "jogador" WHERE "nickname" = 'Will';
```

### 2. Busca pelos dados do Mundo do Jogador:
Vamos supor que o sistema precise obter os dados do `Mundo` do jogador _'Will'_ para que o jogo consiga exibir informações como o Nível do Mundo, Período Atual e o Dia que o jogador está. Para isso, podemos realizar a seguinte consulta:

```Postgres
SELECT * FROM "mundo" WHERE "nickname" = 'Will';
```

### 3. Busca por dados da Loja do Jogador:
Vamos supor que o sistema precise obter os dados da Loja do Jogador do `Mundo` do jogador _'Will'_ porque ele entrou em sua loja. Podemos realizar a seguinte consulta:

```Postgres
SELECT LJ."seedMundo", LJ."nomeLocal", LJ."nivel", LJ."exposicaoMaxima", LJ."esposicaoUsada"
FROM "loja_jogador" LJ
  INNER JOIN "mapa" M
  ON M."seedMundo" = LJ."seedMundo"
WHERE M."nickname" = 'Will';
```

### 4. Busca por Itens do Inventário do Jogador:
Vamos supor que o sistema precise obter o `nome` e a `quantidade` de itens carregado pelo jogador _'Will'_, porque ele solicitou a abertura de seu inventário. É necessário considerar que, no jogo Moonlighter, o **inventário do jogador é composto pela Mochila, Bolsos e Equipamentos** (Armadura, Arma 1, Arma 2, Acessório), por esse motivo, além dos campos nome e quantidade, é necessário indicar em qual `tipo de inventário` o item está para o jogador. Podemos realizar a seguinte consulta:

```Postgres
SELECT I."nome", II."quantidade", IN."nome"
FROM "item" I
  INNER JOIN "inst_item" II
  ON I."idItem" = II."idItem"
  INNER JOIN "inst_inventario" IIN
  ON II."nickname" = IIN."nickname"
  INNER JOIN "inventario" IN
  ON IIN."idInventario" = IN."idInventario"
WHERE II."nickname" = 'Will';
```

### 5. Busca por Diálogos
#### 5.1. Quando o diálogo é o primeiro da ordem:
Vamos supor que o sistema precise obter o **primeiro** diálogo de um NPC chamado _'Zenon'_, pois o jogador acabou interagir com ele. Podemos realizar a seguinte consulta:

```Postgres
SELECT D."conteudo"
FROM "dialogo" D
  INNER JOIN "dialogo_npc" DN
  ON D."idDialogo" = DN."idDialogo"
  INNER JOIN "npc" N
  ON DN."idNPC" = N."idNPC"
WHERE N."nome" = 'Zenon' AND D."ordem" = 1;
```

#### 5.2. Quando o diálogo sucede um diálogo Pai:
Vamos supor que o sistema precise obter o **próximo** diálogo após o diálogo de conteúdo:

> _"Dentre as estrelas da noite, existe uma terra mais velha que a imaginação"_ 

Vamos considerar também que não sabemos a ordem em que este diálogo aconteceu, mesmo assim, o banco precisa ser capaz de buscar pelo próximo diálogo. Podemos realizar a seguinte consulta:

```Postgres
SELECT D_ATUAL."conteudo"
FROM "dialogo" D_ATUAL
  INNER JOIN "dialogo" D_ANTIGO
  ON D_ATUAL."idDialogoPai" = D_ANTIGO."idDialogo"
WHERE D_ANTIGO."conteudo" = 'Dentre as estrelas da noite, existe uma terra mais velha que a imaginação';
```

### 6. Buscar por Itens que a Loja, no Mapa do Jogador, Vende:
Vamos considerar que o usuário de seu jogador _'Will'_ acessou um dos varejos da cidade. O sistema precisa realizar uma busca pelo nome dos itens e o preço base que esteja vendendo. Podemos realizar a seguinte consulta:

```Postgres
SELECT I."nome", I."precoBase"
FROM "item" I
  INNER JOIN "inst_item" II
  ON I."idItem" = II."idItem"
WHERE II."nickname" = 'Will';
```

### 7. Bucar por Itens que a Forjaria, no Mapa do jogador, Forja:
Vamos considerar que o usuário de seu jogador _'Will'_ acessou uma das forjarias da cidade. O sistema precisa realizar uma busca pelo nome dos itens que forja os itens necessários para fabricação. Podemos realizar a seguinte consulta:

```Postgres
SELECT IFA."nome" AS "Item Forjado", IFB."nome" AS "Item Necessário", R."quantidade"
FROM "item" IFA
  INNER JOIN "receita" R
  ON IFA."idItem" = R."idItemFabricado"
  INNER JOIN "item" IFB
  ON R."idItemFabricador" = IFB."idItem"
  INNER JOIN "inst_forja_item" IFI
  ON IFA."idItem" = IFI."idItem"
  INNER JOIN "mundo" M
  ON IFB."seedMundo" = M."seedMundo"
WHERE M."nickname" = 'Will'
GROUP BY IFA."nome"
```


## Versão

| Data       | Versão | Autor(es)        | Mudanças                                               |
| ---------- | ------ | ---------------- | ------------------------------------------------------ |
| 11/06/2025 | `1.0`  | Todos da Equipe  | Criação da Página e Inserção do DQL                    |