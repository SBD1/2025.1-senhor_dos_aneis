# 📝 Modificações do Jogo

## 🔄 **Resumo das Alterações**

Além do sistema de quests e da expansão dos personagens, foram adicionadas novas tabelas ao banco de dados para aprimorar a associação entre cenários, NPCs e criaturas, bem como para registrar eventos, progresso e o status de vida/mana dos jogadores. Essas mudanças tornam o mundo do jogo mais dinâmico, flexível e auditável.

---

## 📁 **Novos Arquivos e Scripts Adicionados**

### 1. **`quests.sql`** - Sistema de Quests Completo

- **Tabelas Criadas:**

  - `quest` - Definição das missões
  - `quest_progresso` - Acompanhamento do progresso
  - `diario_eventos` - Logs de eventos do jogador
  - `jogador_status` - Registro de vida e mana atuais do jogador

- **Funcionalidades:**
  - Triggers automáticos para iniciar quests
  - Stored procedures para completar quests e atualizar progresso
  - Sistema de recompensas (XP e itens)
  - Quests principais e secundárias
  - Registro de vida e mana atuais do jogador

### 2. **`popular_cenarios.sql`** - Personagens LOTR

- **40+ Personagens** do universo LOTR adicionados
- **20+ Criaturas** temáticas
- **Associação NPCs/Criaturas** aos cenários
- **Distribuição temática** por localização

### 3. **`adicionar_npcs_cenarios.sql`** - Associações Específicas

- **Mapeamento detalhado** de NPCs por cenário
- **Distribuição estratégica** de personagens

---

## 🗄️ **Novas Tabelas do Sistema**

### **Tabelas de Quests, Eventos e Status**

```sql
CREATE TABLE quest (
    id_quest SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    recompensa_xp INTEGER DEFAULT 0,
    recompensa_item VARCHAR(100),
    pre_requisito_level INTEGER DEFAULT 1,
    tipo_quest VARCHAR(50) DEFAULT 'Principal',
    status VARCHAR(20) DEFAULT 'Disponível',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quest_progresso (
    id_progresso SERIAL PRIMARY KEY,
    id_jogador INTEGER NOT NULL,
    id_quest INTEGER NOT NULL,
    progresso_atual INTEGER DEFAULT 0,
    progresso_maximo INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'Em Progresso',
    iniciado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completado_em TIMESTAMP NULL,
    FOREIGN KEY (id_jogador) REFERENCES jogador(ID_personagem),
    FOREIGN KEY (id_quest) REFERENCES quest(id_quest),
    UNIQUE(id_jogador, id_quest)
);

CREATE TABLE diario_eventos (
    id_evento SERIAL PRIMARY KEY,
    id_jogador INTEGER NOT NULL,
    tipo_evento VARCHAR(50) NOT NULL,
    descricao TEXT NOT NULL,
    cenario_id INTEGER,
    timestamp_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_jogador) REFERENCES jogador(ID_personagem),
    FOREIGN KEY (cenario_id) REFERENCES cenario(id_cenario) ON DELETE SET NULL
);

-- Tabela correta: Status de Vida e Mana do Jogador
CREATE TABLE IF NOT EXISTS jogador_status (
    id_jogador INTEGER PRIMARY KEY,
    vida_atual INTEGER NOT NULL DEFAULT 100,
    mana_atual INTEGER NOT NULL DEFAULT 100,
    FOREIGN KEY (id_jogador) REFERENCES jogador(ID_personagem) ON DELETE CASCADE
);

-- Inserir registros iniciais para jogadores existentes
INSERT INTO jogador_status (id_jogador, vida_atual, mana_atual)
SELECT
    j.ID_personagem,
    p.vida_maxima,
    p.mana_maxima
FROM jogador j
JOIN personagem p ON j.ID_personagem = p.ID_personagem
WHERE NOT EXISTS (
    SELECT 1 FROM jogador_status js WHERE js.id_jogador = j.ID_personagem
);

-- Mostrar quantos registros foram criados
SELECT COUNT(*) as jogadores_com_status FROM jogador_status;
```

### **Tabelas de Associação**

```sql
CREATE TABLE cenario_npc (
    id_cenario INTEGER,
    id_personagem INTEGER,
    PRIMARY KEY (id_cenario, id_personagem),
    FOREIGN KEY (id_cenario) REFERENCES cenario(id_cenario),
    FOREIGN KEY (id_personagem) REFERENCES personagem(ID_personagem)
);

CREATE TABLE cenario_criatura (
    id_cenario INTEGER,
    id_personagem INTEGER,
    PRIMARY KEY (id_cenario, id_personagem),
    FOREIGN KEY (id_cenario) REFERENCES cenario(id_cenario),
    FOREIGN KEY (id_personagem) REFERENCES personagem(ID_personagem)
);
```

---

## 👥 **Novos Personagens e Criaturas LOTR**

- **NPCs Principais:** Samwise, Gandalf, Legolas, Gimli, Aragorn, Boromir, Frodo, Merry, Pippin, Galadriel, Elrond, Théoden, Éowyn, Faramir, Denethor, Treebeard, Tom Bombadil, Goldberry, Bilbo, Radagast, entre outros.
- **Criaturas Temáticas:** Lobo Sombrio, Aranha Gigante, Orc Guerreiro, Troll das Montanhas, Nazgûl, Balrog, Dragão de Gelo, Goblin Arqueiro, Warg, Cave Troll, Haradrim, Uruk-hai, Múmia Antiga, Esqueleto Guerreiro, Fantasma do Pântano, Golem de Pedra, Basilisco, Hidra, Minotauro, Quimera, entre outros.

---

## 🗺️ **Distribuição por Cenários**

- **O Condado:** Samwise, Frodo, Merry, Pippin, Bilbo, Lobo Sombrio, Goblin Arqueiro
- **Floresta Sombria:** Legolas, Gimli, Treebeard, Tom Bombadil, Goldberry, Aranha Gigante, Warg, Basilisco
- **Montanhas Nebulosas:** Gandalf, Aragorn, Radagast, Troll das Montanhas, Dragão de Gelo, Golem de Pedra
- **Ruínas de Osgiliath:** Boromir, Faramir, Denethor, Nazgûl, Esqueleto Guerreiro, Múmia Antiga
- **Pântano dos Mortos:** Gollum, Fantasma do Pântano, Hidra
- **Minas de Moria:** Gimli, Balrog, Cave Troll, Goblin Arqueiro
- **Colinas do Vento:** Théoden, Éowyn, Orc Guerreiro, Uruk-hai, Warg
- **Porto Cinzento:** Galadriel, Elrond, Quimera, Minotauro

---

## 🎯 **Sistema de Quests Implementado**

- **Quests Principais:** Ex: "A Busca do Palantír", "O Chamado de Minas Tirith"
- **Quests Secundárias:** Ex: "Defensor do Condado", "Explorador da Terra Média", "Caçador de Goblins"
- **Funcionalidades:** Início automático, progresso dinâmico, recompensas (XP/itens), logs de eventos
- **Status de Vida/Mana:** Agora o status de vida e mana do jogador é registrado separadamente, permitindo controle preciso durante batalhas, exploração e uso de habilidades.

---

## 🎮 **Impacto no Jogo Python**

- **Sistema de Quests Integrado:** Funções para gerenciar quests, progresso e recompensas
- **NPCs e Criaturas Dinâmicos:** Busca e associação por cenário
- **Novas Tabelas:** Permitem maior flexibilidade e controle sobre o mundo do jogo
- **Progresso, Eventos e Status:** Registro detalhado das ações e condições do jogador, incluindo vida e mana atuais

---
