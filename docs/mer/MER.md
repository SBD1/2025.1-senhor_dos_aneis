# MER - Modelo Entidade Relacionamento

O Modelo Entidade Relacionamento de um banco de dados é um modelo conceitual que descreve as entidades de um domínio de negócios, com seus atributos e seus relacionamentos.

**Entidades**: os objetos da realidade a ser modelada.  
**Relacionamentos**: as associações entre as entidades.  
**Atributos**: características específicas de uma entidade.

## 1. Entidades
- Personagem
- NPC
- Jogador
- Criatura
- Goblin
- Boss
- Guerreiro
- Sacerdote
- Mago
- Arqueiro
- Inventário
- Item
- Arma
- Armadura
- Guia
- Comerciante
- Combate
- Batalha
- Cenário
- Características

## 2. Atributos

**Personagem**:  
id_personagem, nome, vida_maxima, mana_maxima, ataque, defesa, velocidade, nivel, experiencia, dialogo

**NPC**:  
id_personagem (FK), quest, localizacao, horaAparicao

**Jogador**:  
id_personagem (FK), tipo_armaPreferida, cenário (FK)

**Criatura**:  
id_personagem (FK), XP

**Goblin**:  
id_personagem (FK), furtividade, ruido

**Boss**:  
id_personagem (FK), nivelChefe, imunidades

**Guerreiro**:  
id_personagem (FK), atk_fisico, bloquear_dano

**Sacerdote**:  
id_personagem (FK), bençao_cura, atk_especial

**Mago**:  
id_personagem (FK), atk_magico, atk_multiElementos

**Arqueiro**:  
id_personagem (FK), atk_preciso, atk_rapido

**Inventário**:  
id_inventario, id_personagem (FK), peso

**Item**:  
id_item, nome, peso, durabilidade

**Arma**:  
id_item (FK), dano, alcance

**Armadura**:  
id_item (FK), defesa

**Guia**:  
curios_orientacao, id_personagem (FK)

**Comerciante**:  
vende_item, compra_item, id_personagem (FK)

**Combate**:  
idCombate, vencedor, criatura_id (FK), jogador_id (FK)

**Batalha**:  
id_batalha, dano_causado, contexto, duracao_batalha, dano_sofrido

**Cenário**:  
id_cenario, tempo_id, clima_id, evento_id, sol_id, lua_id, chave, noite, dia

**Características**:  
id_jogador, fogo, agua, terra, ar

## 3. Relacionamentos

- Um **Jogador** é um tipo de **Personagem**
- Um **NPC** é um tipo de **Personagem**
- Um **Criatura** é um tipo de **Personagem**, podendo ser um **Goblin**, **Ork** ou **Boss**
- Um **Personagem** pode possuir um **Inventário**, que armazena vários **Itens**
- Um **Item** pode ser uma **Arma** ou uma **Armadura**
- **NPCs** podem ser **Guias** ou **Comerciantes**
- **Jogadores** podem ser **Guerreiros**, **Magos**, **Sacerdotes** ou **Arqueiros**
- Um **Combate** envolve uma **Criatura** e um **Jogador**
- Uma **Batalha** possui atributos relacionados à luta
- O **Cenário** influencia o estado do **Jogador**
- O **Jogador** possui características (elementais)

# Tabela de Versionamento 

| Versão | Data       | Descrição                                     | Autor(es)                                                             | Revisor(es)                                                          |
|--------|------------|-----------------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------|
| 1.0    | 02/05/2025 | Desenvolvimento do artefato   | <a style="color:gold;" href="https://github.com/leozinlima" target="_blank">Felipe das Neves</a> | Todos os Integrantes |

