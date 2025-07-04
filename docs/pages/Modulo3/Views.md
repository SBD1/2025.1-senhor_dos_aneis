<span style="background-color:#c5a352; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Versão 1.0</span>

# Views (Visões de Dados)

## Conceito:

Uma **View** (Visão) é uma tabela virtual cujo conteúdo é definido por uma consulta SQL. Ela funciona como uma representação salva de uma instrução `SELECT`, permitindo que os desenvolvedores acessem dados de múltiplas tabelas como se estivessem em uma única tabela, sem armazenar os dados fisicamente de novo. Views são utilizadas para simplificar consultas complexas, encapsular a lógica de junção de dados, fornecer uma camada de abstração sobre a estrutura das tabelas e restringir o acesso a dados sensíveis, mostrando apenas colunas e linhas específicas. A criação é feita com o comando `CREATE VIEW`.

-----

## Views Implementadas no Software:

### **Visão Geral das Views**

Para facilitar o acesso e a manipulação dos dados do jogo, foram criadas quatro views principais. Cada uma delas consolida informações de várias tabelas relacionadas, fornecendo uma interface simplificada e lógica para as consultas mais comuns. Elas servem como "fichas de personagem", "catálogos de itens" e "históricos de eventos" prontos para serem consumidos pela aplicação.

A seguir, apresento a criação de cada view:

!!! Warning "Atenção!"
    O conteúdo deste tópico **poderá sofrer alterações** ao longo da Disciplina de Sistema de Banco de Dados 1. Portanto, à medida que novas inserções forem necessárias, o arquivo atual sempre sempre se manterá atualizado com a nova versão.

-----

### **1. View de Detalhes do Jogador (`vw_detalhes_jogador`)**

**Finalidade:**
Esta View resolve o problema de ter que juntar múltiplas tabelas (`personagem`, `jogador`, `skill`, `caracteristicas`, `cenario`) toda vez que se precisa de uma ficha completa do personagem do jogador. Ela centraliza todos os atributos relevantes, desde stats básicos até a localização atual, em um único objeto de fácil consulta.

**Estrutura SQL:**

```postgres
CREATE OR REPLACE VIEW vw_detalhes_jogador AS
SELECT
    p.id_personagem,
    p.nome,
    p.level,
    p.vida_maxima,
    p.mana_maxima,
    p.habilidade,
    p.resistencia,
    j.tipo_equipamento,
    s.atq AS ataque,
    c.fogo,
    c.agua,
    c.terra,
    c.ar,
    cen.id_cenario AS cenario_atual_id,
    cen.sol AS clima_cenario_atual
FROM
    personagem p
    INNER JOIN jogador j ON p.id_personagem = j.id_personagem
    LEFT JOIN skill s ON j.id_personagem = s.id_jogador
    LEFT JOIN caracteristicas c ON j.id_personagem = c.id_jogador
    LEFT JOIN cenario cen ON j.cenario = cen.id_cenario;
```

**Exemplo de Uso:**

```postgres
-- Para ver a ficha completa de todos os jogadores
SELECT * FROM vw_detalhes_jogador;

-- Para buscar os detalhes de um jogador específico
SELECT * FROM vw_detalhes_jogador WHERE nome = 'Roric, o Guia';
```

-----

### **2. View de Itens Completos (`vw_itens_completos`)**

**Finalidade:**
Simplifica drasticamente a consulta de itens. Em vez de verificar as tabelas `item`, `arma` e `armadura` separadamente, esta View apresenta todos os atributos em um único local, usando um `CASE` para classificar o tipo de item. Além disso, ela já informa a qual personagem o item pertence.

**Estrutura SQL:**

```postgres
CREATE OR REPLACE VIEW vw_itens_completos AS
SELECT
    i.id_item,
    i.nome AS nome_item,
    i.peso,
    i.durabilidade,
    a.dano,
    a.mãos,
    ar.defesa,
    p.id_personagem AS dono_id,
    p.nome AS dono_nome,
    CASE
        WHEN a.id_item IS NOT NULL THEN 'Arma'
        WHEN ar.id_item IS NOT NULL THEN 'Armadura'
        ELSE 'Item Comum'
    END AS tipo_de_item
FROM
    item i
    LEFT JOIN arma a ON i.id_item = a.id_item
    LEFT JOIN armadura ar ON i.id_item = ar.id_item
    LEFT JOIN inventario inv ON i.id_inventario = inv.id_inventario
    LEFT JOIN personagem p ON inv.id_personagem = p.id_personagem;
```

