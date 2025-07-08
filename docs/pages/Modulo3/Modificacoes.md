# 📝 Modificações do Jogo - Sistema de Quests e Personagens

## 🔄 **Resumo das Alterações**

Foram adicionados novos arquivos e funcionalidades que expandiram significativamente o sistema do jogo, incluindo um sistema completo de quests e personagens temáticos do universo "O Senhor dos Anéis".

---

## 📁 **Novos Arquivos Adicionados**

### 1. **`quests.sql`** - Sistema de Quests Completo

- **Tabelas Criadas:**

  - `quest` - Definição das missões
  - `quest_progresso` - Acompanhamento do progresso
  - `diario_eventos` - Logs de eventos do jogador

- **Funcionalidades:**
  - Triggers automáticos para iniciar quests
  - Stored procedures para completar quests
  - Sistema de recompensas (XP e itens)
  - Quests principais e secundárias

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

### **Tabelas de Quest System:**

```sql
-- Tabela principal de quests
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

-- Progresso das quests por jogador
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

-- Log de eventos do jogador
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
```

### **Tabelas de Associação:**

```sql
-- Associação NPCs aos cenários
CREATE TABLE cenario_npc (
    id_cenario INTEGER,
    id_personagem INTEGER,
    PRIMARY KEY (id_cenario, id_personagem),
    FOREIGN KEY (id_cenario) REFERENCES cenario(id_cenario),
    FOREIGN KEY (id_personagem) REFERENCES personagem(ID_personagem)
);

-- Associação criaturas aos cenários
CREATE TABLE cenario_criatura (
    id_cenario INTEGER,
    id_personagem INTEGER,
    PRIMARY KEY (id_cenario, id_personagem),
    FOREIGN KEY (id_cenario) REFERENCES cenario(id_cenario),
    FOREIGN KEY (id_personagem) REFERENCES personagem(ID_personagem)
);
```

---

## 👥 **Novos Personagens LOTR Adicionados**

### **NPCs Principais (20 personagens):**

1. **Samwise Gamgee** - Lealdade, Nível 8
2. **Gandalf, o Cinzento** - Magia Branca, Nível 25
3. **Legolas** - Arco Élfico, Nível 15
4. **Gimli** - Machado Anão, Nível 14
5. **Aragorn** - Espada de Gondor, Nível 20
6. **Boromir** - Horn of Gondor, Nível 18
7. **Frodo Baggins** - Portador do Anel, Nível 12
8. **Merry Brandybuck** - Espada de Rohan, Nível 9
9. **Pippin Took** - Coragem Hobbit, Nível 8
10. **Galadriel** - Poder Élfico, Nível 30
11. **Elrond** - Sabedoria Élfica, Nível 28
12. **Théoden** - Rei de Rohan, Nível 22
13. **Éowyn** - Escudo-Maiden, Nível 18
14. **Faramir** - Capitão de Gondor, Nível 19
15. **Denethor** - Senescal de Gondor, Nível 25
16. **Treebeard** - Ent, Nível 35
17. **Tom Bombadil** - Mestre da Floresta, Nível 50
18. **Goldberry** - Filha do Rio, Nível 25
19. **Bilbo Baggins** - Aventureiro Aposentado, Nível 15
20. **Radagast** - Mago Marrom, Nível 20

### **Criaturas Temáticas (20 criaturas):**

1. **Lobo Sombrio** - Caça Noturna, Nível 5
2. **Aranha Gigante** - Tecelã de Seda, Nível 8
3. **Orc Guerreiro** - Combate Brutal, Nível 7
4. **Troll das Montanhas** - Força Bruta, Nível 12
5. **Nazgûl** - Terror Sombrio, Nível 20
6. **Balrog** - Demônio Antigo, Nível 25
7. **Dragão de Gelo** - Sopro Congelante, Nível 22
8. **Goblin Arqueiro** - Tiro Preciso, Nível 6
9. **Warg** - Caçador em Matilha, Nível 6
10. **Cave Troll** - Destruidor, Nível 10
11. **Haradrim** - Guerreiro do Sul, Nível 7
12. **Uruk-hai** - Elite Orc, Nível 9
13. **Múmia Antiga** - Maldição Eterna, Nível 8
14. **Esqueleto Guerreiro** - Lâmina Óssea, Nível 5
15. **Fantasma do Pântano** - Assombração, Nível 6
16. **Golem de Pedra** - Guardião Antigo, Nível 11
17. **Basilisco** - Olhar Mortal, Nível 15
18. **Hidra** - Múltiplas Cabeças, Nível 18
19. **Minotauro** - Fúria Selvagem, Nível 10
20. **Quimera** - Bestas Múltiplas, Nível 16

---

## 🗺️ **Distribuição por Cenários**

### **O Condado (Cenário 1):**

- **NPCs:** Samwise, Frodo, Merry, Pippin, Bilbo
- **Criaturas:** Lobo Sombrio, Goblin Arqueiro

### **Floresta Sombria (Cenário 2):**

- **NPCs:** Legolas, Gimli, Treebeard, Tom Bombadil, Goldberry
- **Criaturas:** Aranha Gigante, Warg, Basilisco

### **Montanhas Nebulosas (Cenário 3):**

- **NPCs:** Gandalf, Aragorn, Radagast
- **Criaturas:** Troll das Montanhas, Dragão de Gelo, Golem de Pedra

### **Ruínas de Osgiliath (Cenário 4):**

- **NPCs:** Boromir, Faramir, Denethor
- **Criaturas:** Nazgûl, Esqueleto Guerreiro, Múmia Antiga

### **Pântano dos Mortos (Cenário 5):**

- **NPCs:** Gollum
- **Criaturas:** Fantasma do Pântano, Hidra

### **Minas de Moria (Cenário 6):**

- **NPCs:** Gimli
- **Criaturas:** Balrog, Cave Troll, Goblin Arqueiro

### **Colinas do Vento (Cenário 7):**

- **NPCs:** Théoden, Éowyn
- **Criaturas:** Orc Guerreiro, Uruk-hai, Warg

### **Porto Cinzento (Cenário 8):**

- **NPCs:** Galadriel, Elrond
- **Criaturas:** Quimera, Minotauro

---

## 🎯 **Sistema de Quests Implementado**

### **Quests Principais:**

1. **"A Busca do Palantír"** - Encontrar 3 fragmentos (1000 XP)
2. **"O Chamado de Minas Tirith"** - Chegar a Minas Tirith (600 XP)

### **Quests Secundárias:**

1. **"Defensor do Condado"** - Derrotar 5 criaturas (500 XP)
2. **"Explorador da Terra Média"** - Visitar 4 cenários (300 XP)
3. **"Caçador de Goblins"** - Eliminar 3 Goblins (400 XP)

### **Funcionalidades do Sistema:**

- **Início Automático:** Quests principais iniciam automaticamente
- **Progresso Dinâmico:** Atualização baseada em ações do jogador
- **Recompensas:** XP e itens especiais
- **Logs:** Registro completo de eventos

---

## 🎮 **Impacto no Jogo Python**

### **Modificações no `jogo.py`:**

- **Sistema de Quests Integrado:** Funções para gerenciar quests
- **NPCs Dinâmicos:** Busca de NPCs por cenário
- **Criaturas Específicas:** Criaturas únicas por localização
- **Progresso de Quest:** Atualização automática baseada em ações

### **Novas Funcionalidades:**

- `setup_quest_system()` - Configuração inicial
- `update_quest_progress()` - Atualização de progresso
- `complete_quest()` - Completar quests
- `check_quests()` - Verificar quests disponíveis

---
