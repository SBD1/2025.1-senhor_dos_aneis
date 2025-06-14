<span style="background-color:#1ec68e; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Versão 1.0</span>

# Data Manipulation Language

!!! Warning "Atenção!"
    O conteúdo deste tópico **poderá sofrer alterações** ao longo da Disciplina de Sistema de Banco de Dados 1. Portanto, à medida que novas inserções forem necessárias, o arquivo atual sempre sempre se manterá atualizado com a nova versão.

## Conceito:

A Data Manipulation Language (DML), ou Linguagem de Manipulação de Dados, é a parte do SQL responsável por lidar diretamente com os dados armazenados nas estruturas definidas pela DDL. Enquanto a DDL define "onde" os dados vão ficar, a DML atua sobre "quais" dados vão ocupar esses espaços e "como" serão manipulados. Com comandos como `SELECT`, `INSERT`, `UPDATE` e `DELETE`, a DML permite consultar, adicionar, modificar e remover registros dentro das tabelas do banco de dados.

Ao contrário dos comandos DDL, que geralmente afetam a estrutura do banco de forma permanente, os comandos DML operam sobre os dados em si e podem ser revertidos com o uso de transações (`BEGIN`, `COMMIT`, `ROLLBACK`). Isso garante maior controle sobre as operações, especialmente em aplicações que exigem consistência e segurança na manipulação de dados.

---
## Declarações de DML no Software:

!!! Tip "Atenção!"
    Alguns DML's abaixo **também utiliza de comandos DQL (Data Query Language) de forma integrada**, isto é, comandos `SELECT` a fim de não comprometer as referências às chaves primárias à medida que o software evolui. Dessa maneira, entenda que ao invés da equipe inserir manualmente os valores de _ID's_ ou _Seeds_ nos campos de chave estrangeira, foi feito uma busca com `SELECT` sob alguns parâmetros com `WHERE` para capturar estes valores.  

??? info "_local_ INSERT's"

    ```Postgres
    INSERT INTO "local" VALUES
        ('Vila Rynoka', '', 'Local', NULL);
    -- INSERÇÃO DE FILHOS NA TABELA LOCAL:
    INSERT INTO "local" VALUES
        ('Centro Comercial', '', 'Local', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Vila Rynoka')),
        ('Praça', '', 'Local', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Vila Rynoka')),
        ('Moonlighter', '', 'Estabelecimento', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Vila Rynoka')),
        ('Área das Masmorras', '', 'Local', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Vila Rynoka'));
    INSERT INTO "local" VALUES
        ('Masmorra do Golem', 'Primeira masmorra acessível, repleta de sentinelas golem e criaturas de pedra. Enfrente o Rei Golem no 3º andar.', 'Masmorra', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Área das Masmorras')),
        ('Masmorra da Floresta', 'Masmorra florestal estreita, infestada de plantas mutantes e a Mutae Carnívora como chefe no último andar.', 'Masmorra', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Área das Masmorras')),
        ('Masmorra do Deserto', 'Antigas ruínas desérticas com tempestades de areia e o Guardião do Deserto aguardando no 3º andar.', 'Masmorra', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Área das Masmorras')),
        ('Masmorra da Tecnologia', 'Instalações tecnológicas abandonadas, protegidas por robôs, com o Guardião da Tecnologia aguardando no último andar.', 'Masmorra', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Área das Masmorras')),
        ('Forja Vulcânica', '', 'Estabelecimento', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Centro Comercial')),
        ('O Chapéu de Madeira', '', 'Estabelecimento', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Centro Comercial')),
        ('Banco de Rynoka', '', 'Estabelecimento', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Centro Comercial')),
        ('Tenda da Bruxa', '', 'Estabelecimento', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Centro Comercial')),
        ('Barraca do Tom', '', 'Estabelecimento', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Centro Comercial')),
        ('Quarto', '', 'Local', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Moonlighter')),
        ('Salão de Exposição', '', 'Local', (SELECT "nomeLocal" FROM "local" WHERE "nomeLocal" = 'Moonlighter'));
    ```

??? info "_masmorra_ INSERT"

    ```Postgres
    -- INSERÇÃO NA TABELA MASMORRA:
    INSERT INTO "masmorra"
        VALUES
        ('Masmorra do Golem', 1, 3),
        ('Masmorra da Floresta', 2, 3),
        ('Masmorra do Deserto', 3, 3),
        ('Masmorra da Tecnologia', 4, 3);
    ```

??? info "_estabelecimento_ INSERT"

    ```Postgres
    -- INSERÇÃO NA TABELA ESTABELECIMENTO:
    INSERT INTO "estabelecimento" 
        VALUES
        ('Moonlighter'),
        ('Forja Vulcânica'),
        ('O Chapéu de Madeira'),
        ('Banco de Rynoka'),
        ('Tenda da Bruxa'),
        ('Barraca do Tom');
    ```

??? info "_efeito_ INSERT"

    ```Postgres
    -- INSERÇÃO NA TABELA EFEITOS:
    INSERT INTO "efeito"
        ("nome", "descricao", "tipo", "valor", "duracaoTurnos")
        VALUES
        ('Envenenado', 'Dano contínuo de veneno ao longo do tempo', 'debuff', 3, 5),
        ('Queimado', 'Dano contínuo de fogo ao longo do tempo', 'debuff', 5, 4),
        ('Congelado', 'Congela o inimigo, impedindo seus movimentos e ações','debuff', 2, 2),
        ('Atordoado', 'Paralisa o alvo temporariamente', 'debuff', 0, 1),
        ('Proteção', 'Escudo temporário que absorve dano', 'buff', 20, 3),
        ('Cobiçado', 'Aumenta valor de venda do item', 'economia', 0, NULL),
        ('Amaldiçoado', 'Dano se item estiver no inventário', 'maldição', 8, NULL),
        ('Maldição da Bolsa', 'Bloqueia uso do inventário', 'debuff', 0, 3),
        ('Cura Pequena', 'Restaura 35 pontos de vida', 'cura', 35, 0),
        ('Cura Média', 'Restaura 70 pontos de vida', 'cura', 70, 0),
        ('Cura Grande', 'Restaura 150 pontos de vida', 'cura', 150, 0);
    ```

