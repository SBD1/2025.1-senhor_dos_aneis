<span style="background-color:#c5a352; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Versão 1.1</span>

# Dicionário de Dados

## O que é um Dicionário de Dados?

Um Dicionário de Dados é um documento ou repositório central que descreve detalhadamente os elementos de dados utilizados em um sistema ou banco de dados. Ele contém informações sobre cada campo, como nome, tipo de dado, tamanho, formato, restrições, padrão de preenchimento e significado. O objetivo principal do dicionário é padronizar e organizar os dados para que todos os envolvidos no projeto — analistas, desenvolvedores, testadores e usuários — tenham uma compreensão clara e consistente sobre o que cada dado representa e como deve ser tratado.

Além de auxiliar no desenvolvimento e manutenção de sistemas, o dicionário de dados também facilita a comunicação entre as equipes e a documentação do projeto, servindo como uma fonte de referência durante todas as fases do ciclo de vida do software. Ele pode abranger tanto dados estruturados (como tabelas de banco de dados relacionais) quanto dados utilizados em interfaces, relatórios e integrações com outros sistemas.

## Dicionário de Dados do Jogo

!!! Warning "Atenção!"
    O conteúdo deste tópico **poderá sofrer alterações** ao longo da Disciplina de Sistema de Banco de Dados 1. Portanto, as tabelas serão organizadas iniciando pela versão mais recente e finalizando com a versão mais antiga.

O dicionário de dados do Jogo Lord of The Rings apresenta a descrição detalhada dos atributos utilizados nas tabelas do Modelo Relacional. Ele serve como um guia técnico que traduz, de forma objetiva e organizada, as informações presentes na modelagem conceitual e lógica do banco de dados, facilitando o entendimento e a padronização dos dados por parte da equipe de desenvolvimento, análise e demais envolvidos no projeto.

Cada tabela está documentada com seus respectivos campos, tipos de dados, restrições e limites, garantindo transparência na estruturação das informações e contribuindo para a manutenção da integridade e consistência do sistema.

<center>
  <span style="background-color:#1ec68e; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Dicionário de Dados | Versão 1.0</span>
</center>

??? info "Tabela Personagem | 1.0v"
    **Nome da Tabela:** Personagem <br/>
    **Descrição**: Armazena informações detalhadas sobre os personagens do jogo <br/>

    | Atributo       | Descrição                     | Tipo         | Limite | Restrições                  |
    | -------------- | ----------------------------- | ------------ | ------ | --------------------------- |
    | `iD_Personagem`| Identificador do personagem   | Integer      |        | `PK`, `> 0`, `NOT NULL`     |
    | `vida_Maxima`  | Valor máximo de vida          | Integer      |        | `>= 0`, `NOT NULL`          |
    | `mana_Maxima`  | Valor máximo de mana          | Integer      |        | `>= 0`, `NULL ALLOWED`      |
    | `habilidade`   | Nome da habilidade            | Varchar      | 100    | `NULL ALLOWED`              |
    | `hostilidade`  | Indica a hostilidade          | Boolean      |        | `NOT NULL`                  |
    | `level`        | Nível do personagem           | Integer      |        | `>= 1`, `NOT NULL`          |
    | `resistencias` | Resistências do personagem    | Text         |        | `NULL ALLOWED`              |
    | `dialogo`      | Diálogo do personagem         | Text         |        | `NULL ALLOWED`              |

---

??? info "Tabela Jogador | 1.0v"
    **Nome da Tabela:** Jogador <br/>
    **Descrição**: Jogador é um tipo de personagem que pode interagir com o jogo <br/>

    | Atributo           | Descrição                 | Tipo    | Limite | Restrições |
    | ------------------ | ------------------------- | ------- | ------ | ---------- |
    | `ID_Jogador`       | Identificador do jogador  | Integer |        | `NOT NULL` |
    | `tipo_equipamento` | Tipo de equipamento usado | Varchar | 50     |            |
    | `cenario`          | Nome do cenário           | Varchar | 50     | `PF`       |

---

??? info "Tabela Inventário | 1.0v"
    **Nome da Tabela:** Inventário <br/>
    **Descrição**: Armazena os itens que um jogador possui <br/>

    | Atributo        | Descrição                             | Tipo    | Limite | Restrições       |
    | --------------- | ------------------------------------- | ------- | ------ | ---------------- |
    | `ID_inventário` | Identificador do inventário           | Integer |        | `PK`, `NOT NULL` |
    | `id_jogador`    | Jogador ao qual pertence o inventário | Integer |        | `NOT NULL`       |
    | `Pods`          | Capacidade do inventário              | Float   |        | `FK`             |

---

??? info "Tabela Características | 1.0v"
    **Nome da Tabela:** Características <br/>
    **Descrição**: Atributos vinculados ao jogador <br/>

    | Atributo     | Descrição             | Tipo    | Limite | Restrições       |
    | ------------ | --------------------- | ------- | ------ | ---------------- |
    | `ID_Jogador` | Referência ao jogador | Integer |        | `FK`, `NOT NULL` |
    | `fogo`       | Elemento fogo         | Integer |        |                  |
    | `agua`       | Elemento água         | Integer |        |                  |
    | `terra`      | Elemento terra        | Integer |        |                  |
    | `ar`         | Elemento ar           | Integer |        |                  |

