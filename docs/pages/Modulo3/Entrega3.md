> ## Descrição Geral

> Esta terceira entrega consolida o desenvolvimento do nosso RPG inspirado em Senhor dos Anéis, integrando banco de dados relacional, lógica de jogo em Python e recursos avançados como triggers, procedures e sistema de quests. O projeto evoluiu desde a modelagem conceitual até a implementação de funcionalidades completas e automatizadas.

---

## Contexto das Entregas Anteriores

- **Entrega 1:** Modelagem do DER, MER, MR e Dicionário de Dados, definindo as entidades principais (jogadores, personagens, cenários, itens, NPCs, criaturas).
- **Entrega 2:** Implementação da estrutura do banco (DDL), povoamento inicial (DML), consultas essenciais (DQL) e suporte a funcionalidades como combate, inventário, NPCs e navegação.

---

## Funcionalidades Implementadas

- Criação de personagens com classes distintas (Guerreiro, Mago, Arqueiro, Sacerdote)
- Exploração de cenários e navegação entre ambientes
- Sistema de inventário e gerenciamento de itens
- Interação com NPCs (comerciantes, guias, quest givers)
- Sistema de batalhas contra criaturas
- Sistema de quests (missões principais, secundárias e épicas)
- Salvamento automático do progresso do jogador

---

## Recursos Avançados: Triggers e Procedures

### Triggers

1. **Validação de Peso do Inventário (`trg_check_inventory_weight`)**
   - Garante que o peso total dos itens não ultrapasse a capacidade máxima do inventário.
2. **Concessão de XP ao Jogador Após Vitória (`trg_grant_xp_on_victory`)**
   - Ao vencer uma batalha, o jogador recebe XP automaticamente e pode subir de nível.
3. **Log de Alterações de Nível (`trg_log_personagem_level_up`)**
   - Registra toda alteração de nível dos personagens para auditoria.
4. **Início Automático de Quests (`trg_auto_iniciar_quests`)**
   - Quando o jogador sobe de nível, quests principais disponíveis são automaticamente iniciadas.
5. **Log de Movimentação do Jogador (`trg_log_movimento`)**
   - Registra cada vez que o jogador muda de cenário.

### Procedures

1. **Batalha Completa (`sp_executar_batalha`)**
   - Executa toda a lógica de uma batalha entre jogador e criatura, registrando resultados e disparando triggers de XP.
2. **Transferência de Item (`sp_transferir_item`)**
   - Gerencia a transferência de itens entre personagens, validando posse e capacidade do inventário.
3. **Completar Quest (`sp_completar_quest`)**
   - Marca uma quest como concluída, concede recompensas e atualiza o progresso do jogador.
4. **Atualizar Progresso de Quest (`sp_atualizar_progresso_quest`)**
   - Atualiza o progresso de uma quest e chama a procedure de conclusão se necessário.

---

## Passo a Passo para Rodar o Jogo

### Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- Dependências Python (instaladas via `requirements.txt`)

### 1. Clonar o repositório

```bash
git clone https://github.com/sbd1/2025.1-senhor_dos_aneis.git
cd 2025.1-senhor_dos_aneis
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar o Banco de Dados

- Crie um banco chamado `senhor_dos_aneis` no PostgreSQL.
- Execute os scripts na seguinte ordem:
  1. `game/DDL.sql` (criação das tabelas)
  2. `game/dml.sql` (dados iniciais)
  3. `game/trigger_sp.sql` (triggers e procedures)
  4. `game/quests.sql` (sistema de quests)
  5. Outros scripts opcionais: `game/views.sql`, `game/adicionar_npcs_cenarios.sql`, `game/popular_cenarios.sql`, `game/teste_trigger.sql`

No terminal do PostgreSQL (psql):

```sql
\c senhor_dos_aneis
\i caminho/para/game/DDL.sql
\i caminho/para/game/dml.sql
\i caminho/para/game/trigger_sp.sql
\i caminho/para/game/quests.sql
```

### 4. Configurar as credenciais do banco

No arquivo do jogo (ex: `jogo.py`), ajuste as credenciais de acesso ao banco conforme seu ambiente:

```python
self.connection = psycopg2.connect(
    host="localhost",
    database="senhor_dos_aneis",
    user="SEU_USUARIO",
    password="SUA_SENHA",
    port="5432"
)
```

### 5. Executar o Jogo

#### No Linux

```bash
python3 game/jogo.py
```

#### No Windows

```powershell
python game\jogo.py
```

---

> _"Mesmo a menor das pessoas pode mudar o curso do futuro."_ – Galadriel