??? info "_monstro_ INSERT"


    ```Postgres
    -- INSERÇÃO NA TABELA MONSTRO:
    INSERT INTO "monstro"
        ("nome", "descricao", "nivel", "vidaMaxima", "ouroDropado", "dadoAtaque",
        "chanceCritico", "multiplicador", "multiplicadorCritico", "chefe",
        "nomeLocal", "idEfeito")
        VALUES
        -- Masmorra do Golem (nível 1)
        ('Baby Slime', 'Pequeno slime que ataca em grupo.', 1, 60, 10, '1d4', 0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Torre Golem Quebrada', 'Torre de pedra inoperante que dispara fragmentos.', 1, 80, 15, '1d6', 0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Guerreiro Golem Corrompido','Guerreiro golem com ataques pesados.', 1, 120,  20, '1d8', 0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Golem Voador', 'Drone voador que investe em alta velocidade.', 1, 100, 15, '1d6', 0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Golem Reparador Voador', 'Drone que repara aliados e empurra o jogador.', 1,  90, 12, '1d4', 0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Mimico Dourado', 'Baú dourado que se revela monstro ao ser atacado.', 1, 110, 25, '1d6', 0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Cabeça de Golem', 'Cabeça de golem que rola em direção ao jogador.', 1, 70, 12, '1d4', 0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Mina Golem', 'Dispositivo que explode ao se aproximar.', 1, 50, 10, '1d4', 0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Torre Golem', 'Torre que dispara projéteis de energia.', 1,  85,  15, '1d6', 0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Guerreiro Golem', 'Guerreiro de pedra padrão com ataques físicos.', 1, 130, 20, '1d8',  0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Mimico de Ferro', 'Baú metálico que se transforma em monstro.', 1, 115, 25, '1d6', 0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Slime', 'Grande slime que pode engolir o jogador.', 1, 140,  18, '1d8',  0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Manopla de Slime', 'Mão de pedra gigante com base de slime.', 1, 150,  22, '1d10', 0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Mordomo de Pedra', 'Golem com escudo e bastão que dispara luz.', 1, 120,  18, '1d8',  0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Soldado de Pedra',        'Soldado de pedra com capa que ataca com espada.',   1, 160,  20, '1d10', 0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Tangle',               'Criatura que se move em zigue-zague.',             1,  90,  12, '1d6',  0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        ('Rei Golem',       'Rei dos golems, imenso e imóvel; braço de pedra.',  1, 500, 100, '2d12', 0.10, 2, 3, TRUE,  'Masmorra do Golem', NULL),
        ('Errante',             'Inimigo raro que surge aleatoriamente.',           1, 300,  50, '1d12', 0.10, 2, 3, FALSE, 'Masmorra do Golem', NULL),
        ('Mimico de Madeira',           'Baú de madeira que se transforma em monstro.',     1, 125,  25, '1d6',  0.05, 1, 2, FALSE, 'Masmorra do Golem', NULL),
        -- Masmorra da Floresta (nível 2)
        ('Baby Slime Venenoso',    'Pequeno slime venenoso que aparece em grupos.',    2,  70,  12, '1d4',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', 1),
        ('Árvore Lâmina',           'Tronco móvel que lança folhas afiadas.',           2, 110,  18, '1d6',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Mutae Carnívora',    'Planta gigante com tentáculos que atacam em área.',2, 400,  60, '2d10', 0.10, 2, 3, TRUE,  'Masmorra da Floresta', NULL),
        ('Árvore Mavu Corrompida',  'Árvore corrompida que invoca ramos venenosos.',     2, 130,  22, '1d8',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Tangle da Floresta',        'Planta carnívora que se move rapidamente.',        2, 100,  16, '1d6',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Torre de Fruta',         'Estrutura de madeira que dispara sementes.',      2,  90,  14, '1d4',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Mimico Dourado',           'Baú dourado que se revela monstro ao ser atacado.',2, 145,  30, '1d6',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Mimico de Ferro',           'Baú metálico que se transforma em monstro.',      2, 140,  28, '1d6',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Jardineiro',           'Humanoide que lança espinhos e armadilhas.',      2, 150,  25, '1d8',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Árvore Mavu',            'Árvore que lança explosões de sementes tóxicas.',2, 125,  20, '1d8',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Slime Venenoso',         'Slime grande que solta veneno ao contato.',       2, 180,  24, '1d10', 0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Semeador',               'Dispositivo que planta sementes explosivas.',    2,  95,  15, '1d6',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Cogumelo Giratório',    'Cogumelo que gira arremessando fragmentos.',      2, 120,  20, '1d8',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Arbusto de Esporos',           'Arbusto que dispara nuvens de esporos venenosos.',2, 110,  18, '1d6',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Tangle Venenoso',      'Variante tóxica do Tangle com chifres venenosos.',2, 105,  18, '1d6',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Errante',             'Inimigo raro que surge aleatoriamente.',         2, 320,  55, '1d12', 0.10, 2, 3, FALSE, 'Masmorra da Floresta', NULL),
        ('Árvore do Vento',            'Árvore que usa folha para lançar rajadas de vento.',2, 115,  19, '1d6',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        ('Mimico de Madeira',           'Baú de madeira que se transforma em monstro.',    2, 150,  28, '1d6',  0.06, 1, 2, FALSE, 'Masmorra da Floresta', NULL),
        -- Masmorra do Deserto (nível 3)
        ('Baby Slime de Fogo',      'Pequeno slime de fogo que explode ao morrer.',    3,  80,  14, '1d4',  0.07, 1, 2, FALSE, 'Masmorra do Deserto', 2),
        ('Fantoche Bardo',          'Fantoche que toca lâminas giratórias.',         3, 120,  20, '1d8',  0.07, 1, 2, FALSE, 'Masmorra do Deserto', NULL),
        ('Tangle de Pano',         'Tangle reforçado com tecido resistente ao fogo.',3, 110,  18, '1d6',  0.07, 1, 2, FALSE, 'Masmorra do Deserto', NULL),
        ('Hexa Corrompido',       'Caixa voadora corrompida que emite explosões.',3, 100,  16, '1d6',  0.07, 1, 2, FALSE, 'Masmorra do Deserto', NULL),
        ('Fantoche de Fogo',          'Fantoche flamejante que libera ondas de calor.',3, 140,  25, '1d10', 0.07, 1, 2, FALSE, 'Masmorra do Deserto', 2),
        ('Slime de Fogo',           'Slime ardente que queima tudo ao redor.',       3, 180,  30, '1d12', 0.07, 1, 2, FALSE, 'Masmorra do Deserto', 2),
        ('Mimico Dourado',           'Baú dourado que se revela monstro ao ser atacado.',3,155,  32, '1d6',  0.07, 1, 2, FALSE, 'Masmorra do Deserto', NULL),
        ('Hexa',                 'Caixa flutuante que dispara rajadas de areia.',3, 130,  22, '1d8',  0.07, 1, 2, FALSE, 'Masmorra do Deserto', NULL),
        ('Mimico de Ferro',           'Baú metálico que se transforma em monstro.',    3, 160,  30, '1d6',  0.07, 1, 2, FALSE, 'Masmorra do Deserto', NULL),
        ('Golem Katamari',       'Golem esférico que rola em alta velocidade.',   3, 200,  28, '1d10', 0.07, 1, 2, FALSE, 'Masmorra do Deserto', NULL),
        ('Catapulta de Lava',        'Mecanismo que lança glóbulos de lava.',        3, 125,  20, '1d8',  0.07, 1, 2, FALSE, 'Masmorra do Deserto', 2),
        ('Fantoche Mágico',      'Fantoche que lança fogo e teleporta.',         3, 140,  24, '1d8',  0.07, 1, 2, FALSE, 'Masmorra do Deserto', 2),
        ('Golem Mãe',         'Golem enorme que invoca miniaturas.',           3, 450,  65, '2d10', 0.10, 2, 3, TRUE,  'Masmorra do Deserto', NULL),
        ('Naja',                 'Guardião serpentino das ruínas desérticas.',    3, 480,  70, '2d12', 0.10, 2, 3, TRUE,  'Masmorra do Deserto', NULL),
        ('Golem Patrulheiro',         'Golem que patrulha corredores e investe.',     3, 170,  28, '1d10', 0.07, 1, 2, FALSE, 'Masmorra do Deserto', NULL),
        ('Errante',             'Inimigo raro que surge aleatoriamente.',         3, 350,  60, '1d12', 0.10, 2, 3, FALSE, 'Masmorra do Deserto', NULL),
        ('Mimico de Madeira',           'Baú de madeira que se transforma em monstro.',  3, 160,  32, '1d6',  0.07, 1, 2, FALSE, 'Masmorra do Deserto', NULL),
        -- Masmorra da Tecnologia (nível 4)
        ('Baby Slime Elétrico',  'Pequeno slime elétrico que causa choque.',      4,  90,  16, '1d4',  0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Oscilador Corrompido', 'Dispositivo que emite ondas elétricas.',       4, 130,  22, '1d6',  0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Gerador da Morte',      'Gerador que dispara rajadas de energia mortal.',4, 140,  24, '1d8',  0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Poste Elétrico',        'Torre que dispara raios elétricos.',            4, 120,  20, '1d6',  0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Slime Elétrico',       'Slime que emite descargas elétricas.',          4, 160,  28, '1d10', 0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Bola Eletromagnética', 'Esfera que teleporta e lança raios.',           4, 150,  26, '1d8',  0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Fluxo de Energia',          'Núcleo de energia instável que dispara lasers.', 4, 480,  80, '2d12', 0.12, 2, 3, TRUE,  'Masmorra da Tecnologia', NULL),
        ('Lançador Golem',         'Golem que arremessa projéteis explosivos.',     4, 180,  30, '1d10', 0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Gerador Graaf',      'Dispositivo que gera escudos para aliados.',    4, 125,  18, '1d6',  0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Mimico de Ferro',           'Baú metálico que se transforma em monstro.',    4, 170,  32, '1d6',  0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Oscilador',           'Dispositivo que emite pulsos elétricos.',       4, 135,  24, '1d8',  0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Recarregador',            'Unidade que recarrega energia de aliados.',     4, 140,  26, '1d6',  0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Drone Reparador',         'Drone que repara aliados automaticamente.',     4, 145,  28, '1d6',  0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Redemoinho de Areia',           'Gera redemoinhos de areia para atrapalhar.',    4, 110,  18, '1d4',  0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Armadilha de Slime',           'Armadilha que libera slime pegajoso.',         4, 100,  16, '1d4',  0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Corrente de Espinhos',          'Corrente com espinhos que gira em torno.',      4, 175,  30, '1d10', 0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Errante',             'Inimigo raro que surge aleatoriamente.',         4, 380,  65, '1d12', 0.12, 2, 3, FALSE, 'Masmorra da Tecnologia', NULL),
        ('Mimico de Madeira',           'Baú de madeira que se transforma em monstro.',  4, 180,  34, '1d6',  0.08, 1, 2, FALSE, 'Masmorra da Tecnologia', NULL);
    ```