---

??? info "Tabela Skill | 1.0v"
    **Nome da Tabela:** Skill <br/>
    **Descrição**: Habilidades de um jogador <br/>

    | Atributo     | Descrição                | Tipo    | Limite | Restrições       |
    | ------------ | ------------------------ | ------- | ------ | ---------------- |
    | `ID_Jogador` | Referência ao jogador    | Integer |        | `FK`, `NOT NULL` |
    | `atq`        | Ataque básico do jogador | Integer |        |                  |

---

??? info "Tabela Mago | 1.0v"
    **Nome da Tabela:** Mago <br/>
    **Descrição**: Especialização de um jogador com poderes mágicos <br/>

    | Atributo           | Descrição               | Tipo    | Limite | Restrições       |
    | ------------------ | ----------------------- | ------- | ------ | ---------------- |
    | `ID_Jogador`       | Referência ao jogador   | Integer |        | `FK`, `NOT NULL` |
    | `atq_Magico`       | Ataques mágicos         | Integer |        | `NOT NULL`       |
    | `atq_MultElemento` | Multiplicador elemental | Boolean |        |                  |

---

??? info "Tabela Guerreiro | 1.0v"
    **Nome da Tabela:** Guerreiro <br/>
    **Descrição**: Classe especializada em combate corpo a corpo <br/>

    | Atributo        | Descrição                   | Tipo    | Limite | Restrições       |
    | --------------- | --------------------------- | ------- | ------ | ---------------- |
    | `ID_Jogador`    | Identificador do guerreiro  | Integer |        | `FK`, `NOT NULL` |
    | `atq_Fisico`    | Força de ataque físico      | Integer |        | `NOT NULL`       |
    | `bloquear_Dano` | Capacidade de bloquear dano | Integer |        |                  |

---

??? info "Tabela Arqueiro | 1.0v"
    **Nome da Tabela:** Arqueiro <br/>
    **Descrição**: Especialização de um jogador com foco em ataques à distância <br/>

    | Atributo      | Descrição              | Tipo    | Limite | Restrições       |
    | ------------- | ---------------------- | ------- | ------ | ---------------- |
    | `ID_Jogador`  | Referência ao jogador  | Integer |        | `FK`, `NOT NULL` |
    | `atq_Preciso` | Precisão dos ataques   | Integer |        |                  |
    | `atq_Rapido`  | Velocidade dos ataques | Integer |        |                  |

---

??? info "Tabela Sacerdote | 1.0v"
    **Nome da Tabela:** Sacerdote <br/>
    **Descrição**: Especialização de um jogador com habilidades de cura <br/>

    | Atributo       | Descrição               | Tipo    | Limite | Restrições       |
    | -------------- | ----------------------- | ------- | ------ | ---------------- |
    | `ID_Jogador`   | Referência ao jogador   | Integer |        | `FK`, `NOT NULL` |
    | `bencao_Cura`  | Poder de cura           | Integer |        |                  |
    | `atq_Especial` | Dano de ataque especial | Integer |        |                  |

---

??? info "Tabela Criatura | 1.0v"
    **Nome da Tabela:** Criatura <br/>
    **Descrição**: Representa as criaturas do jogo <br/>

    | Atributo      | Descrição                 | Tipo    | Limite | Restrições       |
    | ------------- | ------------------------- | ------- | ------ | ---------------- |
    | `ID_Criatura` | Identificador da criatura | Integer |        | `PK`, `NOT NULL` |
    | `XP`          | Experiência concedida     | Integer |        | `NOT NULL`       |

---

??? info "Tabela Ork | 1.0v"
    **Nome da Tabela:** Ork <br/>
    **Descrição**: Tipo específico de criatura com agressividade <br/>

    | Atributo      | Descrição             | Tipo    | Limite | Restrições       |
    | ------------- | --------------------- | ------- | ------ | ---------------- |
    | `ID_Criatura` | Referência à criatura | Integer |        | `FK`, `NOT NULL` |
    | `Raiva`       | Grau de agressividade | Integer |        |                  |

---

??? info "Tabela Goblin | 1.0v"
    **Nome da Tabela:** Goblin <br/>
    **Descrição**: Tipo específico de criatura com furtividade <br/>

    | Atributo      | Descrição             | Tipo    | Limite | Restrições       |
    | ------------- | --------------------- | ------- | ------ | ---------------- |
    | `ID_Criatura` | Referência à criatura | Integer |        | `FK`, `NOT NULL` |
    | `Raiva`       | Grau de agressividade | Integer |        |                  |
    | `furtividade` | Nível de furtividade  | Integer |        |                  |
    | `roubo`       | Capacidade de roubo   | Integer |        |                  |

---

