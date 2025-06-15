<span style="background-color:#c5a352; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Versão 1.0</span>

# Data Query Language

## Conceito:

A Data Query Language (DQL), ou Linguagem de Consulta de Dados, é um subconjunto do SQL voltado especificamente para a recuperação de informações armazenadas no banco de dados. Seu principal comando é o `SELECT`, que permite realizar consultas para buscar dados com base em critérios definidos, podendo incluir filtros, ordenações, agrupamentos e junções entre tabelas. A DQL é essencial para exibir os dados de forma útil e significativa dentro das aplicações, como páginas de perfil, dashboards, rankings ou qualquer tela que dependa de dados dinâmicos.

Apesar de possuir apenas um comando principal, a DQL é extremamente poderosa quando combinada com cláusulas como `WHERE`, `JOIN`, `GROUP BY`, `HAVING` e `ORDER BY`. Essas cláusulas aumentam a flexibilidade e a precisão das consultas, permitindo desde buscas simples até relatórios complexos.

---
## Declarações DQL essenciais para funcionamento do jogo:

!!! Warning "Atenção!"
    O conteúdo deste tópico **poderá sofrer alterações** ao longo da Disciplina de Sistema de Banco de Dados 1. Portanto, à medida que novas inserções forem necessárias, o arquivo atual sempre sempre se manterá atualizado com a nova versão.


### 1. Consultas na Tabela `personagem`

#### 1.1. Listar todos os personagens
Para obter uma lista completa de todos os personagens cadastrados no jogo, desde NPCs e jogadores até criaturas, podemos usar uma consulta simples que retorna todos os registros da tabela.

```Postgres
SELECT * FROM personagem;
```

#### 1.2. Encontrar personagens poderosos
Se quisermos encontrar apenas os personagens mais fortes e de nível elevado, para uma missão especial, por exemplo, podemos filtrar por `vida_maxima` e `level`, ordenando do maior nível para o menor.

```Postgres
SELECT nome, vida_maxima, level
FROM personagem
WHERE vida_maxima > 100 AND level > 10
ORDER BY level DESC;
```

### 2. Consulta de Cenários e suas Conexões
Para que o sistema possa exibir o mapa do jogo e as opções de navegação para o jogador, ele precisa entender como os cenários se conectam. A consulta a seguir busca um cenário e mostra informações sobre os locais adjacentes (norte, sul, leste, oeste).

```Postgres
SELECT 
    c.id_cenario,
    c.sol,
    c.dia,
    norte.sol AS sol_norte,
    leste.sol AS sol_leste,
    oeste.sol AS sol_oeste,
    sul.sol AS sol_sul
FROM cenario c
LEFT JOIN cenario norte ON c.norte_id = norte.id_cenario
LEFT JOIN cenario leste ON c.leste_id = leste.id_cenario
LEFT JOIN cenario oeste ON c.oeste_id = oeste.id_cenario
LEFT JOIN cenario sul ON c.sul_id = sul.id_cenario;
```

### 3. Busca de Dados Combinados do Jogador
Quando o jogador entra no jogo, o sistema precisa carregar suas informações básicas (como o nome, que está na tabela `personagem`) e sua localização atual (que está na tabela `cenario`). A consulta a seguir une essas três tabelas para obter um resumo completo.

```Postgres
SELECT
    j.ID_personagem,
    p.nome AS nome_personagem,
    j.tipo_equipamento,
    c.id_cenario,
    c.sol AS clima_atual,
    c.dia AS periodo_dia
FROM jogador j
INNER JOIN personagem p ON j.ID_personagem = p.ID_personagem
INNER JOIN cenario c ON j.cenario = c.id_cenario;
```

### 4. Visualizar o Inventário de um Personagem
Para exibir a tela de inventário de um personagem, precisamos buscar os dados do inventário, as informações do personagem e a lista de todos os itens que ele carrega.

```Postgres
SELECT 
    i.id_inventario,
    p.nome AS nome_personagem,
    i.pods AS capacidade_inventario,
    it.nome AS nome_item,
    it.peso,
    it.durabilidade
FROM inventario i
INNER JOIN personagem p ON i.id_personagem = p.ID_personagem
LEFT JOIN item it ON it.id_inventario = i.id_inventario
WHERE p.nome = 'Roric, o Guia'; -- Exemplo para um personagem específico
```

### 5. Detalhar um Item Específico (Arma ou Armadura)
Quando o jogador clica em um item, o sistema precisa mostrar se é uma arma, uma armadura ou um item comum, exibindo seus atributos específicos (dano ou defesa).