??? info "_item_ INSERT"

    ```Postgres
    -- INSERÇÃO NA TABELA ITENS:
    INSERT INTO "item"
        ("nome", "descricao", "tipo", "precoBase", "cultura", "stackMaximo", "idEfeito")
        VALUES
        -- ITENS SEM CATEGORIA:
        ('Espada Quebrada', 'Bastante inútil na sua forma atual, mas eu poderia ser facilmente derretido para criar algo novo!', 'Item', 150, 'Golem', 5, NULL),
        ('Tecido', 'Robusto, mas áspero ao tato. Imagino que alguns queiram utilizá-lo na criação de decorações.', 'Item', 250, 'Golem', 5, NULL),
        ('Restos de Fundição', 'Creio que isto são os restos de uma antiga fundição. Se os Golems foram criados, o que é que os criou?', 'Item', 150, 'Golem', 5, NULL),
        ('Cinzel de Golem', 'Esse é definitivamente um cinzel usado para esculpir e moldar um Golem. Por sua estrutura, imagino que os arquitetos não eram muito diferentes de nós.', 'Item', 500, 'Golem', 5, NULL),
        ('Aço Endurecido', 'O aço mais forte que já encontrei. Perfeito para a criação de novos equipamentos.', 'Item', 300, 'Golem', 5, NULL),
        ('Barra de Ferro', 'Ferro. Bastante básico, mas a pedra fundamental de qualquer equipamento de nível médio que se queira fabricar.', 'Item', 25, 'Golem', 10, NULL),
        ('Geléia Rica', 'Substância gelatinosa com muitas propriedades curativas. Pode ser extraída de vários Slimes. Essencial na preparação de poções.', 'Item', 5, 'Mercador', 10, NULL),
        ('Raiz', 'Uma raiz de uma planta gigante. Muito útil para a criação de novos arcos.', 'Item', 5, 'Golem', 10, NULL),
        ('Ferramenta Rúnica', 'Parece ter sido uma ferramenta usada para inscrever texto em metal e pedra. Talvez possa ser usada para inscrever runas em meu equipamento.', 'Item', 1500, 'Golem', 5, NULL),
        ('Pedra de Dente', 'Pedra muito afiada, comumente encontrada nos corpos de Golems antigos.', 'Item', 5, 'Golem', 10, NULL),
        ('Cipó', 'Um material forte, porém flexível, usado pelas criaturas Tangle para se protegerem.', 'Item', 2, 'Golem', 10, NULL),
        ('Esfera de Água', 'Uma esfera branca leitosa ou algum material desconhecido contendo água emitindo uma luz estranha, quase sinistra.', 'Item', 100, 'Golem', 10, NULL),
        ('Pedra de Amolar', 'Pedra básica usada por ferreiros para amolar e afiar armas. Nunca é demais ter uma pedra dessas.', 'Item', 15, 'Golem', 10, NULL),
        ('Madeira Antiga', 'Madeira petrificada devido a anos de permanência em ambientes com elementos específicos.', 'Item', 1000, 'Floresta', 5, NULL),
        ('Madeira Mágica', 'Madeira embebida em resíduos mágicos durante anos. Emite pequenas faíscas azuis. Material potencialmente útil para resistir a outras magias elementares.', 'Item', 100, 'Floresta', 10, NULL),
        ('Bulbo Antigo', 'Um bulbo bastante grande que pertenceu a uma planta já morta... Não está vivo... mas também não está realmente morto...', 'Item', 2000, 'Floresta', 5, NULL),
        ('Raiz Preservada', 'Uma raiz muito antiga e muito bem preservada.', 'Item', 600, 'Floresta', 5, NULL),
        ('Ácido Puro', 'Puro ácido. Não sei o que me levou a tentar colecionar esse material. Derrete em quase tudo.', 'Item', 400, 'Floresta', 10, NULL),
        ('Palha', 'Uma simples pilha de palha. Nada surpreendente. No entanto, parece estar coberto por alguns líquidos corrosivos. Talvez tenha sido usado como isolamento para alguma coisa?', 'Item', 500, 'Floresta', 5, NULL),
        ('Folhas Fortes', 'Folhas endurecidas que são flexíveis o suficiente para ricochetear nas paredes em vez de se estilhaçar. Essa foi uma lição duramente aprendida...', 'Item', 400, 'Floresta', 10, NULL),
        ('Geléia de Veneno', 'Uma variante de geleia venenosa encontrada em slimes da floresta. Extraia com cuidado.', 'Item', 20, 'Floresta', 10, NULL),
        ('Corda do Deserto', 'Uma corda... que não pega fogo... Quem quer que tenha residido na Masmorra do Deserto deve ter sido um povo incrivelmente inventivo.', 'Item', 450, 'Deserto', 5, NULL),
        ('Lingote de Aço do Deserto', 'Aço bruto encontrado na Masmorra do Deserto. Anos de ventos arenosos parecem tê-lo endurecido mais do que a maioria dos metais.', 'Item', 7500, 'Deserto', 5, NULL),
        ('Joia de Fogo', 'Faísca instantânea ao entrar em contato com uma pedra ou até mesmo com um pano grosso. Um iniciador de fogo perfeito.', 'Item', 1700, 'Deserto', 10, NULL),
        ('Geléia de Fogo', 'Uma variante de gelatina que parece estar sempre pegando fogo... Encontrada nos Slimes do Deserto. Não posso beber nada feito com isso... posso?', 'Item', 100, 'Mercador', 10, NULL),
        ('Tecido à Prova de Fogo', 'Um tecido que se recusa a queimar. Frequentemente encontrado enrolado em pilhas de areia. Possivelmente usado para proteger a areia durante um processo de aquecimento extremo?', 'Item', 1150, 'Deserto', 10, NULL),
        ('Pó Inflamável', 'Pó altamente inflamável. Ótimo para reacender o fogo. Preciso ter alguns em estoque perto do fogão.', 'Item', 400, 'Deserto', 10, NULL),
        ('Pó Isolante', 'Pó usado para isolar conduítes do calor.', 'Item', 2050, 'Deserto', 10, NULL),
        ('Magnetita', 'Um mineral usado para magnetizar outros materiais.', 'Item', 800, 'Deserto', 10, NULL),
        ('Motor Termomagnético', 'Com tantas peças giratórias, ele parece mágico. Um dispositivo que transforma a energia térmica em ondas magnéticas.', 'Item', 9200, 'Deserto', 5, NULL),
        ('Metal Condutor', 'Sucata de metal encontrada em torno da Masmorra da Tecnologia. Pode ser usado como condutor durante a fabricação.', 'Item', 600, 'Tecnologia', 10, NULL),
        ('Bobina de Cobre', 'O cobre condutor é fiado em fios e depois enrolado nessa bobina. Fácil de acessar. Design criativo.', 'Item', 7500, 'Tecnologia', 5, NULL),
        ('Geléia Elétrica', 'Essa geleia é elétrica, e não estou falando de movimentos de dança... Extraído de Slimes da Tecnologia. Eu poderia criar algumas armas inéditas com isso.', 'Item', 400, 'Mercador', 10, NULL),
        ('Fios de Ouro', 'Fios de ouro reais entrelaçados em fios usados por muitas das máquinas das masmorras da Tecnologia. A manutenção deve ser cara.', 'Item', 2100, 'Tecnologia', 10, NULL),
        ('Madeira Tratada', 'Madeira tratada para resistir a líquidos corrosivos.', 'Item', 5150, 'Tenologia', 5 , NULL),
        ('Bateria de Célula Tripla', 'Uma variante muito maior do Capacitor. Aparentemente, ele pode armazenar grandes quantidades de energia não mágica.', 'Item', 10000, 'Tecnologia', 5, NULL),
        ('Pistola de Solda', 'Com o uso de vários outros recursos, esse dispositivo pode unir firmemente determinados metais.', 'Item', 11650, 'Tecnologia', 5, NULL),
        ('Fios', 'Pequenos fios de metal usados para conduzir eletricidade.', 'Item', 2550, 'Tecnologia', 10, NULL),
        ('Pedra de Wolfram', 'Uma versão bruta do metal tungstênio. Não processado, mas certamente valioso para quem precisa do material.', 'Item', 6350, 'Tecnologia', 5, NULL),
        ('Adapatador AC', 'Normalmente, eles se encontram entre uma "bateria" e o que requer energia. Deve ser algum tipo de conversor.', 'Item', 15550, 'Tenologia', 5, NULL),
        ('Pote Antigo', 'Tem uma ou duas pequenas rachaduras, mas ainda pode conter algo. Muito bem trabalhado. Curioso para saber para que poderia ter sido usado.', 'Item', 100, 'Tecnologia', 5, NULL),
        ('Frasco de Argônio', 'Com frequência, eu encontrava o gás nesse frasco perto de metal limpo e sem manchas. Ele deve evitar algum tipo de processo químico que resulte em ferrugem.', 'Item', 12050, 'Tecnologia', 5, NULL),
        ('Folhas de Lâminas', 'Folhas afiadas usadas como armas de projétil por vários inimigos bastante incômodos...', 'Item', 300, 'Floresta', 10, NULL),
        ('Anotações de Botânica I', 'Originalmente, queríamos melhorar o tamanho da colheita, mas a introdução da cepa LF1 parece ter dado às plantas uma autoconsciência...', 'Livro', 2000, 'Floresta', 5, NULL),
        ('Anotações de Botânica II', 'Plantas que se movem por conta própria? As possibilidades são ilimitadas. Uma colheita melhor é apenas o começo! Será que poderíamos domesticá-las?', 'Livro', 2000, 'Floresta', 5, NULL),
        ('Anotações de Botânica III', 'Com a injeção contínua da cepa LF1, determinadas plantas se tornaram criaturas formidáveis capazes de agressão. Precisamos manter isso na linha.', 'Livro', 2000, 'Floresta', 5, NULL),
        ('Bateria Quebrada', 'Um receptáculo quebrado para energia não mágica... Quem criou todos esses artefatos?', 'Item', 2850, 'Tecnologia', 10, NULL),
        ('Taco Quebrado', 'O taco está quebrado e não tem conserto.', 'Item', 300, 'Mercador', 1, NULL),
        ('Arco Quebrado', 'O Arco e Flexa está quebrado e não tem conserto', 'Item', 10000, 'Mercador', 1, NULL),
        ('Adaga Quebrada', 'A Adaga está quebrada e não tem conserto', 'Item', 20000, 'Mercador', 1, NULL),
        ('Katana Quebrada', 'A Katana está quebrada e não tem conserto', 'Item', 2000, 'Mercador', 1, NULL),
        ('Maça Qubrada', 'A Maça está quebrada e não tem conserto', 'Item', 300, 'Mercador', 1, NULL),
        ('Clava Quebrada', 'A Clava está quebrada e não tem conserto', 'Item', 10000, 'Mercador', 1, NULL),
        ('Arpão Quebrado', 'Um pedaço de metal velho, torto e inútil.', 'Item', 2000, 'Mercador', 1, NULL),
        ('Estilingue Quebrado', 'Um pedaço de couro esfarrapado e cheio de buracos. Ele nunca mais disparará um projétil.', 'Item', 300, 'Mercador', 1, NULL),
        ('Chicote Quebrado', 'O couro está completamente estragado, provavelmente já foi um ótimo chicote.', 'Item', 20000, 'Mercador', 1, NULL),
        ('Observações sobre Mutae Carnívora', 'Ao introduzir um fluxo constante de LF1 em uma planta em vez de injeções, esperamos criar uma planta grande o suficiente para produzir frutos para uma cidade!', 'Item', 5000, 'Floresta', 5, NULL),
        ('Sementes de Mutae Carnívora', 'Sementes que saíram do Guardião da Floresta ao derrotá-lo. Elas devem ser únicas. Curioso... Elas poderiam se transformar em algo?...', 'Item', 5000, 'Floresta', 5, NULL),
        ('Lava Resfriada', 'Lava que parece ter sido congelada rapidamente. Sempre fria ao toque.', 'Item', 2500, 'Deserto', 5, NULL),
        ('Tintura de Tecido', 'Parece que esse corante pode ser à prova de fogo em qualquer peça de roupa em que for aplicado. A Masmorra do Deserto está repleta de itens interessantes.', 'Item', 2750, 'Deserto', 5, NULL),
        ('Rocha de Cristal', 'Um belo cristal de muitas cores. Ouvi rumores de que ele está sendo usado como condutor com resultados fantásticos.', 'Item', 75, 'Golem', 10, NULL),
        ('Fragmentos de Cristal', 'Cristais quebrados... O desgaste e as marcas indicam a possibilidade de que algum tipo de energia tenha passado por eles.', 'Item', 500, 'Tecnologia', 10, NULL),
        ('Energia Cristalizada', 'Parece que a energia que surge em um Golem se cristaliza após sua Restos de Fundiçãodestruição. Será que podemos aproveitar esse poder de alguma forma?', 'Item', 100, 'Golem', 10, NULL),
        ('História do Deserto I', 'Três sóis perfuram o céu. Lançando luz quase infinita sobre nós. Suas rotações estão alinhadas para permitir apenas dois dias de escuridão por ano.', 'Livro', 15000, 'Deserto', 5, NULL),
        ('História do Deserto II', 'As três irmãs no céu estão sempre nos vigiando. Nossos dias são longos e quentes, mas a energia das irmãs nos deu muitos presentes.', 'Livro', 15000, 'Deserto', 5, NULL),
        ('História do Deserto III', 'Seu calor ilimitado nos deu o controle das chamas. Ele alimentou nossas máquinas. E criou a lava eterna que protege nossas cidades.', 'Livro', 15000, 'Deserto', 5, NULL),
        ('Chapa de Aço do Deserto', 'Um metal resistente que se torna incrivelmente flexível quando uma corrente magnética passa por ele. É preciso que o ferreiro faça experimentos com isso.', 'Item', 2500, 'Deserto', 10, NULL),
        ('Pedra do Deserto', 'Pedra branca polida com alto ponto de fusão.', 'Item', 2700, 'Deserto', 5, NULL),
        ('Areia Doamantinética', 'Areia que realmente reage a campos magnéticos. É raro, mas já vi várias esculturas usarem esse material para criar cenas flutuantes de areia.', 'Item', 500, 'Deserto', 10, NULL),
        ('Cristal Capacitador', 'Fonte de cristal bruto de poder mágico.', 'Item', 100, 'Mercador', 5, NULL),
        ('Capacitor de Energia', 'Objeto pequeno. Tomo diz que ele pode armazenar energia sem magia. Isso pode ser útil para qualquer pessoa.', 'Item', 4500, 'Tecnologia', 5, NULL),
        ('Solo Fértil', 'Um solo muito rico que, se transportado corretamente, pode levar a uma planta substancialmente mais saudável do que o solo padrão.', 'Item', 1000, 'Floresta', 5, NULL),
        ('Fertilizante', 'Um fertilizante forte que pode levar a um crescimento maior do que a média das plantas.', 'Item', 1000, 'Floresta', 5, NULL),
        ('Condutor de Fluido', 'Um conduíte para o transporte de fluido, provavelmente lava. Parece projetado para minimizar qualquer perda de calor durante o transporte.', 'Item', 3650, 'Deserto', 5, NULL),
        ('Recipiente para Fluidos', 'Desenhos tão ornamentados para algo que parece tão básico. É simplesmente um recipiente destinado a misturar vários fluidos e substâncias.', 'Item', 1550, 'Floresta', 5, NULL),
        ('Observações sobre a Energia de Fluxo', 'Criada por meio de compressão de magia, esta é a maior conquista de nosso tempo - Energia de Fluxo. Para servir tanto como protetor quanto como fonte de energia.', 'Item', 40000, 'Tecnologia', 5, NULL),
        ('Frutas da Floresta', 'Várias frutas colhidas na Masmorra da Floresta... Algumas foram comprovadas como seguras para consumo. Outras... não.', 'Item', 1800, 'Floresta', 5, NULL),
        ('História da Floresta I', 'Éramos uma espécie inteligente. Portanto, quando a escassez de alimentos aumentou, acreditamos que poderíamos resolver nosso problema com a ciência...', 'Livro', 5000, 'Floresta', 5, NULL),
        ('História da Floresta II', 'Criamos o LF1 e, por algum tempo, as coisas foram boas. A comida voltou a ser abundante e as florestas começaram a aparecer pela primeira vez em séculos!', 'Livro', 5000, 'Floresta', 5, NULL),
        ('História da Floresta III', 'No entanto, a floresta não parou de crescer... e, aos poucos, nosso mundo foi coberto. As plantas não pararam de crescer... e lentamente... elas tomaram conta.', 'Livro', 5000, 'Floresta', 5, NULL),
        ('Lentes de Vidro', 'Vidro moldado em uma lente com o único propósito de focalizar a energia mágica. Muito útil na fabricação de armas mágicas.', 'Item', 100, 'Golem', 5, NULL),
        ('Runas de Ouro', 'Essas Runas de Ouro criam padrões maravilhosos nos Golems. Ocasionalmente, você pode recuperar uma intacta após a batalha.', 'Item', 300, 'Golem', 5, NULL),
        ('Núcleo de Golem', 'O núcleo do próprio “coração” de um Golem. Encontramos maneiras de aproveitar a energia, mas não conseguimos criar vida a partir dela.', 'Item', 100, 'Golem', 5, NULL),
        ('Design de Golem I', 'Essas imagens e anotações escritas às pressas parecem se assemelhar a um esquema de algum tipo. Algo parecido com o Golem que perambula pela Masmorra do Golem.', 'Livro', 1500, 'Golem', 5, NULL),
        ('Design de Golem II', 'Assim como nós viemos da terra, a pedra também veio. Aproveitando a energia vital que flui pelo solo, animamos a pedra para nos servir.', 'Livro', 2500, 'Golem', 1, NULL),
        ('Design de Golem III', 'Finalmente, imagens sobre a inserção de uma fonte de energia em um Golem. O mais frustrante, porém, é que a parte sobre a fusão da fonte de energia está riscada...', 'Livro', 1500, 'Golem', 5, NULL),
        ('História do Golem I', 'Todos nós viemos da sujeira. A própria vida é sujeira. Um ciclo de nascimento e decadência. Algo de que nenhum homem, mulher ou mesmo pedra pode escapar.', 'Livro', 2500, 'Golem', 1, NULL),
        ('História do Golem II', 'Assim como nós viemos da terra, a pedra também veio. Aproveitando a energia vital que flui pelo solo, animamos a pedra para nos servir.', 'Livro', 2500, 'Golem', 1, NULL),
        ('História do Golem III', 'A pedra se ergueu para nos ajudar, para nos proteger. Enquanto nossas mãos criavam a vida deles, as mãos deles embalavam a nossa.', 'Livro', 2500, 'Golem', 1, NULL),
        ('Cristal de Energia do Rei Golem', 'Um cristal enorme com energia suficiente para alimentar o enorme Rei Golem...', 'Item', 2500, 'Golem', 5, NULL),
        ('Anotações do Rei Golem', 'O rei da pedra. Imbuída do maior cristal de energia encontrado, essa entidade servirá para nos proteger de qualquer pessoa que nos queira mal.', 'Livro', 2500, 'Golem', 5, NULL),
        ('Livro sobre Golem', 'O texto está muito desgastado, muito desbotado para ser legível. Mas os entalhes na capa de pedra são meticulosamente detalhados.', 'Item', 400, 'Golem', 5, NULL),
        ('Núcleo de Alta Levitação', 'Núcleo grande geralmente preso a grandes pedaços de metal que flutuam sobre a areia diamagnética na Masmorra do deserto. Holay molay essa coisa é cara!', 'Item', 15000, 'Deserto', 5, NULL),
        ('Líquido Inflamável', 'Facilmente inflamável...', 'Item', 4500, 'Deserto', 5, NULL),
        ('Fluído da Vida', 'Um fluido que parece animar e dar vida a plantas comuns. Observação - Mantenha-se afastado da armadilha da mosca de Vênus.', 'Item', 40, 'Floresta', 10, NULL),
        ('Essência de Luz', 'Aparentemente comum quando contido, mas começou a brilhar quando derramado em meu braço. Deve reagir a organismos vivos.', 'Item', 400, 'Floresta', 5, NULL),
        ('Núcleo Magnético', 'Um dispositivo encontrado no centro dos Golems do Deserto, muito semelhante ao encontrado nas estátuas vivas da Masmorra do Golem.', 'Item', 350, 'Deserto', 10, NULL),
        ('Ferramenta Magnética', 'Uma ferramenta usada para criar um campo magnético em torno de um material com a polarização correta.', 'Item', 6500, 'Deserto', 5, NULL),
        ('Mercúrio', 'Metal líquido? Em dias frios, ele parece se solidificar, mas em temperatura ambiente ele simplesmente derrete.', 'Item', 1550, 'Tecnologia', 10, NULL),
        ('Sementes Modificadas', 'Sementes que parecem ter sido modificadas por meio de algum tipo de experimento... Talvez tenham falhado? Elas nunca parecem cultivar nada.', 'Item', 850, 'Floresta', 5, NULL),
        ('Anotações de Naja', 'Em momentos de verdadeira escuridão, surge o verdadeiro terror. Naja, nossa Guardiã feita de pedra, lava e dos três sóis, brilhará mais intensamente.', 'Livro', 15000, 'Deserto', 5, NULL),
        ('Design de um Velho Minion Golem', 'O texto está desbotado, mas parece ser instruções sobre como criar uma das estátuas vivas encontradas na Masmorra do Golem.', 'Livro', 400, 'Golem', 5, NULL),
        ('Pétalas', 'Algumas pétalas de várias plantas nas masmorras que achei particularmente agradáveis aos olhos.', 'Item', 100, 'Floresta', 10, NULL),
        ('Carne Vegetal', 'Alta contagem de fibras nessas plantas. Muito útil para o artesanato.', 'Item', 60, 'Floresta', 10, NULL),
        ('Plástico Filme', 'Uma camada muito fina de "plástico". Encontrei-o enrolado em um monte de fios.', 'Item', 2200, 'Tecnologia', 5, NULL),
        ('Fonte de Energia', 'Um compartimento com formato perfeito para guardar os objetos chamados "baterias".', 'Item', 14550, 'Tecnologia', 5, NULL),
        ('Vidro Resistente', 'Vidro jateado com calor e areia. Usado como isolante para vários objetos contra temperaturas extremas.', 'Item', 4300, 'Deserto', 5, NULL),
        ('Ferro de Solda', 'Uma ferramenta usada para fundir vários metais.', 'Item', 5350, 'Deserto', 5, NULL),
        ('Pó da Velocidade', 'Um pó que pode acelerar o crescimento das plantas. Talvez seja útil em uma poção?', 'Item', 2000, 'Floresta', 5, NULL),
        ('História da Tecnologia I', 'A magia corria desenfreada na terra. Tanto criaturas quanto homens com poderes inimagináveis, obtidos com o lançamento de um dado, aproveitavam-se dos menores...', 'Livro', 40000, 'Tecnologia', 5, NULL),
        ('História da Tecnologia II', 'Foi a divisão entre mágicos e não mágicos que moldou nosso mundo como o conhecemos. Tudo mudou quando a magia foi capturada.', 'Livro', 40000, 'Tecnologia', 5, NULL),
        ('História da Tecnologia III', 'Aproveitada como puro poder, a magia foi disponibilizada a todos que a desejassem. Por meio dessa magia capturada, nossa civilização floresceu.', 'Livro', 40000, 'Tecnologia', 5, NULL),
        ('Motor de Bobina Tesla', 'A eletricidade literalmente salta da bobina. Preciso encontrar uma maneira de transformar isso em uma arma.', 'Item', 5000, 'Tecnologia', 10, NULL),
        ('Tubo de Vácuo', 'Pequeno globo de vidro com alguns galhos de metal em seu interior. Bonito, mas não faço ideia para que serve.', 'Item', 6900, 'Tecnologia', 5, NULL),
        ('Esporos Venenosos', 'O título já diz tudo. Venenoso. Não é divertido. Usado por muitos inimigos na Masmorra da Floresta. Tenha cuidado...', 'Item', 60, 'Floresta', 10, NULL),
        ('Pedra Vulcânica', 'Pedra formada por magma parado em um local por muito tempo. Redonda e muito porosa. Ótima para filtros.', 'Item', 100, 'Deserto', 10, NULL),
        ('Lâmpada de Água', 'Que curioso. Uma lâmpada não de chama, mas de água incandescente. Mais pesada, com certeza, mas mais confiável a longo prazo.', 'Item', 250, 'Golem', 5, NULL),
        ('Hastes de Soldagem', 'Metal em um fio fino. Usado como agente de ligação.', 'Item', 3400, 'Tecnologia', 10, NULL),
        ('Pedra Branca', 'Peça de um recipiente para preservar as propriedades da água infundida.', 'Item', 250, 'Golem', 5, NULL),
        -- ITENS DO TIPO POÇÃO:
        ('Poção do Deserto de Orientação', 'Os vaga-lumes guiarão o usuário até o próximo andar da Masmorra do Deserto.', 'Pocao', 8000, 'Mercador', 5, NULL),
        ('Poção da Floresta de Orientação', 'Os vaga-lumes guiarão o usuário até o próximo andar da Masmorra da Floresta.', 'Pocao', 2500, 'Mercador', 5, NULL),
        ('Poção do Golem de Orientação', 'Os vaga-lumes guiarão o usuário até o próximo andar da Masmorra do Golem.', 'Pocao', 400, 'Mercador', 5, NULL),
        ('Poção da Tecnologia de Orientação', 'Os vaga-lumes guiarão o usuário até o próximo andar da Masmorra da Tecnologia.', 'Pocao', 16000, 'Mercador', 5, NULL),
        ('Poção de Cura I', 'Restaura 40 pontos de vida. Deve-se ter sempre um ou dois desses em mãos.', 'Pocao', 125, 'Mercador', 5, NULL),
        ('Poção de Cura II', 'Restaura 75 pontos de vida. Definitivamente, vale o preço.', 'Pocao', 800, 'Mercador', 5, NULL),
        ('Poção de Cura III', 'Restaura 200 pontos de vida. Teria sido bom ter isso quando encontrei aquela criatura...', 'Pocao', 3000, 'Mercador', 5, NULL),
        ('Poção de Cura IV', 'Restaura 500 pontos de vida. A Bruxa com certeza se superou aqui.', 'Pocao', 8000, 'Mercador', 5, NULL),
        ('Hiper Poção', 'Restaura toda a saúde. Uma poção vital para as masmorras mais difíceis.', 'Pocao', 20520, 'Mercador', 5, NULL),
        ('Cogumelo Mágico', 'Um cogumelo que emite um brilho sutil. O consumo dele concede atributos mágicos aleatórios por algum tempo... Nunca é uma aposta segura, para ser honesto.', 'Pocao', 60, 'Floresta', 10, NULL),
        ('Água Nutritiva', 'Água em redemoinho com nutrientes para o crescimento das plantas. Não para o consumo humano. Zenon não consegue me dizer isso o suficiente...', 'Pocao', 1750, 'Floresta', 5, NULL),
        ('Poção de Revelação do Deserto', 'Revela o mapa da Masmorra do Deserto ao ser usado.', 'Pocao', 16000, 'Mercador', 5, NULL),
        ('Poção de Revelação da Floresta', 'Revela o mapa da Masmorra da Floresta ao ser usado.', 'Pocao', 5000, 'Mercador', 5, NULL),
        ('Poção de Revelação do Golem', 'Revela o mapa da Masmorra do Golem ao ser usado.', 'Pocao', 800, 'Mercador', 5, NULL),
        ('Poção de Revelação da Tecnologia', 'Revela o mapa da Masmorra da Tecnologia ao ser usado.', 'Pocao', 32000, 'Mercador', 5, NULL),
        -- ITENS DO TIPO ARMA:
        ('Espada Grande Blaze', 'Provoca Queimadura. Deve ser a combinação de lava infundida diretamente no metal.', 'Arma', 285000, 'Tecnologia', 1, NULL),
        ('Lança de Vassoura', 'Uma ferramenta com uma finalidade simples. Limpar. Pelo menos, se estiver em mãos não treinadas.', 'Arma', 53, 'Mercador', 1, NULL),
        ('Espada Grande Buster', 'Essa espada grande é o resultado de incontáveis horas de polimento da lâmina usando as rochas e a água exclusivas da Masmorra do Golem.', 'Arma', 4000, 'Golem', 1, NULL),
        ('Monopla de Capitão', 'Ligas metálicas especiais e um processo de fundição experimental tornam essas Monopla mais resistentes do que a maioria, sem adicionar peso desnecessário.', 'Arma', 275600, 'Tecnologia', 1, NULL),
        ('Arco de Catapulta', 'Pode atordoar. Quero dizer... Essa coisa composta de recursos aleatórios da Masmorra do Golem é essencialmente uma pedra de fragmentação.', 'Arma', 4000, 'Golem', 1, NULL),
        ('Espada Curta do Comandante', 'Fundido a partir da lava da Masmorra do Deserto, ele cria uma espada e um escudo poderosos, no padrão de qualquer comandante que se preze.', 'Arma', 250500, 'Deserto', 1, NULL),
        ('Espada Grande de Treinamento', 'É uma espada grande. Tem uma grande área de ataque, mas não é muito afiada. Basicamente, você está balançando um bastão de metal enorme com ela equipada.', 'Arma', 950, 'Mercador', 1, NULL),
        ('Arco de Treinamento', 'Nada muito especial. Você puxa a flecha para trás e ela solta uma flecha. Os arcos são as únicas armas de longo alcance que podem ser encontradas em Rynoka.', 'Arma', 950, 'Mercador', 1, NULL),
        ('Monopla de Treinamento', 'Incrivelmente leves, incrivelmente rápidas, incrivelmente satisfatórias. No entanto, devido ao seu curto alcance, elas são muito mais arriscadas do que outras armas.', 'Arma', 950, 'Mercador', 1, NULL),
        ('Espada Curta de Treinamento', 'Com a espada na mão e o escudo na outra, essa combinação atinge um equilíbrio perfeito entre ataque e defesa.', 'Arma', 950, 'Mercador', 1, NULL),
        ('Lança de Treinamento', 'A lança é a arma corpo a corpo de maior alcance que se pode empunhar. Fácil de arremessar, mas difícil de dominar.', 'Arma', 950, 'Mercador', 1, NULL),
        ('Monopla de Luta', 'Vamos ser honestos por um momento. Essas são apenas garras gigantes feitas de ferro golem. Tão ferozes quanto rudes.', 'Arma', 4000, 'Golem', 1, NULL),
        ('Lança de Perfuração de Golem', 'Pode atordoar. Destinada à mineração, a ponta da lança foi feita para ser incrivelmente difícil de perfurar a rocha. Esse princípio se aplica à maioria dos inimigos.', 'Arma', 4000, 'Golem', 1, NULL),
        ('Arco do Herói', 'Estranho arco antigo feito de materiais que não podem ser encontrados neste mundo.', 'Arma', 4000, 'Deserto', 1, NULL),
        ('Espada do Herói', 'Espada antiga que se diz ter sido carregada por um herói lendário.', 'Arma', 4000, 'Deserto', 1 , NULL),
        ('Arco de Caçador', 'A madeira e o metal da cultura Golem se fundem harmoniosamente para criar um arco bem equilibrado.', 'Arma', 4000, 'Floresta', 1, NULL),
        ('Espada Grande de Pedra', 'Pode atordoar. Realmente, eles decidiram jogar fora a ideia de cortar uma espada com essa. Projetada para simplesmente esmagar seus inimigos.', 'Arma', 4000, 'Floresta', 1, NULL),
        ('Monopla Rústica', 'Pode atordoar. Não se trata tanto de luvas, mas de pequenas pedras grosseiramente presas às suas mãos.', 'Arma', 4000, 'Floresta', 1, NULL),
        ('Espada Curta Enferrujada', 'Pode atordoar. Por que cortar quando você pode bater. Pelo menos.... esse é o pensamento com este.', 'Arma', 4000, 'Floresta', 1, NULL),
        ('Espada Curta de Soldado', 'Os melhores materiais da Masmorra do Golem são polidos ao máximo.', 'Arma', 4000, 'Golem', 1, NULL),
        ('Lança do Guerreiro', 'Uma lança poderosa construída com a força necessária para moldar Golems.', 'Arma', 4000, 'Floresta', 1, NULL),
        ('Monopla dos Espíritos da Floresta', 'Videiras cobertas de espinhos enroladas na mão para simbolizar a morte simples que a própria natureza pode proporcionar.', 'Arma', 65500, 'Floresta', 1, NULL),
        ('Arco do Herói II', 'Estranho arco antigo feito de materiais que não podem ser encontrados neste mundo.', 'Arma', 65500, 'Deserto', 1, NULL),
        ('Espada do Herói II', 'Espada antiga que se diz ter sido carregada por um herói lendário.', 'Arma', 65500, 'Deserto', 1, NULL),
        ('Espada Curta de Cavaleiro', 'Os metais superiores da Masmorra do Golem se fundem com a madeira requintada da Masmorra da Floresta para criar essa peça elaborada de equipamento.', 'Arma', 65500, 'Floresta', 1, NULL),
        ('Arco Natural', 'Os recursos baseados em fibras da Masmorra da Floresta se unem aqui para criar um arco extremamente leve, porém potente.', 'Arma', 65500, 'Floresta', 1, NULL),
        ('Arco Venenoso', 'Venenos. Ao acertar uma flecha, ela se torna envenenada pela corda venenosa do arco. Requer cuidados especiais ao ser usada.', 'Arma', 65500, 'Deserto', 1, NULL),
        ('Espada Grande Venenoso', 'Venenos. Forjado com a injeção dos fluidos envenenados da Masmorra da Floresta diretamente na madeira.', 'Arma', 65500, 'Deserto', 1, NULL),
        ('Espada Curta Venenosa', 'Venenos. Do punho, o veneno se infiltra na lâmina para infligir dor duradoura aos inimigos.', 'Arma', 65500, 'Deserto', 1, NULL),
        ('Lança com Ferrão de Veneno', 'Venenos. Uma simples lança de madeira, mas o veneno que passa pela haste até a ponta da lança deixará qualquer um com dor.', 'Arma', 65500, 'Deserto', 1, NULL),
        ('Monopla Gêmeas Venenosas', 'Venenos. Pequenos sacos de veneno que residem dentro das luvas injetam uma pequena dose de veneno diretamente em seus inimigos.', 'Arma', 65500, 'Deserto', 1, NULL),
        ('Espada Grande Selvagem', 'Lembro-me de comparar aquela espada de treinamento a um taco de beisebol... essa é realmente um taco de beisebol gigante.', 'Arma', 65500, 'Deserto', 1, NULL),
        ('Lança de Madeira', 'Construído de forma robusta, mas incrivelmente flexível. Lindamente trabalhado com madeira encontrada na Masmorra da floresta.', 'Arma', 65500, 'Floresta', 1, NULL),
        ('Monopla Flamejante', 'Provoca Queimadura. Os núcleos magnéticos incorporados a essas luvas mantêm a lava fluindo constantemente, mesmo durante os socos.', 'Arma', 265800, 'Tecnologia', 1, NULL),
        ('Monopla Tempestuosa', ' Cada golpe dessas luvas proporciona um choque elétrico de alta potência projetado a partir de várias partes da cultura tecnológica.', 'Arma', 500000, 'Tecnologia', 1, NULL),
        ('Arco Lança-Chamas', 'Provoca Queimadura. A lava que flui pelo núcleo do arco superaquece as flechas, incendiando-as.', 'Arma', 265800, 'Tecnologia', 1, NULL),
        ('Arco Tempestuoso', 'Provoca Choque. Um arco protótipo altamente não testado que utiliza os materiais mais recentes da Masmorra da Tecnologia.', 'Arma', 265800, 'Tecnologia', 1, NULL),
        ('Lança Infernal', 'Provoca Queimadura. Os três sóis do deserto refletem na haste dessa lança, direcionando altas temperaturas para a cabeça da lança.', 'Arma', 265800, 'Tecnologia', 1, NULL),
        ('Arco do Herói III', 'Estranho arco antigo feito de materiais que não podem ser encontrados neste mundo.', 'Arma', 265800, 'Deserto', 1, NULL),
        ('Arco do Herói IV', 'Estranho arco antigo feito de materiais que não podem ser encontrados neste mundo.', 'Arma', 500000, 'Deserto', 1, NULL),
        ('Arco de Exeter', 'Devido à durabilidade dos materiais usados e à alta produção de danos, essa notável arma se assemelha mais a um rifle de alta potência do que a um arco.', 'Arma', 500000, 'Tecnologia', 1, NULL),
        ('Espada do Herói III', 'Espada antiga que se diz ter sido carregada por um herói lendário.', 'Arma', 265800, 'Deserto', 1, NULL),
        ('Lança do Macaco', 'A história do Rei Macaco vem à mente quando se olha para essa lança carmesim. Verdadeiramente uma lança digna dele.', 'Arma', 265800, 'Tecnologia', 1, NULL),
        ('Espada Curta Reborn', 'Provoca Queimadura. As chamas da forja nunca deixaram essa espada, o calor do deserto ainda irradia da lâmina.', 'Arma', 265800, 'Tecnologia', 1, NULL),
        ('Arco do Soldado', 'Criado de forma rudimentar com as fibras limitadas da Cultura do Deserto, esse arco fica melhor nas mãos de um soldado. De qualquer forma, ele dá conta do recado.', 'Arma', 265800, 'Tecnologia', 1, NULL),
        ('Espada Grande Vulcânica', 'Uma das mais pesadas de Rynoka. Forjada em Aço do Deserto, é uma máquina de destruição imparável.', 'Arma', 265800, 'Deserto', 1, NULL),
        ('Espada Grande Tempestuosa', 'Eletrocuta. A madeira que compõe o cabo é projetada especificamente para proteger o usuário de qualquer eletrocussão indesejada.', 'Arma', 500000, 'Tecnologia', 1, NULL),
        -- ITENS DO TIPO ARMADURA:
        ('Bandana de Tecido', 'Essa bandana semi-ordinária é tecida com as fibras mais resistentes para ajudar a proteger o usuário.', 'Armadura', 4000, 'Mercador', 1, NULL),
        ('Bandana de Tecido II', 'Essa bandana semi-ordinária é tecida com as fibras mais resistentes para ajudar a proteger o usuário.', 'Armadura', 39000, 'Mercador', 1, NULL),
        ('Bandana de Tecido III', 'Essa bandana semi-ordinária é tecida com as fibras mais resistentes para ajudar a proteger o usuário.', 'Armadura', 90500, 'Mercador', 1, NULL),
        ('Bandana de Tecido IV', 'Essa bandana semi-ordinária é tecida com as fibras mais resistentes para ajudar a proteger o usuário.', 'Armadura', 200000, 'Mercador', 1, NULL),
        ('Botas de Tecido', 'Botas feitas de tecido resistente. Perfeitas para viajantes, mas não são as melhores para proteger os pés de ataques inimigos.', 'Armadura' , 4000, 'Mercador', 1, NULL),
        ('Peitoral de Tecido', 'O tecido resistente dessa túnica é durável e, ao mesmo tempo, leve.', 'Armadura', 4000, 'Mercador', 1, NULL),
        ('Botas de Ferro', 'Originalmente produzido em massa para soldados do Grande Exército, mas funciona igualmente bem para qualquer pessoa que esteja mergulhando na masmorra.', 'Armadura', 4000, 'Mercador', 1, NULL),
        ('Peitoral de Ferro', 'Armadura básica mais comumente usada por mercadores. Bastante leve, com resistência e mobilidade decentes.', 'Armadura', 4000, 'Mercador', 1, NULL),
        ('Capacete de Ferro', 'Chapelaria feita com os metais mais leves disponíveis. É uma troca entre armadura e agilidade.', 'Armadura', 4000, 'Mercador', 1, NULL),
        ('Botas de Aço', 'Oferecem uma proteção retumbante. O que é bom, porque ninguém vai se esquivar de musgo com tanto metal preso aos pés.', 'Armadura', 4000, 'Mercador', 1, NULL),
        ('Peitoral de Aço', 'A placa peitoral oferece a melhor proteção contra inimigos. No entanto, é incrivelmente pesado. Basicamente, é um pedaço de aço preso ao peito.', 'Armadura', 4000, 'Mercador', 1, NULL),
        ('Capacete de Aço', 'Camadas dos metais mais pesados e espessos criados em um capacete robusto, resistente e redutor de danos.', 'Armadura', 4000, 'Mercador', 1, NULL),
        ('Botas de Tecido II', 'Botas feitas de tecido resistente. Perfeitas para viajantes, mas não são as melhores para proteger os pés de ataques inimigos.', 'Armadura', 39000, 'Mercador', 1, NULL),
        ('Botas de Tecido III', 'Botas feitas de tecido resistente. Perfeitas para viajantes, mas não são as melhores para proteger os pés de ataques inimigos.', 'Armadura', 90500, 'Mercador', 1, NULL),
        ('Botas de Tecido IV', 'Botas feitas de tecido resistente. Perfeitas para viajantes, mas não são as melhores para proteger os pés de ataques inimigos.', 'Armadura', 200000, 'Mercador', 1, NULL),
        ('Peitoral de Tecido II', 'O tecido resistente dessa túnica é durável e, ao mesmo tempo, leve.', 'Armadura', 39000, 'Mercador', 1, NULL),
        ('Botas de Ferro II', 'Originalmente produzido em massa para soldados do Grande Exército, mas funciona igualmente bem para qualquer pessoa que esteja mergulhando na masmorra.', 'Armadura', 44500, 'Mercador', 1, NULL),
        ('Peitoral de Ferro II', 'Armadura básica mais comumente usada por mercadores. Bastante leve, com resistência e mobilidade decentes.', 'Armadura', 44500, 'Mercador', 1, NULL),
        ('Capacete de Ferro II', 'Chapelaria feita com os metais mais leves disponíveis. É uma troca entre armadura e agilidade.', 'Armadura', 44500, 'Mercador', 1, NULL),
        ('Botas de Aço II', 'Oferecem uma proteção retumbante. O que é bom, porque ninguém vai se esquivar de musgo com tanto metal preso aos pés.', 'Armadura', 44500, 'Mercador', 1, NULL),
        ('Peitoral de Aço II', 'A placa peitoral oferece a melhor proteção contra inimigos. No entanto, é incrivelmente pesado. Basicamente, é um pedaço de aço preso ao peito.', 'Armadura', 44500, 'Mercador', 1, NULL),
        ('Capacete de Aço II', 'Camadas dos metais mais pesados e espessos criados em um capacete robusto, resistente e redutor de danos.', 'Armadura', 44500, 'Mercador', 1, NULL),
        ('Peitoral de Tecido III', 'O tecido resistente dessa túnica é durável e, ao mesmo tempo, leve.', 'Armadura', 90500, 'Mercador', 1, NULL),
        ('Peitoral de Tecido IV', 'O tecido resistente dessa túnica é durável e, ao mesmo tempo, leve.', 'Armadura', 200000, 'Mercador', 1, NULL),
        ('Botas de Ferro III', 'Originalmente produzido em massa para soldados do Grande Exército, mas funciona igualmente bem para qualquer pessoa que esteja mergulhando na masmorra.', 'Armadura', 90000, 'Mercador', 1, NULL),
        ('Botas de Ferro IV', 'Originalmente produzido em massa para soldados do Grande Exército, mas funciona igualmente bem para qualquer pessoa que esteja mergulhando na masmorra.', 'Armadura', 200000, 'Mercador', 1, NULL),
        ('Peitoral de Ferro III', 'Armadura básica mais comumente usada por mercadores. Bastante leve, com resistência e mobilidade decentes.', 'Armadura', 90000, 'Mercador', 1, NULL),
        ('Peitoral de Ferro IV', 'Armadura básica mais comumente usada por mercadores. Bastante leve, com resistência e mobilidade decentes.', 'Armadura', 200000, 'Mercador', 1, NULL),
        ('Capacete de Ferro III', 'Chapelaria feita com os metais mais leves disponíveis. É uma troca entre armadura e agilidade.', 'Armadura', 90500, 'Mercador', 1, NULL),
        ('Capacete de Ferro IV', 'Chapelaria feita com os metais mais leves disponíveis. É uma troca entre armadura e agilidade.', 'Armadura', 200000, 'Mercador', 1, NULL),
        ('Botas de Aço III', 'Oferecem uma proteção retumbante. O que é bom, porque ninguém vai se esquivar de musgo com tanto metal preso aos pés.', 'Armadura', 90000, 'Mercador', 1, NULL),
        ('Botas de Aço IV', 'Oferecem uma proteção retumbante. O que é bom, porque ninguém vai se esquivar de musgo com tanto metal preso aos pés.', 'Armadura', 200000, 'Mercador', 1, NULL),
        ('Peitoral de Aço III', 'A placa peitoral oferece a melhor proteção contra inimigos. No entanto, é incrivelmente pesado. Basicamente, é um pedaço de aço preso ao peito.', 'Armadura', 90000, 'Mercador', 1, NULL),
        ('Peitoral de Aço IV', 'A placa peitoral oferece a melhor proteção contra inimigos. No entanto, é incrivelmente pesado. Basicamente, é um pedaço de aço preso ao peito.', 'Armadura', 200000, 'Mercador', 1, NULL),
        ('Capacete de Aço III', 'Camadas dos metais mais pesados e espessos criados em um capacete robusto, resistente e redutor de danos.', 'Armadura', 90000, 'Mercador', 1, NULL),
        ('Capacete de Aço IV', 'Camadas dos metais mais pesados e espessos criados em um capacete robusto, resistente e redutor de danos.', 'Armadura', 200000, 'Mercador', 1, NULL);
    ```

