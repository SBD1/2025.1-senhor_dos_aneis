<span style="background-color:#c5a352; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Versão 1.0</span>

> ## Descrição

> Nesta segunda fase do projeto concentrou-se no desenvolvimento e na implementação da estrutura completa do banco de dados para um jogo de RPG. O trabalho abrangeu desde a criação das tabelas (DDL), o povoamento com dados iniciais para simular um mundo vivo (DML), até a formulação de consultas essenciais para suportar as mecânicas do jogo (DQL). A arquitetura foi projetada para ser modular e expansível, integrando de forma coesa as principais entidades: jogadores, classes de personagens, NPCs (guias, comerciantes), criaturas (comuns, chefes), cenários navegáveis, itens, equipamentos e inventários.

---

### Objetivos Técnicos Alcançados

* **Criação da Estrutura do Banco (DDL):** Foi definida e criada toda a estrutura relacional do banco de dados. Isso incluiu a modelagem de 25 tabelas, com suas respectivas colunas, tipos de dados, chaves primárias e estrangeiras, garantindo a integridade e o relacionamento correto entre as diferentes entidades do jogo.

* **Povoamento Inicial de Dados (DML - *Seeding*):** Foram criados e executados scripts `INSERT` para popular o banco de dados com um conjunto de dados iniciais. Isso permite que os desenvolvedores testem as funcionalidades em um ambiente que já contém personagens, cenários, itens e inimigos, acelerando o ciclo de desenvolvimento da aplicação.

* **Definição de Consultas Essenciais (DQL):** Foi desenvolvida uma série de consultas `SELECT` que servem como base para as funcionalidades do jogo. Essas consultas foram projetadas para buscar dados de forma eficiente, unindo múltiplas tabelas para obter informações complexas, como o inventário de um jogador, os detalhes de um confronto ou as estatísticas de um personagem com sua classe e equipamentos.

---

### Funcionalidades Suportadas pela Estrutura

* **Criação e Especialização de Personagens:** A estrutura suporta uma tabela `personagem` base, que se especializa em `jogador`, `NPCs` e `criaturas`, permitindo que cada tipo tenha atributos comuns e específicos.
* **Sistema de Classes:** Os jogadores podem ter classes como `guerreiro`, `mago`, `sacerdote` e `arqueiro`, cada uma com seus próprios atributos e habilidades armazenados em tabelas dedicadas.
* **Interação com o Mundo:** Os jogadores estão localizados em `cenários` que se conectam entre si, permitindo a navegação pelo mundo do jogo. Os cenários também possuem características próprias (clima, período do dia).
* **Gerenciamento de Itens e Inventário:** O sistema de `inventario` permite que personagens carreguem `itens`. Os itens podem ser especializados em `arma` ou `armadura`, com atributos distintos como dano, defesa e durabilidade.
* **Mecânicas de Combate:** A estrutura permite registrar `confrontos` entre jogadores e criaturas, armazenando o resultado. Além disso, a tabela `batalha` pode guardar estatísticas detalhadas de cada combate para futuro balanceamento.
* **NPCs com Comportamentos Distintos:** Existem diferentes tipos de NPCs, como `guias` (que oferecem serviços de navegação por um custo) e `comerciantes` (que possuem listas de itens para compra e venda), além de NPCs que oferecem missões (`quests`) e diálogos.

---

## Tecnologias Utilizadas

* Documentação: Markdown via MkDocs
* Cursor para validação do banco
* Pygame para o desenvolvimento inicial do game
* Postgress para o desenvolvimento do banco
---

## Apresentação em Vídeo

A apresentação da segunda etapa pode ser acessada no link abaixo:

🔗 [Assista ao vídeo](https://www.youtube.com/watch?v=c3PBaiwbirc)

<div style="text-align: center;">
  <p><strong>Entrega 2: </strong> 
    <a href="https://www.youtube.com/watch?v=c3PBaiwbirc">Modelagem</a>
  </p>
  <iframe 
    width="560" 
    height="315" 
    src="https://www.youtube.com/embed/c3PBaiwbirc" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen>
  </iframe>
</div>

---

## Tabela de Versionamento

| Versão | Data       | Descrição                                     | Autor(es)                                                             | Revisor(es)                                                          |
|--------|------------|-----------------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------|
|1.0  |15/06/2025     | Desenvolvimento do artefato | [Felipe das Neves](https://github.com/FelipeFreire-gf)  |Todos os Integrantes|