```Postgres
SELECT 
    it.id_item,
    it.nome,
    it.peso,
    it.durabilidade,
    a.mãos AS empunhadura_arma,
    a.dano,
    ar.defesa
FROM item it
LEFT JOIN arma a ON it.id_item = a.id_item
LEFT JOIN armadura ar ON it.id_item = ar.id_item;
```

### 6. Consultas de NPCs Especializados
O jogo precisa buscar informações específicas dependendo do tipo de NPC com que o jogador interage.

#### 6.1. Informações de um Guia
Para buscar as informações de um Guia, incluindo seu nome e o custo de sua orientação.

```Postgres
SELECT 
    p.nome,
    g.custo_orientacao
FROM guia g
INNER JOIN personagem p ON g.ID_personagem = p.ID_personagem;
```

#### 6.2. Informações de um Comerciante
Para exibir a janela de comércio, mostrando o que um Comerciante compra e vende.

```Postgres
SELECT 
    p.nome,
    c.venda_item,
    c.compra_item
FROM comerciante c
INNER JOIN personagem p ON c.ID_personagem = p.ID_personagem;
```

### 7. Consultas de Criaturas e Inimigos
Para preparar um encontro de combate, o sistema busca os dados da criatura que o jogador irá enfrentar.

#### 7.1. Detalhes de um Ork
Busca os dados de um Ork, incluindo sua Fúria.

```Postgres
SELECT 
    p.nome,
    cr.XP,
    o.Raiva
FROM ork o
INNER JOIN criatura cr ON o.ID_personagem = cr.ID_personagem
INNER JOIN personagem p ON o.ID_personagem = p.ID_personagem;
```

#### 7.2. Detalhes de um Chefe (Boss)
Busca os dados de um Chefe, incluindo suas imunidades e a fase atual da batalha.

```Postgres
SELECT 
    p.nome,
    cr.XP,
    b.faseAtual,
    b.imunidades
FROM boss b
INNER JOIN criatura cr ON b.ID_personagem = cr.ID_personagem
INNER JOIN personagem p ON b.ID_personagem = p.ID_personagem;
```

### 8. Histórico de Confrontos
Para exibir um histórico de batalhas, mostrando quem lutou contra quem e qual foi o resultado.

```Postgres
SELECT
    con.Unique_ID,
    jog2.nome AS nome_jogador,
    cri2.nome AS nome_criatura,
    con.vencedor
FROM confronta con
LEFT JOIN criatura cri ON con.criatura_id = cri.ID_personagem
LEFT JOIN personagem cri2 ON cri.ID_personagem = cri2.ID_personagem
LEFT JOIN jogador jog ON con.jogador_id = jog.ID_personagem
LEFT JOIN personagem jog2 ON jog.ID_personagem = jog2.ID_personagem;
```

### 9. Análise de Dados de Batalha
Para balanceamento do jogo, um desenvolvedor pode querer analisar as médias de dano causado e sofrido em cada ambiente de batalha.

```Postgres
SELECT 
    Ambiente_batalha,
    AVG(Dano_causado) AS media_dano_causado,
    AVG(Dano_sofrido) AS media_dano_sofrido
FROM batalha
GROUP BY Ambiente_batalha
ORDER BY media_dano_causado DESC;
```

### 10. Buscar Habilidades e Características de um Jogador
Para exibir a "Ficha de Personagem" do jogador, o sistema busca suas habilidades (`skill`) e suas afinidades elementais (`caracteristicas`).

```Postgres
SELECT 
    p.nome,
    s.atq,
    c.fogo,
    c.agua,
    c.terra,
    c.ar
FROM jogador j
INNER JOIN personagem p ON j.ID_personagem = p.ID_personagem
LEFT JOIN skill s ON j.ID_personagem = s.ID_jogador
LEFT JOIN caracteristicas c ON j.ID_personagem = c.ID_jogador;
```

### 11. Listar Personagens por Classe
Para encontrar todos os personagens que pertencem a uma classe específica, como "Guerreiro".

```Postgres
SELECT 
    p.nome,
    p.level,
    gw.atq_Fisico,
    gw.bloquear_Dano
FROM guerreiro gw
INNER JOIN personagem p ON gw.id_personagem = p.ID_personagem;
```

---

## Tabela de Versionamento

| Versão | Data       | Descrição                                     | Autor(es)                                                             | Revisor(es)                                                          |
|--------|------------|-----------------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------|
|1.0  |15/06/2025     | Todos os integrantes desenvolveram esse artefato | Todos os Integrantes |Todos os Integrantes|