??? info "_receita_ INSERT"

    ```Postgres
    -- INSERÇÃO NA TABELA RECEITA
        INSERT INTO "receita"
        ("idItemFabricado", "idItemFabricador", "quantidade")
        VALUES
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada do Herói'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Quebrada'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada do Herói'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Ferramenta Rúnica'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada do Herói'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Aço Endurecido'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada do Herói II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Espada do Herói'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada do Herói II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Antiga'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada do Herói II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bulbo Antigo'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada do Herói III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Espada do Herói II'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada do Herói III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Lingote de Aço do Deserto'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada do Herói III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Motor Termomagnético'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande de Treinamento'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Quebrada'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande de Treinamento'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Dente'), 10),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande de Treinamento'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Cipó'), 15),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Buster'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande de Treinamento'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Buster'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Aço Endurecido'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Buster'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Ferramenta Rúnica'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Selvagem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Buster'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Selvagem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Antiga'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Selvagem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bulbo Antigo'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Vulcânica'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Selvagem'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Vulcânica'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Lingote de Aço do Deserto'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Vulcânica'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Motor Termomagnético'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande de Pedra'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande de Treinamento'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande de Pedra'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Amolar'), 10),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande de Pedra'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Cinzel de Golem'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Venenoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande de Pedra'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Venenoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Antiga'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Venenoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Ácido Puro'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Blaze'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Venenoso'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Blaze'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Joia de Fogo'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Blaze'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Motor Termomagnético'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Tempestuosa'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Blaze'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Tempestuosa'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bateria de Célula Tripla'), 2), 
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Grande Tempestuosa'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Metal Condutor'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Tecido'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Esfera de Água'), 2), 
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Restos de Fundição'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Palha'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Mágica'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido II'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Corda do Deserto'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Tecido à Prova de Fogo'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido III'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Tratada'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Bandana de Tecido IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Fios'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Tecido'), 6),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Esfera de Água'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Restos de Fundição'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Palha'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Mágica'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido II'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Corda do Deserto'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Tecido à Prova de Fogo'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido III'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Tratada'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Tecido IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Fios'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Tecido'), 10),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Esfera de Água'), 6),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Restos de Fundição'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Palha'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Mágica'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido II'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Corda do Deserto'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Tecido à Prova de Fogo'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido III'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Tratada'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Tecido IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Fios'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Tecido'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Aço Endurecido'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Ferramenta Rúnica'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Antiga'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bulbo Antigo'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói II'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Lingote de Aço do Deserto'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Motor Termomagnético'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói III'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bobina de Cobre'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Herói IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pistola de Solda'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Barra de Ferro'), 6),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Dente'), 14),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Restos de Fundição'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Folhas Fortes'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Raiz Preservada'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro II'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Magnetita'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pó Isolante'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro III'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Wolfram'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Ferro IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Fios de Ouro'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Barra de Ferro'), 6),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Dente'), 14),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Restos de Fundição'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Folhas Fortes'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Raiz Preservada'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro II'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Magnetita'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pó Isolante'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro III'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Wolfram'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Ferro IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Fios de Ouro'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Barra de Ferro'), 6),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Dente'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Restos de Fundição'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Folhas Fortes'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Raiz Preservada'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro II'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Magnetita'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pó Isolante'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro III'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Wolfram'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Ferro IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Fios de Ouro'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Aço Endurecido'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Barra de Ferro'), 12),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Restos de Fundição'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Antiga'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Mágica'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço II'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Lingote de Aço do Deserto'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pó Inflamável'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço III'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Wolfram'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Botas de Aço IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bobina de Cobre'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Aço Endurecido'), 8),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Barra de Ferro'), 14),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Restos de Fundição'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Antiga'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Mágica'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço II'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Lingote de Aço do Deserto'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pó Inflamável'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço III'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Wolfram'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Peitoral de Aço IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bobina de Cobre'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Aço Endurecido'), 6),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Barra de Ferro'), 12),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Restos de Fundição'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Antiga'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço II'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Mágica'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço II'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Lingote de Aço do Deserto'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço III'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pó Inflamável'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço III'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Wolfram'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Capacete de Aço IV'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bobina de Cobre'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Treinamento'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Restos de Fundição'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Treinamento'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Barra de Ferro'), 6),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Treinamento'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Raiz'), 10),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Catapulta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Treinamento'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Catapulta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Amolar'), 10),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Catapulta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Cinzel de Golem'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Venenoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Catapulta'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Venenoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Antiga'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Venenoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Ácido Puro'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Lança-Chamas'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Venenoso'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Lança-Chamas'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Joia de Fogo'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Lança-Chamas'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Motor Termomagnético'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Tempestuoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Lança-Chamas'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Tempestuoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bateria de Célula Tripla'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Tempestuoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Metal Condutor'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Caçador'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Treinamento'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Caçador'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Aço Endurecido'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Caçador'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Ferramenta Rúnica'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Natural'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Caçador'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Natural'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Antiga'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Natural'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bulbo Antigo'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Soldado'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Arco Natural'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Soldado'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Lingote de Aço do Deserto'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Soldado'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Motor Termomagnético'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Exeter'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Arco do Soldado'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Exeter'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bobina de Cobre'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Arco de Exeter'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pistola de Solda'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla de Treinamento'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Dente'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla de Treinamento'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Barra de Ferro'), 6),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla de Treinamento'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Restos de Fundição'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla de Luta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla de Treinamento'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla de Luta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Aço Endurecido'), 5),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla de Luta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Ferramenta Rúnica'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla dos Espíritos da Floresta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla de Luta'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla dos Espíritos da Floresta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Antiga'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla dos Espíritos da Floresta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bulbo Antigo'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla de Capitão'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla dos Espíritos da Floresta'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla de Capitão'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Lingote de Aço do Deserto'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla de Capitão'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Motor Termomagnético'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Rústica'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla de Treinamento'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Rústica'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Amolar'), 10),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Rústica'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Cinzel de Golem'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Gêmeas Venenosas'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Rústica'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Gêmeas Venenosas'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Antiga'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Gêmeas Venenosas'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Ácido Puro'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Flamejante'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Gêmeas Venenosas'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Flamejante'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Joia de Fogo'), 4),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Flamejante'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Motor Termomagnético'), 3),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Tempestuosa'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Flamejante'), 1),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Tempestuosa'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bateria de Célula Tripla'), 2),
        ((SELECT "idItem" FROM "item" WHERE "nome" = 'Monopla Tempestuosa'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Metal Condutor'), 4);
    ```