**Exemplo de Uso:**

```postgres
-- Listar todos os itens do jogo com seus detalhes e donos
SELECT * FROM vw_itens_completos;

-- Listar apenas as armas que 'Roric, o Guia' possui
SELECT nome_item, dano, durabilidade FROM vw_itens_completos 
WHERE dono_nome = 'Roric, o Guia' AND tipo_de_item = 'Arma';
```

-----

### **3. View de Histórico de Confrontos (`vw_historico_confrontos`)**

**Finalidade:**
Torna a tabela de log de batalhas (`confronta`) muito mais legível e útil para exibição ou análise. Ela substitui os IDs do jogador e da criatura por seus nomes reais e traduz o campo booleano `vencedor` para um texto claro e descritivo sobre o resultado do confronto.

**Estrutura SQL:**

```postgres
CREATE OR REPLACE VIEW vw_historico_confrontos AS
SELECT
    c.unique_id,
    jog_p.nome AS nome_jogador,
    cria_p.nome AS nome_criatura,
    CASE
        WHEN c.vencedor = TRUE THEN 'Vitória do Jogador'
        WHEN c.vencedor = FALSE THEN 'Vitória da Criatura'
        ELSE 'Indefinido'
    END AS resultado
FROM
    confronta c
    LEFT JOIN jogador jog ON c.jogador_id = jog.id_personagem
    LEFT JOIN personagem jog_p ON jog.id_personagem = jog_p.id_personagem
    LEFT JOIN criatura cria ON c.criatura_id = cria.id_personagem
    LEFT JOIN personagem cria_p ON cria.id_personagem = cria_p.id_personagem;
```

**Exemplo de Uso:**

```postgres
-- Ver o histórico completo de todos os confrontos de forma legível
SELECT * FROM vw_historico_confrontos ORDER BY unique_id DESC;

-- Ver todas as batalhas envolvendo o 'Rei Demônio'
SELECT nome_jogador, resultado FROM vw_historico_confrontos WHERE nome_criatura = 'Rei Demônio';
```

-----

### **4. View de Informações dos NPCs (`vw_informacoes_npcs`)**

**Finalidade:**
Esta View cria um diretório unificado de todos os Personagens Não-Jogáveis. Ela agrega informações das especializações (`guia`, `comerciante`, `npc`) para mostrar, em uma única consulta, o tipo de cada NPC, suas ofertas (quests, itens à venda) e dados gerais como localização e diálogo.

**Estrutura SQL:**

```postgres
CREATE OR REPLACE VIEW vw_informacoes_npcs AS
SELECT
    p.id_personagem,
    p.nome,
    p.level,
    p.dialogo,
    n.localizacao,
    n.quest,
    n.hora_aparicao,
    co.venda_item,
    co.compra_item,
    g.custo_orientacao,
    CASE
        WHEN g.id_personagem IS NOT NULL THEN 'Guia'
        WHEN co.id_personagem IS NOT NULL THEN 'Comerciante'
        WHEN n.id_personagem IS NOT NULL THEN 'NPC de Quest'
        ELSE 'NPC Comum'
    END AS tipo_npc
FROM
    personagem p
    INNER JOIN npc n ON p.id_personagem = n.id_personagem
    LEFT JOIN comerciante co ON p.id_personagem = co.id_personagem
    LEFT JOIN guia g ON p.id_personagem = g.id_personagem;
```

**Exemplo de Uso:**

```postgres
-- Listar todos os NPCs do jogo e suas funções
SELECT nome, tipo_npc, localizacao, quest FROM vw_informacoes_npcs;

-- Encontrar todos os comerciantes e o que eles vendem
SELECT nome, venda_item, compra_item FROM vw_informacoes_npcs WHERE tipo_npc = 'Comerciante';
```

---


## Tabela de Versionamento

| Versão | Data       | Descrição                                     | Autor(es)                                                             | Revisor(es)                                                          |
|--------|------------|-----------------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------|
|1.0  |04/07/2025     | Criação da documentação para as Views do banco de dados | [Felipe das Neves](https://github.com/FelipeFreire-gf) | [Felipe das Neves](https://github.com/FelipeFreire-gf) |