??? info "Tabela NPC | 1.0v"
    **Nome da Tabela:** NPC <br/>
    **Descrição**: Personagens não jogáveis que interagem com o jogador <br/>

    | Atributo       | Descrição                  | Tipo      | Limite | Restrições       |
    | -------------- | -------------------------- | --------- | ------ | ---------------- |
    | `UniqueID`     | Identificador único do NPC | Integer   |        | `PK`, `NOT NULL` |
    | `quest`        | Missão disponível          | Varchar   | 100    |                  |
    | `localizacao`  | Posição no mapa            | Varchar   | 100    | `NOT NULL`       |
    | `horaAparicao` | Horário de surgimento      | Timestamp |        |                  |

---

??? info "Tabela Comerciante | 1.0v"
    **Nome da Tabela:** Comerciante <br/>
    **Descrição**: NPC especializado em comércio <br/>

    | Atributo      | Descrição           | Tipo    | Limite | Restrições |
    | ------------- | ------------------- | ------- | ------ | ---------- |
    | `venda_Item`  | Pode vender itens?  | Boolean |        | `NOT NULL` |
    | `compra_Item` | Pode comprar itens? | Boolean |        | `NOT NULL` |

---

??? info "Tabela Guia | 1.0v"
    **Nome da Tabela:** Guia <br/>
    **Descrição**: NPC que fornece orientações aos jogadores <br/>

    | Atributo           | Descrição                     | Tipo    | Limite | Restrições |
    | ------------------ | ----------------------------- | ------- | ------ | ---------- |
    | `custo_orientacao` | Custo para receber orientação | Integer |        | `NOT NULL` |

---

??? info "Tabela Item | 1.0v"
    **Nome da Tabela:** Item <br/>
    **Descrição**: Objeto armazenável no inventário <br/>

    | Atributo        | Descrição                       | Tipo    | Limite | Restrições       |
    | --------------- | ------------------------------- | ------- | ------ | ---------------- |
    | `ID_item`       | Identificador do item           | Integer |        | `PK`, `NOT NULL` |
    | `id_inventario` | Inventário ao qual pertence     | Integer |        | `FK`, `NOT NULL` |
    | `peso`          | Peso do item                    | Float   |        | `NOT NULL`       |
    | `durabilidade`  | Número de usos antes de quebrar | Integer |        |                  |

---

??? info "Tabela Arma | 1.0v"
    **Nome da Tabela:** Arma <br/>
    **Descrição**: Item ofensivo usado em batalha <br/>

    | Atributo | Descrição                      | Tipo    | Limite | Restrições |
    | -------- | ------------------------------ | ------- | ------ | ---------- |
    | `mãos`   | Quantidade de mãos necessárias | Integer |        | `NOT NULL` |
    | `dano`   | Dano causado                   | Integer |        | `NOT NULL` |

---

??? info "Tabela Armadura | 1.0v"
    **Nome da Tabela:** Armadura <br/>
    **Descrição**: Item defensivo que reduz dano <br/>

    | Atributo | Descrição              | Tipo    | Limite | Restrições |
    | -------- | ---------------------- | ------- | ------ | ---------- |
    | `defesa` | Capacidade de proteção | Integer |        | `NOT NULL` |

---

??? info "Tabela Batalha | 1.0v"
    **Nome da Tabela:** Batalha <br/>
    **Descrição**: Representa um combate entre personagens e criaturas <br/>

    | Atributo           | Descrição                        | Tipo    | Limite | Restrições       |
    | ------------------ | -------------------------------- | ------- | ------ | ---------------- |
    | `ID_batalha`       | Identificador da batalha         | Integer |        | `PK`, `NOT NULL` |
    | `Dano_Causado`     | Dano total infligido             | Integer |        | `NOT NULL`       |
    | `Controle_Dano`    | Controle de dano                 | Varchar | 50     |                  |
    | `Ambiente_Batalha` | Ambiente da batalha              | Varchar | 50     |                  |
    | `Dano_Sofrido`     | Dano total recebido pelo jogador | Integer |        | `NOT NULL`       |

---

## Bibliografia

> <p><small>CONTENT STUDIO. O que é um dicionário de dados? Disponível em: <a href="https://www.purestorage.com/br/knowledge/what-is-a-data-dictionary.html">https://www.purestorage.com/br/knowledge/what-is-a-data-dictionary.html</a>. Acesso em: 30 abr. 2025.</small></p>


## Tabela de Versionamento

| Versão | Data       | Descrição                                     | Autor(es)                                                             | Revisor(es)                                                          |
|--------|------------|-----------------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------|
|1.0  |02/04/2025     | Desenvolvimento do artefato | [Lucas Soares](https://github.com/https://github.com/lucaaassb) e [Fernanda Vaz](https://github.com/Fernandavazgit1)| [Felipe das Neves](https://github.com/FelipeFreire-gf) |
|1.1  |13/06/2025     | Atualização do Artefato | [Felipe das Neves](https://github.com/FelipeFreire-gf) | [Felipe das Neves](https://github.com/FelipeFreire-gf) |