??? info "_monstro_item_ INSERT"

    ```Postgres
    -- INSERÇÃO DOS DROPS DE MONSTROS
    INSERT INTO "monstro_item" 
        ("idMonstro", "idItem", "chanceDrop", "qtdMinima", "qtdMaxima")
        VALUES
        -- ### Masmorra do Golem ###

        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Baby Slime'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Geléia Rica'), 0.6, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Baby Slime'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Tecido'), 0.1, 1, 1),
        -- Torre Golem Quebrada / Torre Golem (Masmorra do Golem)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Torre Golem Quebrada'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Núcleo de Golem'), 0.25, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Torre Golem Quebrada'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Restos de Fundição'), 0.15, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Torre Golem Quebrada'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Barra de Ferro'), 0.1, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Torre Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Núcleo de Golem'), 0.3, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Torre Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Lentes de Vidro'), 0.15, 1, 1),
        -- Guerreiro Golem Corrompido / Guerreiro Golem / Soldado de Pedra (Masmorra do Golem)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Guerreiro Golem Corrompido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Espada Quebrada'), 0.2, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Guerreiro Golem Corrompido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Barra de Ferro'), 0.25, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Guerreiro Golem Corrompido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Dente'), 0.15, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Guerreiro Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Aço Endurecido'), 0.1, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Guerreiro Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Runas de Ouro'), 0.05, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Soldado de Pedra'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Cinzel de Golem'), 0.1, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Soldado de Pedra'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Amolar'), 0.2, 1, 1),
        -- Golem Voador / Golem Reparador Voador (Masmorra do Golem)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Golem Voador'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Núcleo de Golem'), 0.2, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Golem Voador'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Restos de Fundição'), 0.05, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Golem Reparador Voador'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Núcleo de Golem'), 0.25, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Golem Reparador Voador'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Ferramenta Rúnica'), 0.02, 1, 1),
        -- Mimicos (Masmorra do Golem)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mimico Dourado' AND "nomeLocal" = 'Masmorra do Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Runas de Ouro'), 0.5, 1, 3),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mimico Dourado' AND "nomeLocal" = 'Masmorra do Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Rocha de Cristal'), 0.3, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mimico de Ferro' AND "nomeLocal" = 'Masmorra do Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Barra de Ferro'), 0.8, 2, 5),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mimico de Madeira' AND "nomeLocal" = 'Masmorra do Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Mágica'), 0.8, 2, 4),
        -- Cabeça de Golem (Masmorra do Golem)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Cabeça de Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Núcleo de Golem'), 0.15, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Cabeça de Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Dente'), 0.2, 1, 2),
        -- Slime (Grande) (Masmorra do Golem)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Slime' AND "nomeLocal" = 'Masmorra do Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Geléia Rica'), 0.8, 2, 4),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Slime' AND "nomeLocal" = 'Masmorra do Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Esfera de Água'), 0.1, 1, 1),
        -- Manopla de Slime (Masmorra do Golem)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Manopla de Slime'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Geléia Rica'), 0.5, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Manopla de Slime'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Barra de Ferro'), 0.2, 1, 1),
        -- Mordomo de Pedra (Masmorra do Golem)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mordomo de Pedra'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Tecido'), 0.25, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mordomo de Pedra'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Lâmpada de Água'), 0.1, 1, 1),
        -- Tangle (Masmorra do Golem)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Tangle' AND "nomeLocal" = 'Masmorra do Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Cipó'), 0.7, 1, 3),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Tangle' AND "nomeLocal" = 'Masmorra do Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Raiz'), 0.2, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Rei Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Cristal de Energia do Rei Golem'), 1.0, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Rei Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Anotações do Rei Golem'), 1.0, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Rei Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Energia Cristalizada'), 0.5, 2, 5),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Rei Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Design de Golem II'), 0.3, 1, 1),
        -- Errante (Masmorra do Golem)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Errante' AND "nomeLocal" = 'Masmorra do Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Ferramenta Rúnica'), 0.3, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Errante' AND "nomeLocal" = 'Masmorra do Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Rocha de Cristal'), 0.5, 3, 5),
        -- ### Masmorra da Floresta ###

        -- Baby Slime Venenoso (Masmorra da Floresta)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Baby Slime Venenoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Geléia de Veneno'), 0.6, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Baby Slime Venenoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Ácido Puro'), 0.1, 1, 1),
        -- Árvore Lâmina (Masmorra da Floresta)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Árvore Lâmina'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Folhas de Lâminas'), 0.5, 1, 3),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Árvore Lâmina'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Mágica'), 0.2, 1, 1),
        -- Árvore Mavu Corrompida / Árvore Mavu (Masmorra da Floresta)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Árvore Mavu Corrompida'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Antiga'), 0.25, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Árvore Mavu Corrompida'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Esporos Venenosos'), 0.3, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Árvore Mavu'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Mágica'), 0.3, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Árvore Mavu'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Sementes Modificadas'), 0.1, 1, 1),
        -- Tangle da Floresta / Tangle Venenoso (Masmorra da Floresta)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Tangle da Floresta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Cipó'), 0.5, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Tangle da Floresta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Folhas Fortes'), 0.2, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Tangle Venenoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Cipó'), 0.4, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Tangle Venenoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Esporos Venenosos'), 0.3, 1, 1),
        -- Torre de Fruta / Semeador (Masmorra da Floresta)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Torre de Fruta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Frutas da Floresta'), 0.6, 1, 3),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Torre de Fruta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Mágica'), 0.15, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Semeador'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Sementes Modificadas'), 0.4, 1, 2),
        -- Mimicos (Masmorra da Floresta)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mimico Dourado' AND "nomeLocal" = 'Masmorra da Floresta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Antiga'), 0.3, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mimico de Ferro' AND "nomeLocal" = 'Masmorra da Floresta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Barra de Ferro'), 0.8, 1, 3),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mimico de Madeira' AND "nomeLocal" = 'Masmorra da Floresta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Mágica'), 0.8, 2, 4),
        -- Jardineiro (Masmorra da Floresta)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Jardineiro'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pétalas'), 0.3, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Jardineiro'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Solo Fértil'), 0.1, 1, 1),
        -- Slime Venenoso (Grande) (Masmorra da Floresta)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Slime Venenoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Geléia de Veneno'), 0.8, 2, 4),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Slime Venenoso'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Ácido Puro'), 0.25, 1, 1),
        -- Cogumelo Giratório (Masmorra da Floresta)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Cogumelo Giratório'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Cogumelo Mágico'), 0.4, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Cogumelo Giratório'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Esporos Venenosos'), 0.2, 1, 1),
        -- Arbusto de Esporos (Masmorra da Floresta)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Arbusto de Esporos'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Esporos Venenosos'), 0.7, 1, 3),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Arbusto de Esporos'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Carne Vegetal'), 0.2, 1, 1),
        -- Árvore do Vento (Masmorra da Floresta)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Árvore do Vento'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Folhas Fortes'), 0.5, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Árvore do Vento'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Mágica'), 0.15, 1, 1),
        -- Mutae Carnívora (CHEFE - Masmorra da Floresta)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mutae Carnívora'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Sementes de Mutae Carnívora'), 1.0, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mutae Carnívora'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Observações sobre Mutae Carnívora'), 1.0, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mutae Carnívora'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bulbo Antigo'), 0.5, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mutae Carnívora'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Anotações de Botânica I'), 0.3, 1, 1),
        -- Errante (Masmorra da Floresta)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Errante' AND "nomeLocal" = 'Masmorra da Floresta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bulbo Antigo'), 0.1, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Errante' AND "nomeLocal" = 'Masmorra da Floresta'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Raiz Preservada'), 0.5, 1, 2),
        -- ### Masmorra do Deserto ###

        -- Baby Slime de Fogo (Masmorra do Deserto)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Baby Slime de Fogo'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Geléia de Fogo'), 0.6, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Baby Slime de Fogo'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pó Inflamável'), 0.1, 1, 1),
        -- Fantoche Bardo (Masmorra do Deserto)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Fantoche Bardo'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Corda do Deserto'), 0.3, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Fantoche Bardo'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Tecido à Prova de Fogo'), 0.15, 1, 1),
        -- Tangle de Pano (Masmorra do Deserto)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Tangle de Pano'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Tecido à Prova de Fogo'), 0.5, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Tangle de Pano'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Corda do Deserto'), 0.2, 1, 1),
        -- Hexa Corrompido / Hexa (Masmorra do Deserto)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Hexa Corrompido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Núcleo Magnético'), 0.2, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Hexa Corrompido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Areia Doamantinética'), 0.1, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Hexa'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Núcleo Magnético'), 0.25, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Hexa'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Magnetita'), 0.15, 1, 1),
        -- Fantoche de Fogo / Fantoche Mágico (Masmorra do Deserto)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Fantoche de Fogo'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Joia de Fogo'), 0.3, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Fantoche de Fogo'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Líquido Inflamável'), 0.15, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Fantoche Mágico'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Joia de Fogo'), 0.25, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Fantoche Mágico'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Cristal Capacitador'), 0.1, 1, 1),
        -- Slime de Fogo (Grande) (Masmorra do Deserto)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Slime de Fogo'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Geléia de Fogo'), 0.8, 2, 4),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Slime de Fogo'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra Vulcânica'), 0.2, 1, 2),
        -- Mimicos (Masmorra do Deserto)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mimico Dourado' AND "nomeLocal" = 'Masmorra do Deserto'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Lingote de Aço do Deserto'), 0.2, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mimico de Ferro' AND "nomeLocal" = 'Masmorra do Deserto'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Chapa de Aço do Deserto'), 0.5, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mimico de Madeira' AND "nomeLocal" = 'Masmorra do Deserto'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Tratada'), 0.5, 1, 2),
        -- Golem Katamari / Golem Patrulheiro (Masmorra do Deserto)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Golem Katamari'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Chapa de Aço do Deserto'), 0.3, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Golem Katamari'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra do Deserto'), 0.15, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Golem Patrulheiro'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Aço Endurecido'), 0.25, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Golem Patrulheiro'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Núcleo Magnético'), 0.1, 1, 1),
        -- Catapulta de Lava (Masmorra do Deserto)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Catapulta de Lava'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Lava Resfriada'), 0.4, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Catapulta de Lava'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra Vulcânica'), 0.2, 1, 1),
        -- Golem Mãe (CHEFE - Masmorra do Deserto)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Golem Mãe'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Motor Termomagnético'), 1.0, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Golem Mãe'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Núcleo de Alta Levitação'), 0.3, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Golem Mãe'), (SELECT "idItem" FROM "item" WHERE "nome" = 'História do Deserto I'), 0.5, 1, 1),
        -- Naja (BOSS DAA Masmorra do Deserto)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Naja'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Anotações de Naja'), 1.0, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Naja'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Lingote de Aço do Deserto'), 0.5, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Naja'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Joia de Fogo'), 0.8, 2, 4),
        -- Errante (Masmorra do Deserto)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Errante' AND "nomeLocal" = 'Masmorra do Deserto'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Motor Termomagnético'), 0.2, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Errante' AND "nomeLocal" = 'Masmorra do Deserto'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pó Isolante'), 0.4, 1, 2),
        -- ### Masmorra da Tecnologia ###

        -- Baby Slime Elétrico (Masmorra da Tecnologia)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Baby Slime Elétrico'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Geléia Elétrica'), 0.6, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Baby Slime Elétrico'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Fios'), 0.1, 1, 1),
        -- Oscilador Corrompido / Oscilador (Masmorra da Tecnologia)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Oscilador Corrompido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bateria Quebrada'), 0.3, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Oscilador Corrompido'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Metal Condutor'), 0.15, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Oscilador'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Capacitor de Energia'), 0.25, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Oscilador'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Motor de Bobina Tesla'), 0.1, 1, 1),
        -- Gerador da Morte / Poste Elétrico / Gerador Graaf (Masmorra da Tecnologia)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Gerador da Morte'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Fonte de Energia'), 0.2, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Poste Elétrico'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Fios de Ouro'), 0.15, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Gerador Graaf'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Plástico Filme'), 0.2, 1, 1),
        -- Slime Elétrico (Grande) (Masmorra da Tecnologia)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Slime Elétrico'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Geléia Elétrica'), 0.8, 2, 4),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Slime Elétrico'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bateria de Célula Tripla'), 0.05, 1, 1),
        -- Bola Eletromagnética (Masmorra da Tecnologia)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Bola Eletromagnética'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Mercúrio'), 0.25, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Bola Eletromagnética'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bobina de Cobre'), 0.1, 1, 1),
        -- Lançador Golem (Masmorra da Tecnologia)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Lançador Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Aço Endurecido'), 0.3, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Lançador Golem'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Wolfram'), 0.1, 1, 1),
        -- Mimicos (Masmorra da Tecnologia)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mimico de Ferro' AND "nomeLocal" = 'Masmorra da Tecnologia'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pedra de Wolfram'), 0.3, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Mimico de Madeira' AND "nomeLocal" = 'Masmorra da Tecnologia'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Madeira Tratada'), 0.6, 1, 2),
        -- Recarregador / Drone Reparador (Masmorra da Tecnologia)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Recarregador'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Adapatador AC'), 0.15, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Drone Reparador'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Pistola de Solda'), 0.1, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Drone Reparador'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Hastes de Soldagem'), 0.2, 1, 2),
        -- Redemoinho de Areia / Armadilha de Slime / Corrente de Espinhos (Masmorra da Tecnologia - no jogo, n sao monstros dropaveis, mas da para fazer drops simples tematicos
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Armadilha de Slime'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Geléia Elétrica'), 0.2, 1, 1),
        -- Fluxo de Energia (CHEFE - Masmorra da Tecnologia)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Fluxo de Energia'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Observações sobre a Energia de Fluxo'), 1.0, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Fluxo de Energia'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Bateria de Célula Tripla'), 0.8, 1, 2),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Fluxo de Energia'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Frasco de Argônio'), 0.5, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Fluxo de Energia'), (SELECT "idItem" FROM "item" WHERE "nome" = 'História da Tecnologia I'), 0.3, 1, 1),
        -- Errante (Masmorra da Tecnologia)
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Errante' AND "nomeLocal" = 'Masmorra da Tecnologia'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Adapatador AC'), 0.2, 1, 1),
        ((SELECT "idMonstro" FROM "monstro" WHERE "nome" = 'Errante' AND "nomeLocal" = 'Masmorra da Tecnologia'), (SELECT "idItem" FROM "item" WHERE "nome" = 'Tubo de Vácuo'), 0.3, 1, 1);
    ```
??? info "_npc_ INSERT"

    ```Postgres
    -- INSERÇÃO DOS NPCS
    INSERT INTO "npc" ("nome", "tipoNPC", "descricao", "ativo")
        VALUES
        ('Zenon', 'Guia', 'Sábio ancião que oferece conselhos e conhecimento.', FALSE),
        ('Andrei', 'Ferreiro', 'Ferreiro que aprimora armas e armaduras na Forja Vulcânica.', FALSE),
        ('Eris', 'Alquimista', 'Alquimista que vende e aprimora poções no Chapéu de Madeira.', FALSE),
        ('Edward', 'Banqueiro', 'Banqueiro que gerencia investimentos para a cidade de Rynoka.', FALSE),
        ('Juliette', 'Decoradora', 'Ajuda a melhorar e decorar a loja Moonlighter em "Le Retailer".', FALSE),
        ('Tom', 'Vendedor Ambulante', 'Vendedor ambulante que oferece itens raros e exóticos.', FALSE),
        ('Mercador Viajante', 'Comprador Especializado', 'Compra itens específicos por um preço elevado periodicamente.', FALSE),
        ('Pedro Doidão', 'Residente', 'Residente excêntrico da cidade de Rynoka com dicas peculiares.', FALSE),
        ('Bruxa dos Murmúrios', 'Encantadora', 'Bruxa misteriosa que pode encantar equipamentos com efeitos.', FALSE),
        ('Mundo', 'Mundo', 'Interações relacionadas à narração do mundo', FALSE);
    ```

??? info "_dialogo_ INSERT's"

    ```Postgres
    INSERT INTO "dialogo" ("conteudo", "ordem", "tipo", "idDialogoPai")
        VALUES
        ('Dentre as estrelas da noite, existe uma terra mais velha que a imaginação', 1, 'Tutorial', NULL);
    INSERT INTO "dialogo" ("conteudo", "ordem", "tipo", "idDialogoPai")
        VALUES
        ('Uma noite, labirintos cheios de tesouros extraordinários e criaturas mortais apareceram por lá', 2, 'Tutorial', (SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'Dentre as estrelas da noite, existe uma terra mais velha que a imaginação'));
    INSERT INTO "dialogo" ("conteudo", "ordem", "tipo", "idDialogoPai")
        VALUES
        ('Foram chamados de Masmorras - estranhas, sempre oscilantes ruínas de terras desconhecidas', 3, 'Tutorial', (SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'Uma noite, labirintos cheios de tesouros extraordinários e criaturas mortais apareceram por lá'));
    INSERT INTO "dialogo" ("conteudo", "ordem", "tipo", "idDialogoPai")
        VALUES
        ('Logo, curiosos formaram uma vila próxima a essas masmorras. E a chamaram de Rynoka', 4, 'Tutorial', (SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'Foram chamados de Masmorras - estranhas, sempre oscilantes ruínas de terras desconhecidas'));
    INSERT INTO "dialogo" ("conteudo", "ordem", "tipo", "idDialogoPai")
        VALUES
        ('Entre os moradores, dois grupos se destacaram. Heróis e Mercadores. Glória e Riquezas', 5, 'Tutorial', (SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'Logo, curiosos formaram uma vila próxima a essas masmorras. E a chamaram de Rynoka'));
    INSERT INTO "dialogo" ("conteudo", "ordem", "tipo", "idDialogoPai")
        VALUES
        ('Mas as masmorras se provaram perigosas. E foram fechadas pelas vidas perdidas em suas profundezas', 6, 'Tutorial', (SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'Entre os moradores, dois grupos se destacaram. Heróis e Mercadores. Glória e Riquezas'));
    INSERT INTO "dialogo" ("conteudo", "ordem", "tipo", "idDialogoPai")
        VALUES
        ('A vida se tornou difícil, sobretudo para o jovem dono da loja mais antiga - <NOME_DO_JOGADOR>, da Moonlighter', 7, 'Tutorial', (SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'Mas as masmorras se provaram perigosas. E foram fechadas pelas vidas perdidas em suas profundezas'));
    INSERT INTO "dialogo" ("conteudo", "ordem", "tipo", "idDialogoPai")
        VALUES
        ('Há tanto sonhado em abrir a misteriosa 5ª porta das Masmorras...', 8, 'Tutorial', (SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'A vida se tornou difícil, sobretudo para o jovem dono da loja mais antiga - <NOME_DO_JOGADOR>, da Moonlighter'));
    ```
??? info "_dialogo_npc_ INSERT"

    ```Postgres
    INSERT INTO "dialogo_npc" ("idDialogo", "idNPC")
        VALUES
        ((SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'Dentre as estrelas da noite, existe uma terra mais velha que a imaginação'), (SELECT "idNPC" FROM "npc" WHERE "nome" = 'Mundo')),
        ((SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'Uma noite, labirintos cheios de tesouros extraordinários e criaturas mortais apareceram por lá'), (SELECT "idNPC" FROM "npc" WHERE "nome" = 'Mundo')),
        ((SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'Foram chamados de Masmorras - estranhas, sempre oscilantes ruínas de terras desconhecidas'), (SELECT "idNPC" FROM "npc" WHERE "nome" = 'Mundo')),
        ((SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'Logo, curiosos formaram uma vila próxima a essas masmorras. E a chamaram de Rynoka'), (SELECT "idNPC" FROM "npc" WHERE "nome" = 'Mundo')),
        ((SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'Entre os moradores, dois grupos se destacaram. Heróis e Mercadores. Glória e Riquezas'), (SELECT "idNPC" FROM "npc" WHERE "nome" = 'Mundo')),
        ((SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'Mas as masmorras se provaram perigosas. E foram fechadas pelas vidas perdidas em suas profundezas'), (SELECT "idNPC" FROM "npc" WHERE "nome" = 'Mundo')),
        ((SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'A vida se tornou difícil, sobretudo para o jovem dono da loja mais antiga - <NOME_DO_JOGADOR>, da Moonlighter'), (SELECT "idNPC" FROM "npc" WHERE "nome" = 'Mundo')),
        ((SELECT "idDialogo" FROM "dialogo" WHERE "conteudo" = 'Há tanto sonhado em abrir a misteriosa 5ª porta das Masmorras...'), (SELECT "idNPC" FROM "npc" WHERE "nome" = 'Mundo'));
    ```
??? info "_inventario_ INSERT"

    ```Postgres
    -- INSERÇÃO NA TABELA INVENTÁRIO:
    INSERT INTO "inventario"
        ("nome", "slotMaximo")
        VALUES
        -- Inventários Básicos do Jogador
        ('Mochila', 15),              -- Inventário principal, perde ao morrer
        ('Bolsos', 5),                -- Slots seguros, mantém após morte
        ('Equipamento - Armadura', 1), -- Slot para conjunto de armadura
        ('Equipamento - Arma 1', 1),   -- Slot para arma primária
        ('Equipamento - Arma 2', 1),   -- Slot para arma secundária
        ('Equipamento - Acessório', 3), -- Slots para acessórios
        ('Familiar Mimic', 28);        -- Slots extras do familiar, mantém após morte
    ```

## Versão

| Data       | Versão | Autor(es)        | Mudanças                                               |
| ---------- | ------ | ---------------- | ------------------------------------------------------ |
| 11/06/2025 | `1.0`  | Todos da Equipe  | Criação da Página e Inserção do DML                    |