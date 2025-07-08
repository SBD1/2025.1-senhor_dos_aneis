import psycopg2
import os
import time
import platform
import random
import unicodedata
from typing import Optional, Dict, Any, List, Tuple

class LordOfTheRingsMUD:
    def __init__(self):
        self.connection = None
        self.current_player_id = None
        self.current_scenario_id = None
        self.player_alive = True
        
    def clear_screen(self):
        """Limpa o terminal baseado no sistema operacional"""
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
    
    def pause_and_clear(self, message: str = "⏸️ Pressione Enter para continuar..."):
        """Pausa, aguarda Enter e limpa a tela"""
        input(f"\n{message}")
        self.clear_screen()
        
    def connect_database(self):
        """Conecta ao banco de dados PostgreSQL"""
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="senhor_dos_aneis",
                user="lord", 
                password="12345",
                port="5432"
            )
            print("✅ Conexão com banco de dados estabelecida!")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar com o banco: {e}")
            print("🔧 Verifique se o PostgreSQL está rodando e as credenciais estão corretas.")
            return False

    def setup_quest_system(self):
        """Configura o sistema de quests corrigido usando apenas tabelas existentes"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = 'quest'
                );
            """)
            
            quest_exists = cursor.fetchone()[0]
            
            if not quest_exists:
                print("🔧 Configurando sistema de quests...")
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS quest (
                        id_quest SERIAL PRIMARY KEY,
                        nome VARCHAR(100) NOT NULL,
                        descricao TEXT NOT NULL,
                        recompensa_xp INTEGER DEFAULT 0,
                        recompensa_item VARCHAR(100),
                        pre_requisito_level INTEGER DEFAULT 1,
                        tipo_quest VARCHAR(50) DEFAULT 'Principal',
                        status VARCHAR(20) DEFAULT 'Disponível',
                        quest_dinamica BOOLEAN DEFAULT FALSE
                    );
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS quest_progresso (
                        id_progresso SERIAL PRIMARY KEY,
                        id_jogador INTEGER NOT NULL,
                        id_quest INTEGER NOT NULL,
                        progresso_atual INTEGER DEFAULT 0,
                        progresso_maximo INTEGER NOT NULL,
                        status VARCHAR(20) DEFAULT 'Em Progresso',
                        iniciado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (id_jogador) REFERENCES personagem(ID_personagem),
                        FOREIGN KEY (id_quest) REFERENCES quest(id_quest),
                        UNIQUE(id_jogador, id_quest)
                    );
                """)
                
                cursor.execute("""
                    INSERT INTO quest (nome, descricao, recompensa_xp, recompensa_item, pre_requisito_level, tipo_quest, quest_dinamica) 
                    SELECT * FROM (VALUES
                        ('A Jornada Começa', 'Fale com 2 NPCs diferentes para aprender sobre a Terra Média', 100, 'Poção de Cura', 1, 'Principal', FALSE),
                        ('Defensor das Terras', 'Derrote 3 criaturas para proteger os inocentes', 200, 'Espada de Ferro', 1, 'Principal', FALSE),
                        ('Explorador Iniciante', 'Visite todos os 4 cenários diferentes', 150, 'Mapa Élfico', 1, 'Secundária', FALSE),
                        ('Comerciante Amigável', 'Realize 2 transações comerciais', 75, 'Bolsa de Moedas', 1, 'Secundária', FALSE),
                        ('O Palantír Perdido', 'Encontre os três fragmentos do Palantír perdido espalhados pela Terra Média', 500, 'Palantír Restaurado', 1, 'Épica', FALSE)
                    ) AS v(nome, descricao, recompensa_xp, recompensa_item, pre_requisito_level, tipo_quest, quest_dinamica)
                    WHERE NOT EXISTS (
                        SELECT 1 FROM quest WHERE quest.nome = v.nome
                    )
                """)
                
                self.connection.commit()
                print("✅ Sistema de quests configurado!")
            
            cursor.close()
            
        except Exception as e:
            print(f"❌ Erro ao configurar sistema de quests: {e}")
            self.connection.rollback()

    def get_available_classes(self) -> List[Dict[str, str]]:
        """Busca as classes disponíveis no banco de dados"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('guerreiro', 'mago', 'arqueiro', 'sacerdote')
                ORDER BY table_name
            """)
            
            classes = []
            class_descriptions = {
                'arqueiro': {'name': 'Arqueiro', 'emoji': '🏹', 'desc': 'Preciso com ataques à distância'},
                'guerreiro': {'name': 'Guerreiro', 'emoji': '⚔️', 'desc': 'Especialista em combate corpo a corpo'},
                'mago': {'name': 'Mago', 'emoji': '🔮', 'desc': 'Mestre das artes arcanas'},
                'sacerdote': {'name': 'Sacerdote', 'emoji': '✨', 'desc': 'Curandeiro e suporte'}
            }
            
            for row in cursor.fetchall():
                class_name = row[0]
                if class_name in class_descriptions:
                    classes.append({
                        'table': class_name,
                        'name': class_descriptions[class_name]['name'],
                        'emoji': class_descriptions[class_name]['emoji'],
                        'description': class_descriptions[class_name]['desc']
                    })
            
            cursor.close()
            return classes
            
        except Exception as e:
            print(f"❌ Erro ao buscar classes: {e}")
            return []

    def create_player_character(self, name: str, character_class: str) -> bool:
        """Cria um novo personagem jogador"""
        try:
            cursor = self.connection.cursor()
            
            class_stats = {
                'guerreiro': {'vida': 150, 'mana': 80, 'habilidade': 'Combate Corpo a Corpo', 'resistencia': 'Físico'},
                'mago': {'vida': 90, 'mana': 200, 'habilidade': 'Feitiçaria Arcana', 'resistencia': 'Fogo'},
                'arqueiro': {'vida': 110, 'mana': 120, 'habilidade': 'Tiro Certeiro', 'resistencia': 'Ar'},
                'sacerdote': {'vida': 120, 'mana': 180, 'habilidade': 'Cura Divina', 'resistencia': 'Luz'}
            }
            
            stats = class_stats.get(character_class, class_stats['guerreiro'])
            
            cursor.execute("""
                INSERT INTO personagem (nome, vida_maxima, mana_maxima, habilidade, dificuldade, level, resistencia, dialogo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING ID_personagem
            """, (name, stats['vida'], stats['mana'], stats['habilidade'], 'Normal', 1, stats['resistencia'], f"Sou {name}, um {character_class} da Terra Média!"))
            
            player_id = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO jogador (ID_personagem, cenario, tipo_equipamento)
                VALUES (%s, %s, %s)
            """, (player_id, 1, "Equipamento Básico"))
            
            class_attack = {
                'guerreiro': 70, 'mago': 55, 'arqueiro': 65, 'sacerdote': 45
            }
            
            cursor.execute("""
                INSERT INTO skill (ID_jogador, atq) VALUES (%s, %s)
            """, (player_id, class_attack.get(character_class, 50)))
            
            elemental_stats = {
                'guerreiro': {'fogo': 20, 'agua': 20, 'terra': 40, 'ar': 20},
                'mago': {'fogo': 50, 'agua': 30, 'terra': 10, 'ar': 30},
                'arqueiro': {'fogo': 25, 'agua': 25, 'terra': 25, 'ar': 45},
                'sacerdote': {'fogo': 35, 'agua': 35, 'terra': 35, 'ar': 15}
            }
            
            stats_elem = elemental_stats.get(character_class, elemental_stats['guerreiro'])
            cursor.execute("""
                INSERT INTO caracteristicas (ID_jogador, fogo, agua, terra, ar)
                VALUES (%s, %s, %s, %s, %s)
            """, (player_id, stats_elem['fogo'], stats_elem['agua'], stats_elem['terra'], stats_elem['ar']))
            
            if character_class == "guerreiro":
                cursor.execute("""
                    INSERT INTO guerreiro (id_personagem, atq_Fisico, bloquear_Dano)
                    VALUES (%s, %s, %s)
                """, (player_id, 80, 60))
            elif character_class == "mago":
                cursor.execute("""
                    INSERT INTO mago (id_personagem, atq_Magico, atq_MultiElemento)
                    VALUES (%s, %s, %s)
                """, (player_id, 90, 70))
            elif character_class == "arqueiro":
                cursor.execute("""
                    INSERT INTO arqueiro (id_personagem, atq_Preciso, atq_Rapido)
                    VALUES (%s, %s, %s)
                """, (player_id, 85, 75))
            elif character_class == "sacerdote":
                cursor.execute("""
                    INSERT INTO sacerdote (id_personagem, bencao_Cura, atq_Especial)
                    VALUES (%s, %s, %s)
                """, (player_id, 95, 40))
            
            cursor.execute("""
                INSERT INTO inventario (id_personagem, pods) VALUES (%s, %s) RETURNING id_inventario
            """, (player_id, 100))
            
            inv_id = cursor.fetchone()[0]
            
            initial_items = {
                'guerreiro': ('Espada de Ferro', 2.5, 100),
                'mago': ('Cajado Mágico', 1.5, 80),
                'arqueiro': ('Arco Élfico', 2.0, 90),
                'sacerdote': ('Bastão Sagrado', 1.8, 85)
            }
            
            item_name, peso, durabilidade = initial_items.get(character_class, initial_items['guerreiro'])
            cursor.execute("""
                INSERT INTO item (nome, peso, durabilidade, id_inventario) VALUES (%s, %s, %s, %s)
            """, (item_name, peso, durabilidade, inv_id))
            
            for _ in range(10):
                cursor.execute("""
                    INSERT INTO item (nome, peso, durabilidade, id_inventario) VALUES (%s, %s, %s, %s)
                """, ("Moeda de Ouro", 0.01, 999, inv_id))
            
            # Criar registro de status inicial (vida e mana atuais)
            cursor.execute("""
                INSERT INTO jogador_status (id_jogador, vida_atual, mana_atual)
                VALUES (%s, %s, %s)
            """, (player_id, stats['vida'], stats['mana']))
            
            self.connection.commit()
            self.current_player_id = player_id
            self.current_scenario_id = 1
            
            print(f"🎉 {name} o {character_class} desperta no Condado!")
            print("📜 Uma nova jornada épica começa...")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar personagem: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def get_player_stats(self) -> Optional[Dict[str, Any]]:
        """Obtém stats completos do jogador"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT p.nome, p.vida_maxima, p.mana_maxima, p.level, p.habilidade, 
                       p.resistencia, j.tipo_equipamento, j.cenario, s.atq, c.fogo, c.agua, c.terra, c.ar,
                       CASE 
                         WHEN EXISTS(SELECT 1 FROM guerreiro g WHERE g.id_personagem = p.ID_personagem) THEN 'Guerreiro'
                         WHEN EXISTS(SELECT 1 FROM mago m WHERE m.id_personagem = p.ID_personagem) THEN 'Mago'
                         WHEN EXISTS(SELECT 1 FROM arqueiro a WHERE a.id_personagem = p.ID_personagem) THEN 'Arqueiro'
                         WHEN EXISTS(SELECT 1 FROM sacerdote s WHERE s.id_personagem = p.ID_personagem) THEN 'Sacerdote'
                         ELSE 'Desconhecida'
                       END as classe,
                       COALESCE(js.vida_atual, p.vida_maxima) as vida_atual,
                       COALESCE(js.mana_atual, p.mana_maxima) as mana_atual
                FROM personagem p
                JOIN jogador j ON p.ID_personagem = j.ID_personagem
                LEFT JOIN skill s ON j.ID_personagem = s.ID_jogador
                LEFT JOIN caracteristicas c ON j.ID_personagem = c.ID_jogador
                LEFT JOIN jogador_status js ON j.ID_personagem = js.id_jogador
                WHERE p.ID_personagem = %s
            """, (self.current_player_id,))
            
            result = cursor.fetchone()
            if result:
                self.current_scenario_id = result[7]
                return {
                    "nome": result[0], "vida_maxima": result[1], "mana_maxima": result[2], "level": result[3],
                    "habilidade": result[4], "resistencia": result[5], "equipamento": result[6],
                    "cenario": result[7], "ataque": result[8], "fogo": result[9], "agua": result[10], 
                    "terra": result[11], "ar": result[12], "classe": result[13], "vida": result[14], "mana": result[15]
                }
            return None
        except Exception as e:
            print(f"❌ Erro ao obter stats do jogador: {e}")
            return None
        finally:
            cursor.close()

    def get_scenario_info(self, scenario_id: int) -> Optional[Dict[str, Any]]:
        """Obtém informações detalhadas do cenário"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT id_cenario, sol, chuva, noite, dia, norte_id, leste_id, oeste_id, sul_id
                FROM cenario WHERE id_cenario = %s
            """, (scenario_id,))
            
            result = cursor.fetchone()
            if result:
                return {
                    "id": result[0], "sol": result[1], "chuva": result[2], "noite": result[3],
                    "dia": result[4], "norte": result[5], "leste": result[6], 
                    "oeste": result[7], "sul": result[8]
                }
            return None
        except Exception as e:
            print(f"❌ Erro ao obter informações do cenário: {e}")
            return None
        finally:
            cursor.close()

    def get_scenario_descriptions(self) -> Dict[int, str]:
        """Descrições imersivas dos cenários"""
        return {
            1: "🏞️ **O Condado** - Campos verdejantes se estendem até onde a vista alcança. Hobbits trabalham pacificamente em suas fazendas.",
            2: "🌲 **Floresta Sombria** - Árvores anciãs sussurram segredos sombrios. Galhos retorcidos bloqueiam a luz do sol.",
            3: "⛰️ **Montanhas Nebulosas** - Picos nevados perfuram as nuvens. O vento frio corta como lâminas de gelo.",
            4: "🏰 **Ruínas de Osgiliath** - Pedras ancestrais contam histórias de glória e destruição. Ecos do passado ressoam pelos corredores vazios.",
            5: "💀 **Pântano dos Mortos** - Uma névoa densa cobre águas paradas. Vozes sussurram entre as sombras e luzes fantasmagóricas flutuam sobre o brejo.",
            6: "⛏️ **Minas de Moria** - Túneis escuros e ecoantes, repletos de antigas ruínas anãs e perigos ocultos nas profundezas.",
            7: "🌬️ **Colinas do Vento** - Gramados altos e ventos constantes. O horizonte se estende sem fim sob um céu aberto.",
            8: "⚓ **Porto Cinzento** - O mar encontra a Terra Média em um porto antigo, onde navios élficos partem para o Oeste. O ar é salgado e cheio de esperança."
        }

    def get_random_creatures_for_scenario(self, scenario_id: int) -> List[Tuple[int, str, int, int]]:
        """Retorna criaturas específicas do cenário, exceto as já derrotadas"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT c.ID_personagem, p.nome, p.vida_maxima, c.XP
                FROM criatura c
                JOIN personagem p ON c.ID_personagem = p.ID_personagem
                JOIN cenario_criatura cc ON c.ID_personagem = cc.id_personagem
                WHERE cc.id_cenario = %s 
                AND c.ID_personagem NOT IN (
                    SELECT id_criatura FROM criaturas_derrotadas WHERE id_jogador = %s
                )
                ORDER BY RANDOM()
                LIMIT 2
            """, (scenario_id, self.current_player_id))
            
            creatures = cursor.fetchall()
            cursor.close()
            
            if not creatures:
                return []
            
            return random.sample(creatures, min(2, len(creatures)))
            
        except Exception as e:
            print(f"❌ Erro ao buscar criaturas: {e}")
            return []

    def mark_creature_defeated(self, creature_id: int):
        """Marca uma criatura como derrotada no banco de dados"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO criaturas_derrotadas (id_jogador, id_criatura)
                VALUES (%s, %s)
                ON CONFLICT (id_jogador, id_criatura) DO NOTHING
            """, (self.current_player_id, creature_id))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"❌ Erro ao marcar criatura como derrotada: {e}")
            self.connection.rollback()

    def update_player_status(self, vida_atual: int = None, mana_atual: int = None):
        """Atualiza a vida e/ou mana atual do jogador, com debug"""
        try:
            cursor = self.connection.cursor()
            # Debug: mostrar valores antes
            cursor.execute("""
                SELECT vida_atual, mana_atual FROM jogador_status WHERE id_jogador = %s
            """, (self.current_player_id,))
            before = cursor.fetchone()
            print(f"[DEBUG] Status antes: vida_atual={before[0] if before else None}, mana_atual={before[1] if before else None}")
            if vida_atual is not None and mana_atual is not None:
                cursor.execute("""
                    INSERT INTO jogador_status (id_jogador, vida_atual, mana_atual)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id_jogador) 
                    DO UPDATE SET vida_atual = EXCLUDED.vida_atual, mana_atual = EXCLUDED.mana_atual
                """, (self.current_player_id, vida_atual, mana_atual))
            elif vida_atual is not None:
                cursor.execute("""
                    INSERT INTO jogador_status (id_jogador, vida_atual, mana_atual)
                    VALUES (%s, %s, (SELECT mana_atual FROM jogador_status WHERE id_jogador = %s))
                    ON CONFLICT (id_jogador) 
                    DO UPDATE SET vida_atual = EXCLUDED.vida_atual
                """, (self.current_player_id, vida_atual, self.current_player_id))
            elif mana_atual is not None:
                cursor.execute("""
                    INSERT INTO jogador_status (id_jogador, vida_atual, mana_atual)
                    VALUES (%s, (SELECT vida_atual FROM jogador_status WHERE id_jogador = %s), %s)
                    ON CONFLICT (id_jogador) 
                    DO UPDATE SET mana_atual = EXCLUDED.mana_atual
                """, (self.current_player_id, self.current_player_id, mana_atual))
            self.connection.commit()
            # Debug: mostrar valores depois
            cursor.execute("""
                SELECT vida_atual, mana_atual FROM jogador_status WHERE id_jogador = %s
            """, (self.current_player_id,))
            after = cursor.fetchone()
            print(f"[DEBUG] Status depois: vida_atual={after[0] if after else None}, mana_atual={after[1] if after else None}")
            cursor.close()
        except Exception as e:
            print(f"❌ Erro ao atualizar status do jogador: {e}")
            self.connection.rollback()

    def regenerate_mana(self, amount: int = 10):
        """Regenera mana do jogador (usado após descanso ou tempo)"""
        try:
            player_stats = self.get_player_stats()
            if not player_stats:
                return
            
            current_mana = player_stats['mana']
            max_mana = player_stats['mana_maxima']
            new_mana = min(current_mana + amount, max_mana)
            
            if new_mana > current_mana:
                self.update_player_status(mana_atual=new_mana)
                print(f"💙 Mana regenerada! +{new_mana - current_mana} mana")
            
        except Exception as e:
            print(f"❌ Erro ao regenerar mana: {e}")

    def get_player_money(self) -> int:
        """Conta o dinheiro do jogador - CORRIGIDO E ROBUSTO"""
        try:
            if not self.current_player_id:
                print("⚠️ current_player_id é None")
                return 0
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT COUNT(i.id_item) as money_count
                FROM inventario inv
                INNER JOIN item i ON inv.id_inventario = i.id_inventario
                WHERE inv.id_personagem = %s AND i.nome = 'Moeda de Ouro'
            """, (self.current_player_id,))
            result = cursor.fetchone()
            cursor.close()
            if result and len(result) > 0 and result[0] is not None:
                return int(result[0])
            else:
                print("Tupla vazia ou None")
                return 0
        except Exception as e:
            print(f"❌ Erro ao contar dinheiro: {e}")
            return 0

    def update_quest_progress(self, quest_type: str, increment: int = 1, scenario_id: int = None):
        """Atualiza progresso de quests baseado no tipo de ação"""
        quest_mapping = {
            'npc_talk': 2,      
            'creature_kill': 2,  
            'explore': 3,        
            'trade': 4,          
            'palantir_fragment': 1,
            'creature_kill_condado': 'dinamica',
            'creature_kill_osgiliath': 'dinamica',
            'creature_kill_rohan': 'dinamica',
            'creature_kill_floresta': 'dinamica',
            'generic_quest': 'dinamica'
        }
        
        quest_id = quest_mapping.get(quest_type)
        if not quest_id:
            return
            
        try:
            cursor = self.connection.cursor()
            
            if quest_id == 'dinamica':
                # Atualizar quests dinâmicas baseadas no tipo e cenário
                cursor.execute("""
                    SELECT qp.id_quest, qp.progresso_atual, qp.progresso_maximo, q.nome
                    FROM quest_progresso qp
                    JOIN quest q ON qp.id_quest = q.id_quest
                    WHERE qp.id_jogador = %s AND qp.status = 'Em Progresso' AND q.quest_dinamica = TRUE
                """, (self.current_player_id,))
                
                quests_dinamicas = cursor.fetchall()
                
                for quest_row in quests_dinamicas:
                    q_id, atual, maximo, nome = quest_row
                    objetivos = self.get_quest_objectives(nome)
                    
                    # Verificar se o tipo de progresso corresponde
                    if objetivos['tipo_progresso'] == quest_type:
                        novo_progresso = min(atual + increment, maximo)
                        
                        cursor.execute("""
                            UPDATE quest_progresso 
                            SET progresso_atual = %s
                            WHERE id_jogador = %s AND id_quest = %s AND status = 'Em Progresso'
                        """, (novo_progresso, self.current_player_id, q_id))
                        
                        if novo_progresso >= maximo:
                            self.complete_quest(q_id)
                        
                        print(f"📈 Progresso na missão '{nome}': {novo_progresso}/{maximo}")
            else:
                # Sistema original para quests estáticas
                cursor.execute("""
                    SELECT progresso_atual, progresso_maximo FROM quest_progresso
                    WHERE id_jogador = %s AND id_quest = %s AND status = 'Em Progresso'
                """, (self.current_player_id, quest_id))
                
                result = cursor.fetchone()
                if result:
                    atual, maximo = result
                    novo_progresso = min(atual + increment, maximo)
                    
                    cursor.execute("""
                        UPDATE quest_progresso 
                        SET progresso_atual = %s
                        WHERE id_jogador = %s AND id_quest = %s AND status = 'Em Progresso'
                    """, (novo_progresso, self.current_player_id, quest_id))
                    
                    if novo_progresso >= maximo:
                        self.complete_quest(quest_id)
                
            self.connection.commit()
            cursor.close()
            
        except Exception as e:
            print(f"❌ Erro ao atualizar quest: {e}")
            self.connection.rollback()

    def start_initial_quest(self):
        """Inicia apenas a primeira quest para novos jogadores"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) FROM quest_progresso WHERE id_jogador = %s
            """, (self.current_player_id,))
            
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO quest_progresso (id_jogador, id_quest, progresso_atual, progresso_maximo, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (self.current_player_id, 1, 0, 3, 'Em Progresso'))  
                
                cursor.execute("""
                    INSERT INTO quest_progresso (id_jogador, id_quest, progresso_atual, progresso_maximo, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (self.current_player_id, 2, 0, 5, 'Em Progresso'))  
                
                self.connection.commit()
            
            cursor.close()
            
        except Exception as e:
            print(f"❌ Erro ao iniciar quest inicial: {e}")
            self.connection.rollback()

    def complete_quest(self, quest_id: int):
        """Completa uma quest e dá recompensas"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT nome, recompensa_xp, recompensa_item FROM quest WHERE id_quest = %s
            """, (quest_id,))
            
            quest_data = cursor.fetchone()
            if quest_data:
                nome, xp_reward, item_reward = quest_data
                
                cursor.execute("""
                    UPDATE quest_progresso 
                    SET status = 'Completada'
                    WHERE id_jogador = %s AND id_quest = %s
                """, (self.current_player_id, quest_id))
                
                print(f"\n🎉 QUEST COMPLETADA: {nome}")
                
                if xp_reward > 0:
                    print(f"✨ Você ganhou {xp_reward} XP!")
                    
                    current_level = self.get_player_stats()['level']
                    new_level = current_level + (xp_reward // 500)
                    
                    if new_level > current_level:
                        cursor.execute("""
                            UPDATE personagem SET level = %s WHERE ID_personagem = %s
                        """, (new_level, self.current_player_id))
                        print(f"🆙 Você subiu para o nível {new_level}!")
                
                if item_reward:
                    cursor.execute("""
                        SELECT id_inventario FROM inventario WHERE id_personagem = %s
                    """, (self.current_player_id,))
                    
                    inv_id = cursor.fetchone()[0]
                    cursor.execute("""
                        INSERT INTO item (nome, peso, durabilidade, id_inventario)
                        VALUES (%s, %s, %s, %s)
                    """, (item_reward, 0.5, 999, inv_id))
                    
                    print(f"🎁 Você recebeu: {item_reward}")
                
                if quest_id == 1:  
                    cursor.execute("""
                        INSERT INTO quest_progresso (id_jogador, id_quest, progresso_atual, progresso_maximo, status)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (id_jogador, id_quest) DO NOTHING
                    """, (self.current_player_id, 3, 0, 4, 'Em Progresso')) 
                elif quest_id == 2:  
                    cursor.execute("""
                        INSERT INTO quest_progresso (id_jogador, id_quest, progresso_atual, progresso_maximo, status)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (id_jogador, id_quest) DO NOTHING
                    """, (self.current_player_id, 4, 0, 3, 'Em Progresso'))  
                
                self.connection.commit()
            
            cursor.close()
            
        except Exception as e:
            print(f"❌ Erro ao completar quest: {e}")
            self.connection.rollback()

    def move_player(self, direction: str) -> bool:
        """Sistema de movimento que salva no banco"""
        try:
            scenario = self.get_scenario_info(self.current_scenario_id)
            if not scenario:
                return False
            
            direction_map = {
                "norte": scenario["norte"], "sul": scenario["sul"],
                "leste": scenario["leste"], "oeste": scenario["oeste"]
            }
            
            new_scenario_id = direction_map.get(direction.lower())
            if new_scenario_id is None:
                print("🚫 Não há caminho nessa direção!")
                time.sleep(1.5)
                return False
            
            # Animação de movimento
            direction_emoji = {"norte": "🔼", "sul": "🔽", "leste": "▶️", "oeste": "◀️"}
            
            print(f"\n{direction_emoji.get(direction, '🚶')} Você caminha para o {direction}...")
            for i in range(3):
                print("." * (i + 1))
                time.sleep(0.5)
            
            # Atualizar cenário no banco
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE jogador SET cenario = %s WHERE ID_personagem = %s
            """, (new_scenario_id, self.current_player_id))
            
            self.connection.commit()
            self.current_scenario_id = new_scenario_id
            
            # Descrição da chegada
            descriptions = self.get_scenario_descriptions()
            new_description = descriptions.get(new_scenario_id, f"Região #{new_scenario_id}")
            print(f"\n📍 {new_description}")
            
            # Atualizar quest de exploração
            self.update_quest_progress('explore', 1)
            
            # Regenerar um pouco de mana ao explorar
            self.regenerate_mana(5)
            
            cursor.close()
            return True
            
        except Exception as e:
            print(f"❌ Erro ao mover jogador: {e}")
            self.connection.rollback()
            return False

    def battle_creature(self, creature_id: int, creature_name: str, creature_hp: int, creature_xp: int):
        """Sistema de combate melhorado - ATUALIZADO para quests dinâmicas"""
        try:
            player_stats = self.get_player_stats()
            if not player_stats:
                return False
                
            player_attack = player_stats['ataque']
            player_hp = player_stats['vida']
            player_mana = player_stats['mana']
            
            print(f"\n⚔️ **BATALHA ÉPICA** ⚔️")
            print(f"🧙‍♂️ {player_stats['nome']} VS {creature_name} 👹")
            print("="*50)
            
            # Combate por turnos
            turn = 1
            while creature_hp > 0 and player_hp > 0:
                print(f"\n🔄 Turno {turn}")
                print(f"👤 Sua vida: {player_hp} | 💙 Mana: {player_mana} | 👹 Vida do {creature_name}: {creature_hp}")
                
                print("\n1. ⚔️ Ataque normal")
                print("2. 🔥 Ataque elemental (Custo: 15 mana)")
                print("3. 🛡️ Defender")
                print("4. 🏃 Fugir")
                
                choice = input("\n➤ Sua ação: ").strip()
                
                damage_reduction = 1.0
                
                if choice == "1":
                    # Ataque normal
                    damage = random.randint(player_attack - 10, player_attack + 10)
                    creature_hp -= damage
                    print(f"⚔️ Você ataca causando {damage} de dano!")
                    
                elif choice == "2":
                    # Ataque elemental baseado na classe
                    if player_mana >= 15:
                        elemental_bonus = max(player_stats['fogo'], player_stats['agua'], 
                                            player_stats['terra'], player_stats['ar'])
                        damage = random.randint(player_attack, player_attack + elemental_bonus)
                        creature_hp -= damage
                        player_mana -= 15
                        print(f"🔥 Ataque elemental! {damage} de dano! (-15 mana)")
                    else:
                        print("❌ Mana insuficiente para ataque elemental!")
                        print("⚔️ Usando ataque normal...")
                        damage = random.randint(player_attack - 10, player_attack + 10)
                        creature_hp -= damage
                        print(f"⚔️ Você ataca causando {damage} de dano!")
                    
                elif choice == "3":
                    # Defender
                    print("🛡️ Você se prepara para se defender...")
                    damage_reduction = 0.5
                    
                elif choice == "4":
                    # Fugir
                    if random.random() < 0.7:
                        print("🏃 Você conseguiu fugir da batalha!")
                        return False
                    else:
                        print("❌ Não conseguiu fugir!")
                
                # Turno da criatura
                if creature_hp > 0:
                    base_damage = random.randint(15, 25)
                    creature_damage = int(base_damage * damage_reduction)
                    
                    player_hp -= creature_damage
                    print(f"👹 {creature_name} ataca causando {creature_damage} de dano!")
                
                turn += 1
                time.sleep(1.5)
            
            # Resultado da batalha
            victory = creature_hp <= 0
            
            # Atualizar vida e mana no banco de dados
            self.update_player_status(vida_atual=player_hp, mana_atual=player_mana)
            
            # Registrar no banco
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO batalha (Dano_causado, Controle_Dano, Ambiente_batalha, Dano_sofrido)
                VALUES (%s, %s, %s, %s)
            """, (player_attack, 100, f"Cenário {self.current_scenario_id}", 
                  player_stats['vida_maxima'] - player_hp))
            
            cursor.execute("""
                INSERT INTO confronta (vencedor, criatura_id, jogador_id)
                VALUES (%s, %s, %s)
            """, (victory, creature_id, self.current_player_id))
            
            if victory:
                print(f"\n🎉 VITÓRIA! Você derrotou {creature_name}!")
                print(f"✨ Você ganhou {creature_xp} XP!")
                
                # Marcar criatura como derrotada
                self.mark_creature_defeated(creature_id)
                
                # --- RECOMPENSA EM MOEDAS PARA CRIATURAS DIFÍCEIS ---
                # Buscar ataque da criatura
                cursor.execute("""
                    SELECT s.atq FROM skill s WHERE s.ID_jogador = %s
                """, (creature_id,))
                skill_row = cursor.fetchone()
                creature_atq = skill_row[0] if skill_row else 0
                # Critérios de dificuldade
                is_dificil = (creature_hp + damage >= 120) or (creature_atq > 40)
                # creature_hp pode estar negativo, então use o valor original passado para a função
                # Para isso, salve o valor original no início da função
                # (vou adicionar isso no início do método)
                #
                # Calcule moedas
                if not hasattr(self, '_creature_hp_original'):
                    self._creature_hp_original = creature_hp + sum([random.randint(player_attack - 10, player_attack + 10) for _ in range(turn-1)])
                vida_original = self._creature_hp_original if hasattr(self, '_creature_hp_original') else creature_hp
                if vida_original < creature_hp:
                    vida_original = creature_hp
                if (vida_original > 120) or (creature_atq > 40):
                    moedas_recompensa = max(1, (vida_original // 50) + (creature_atq // 10))
                    # Buscar inventário do jogador
                    cursor.execute("""
                        SELECT id_inventario FROM inventario WHERE id_personagem = %s
                    """, (self.current_player_id,))
                    inv_id = cursor.fetchone()[0]
                    for _ in range(moedas_recompensa):
                        cursor.execute("""
                            INSERT INTO item (nome, peso, durabilidade, id_inventario)
                            VALUES (%s, %s, %s, %s)
                        """, ("Moeda de Ouro", 0.01, 999, inv_id))
                    print(f"💰 Você recebeu {moedas_recompensa} moedas pela vitória!")
                # --- FIM RECOMPENSA ---
                
                # Atualizar quest de combate baseado no cenário atual
                if self.current_scenario_id == 1:  # Condado
                    self.update_quest_progress('creature_kill_condado', 1)
                elif self.current_scenario_id == 4:  # Osgiliath
                    self.update_quest_progress('creature_kill_osgiliath', 1)
                elif self.current_scenario_id == 7:  # Rohan
                    self.update_quest_progress('creature_kill_rohan', 1)
                elif self.current_scenario_id == 2:  # Floresta
                    self.update_quest_progress('creature_kill_floresta', 1)
                else:
                    # Quest genérica para outros cenários
                    self.update_quest_progress('creature_kill', 1)
                
                # Level up simples
                current_level = player_stats['level']
                if creature_xp >= 200:
                    new_level = current_level + 1
                    cursor.execute("""
                        UPDATE personagem SET level = %s WHERE ID_personagem = %s
                    """, (new_level, self.current_player_id))
                    print(f"🆙 Você subiu para o nível {new_level}!")
                
            else:
                print(f"\n💀 DERROTA! {creature_name} foi mais forte...")
                print("🏥 Você foi transportado para um local seguro para se recuperar...")
            
            self.connection.commit()
            cursor.close()
            return victory
            
        except Exception as e:
            print(f"❌ Erro durante a batalha: {e}")
            self.connection.rollback()
            return False

    def search_for_items(self):
        """Procura por itens na área atual, incluindo fragmentos do Palantír"""
        print("\n🔍 Você procura por itens perdidos...")
        time.sleep(2)
        
        # Chance de encontrar item
        if random.random() < 0.4:  # 40% de chance
            # Chance especial de encontrar fragmento do Palantír (10%)
            if random.random() < 0.1:
                found_item = "Fragmento do Palantír"
                print(f"✨ DESCOBERTA ÉPICA! Você encontrou: {found_item}!")
                # Atualizar quest do Palantír
                self.update_quest_progress('palantir_fragment', 1)
            else:
                # Itens normais aleatórios
                scenario_items = [
                    "Erva Medicinal", "Moeda de Prata", "Pão de Lemba", "Madeira Élfica", 
                    "Cristal Sombrio", "Pele de Lobo", "Ferro das Montanhas", "Gema Congelada", 
                    "Osso de Dragão", "Fragmento Antigo", "Runa Perdida", "Pedra do Rei",
                    "Poção de Cura", "Pergaminho Antigo", "Anel Simples"
                ]
                found_item = random.choice(scenario_items)
                print(f"🎁 Você encontrou: {found_item}!")
            
            try:
                cursor = self.connection.cursor()
                
                # Buscar inventário do jogador
                cursor.execute("""
                    SELECT id_inventario FROM inventario WHERE id_personagem = %s
                """, (self.current_player_id,))
                
                inv_id = cursor.fetchone()[0]
                
                # Adicionar item
                cursor.execute("""
                    INSERT INTO item (nome, peso, durabilidade, id_inventario)
                    VALUES (%s, %s, %s, %s)
                """, (found_item, 0.5, 100, inv_id))
                
                self.connection.commit()
                cursor.close()
                
            except Exception as e:
                print(f"❌ Erro ao adicionar item: {e}")
        else:
            print("🤷 Você não encontrou nada de interessante...")
        
        time.sleep(2)

    def show_shop(self, merchant_name: str, sell_items: List[str], buy_items: List[str]):
        """Sistema de compra e venda implementado"""
        while True:
            self.clear_screen()
            print(f"🛒 LOJA DE {merchant_name.upper()} 🛒")
            print("="*50)
            
            # Mostrar dinheiro do jogador
            player_money = self.get_player_money()
            print(f"💰 Suas moedas: {player_money}")
            
            print("\n1. 🛍️ Comprar itens")
            print("2. 💰 Vender itens")
            print("3. 🚶 Sair da loja")
            
            choice = input("\n➤ O que deseja fazer? ").strip()
            
            if choice == "1":
                self.buy_menu(merchant_name, sell_items)
            elif choice == "2":
                self.sell_menu(merchant_name, buy_items)
            elif choice == "3":
                break
            else:
                print("❓ Opção inválida!")
                time.sleep(1)

    def buy_menu(self, merchant_name: str, available_items: List[str]):
        """Menu de compra aprimorado"""
        item_prices = {
            "Poção de Cura": 3,
            "Adaga de Ferro": 5,
            "Espada de Ferro": 10,
            "Armadura de Couro": 8,
            "Escudo de Madeira": 4,
            "Poção de Mana": 3,
            "Anel de Proteção": 15,
            "Poções de cura": 3,
            "Adagas de ferro": 5,
            "Cajado Mágico": 12,
            "Arco Élfico": 9,
            "Bastão Sagrado": 11,
            "Capacete de Ferro": 6,
            "Botas de Couro": 3,
            "Pergaminho Antigo": 2,
            "Runa de Proteção": 7
        }
        
        print(f"\n🛍️ {merchant_name}: \"Veja meus melhores itens:\"")
        print("-" * 50)
        
        player_money = self.get_player_money()
        print(f"💰 Suas moedas: {player_money}")
        print()
        
        for i, item in enumerate(available_items, 1):
            price = item_prices.get(item, 3)
            affordable = "✅" if player_money >= price else "❌"
            print(f"{i:2d}. {affordable} {item} - {price} moedas")
        
        print("\n0. Voltar")
        print("-" * 50)
        
        try:
            choice = int(input("\n➤ Qual item comprar? ").strip())
            if choice == 0:
                return
            elif 1 <= choice <= len(available_items):
                item = available_items[choice - 1]
                price = item_prices.get(item, 3)
                
                if player_money >= price:
                    # Confirmar compra
                    print(f"\n💰 {merchant_name}: \"{item} custa {price} moedas.\"")
                    confirm = input("➤ Confirmar compra? (s/n): ").strip().lower()
                    
                    if confirm in ['s', 'sim', 'y', 'yes']:
                        if self.purchase_item(item, price):
                            print(f"✅ Você comprou {item} por {price} moedas!")
                            self.update_quest_progress('trade', 1)
                        else:
                            print("❌ Erro na compra!")
                    else:
                        print("❌ Compra cancelada.")
                else:
                    print("❌ Dinheiro insuficiente!")
            else:
                print("❓ Opção inválida!")
        except ValueError:
            print("❓ Digite um número válido!")
        
        time.sleep(2)

    def sell_menu(self, merchant_name: str, wanted_items: List[str]):
        """Menu de venda aprimorado - MELHORADO"""
        try:
            cursor = self.connection.cursor()
            # Buscar itens do jogador (exceto moedas) com quantidade
            cursor.execute("""
                SELECT MIN(i.id_item) as id_item, i.nome, COUNT(*) as quantidade
                FROM item i
                JOIN inventario inv ON i.id_inventario = inv.id_inventario
                WHERE inv.id_personagem = %s AND i.nome NOT LIKE '%Moeda%'
                GROUP BY i.nome
                ORDER BY i.nome
            """, (self.current_player_id,))
            player_items = cursor.fetchall()
            cursor.close()

            if not player_items:
                print("🎒 Você não tem itens para vender.")
                print("💡 Dica: Explore áreas para encontrar itens valiosos!")
                input("⏸️ Pressione Enter para voltar...")
                return
            
            print(f"\n💰 {merchant_name}: \"Deixe-me ver o que você tem para vender...\"")
            print("-" * 50)
            
            # Mostrar dinheiro atual
            player_money = self.get_player_money()
            print(f"💰 Suas moedas atuais: {player_money}")
            print()
            
            # Sistema de preços baseado no tipo de item - MELHORADO
            item_prices = {
                # Armas
                "Espada": 8, "Adaga": 5, "Arco": 7, "Cajado": 6, "Bastão": 6, "Machado": 9,
                # Armaduras
                "Armadura": 10, "Escudo": 4, "Capacete": 3, "Botas": 2,
                # Poções
                "Poção": 4, "Poções": 4,
                # Materiais
                "Ferro": 3, "Madeira": 2, "Cristal": 5, "Gema": 6, "Pedra": 1, "Ouro": 8, "Prata": 4,
                # Itens especiais
                "Fragmento": 15, "Anel": 12, "Pergaminho": 3, "Runa": 8, "Palantír": 50,
                # Comida
                "Pão": 1, "Erva": 2, "Pele": 3, "Osso": 2, "Lemba": 2,
                # Itens únicos
                "Élfico": 10, "Sagrado": 12, "Mágico": 15, "Antigo": 8
            }
            
            sellable_items = []
            for row in player_items:
                print(f"[DEBUG] player_items row: {row}")
                if not row or len(row) < 3:
                    print(f"[DEBUG] Linha inesperada em player_items: {row}")
                    continue
                item_id, nome, quantidade = row[:3]
                if not nome or quantidade is None:
                    print(f"[DEBUG] Dados incompletos: {row}")
                    continue
                # Calcular preço baseado no tipo de item
                base_price = 2  # Preço padrão
                for item_type, price in item_prices.items():
                    if item_type.lower() in nome.lower():
                        base_price = price
                        break
                # Ajustar preço baseado na raridade e especificidade
                if "Fragmento do Palantír" in nome:
                    base_price = 50  # Fragmentos do Palantír são extremamente valiosos
                elif "Palantír" in nome:
                    base_price = 100  # Palantír completo é inestimável
                elif "Fragmento" in nome:
                    base_price = 20  # Outros fragmentos são muito valiosos
                elif "Anel" in nome and ("Proteção" in nome or "Poder" in nome):
                    base_price = 25  # Anéis mágicos são valiosos
                elif "Élfico" in nome:
                    base_price = 12  # Itens élficos são valiosos
                elif "Sagrado" in nome or "Mágico" in nome:
                    base_price = 15  # Itens mágicos são valiosos
                sellable_items.append((item_id, nome, quantidade, base_price))
            
            if not sellable_items:
                print("❌ Você não tem nada que eu queira comprar.")
                print("💡 Dica: Procure por itens mais valiosos em diferentes regiões!")
                time.sleep(2)
                return
            
            print("📋 **SEUS ITENS DISPONÍVEIS PARA VENDA:**")
            print("=" * 60)
            
            for i, (item_id, nome, quantidade, base_price) in enumerate(sellable_items, 1):
                if quantidade > 1:
                    total_value = base_price * quantidade
                    print(f"{i:2d}. {nome} x{quantidade} - {base_price} moedas cada (Total: {total_value})")
                else:
                    print(f"{i:2d}. {nome} - {base_price} moedas")
            
            print("\n0. Voltar")
            print("99. 📋 Ver inventário completo")
            print("88. 💰 Ver valor total dos itens")
            print("77. 🛒 Vender todos os itens")
            print("-" * 60)
            
            try:
                choice = input("\n➤ Qual item vender? ").strip()
                if choice == "0":
                    return
                elif choice == "99":
                    # Mostrar inventário completo
                    self.clear_screen()
                    print("📋 **INVENTÁRIO COMPLETO**")
                    print("=" * 50)
                    self.show_inventory()
                    input("\n⏸️ Pressione Enter para voltar...")
                    return
                elif choice == "88":
                    # Calcular valor total
                    total_value = sum(base_price * quantidade for _, _, quantidade, base_price in sellable_items)
                    print(f"\n💰 **VALOR TOTAL DOS ITENS:** {total_value} moedas")
                    print("💡 Dica: Vender todos os itens renderia uma boa quantia!")
                    input("⏸️ Pressione Enter para continuar...")
                    return
                elif choice == "77":
                    # Vender todos os itens
                    total_value = sum(base_price * quantidade for _, _, quantidade, base_price in sellable_items)
                    total_items = sum(quantidade for _, _, quantidade, _ in sellable_items)
                    print(f"\n💰 {merchant_name}: \"Vou pagar {total_value} moedas por todos os seus {total_items} itens.\"")
                    print(f"💡 Após a venda, você terá {player_money + total_value} moedas.")
                    confirm = input("➤ Confirmar venda de TODOS os itens? (s/n): ").strip().lower()
                    if confirm in ['s', 'sim', 'y', 'yes']:
                        if self.sell_all_items():
                            print(f"✅ Você vendeu todos os itens por {total_value} moedas!")
                            print(f"💰 Agora você tem {self.get_player_money()} moedas!")
                            self.update_quest_progress('trade', 1)
                        else:
                            print("❌ Erro na venda em massa!")
                    else:
                        print("❌ Venda cancelada.")
                elif choice.isdigit():
                    idx = int(choice)
                    if 1 <= idx <= len(sellable_items):
                        item_id, nome, quantidade, base_price = sellable_items[idx - 1]
                        if quantidade > 1:
                            print(f"\n💰 {merchant_name}: \"Você tem {quantidade} {nome}. Quantos quer vender?\"")
                            print(f"💡 Preço por unidade: {base_price} moedas")
                            try:
                                sell_quantity = int(input(f"➤ Quantidade (1-{quantidade}): ").strip())
                                if sell_quantity < 1 or sell_quantity > quantidade:
                                    print("❌ Quantidade inválida!")
                                    time.sleep(2)
                                    return
                            except ValueError:
                                print("❌ Digite um número válido!")
                                time.sleep(2)
                                return
                        else:
                            sell_quantity = 1
                        total_price = base_price * sell_quantity
                        print(f"\n💰 {merchant_name}: \"Vou pagar {total_price} moedas por {sell_quantity} {nome}.\"")
                        print(f"💡 Após a venda, você terá {player_money + total_price} moedas.")
                        confirm = input("➤ Confirmar venda? (s/n): ").strip().lower()
                        if confirm in ['s', 'sim', 'y', 'yes']:
                            if self.sell_item_quantity(item_id, nome, sell_quantity, total_price):
                                print(f"✅ Você vendeu {sell_quantity} {nome} por {total_price} moedas!")
                                print(f"💰 Agora você tem {self.get_player_money()} moedas!")
                                self.update_quest_progress('trade', 1)
                            else:
                                print("❌ Erro na venda!")
                        else:
                            print("❌ Venda cancelada.")
                    else:
                        print("❌ Opção inválida! Escolha um número da lista.")
                        time.sleep(2)
                else:
                    print("❌ Opção inválida! Digite um número da lista ou um comando especial.")
                    time.sleep(2)
            except Exception as e:
                print(f"❌ Erro inesperado no menu de venda: {e}")
                time.sleep(2)
            
        except Exception as e:
            print(f"❌ Erro no menu de venda: {e}")
            time.sleep(2)

    def purchase_item(self, item_name: str, price: int):
        """Compra um item"""
        try:
            cursor = self.connection.cursor()

            # Buscar id_inventario ANTES de remover moedas
            cursor.execute("""
                SELECT id_inventario FROM inventario WHERE id_personagem = %s
            """, (self.current_player_id,))
            inv_row = cursor.fetchone()
            if not inv_row:
                print("❌ Inventário não encontrado para o jogador!")
                cursor.close()
                return False
            inv_id = inv_row[0]

            # Verificar se há moedas suficientes
            cursor.execute("""
                SELECT COUNT(*) FROM item WHERE id_inventario = %s AND nome = 'Moeda de Ouro'
            """, (inv_id,))
            moedas = cursor.fetchone()[0]
            if moedas < price:
                print("❌ Dinheiro insuficiente para a compra!")
                cursor.close()
                return False

            # Remover moedas (uma por vez até atingir o preço)
            for _ in range(price):
                cursor.execute("""
                    DELETE FROM item WHERE id_item IN (
                        SELECT id_item FROM item WHERE id_inventario = %s AND nome = 'Moeda de Ouro' LIMIT 1
                    )
                """, (inv_id,))

            # Adicionar item comprado
            cursor.execute("""
                INSERT INTO item (nome, peso, durabilidade, id_inventario)
                VALUES (%s, %s, %s, %s)
            """, (item_name, 1.0, 100, inv_id))

            self.connection.commit()
            cursor.close()
            return True

        except Exception as e:
            print(f"❌ Erro na compra: {e}")
            self.connection.rollback()
            return False

    def sell_item(self, item_id: int, price: int):
        """Vende um item (método legado)"""
        return self.sell_item_quantity(item_id, "Item", 1, price)

    def sell_item_quantity(self, item_id: int, item_name: str, quantity: int, total_price: int):
        """Vende uma quantidade específica de itens - MELHORADA"""
        try:
            cursor = self.connection.cursor()
            
            # Buscar o inventário do jogador
            cursor.execute("""
                SELECT id_inventario FROM inventario WHERE id_personagem = %s
            """, (self.current_player_id,))
            inv_result = cursor.fetchone()
            if not inv_result:
                print("❌ Inventário não encontrado!")
                cursor.close()
                return False
            inv_id = inv_result[0]

            # Verificar se o jogador tem a quantidade suficiente do item
            cursor.execute("""
                SELECT COUNT(*) FROM item
                WHERE id_inventario = %s AND nome = %s
            """, (inv_id, item_name))
            available_quantity = cursor.fetchone()[0]
            
            if available_quantity < quantity:
                print(f"❌ Você não tem {quantity} {item_name} para vender! (Disponível: {available_quantity})")
                cursor.close()
                return False

            # Remover a quantidade especificada de itens pelo nome
            # Usar uma abordagem mais segura com LIMIT
            cursor.execute("""
                DELETE FROM item
                WHERE id_item IN (
                    SELECT id_item FROM item 
                    WHERE id_inventario = %s AND nome = %s 
                    LIMIT %s
                )
            """, (inv_id, item_name, quantity))
            
            # Verificar se a remoção foi bem-sucedida
            if cursor.rowcount != quantity:
                print(f"❌ Erro: Esperava remover {quantity} itens, mas removeu {cursor.rowcount}")
                self.connection.rollback()
                cursor.close()
                return False
            
            # Adicionar moedas ao inventário de forma mais eficiente
            for _ in range(total_price):
                cursor.execute("""
                    INSERT INTO item (nome, peso, durabilidade, id_inventario)
                    VALUES (%s, %s, %s, %s)
                """, ("Moeda de Ouro", 0.01, 999, inv_id))
            
            self.connection.commit()
            cursor.close()
            
            # Verificar se a transação foi bem-sucedida
            new_money = self.get_player_money()
            print(f"💰 Transação concluída! Moedas recebidas: {total_price}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na venda: {e}")
            self.connection.rollback()
            return False

    def interact_with_npc(self, npc_id: int, npc_name: str, npc_type: str):
        """Interação aprimorada com NPCs"""
        self.clear_screen()
        print(f"🧙‍♂️ CONVERSANDO COM {npc_name.upper()} 🧙‍♂️")
        print("="*60)
        self.display_status()
        
        try:
            cursor = self.connection.cursor()
            
            # Buscar diálogo
            cursor.execute("SELECT dialogo FROM personagem WHERE ID_personagem = %s", (npc_id,))
            dialog_result = cursor.fetchone()
            dialog = dialog_result[0] if dialog_result else "Olá, aventureiro!"
            
            print(f"\n💬 {npc_name}: \"{dialog}\"")
            
            if npc_type == "Guia":
                self.interact_with_guide(cursor, npc_id, npc_name)
            elif npc_type == "Comerciante":
                self.interact_with_merchant(cursor, npc_id, npc_name)
            elif npc_type == "NPC":
                self.interact_with_quest_npc(cursor, npc_id, npc_name)
            
            # Atualizar quest de conversa apenas para NPCs de quest (não comerciantes)
            if npc_type == "NPC":
                cursor.execute("""
                    SELECT COUNT(*) FROM quest_progresso qp
                    WHERE qp.id_jogador = %s AND qp.id_quest = 1 
                    AND qp.progresso_atual < qp.progresso_maximo
                """, (self.current_player_id,))
                
                if cursor.fetchone()[0] > 0:
                    self.update_quest_progress('npc_talk', 1)
            
            cursor.close()
            
        except Exception as e:
            print(f"❌ Erro ao interagir com NPC: {e}")
            time.sleep(2)

    def interact_with_merchant(self, cursor, npc_id: int, npc_name: str):
        """Interação específica com Comerciantes"""
        try:
            cursor.execute("""
                SELECT c.venda_item, c.compra_item FROM comerciante c WHERE c.ID_personagem = %s
            """, (npc_id,))
            
            result = cursor.fetchone()
            if result:
                venda_item, compra_item = result
                
                # Converter strings em listas
                sell_items = [item.strip() for item in venda_item.split(",")]
                buy_items = [item.strip() for item in compra_item.split(",")]
                
                print(f"\n🛒 {npc_name}: \"Bem-vindo à minha loja!\"")
                
                choice = input("\n➤ Deseja entrar na loja? (s/n): ").strip().lower()
                if choice in ['s', 'sim', 'y', 'yes']:
                    self.show_shop(npc_name, sell_items, buy_items)
                
        except Exception as e:
            print(f"❌ Erro na interação com comerciante: {e}")

    def interact_with_guide(self, cursor, npc_id: int, npc_name: str):
        """Interação específica com Guias"""
        try:
            cursor.execute("""
                SELECT g.custo_orientacao FROM guia g WHERE g.ID_personagem = %s
            """, (npc_id,))
            
            result = cursor.fetchone()
            if result:
                custo = result[0]
                
                print(f"\n🗺️ {npc_name} oferece orientação.")
                print("\n1. 🧭 Pedir mapa da região")
                print("2. 📍 Perguntar sobre locais importantes") 
                print("3. ⚔️ Pedir dicas de combate")
                print("4. 🔮 Perguntar sobre o Palantír")
                print("5. 🚶 Despedir-se")
                
                choice = input("\n➤ O que você quer? ").strip()
                
                if choice == "1":
                    print(f"\n{npc_name}: \"Aqui está um mapa básico da região...\"")
                    print("📜 Você recebeu conhecimento sobre os caminhos!")
                    
                elif choice == "2":
                    print(f"\n{npc_name}: \"Cuidado com as criaturas que vagam por aí...\"")
                    print("\"Elas podem aparecer em qualquer lugar da Terra Média.\"")
                    
                elif choice == "3":
                    print(f"\n{npc_name}: \"Use seus ataques elementais sabiamente.\"")
                    print("\"Defender pode salvar sua vida em batalhas difíceis.\"")
                    
                elif choice == "4":
                    print(f"\n{npc_name}: \"Dizem que fragmentos do Palantír estão espalhados...\"")
                    print("\"Procure bem ao explorar cada região. São muito raros!\"")
                    
                elif choice == "5":
                    print(f"\n{npc_name}: \"Que os ventos guiem seus passos!\"")
                
                time.sleep(3)
        except Exception as e:
            print(f"❌ Erro na interação com guia: {e}")

    def create_dynamic_quest(self, quest_name: str, quest_description: str, npc_name: str, location: str) -> int:
        """Cria uma quest dinâmica baseada na missão de um NPC"""
        try:
            cursor = self.connection.cursor()
            
            # Verificar se a quest já existe
            cursor.execute("""
                SELECT id_quest FROM quest WHERE nome = %s AND quest_dinamica = TRUE
            """, (quest_name,))
            
            existing_quest = cursor.fetchone()
            if existing_quest:
                cursor.close()
                return existing_quest[0]
            
            # Criar nova quest dinâmica
            cursor.execute("""
                INSERT INTO quest (nome, descricao, recompensa_xp, recompensa_item, pre_requisito_level, tipo_quest, quest_dinamica)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_quest
            """, (
                quest_name,
                quest_description,
                150,  # XP base para quests dinâmicas
                'Recompensa Especial',  # Item base
                1,  # Level mínimo
                'NPC',  # Tipo especial para quests de NPC
                True  # Marca como quest dinâmica
            ))
            
            quest_id = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            
            return quest_id
            
        except Exception as e:
            print(f"❌ Erro ao criar quest dinâmica: {e}")
            self.connection.rollback()
            return None

    def get_quest_objectives(self, quest_name: str) -> Dict[str, Any]:
        """Retorna objetivos específicos para diferentes tipos de quests"""
        objectives = {
            "Ajude a proteger o Condado dos perigos que se aproximam": {
                "objetivo": "Derrote 2 criaturas hostis no Condado",
                "progresso_maximo": 2,
                "tipo_progresso": "creature_kill_condado",
                "recompensa_xp": 120,
                "recompensa_item": "Escudo do Condado"
            },
            "Gondor precisa de heróis para defender Osgiliath": {
                "objetivo": "Derrote 3 inimigos nas Ruínas de Osgiliath",
                "progresso_maximo": 3,
                "tipo_progresso": "creature_kill_osgiliath",
                "recompensa_xp": 200,
                "recompensa_item": "Espada de Gondor"
            },
            "Rohan enfrenta ameaças das planícies": {
                "objetivo": "Derrote 2 criaturas nas Colinas do Vento",
                "progresso_maximo": 2,
                "tipo_progresso": "creature_kill_rohan",
                "recompensa_xp": 180,
                "recompensa_item": "Lança de Rohan"
            },
            "A floresta anciã precisa de proteção": {
                "objetivo": "Derrote 2 criaturas na Floresta Sombria",
                "progresso_maximo": 2,
                "tipo_progresso": "creature_kill_floresta",
                "recompensa_xp": 160,
                "recompensa_item": "Bastão da Floresta"
            }
        }
        
        return objectives.get(quest_name, {
            "objetivo": "Complete a missão para receber recompensas",
            "progresso_maximo": 1,
            "tipo_progresso": "generic_quest",
            "recompensa_xp": 100,
            "recompensa_item": "Recompensa Especial"
        })

    def interact_with_quest_npc(self, cursor, npc_id: int, npc_name: str):
        """Interação específica com NPCs de Quest - MELHORADA"""
        try:
            cursor.execute("""
                SELECT n.quest, n.localizacao FROM npc n WHERE n.ID_personagem = %s
            """, (npc_id,))
            
            result = cursor.fetchone()
            if result:
                quest_desc, localizacao = result
                
                if quest_desc:
                    # Obter objetivos da missão
                    objetivos = self.get_quest_objectives(quest_desc)
                    
                    print(f"\n📜 **MISSÃO ESPECIAL DE {npc_name.upper()}**")
                    print("="*60)
                    print(f"🎯 **MISSÃO:** {quest_desc}")
                    print(f"📍 **LOCAL:** {localizacao}")
                    print(f"📋 **OBJETIVO:** {objetivos['objetivo']}")
                    print(f"💰 **RECOMPENSA:** {objetivos['recompensa_xp']} XP + {objetivos['recompensa_item']}")
                    print("="*60)
                    
                    print("\n1. ✅ Aceitar missão")
                    print("2. ❓ Mais detalhes")
                    print("3. 🚶 Recusar")
                    
                    choice = input("\n➤ Sua decisão: ").strip()
                    
                    if choice == "1":
                        print(f"\n{npc_name}: \"Excelente! A Terra Média precisa de heróis como você!\"")
                        print("📝 Missão aceita com sucesso!")

                        # Criar ou buscar quest dinâmica
                        quest_id = self.create_dynamic_quest(quest_desc, quest_desc, npc_name, localizacao)
                        
                        if quest_id:
                            # Verificar se já não está ativa
                            cursor.execute("""
                                SELECT COUNT(*) FROM quest_progresso WHERE id_jogador = %s AND id_quest = %s
                            """, (self.current_player_id, quest_id))
                            
                            if cursor.fetchone()[0] == 0:
                                # Iniciar a quest
                                cursor.execute("""
                                    INSERT INTO quest_progresso (id_jogador, id_quest, progresso_atual, progresso_maximo, status)
                                    VALUES (%s, %s, %s, %s, %s)
                                """, (self.current_player_id, quest_id, 0, objetivos['progresso_maximo'], 'Em Progresso'))
                                
                                # Atualizar recompensas da quest
                                cursor.execute("""
                                    UPDATE quest SET recompensa_xp = %s, recompensa_item = %s 
                                    WHERE id_quest = %s
                                """, (objetivos['recompensa_xp'], objetivos['recompensa_item'], quest_id))
                                
                                self.connection.commit()
                                print(f"🎉 **MISSÃO ATIVADA:** {quest_desc}")
                                print(f"📊 Progresso: 0/{objetivos['progresso_maximo']}")
                                print(f"🎯 Objetivo: {objetivos['objetivo']}")
                            else:
                                print("⚠️ Você já aceitou esta missão anteriormente!")
                        else:
                            print("❌ Erro ao criar missão!")
                    
                    elif choice == "2":
                        print(f"\n{npc_name}: \"Esta missão testará sua coragem e habilidade...\"")
                        print(f"\"Você precisará enfrentar os perigos em {localizacao}.\"")
                        print(f"\"{objetivos['objetivo']}\"")
                        print("\n\"Prepare-se bem antes de partir, herói!\"")
                        
                    elif choice == "3":
                        print(f"\n{npc_name}: \"Entendo. Talvez outro herói aceite este desafio...\"")
                        print("\"Pense na minha proposta. O destino pode depender disso.\"")
                else:
                    print(f"\n{npc_name}: \"Por enquanto não tenho tarefas para você.\"")
                    print("\"Mas continue sua jornada, herói!\"")
                
                time.sleep(3)
        except Exception as e:
            print(f"❌ Erro na interação com NPC de quest: {e}")

    def explore_area(self):
        """Explora área atual com criaturas aleatórias"""
        self.clear_screen()
        print("🧙‍♂️ SENHOR DOS ANÉIS - EXPLORAÇÃO 🧙‍♂️")
        print("="*60)
        self.display_status()
        self.display_scenario()
        
        try:
            cursor = self.connection.cursor()
            
            print("\n🔍 Você examina cuidadosamente a área...")
            time.sleep(1.5)
            
            # Verificar NPCs específicos do cenário
            cursor.execute("""
                SELECT p.ID_personagem, p.nome, p.dialogo,
                       CASE 
                         WHEN EXISTS(SELECT 1 FROM guia g WHERE g.ID_personagem = p.ID_personagem) THEN 'Guia'
                         WHEN EXISTS(SELECT 1 FROM comerciante c WHERE c.ID_personagem = p.ID_personagem) THEN 'Comerciante'
                         WHEN EXISTS(SELECT 1 FROM npc n WHERE n.ID_personagem = p.ID_personagem) THEN 'NPC'
                         ELSE 'Pessoa'
                       END as tipo
                FROM personagem p
                JOIN cenario_npc cn ON p.ID_personagem = cn.id_personagem
                WHERE cn.id_cenario = %s
                AND p.ID_personagem IN (
                    SELECT ID_personagem FROM guia 
                    UNION 
                    SELECT ID_personagem FROM comerciante 
                    UNION 
                    SELECT ID_personagem FROM npc
                )
                ORDER BY RANDOM()
                LIMIT 3
            """, (self.current_scenario_id,))
            
            npcs = cursor.fetchall()
            
            # Verificar criaturas aleatórias
            creatures = self.get_random_creatures_for_scenario(self.current_scenario_id)
            
            print("\n🎭 **O QUE VOCÊ ENCONTRA:**")
            print("-" * 40)
            
            options = []
            option_num = 1
            
            # Adicionar NPCs
            if npcs:
                print("👥 Pessoas por aqui:")
                for npc in npcs:
                    npc_id, nome, dialogo, tipo = npc
                    print(f"  {option_num}. {tipo} {nome}")
                    options.append(('npc', npc))
                    option_num += 1
            
            # Adicionar criaturas
            if creatures:
                print("\n👹 Criaturas avistadas:")
                for creature in creatures:
                    creature_id, nome, vida, xp = creature
                    print(f"  {option_num}. ⚔️ Combater {nome} (Vida: {vida})")
                    options.append(('creature', creature))
                    option_num += 1
            
            # Opções especiais
            print(f"\n{option_num}. 🔍 Procurar itens")
            options.append(('search', None))
            option_num += 1
            
            print(f"{option_num}. 📜 Verificar missões")
            options.append(('quests', None))
            option_num += 1
            
            print(f"{option_num}. 🚶 Voltar")
            options.append(('back', None))
            
            if not creatures:
                print("\n👀 Não há criaturas hostis nesta área no momento.")
                print("   (Você pode conversar com os habitantes locais ou explorar)")
            
            try:
                choice = int(input(f"\n➤ O que deseja fazer? (1-{len(options)}): ").strip())
                if 1 <= choice <= len(options):
                    action_type, data = options[choice - 1]
                    
                    if action_type == 'npc':
                        self.interact_with_npc(data[0], data[1], data[3])
                    elif action_type == 'creature':
                        result = self.battle_creature(data[0], data[1], data[2], data[3])
                        time.sleep(2)
                    elif action_type == 'search':
                        self.search_for_items()
                    elif action_type == 'quests':
                        self.check_quests()
                        time.sleep(3)
                    elif action_type == 'back':
                        return
                else:
                    print("❓ Opção inválida!")
                    time.sleep(1)
            except ValueError:
                print("❓ Por favor, digite um número válido!")
                time.sleep(1)
            
            cursor.close()
            
            # Regenerar mana ao explorar
            self.regenerate_mana(3)
            
        except Exception as e:
            print(f"❌ Erro ao explorar área: {e}")
            time.sleep(2)

    def check_quests(self):
        """Verifica e exibe quests ativas do jogador - MELHORADA"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT q.nome, q.descricao, qp.progresso_atual, qp.progresso_maximo, qp.status, q.quest_dinamica
                FROM quest_progresso qp
                JOIN quest q ON qp.id_quest = q.id_quest
                WHERE qp.id_jogador = %s AND qp.status = 'Em Progresso'
                ORDER BY q.quest_dinamica DESC, q.tipo_quest, q.nome
            """, (self.current_player_id,))
            
            quests = cursor.fetchall()
            
            if quests:
                print("\n📜 **MISSÕES ATIVAS**")
                print("="*60)
                
                for quest in quests:
                    nome, desc, atual, maximo, status, dinamica = quest
                    progresso_bar = "█" * atual + "░" * (maximo - atual)
                    
                    if dinamica:
                        # Para quests dinâmicas, mostrar objetivos específicos
                        objetivos = self.get_quest_objectives(nome)
                        print(f"🎯 **{nome}** (Missão de NPC)")
                        print(f"   📋 Objetivo: {objetivos['objetivo']}")
                        print(f"   📊 Progresso: [{progresso_bar}] {atual}/{maximo}")
                        print(f"   💰 Recompensa: {objetivos['recompensa_xp']} XP + {objetivos['recompensa_item']}")
                    else:
                        # Para quests estáticas
                        print(f"🎯 **{nome}**")
                        print(f"   📝 {desc}")
                        print(f"   📊 Progresso: [{progresso_bar}] {atual}/{maximo}")
                    
                    print()
            else:
                print("\n📜 Nenhuma missão ativa no momento.")
                print("💡 Dica: Converse com NPCs para receber missões!")
            
            cursor.close()
            
        except Exception as e:
            print(f"❌ Erro ao verificar quests: {e}")

    def display_scenario(self):
        """Exibe descrição imersiva do cenário atual"""
        scenario = self.get_scenario_info(self.current_scenario_id)
        if not scenario:
            return
        
        descriptions = self.get_scenario_descriptions()
        description = descriptions.get(scenario['id'], f"Região Desconhecida #{scenario['id']}")
        
        print("\n" + "="*70)
        print(description)
        print(f"🌤️ O dia está {scenario['dia']}, {scenario['sol']}")
        if scenario['chuva'] != 'Sem chuva':
            print(f"🌧️ {scenario['chuva']}")
        print("="*70)

    def display_status(self):
        """Exibe status detalhado do jogador"""
        player = self.get_player_stats()
        if player:
            money = self.get_player_money()
            print(f"\n👤 **{player['nome']}** - {player['classe']} | Nível {player['level']}")
            print(f"❤️ Vida: {player['vida']} | 💙 Mana: {player['mana']} | ⚔️ Ataque: {player['ataque']} | 💰 {money} moedas")
            print(f"🎯 {player['habilidade']} | 🛡️ Resistência: {player['resistencia']}")

    def show_inventory(self):
        """Sistema de inventário aprimorado com opção de usar/equipar itens"""
        self.clear_screen()
        print("🧙‍♂️ SENHOR DOS ANÉIS - INVENTÁRIO 🧙‍♂️")
        print("="*60)
        self.display_status()
        
        try:
            cursor = self.connection.cursor()
            # Buscar inventário completo
            cursor.execute("""
                SELECT i.pods, 
                       COALESCE(SUM(it.peso), 0) as peso_usado,
                       COUNT(it.id_item) as num_itens
                FROM inventario i
                LEFT JOIN item it ON i.id_inventario = it.id_inventario
                WHERE i.id_personagem = %s
                GROUP BY i.id_inventario, i.pods
            """, (self.current_player_id,))
            result = cursor.fetchone()
            if result:
                capacidade, peso_usado, num_itens = result
                print(f"\n🎒 **INVENTÁRIO**")
                print(f"📦 Capacidade: {peso_usado:.1f}/{capacidade} kg utilizados")
                print(f"📋 Total de itens: {num_itens}")
                # Buscar itens agrupados
                cursor.execute("""
                    SELECT it.nome, it.peso, it.durabilidade, COUNT(*) as quantidade
                    FROM item it
                    JOIN inventario inv ON it.id_inventario = inv.id_inventario
                    WHERE inv.id_personagem = %s
                    GROUP BY it.nome, it.peso, it.durabilidade
                    ORDER BY it.nome
                """, (self.current_player_id,))
                itens = cursor.fetchall()
                if itens:
                    print("\n📋 **SEUS ITENS:**")
                    print("-" * 50)
                    for i, (nome, peso, durabilidade, quantidade) in enumerate(itens, 1):
                        durability_bar = "█" * (durabilidade // 20) + "░" * (5 - durabilidade // 20)
                        if quantidade > 1:
                            print(f"{i:2d}. {nome} x{quantidade}")
                        else:
                            print(f"{i:2d}. {nome}")
                        
                        print()
                    # Opção de usar/equipar
                    print("0. Voltar")
                    print("U. Usar/Equipar item")
                    choice = input("\n➤ Escolha uma opção (número/U/0): ").strip().lower()
                    if choice == "0":
                        return
                    elif choice == "u":
                        self.use_or_equip_item(itens)
                        self.pause_and_clear()
                        return self.show_inventory()
                else:
                    print("\n📭 Seu inventário está vazio.")
            else:
                print("🎒 Inventário não encontrado.")
            cursor.close()
        except Exception as e:
            print(f"❌ Erro ao mostrar inventário: {e}")

    def use_or_equip_item(self, itens):
        """Permite ao jogador usar ou equipar um item do inventário"""
        print("\n🔧 **USAR/EQUIPAR ITEM**")
        print("-" * 40)
        for i, (nome, peso, durabilidade, quantidade) in enumerate(itens, 1):
            print(f"{i:2d}. {nome} x{quantidade}")
        print("0. Voltar")
        def normalize(text):
            return unicodedata.normalize('NFKD', text.lower().strip()).encode('ASCII', 'ignore').decode('ASCII')
        try:
            idx = int(input("\n➤ Qual item deseja usar/equipar? (número): ").strip())
            if idx == 0:
                return
            if 1 <= idx <= len(itens):
                nome, peso, durabilidade, quantidade = itens[idx-1]
                nome_norm = normalize(nome)
                if ("pocao de cura" in nome_norm) or ("pocoes de cura" in nome_norm):
                    self.consume_heal_potion(nome)
                elif ("pocao de mana" in nome_norm) or ("pocoes de mana" in nome_norm):
                    self.consume_mana_potion(nome)
                elif "espada" in nome_norm:
                    self.equip_weapon(nome)
                elif "armadura" in nome_norm:
                    self.equip_armor(nome)
                else:
                    print("❌ Este item não pode ser usado ou equipado diretamente.")
            else:
                print("❌ Opção inválida!")
        except ValueError:
            print("❌ Digite um número válido!")

    def consume_heal_potion(self, nome_item):
        """Consome uma poção de cura e recupera vida"""
        try:
            cursor = self.connection.cursor()
            # Buscar inventário
            cursor.execute("""
                SELECT id_inventario FROM inventario WHERE id_personagem = %s
            """, (self.current_player_id,))
            inv_id = cursor.fetchone()[0]
            # Remover uma poção
            cursor.execute("""
                DELETE FROM item WHERE id_inventario = %s AND nome = %s LIMIT 1
            """, (inv_id, nome_item))
            # Recuperar vida (ex: +50)
            player = self.get_player_stats()
            vida_max = player['vida_maxima']
            vida_atual = player['vida']
            nova_vida = min(vida_atual + 50, vida_max)
            self.update_player_status(vida_atual=nova_vida)
            self.connection.commit()
            cursor.close()
            print(f"❤️ Você usou {nome_item} e recuperou vida! ({vida_atual} → {nova_vida})")
        except Exception as e:
            print(f"❌ Erro ao consumir poção de cura: {e}")

    def consume_mana_potion(self, nome_item):
        """Consome uma poção de mana e recupera mana"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT id_inventario FROM inventario WHERE id_personagem = %s
            """, (self.current_player_id,))
            inv_id = cursor.fetchone()[0]
            cursor.execute("""
                DELETE FROM item WHERE id_inventario = %s AND nome = %s LIMIT 1
            """, (inv_id, nome_item))
            player = self.get_player_stats()
            mana_max = player['mana_maxima']
            mana_atual = player['mana']
            nova_mana = min(mana_atual + 40, mana_max)
            self.update_player_status(mana_atual=nova_mana)
            self.connection.commit()
            cursor.close()
            print(f"💙 Você usou {nome_item} e recuperou mana! ({mana_atual} → {nova_mana})")
        except Exception as e:
            print(f"❌ Erro ao consumir poção de mana: {e}")

    def equip_weapon(self, nome_item):
        """Equipe uma espada e aumente o ataque do jogador, removendo bônus anterior se já houver espada equipada"""
        try:
            cursor = self.connection.cursor()
            # Verificar se já há uma espada equipada
            cursor.execute("""
                SELECT tipo_equipamento FROM jogador WHERE ID_personagem = %s
            """, (self.current_player_id,))
            tipo_equip = cursor.fetchone()[0]
            # Se já há uma espada equipada, remova o bônus anterior
            if tipo_equip and "espada" in tipo_equip.lower():
                cursor.execute("""
                    UPDATE skill SET atq = atq - 20 WHERE ID_jogador = %s
                """, (self.current_player_id,))
            # Atualizar tipo_equipamento para a nova espada
            cursor.execute("""
                UPDATE jogador SET tipo_equipamento = %s WHERE ID_personagem = %s
            """, (nome_item, self.current_player_id))
            # Aplicar bônus da nova espada
            cursor.execute("""
                UPDATE skill SET atq = atq + 20 WHERE ID_jogador = %s
            """, (self.current_player_id,))
            self.connection.commit()
            cursor.close()
            print(f"⚔️ Você equipou {nome_item}! Seu ataque aumentou.")
        except Exception as e:
            print(f"❌ Erro ao equipar arma: {e}")

    def equip_armor(self, nome_item):
        """Equipe uma armadura e aumente a defesa do jogador, removendo bônus anterior se já houver armadura equipada"""
        try:
            cursor = self.connection.cursor()
            # Verificar se já há uma armadura equipada
            cursor.execute("""
                SELECT tipo_equipamento FROM jogador WHERE ID_personagem = %s
            """, (self.current_player_id,))
            tipo_equip = cursor.fetchone()[0]
            # Se já há uma armadura equipada, remova o bônus anterior
            if tipo_equip and "armadura" in tipo_equip.lower():
                cursor.execute("""
                    ALTER TABLE skill ADD COLUMN IF NOT EXISTS defesa INTEGER DEFAULT 0;
                """)
                cursor.execute("""
                    UPDATE skill SET defesa = defesa - 15 WHERE ID_jogador = %s
                """, (self.current_player_id,))
            # Atualizar tipo_equipamento para a nova armadura
            cursor.execute("""
                UPDATE jogador SET tipo_equipamento = %s WHERE ID_personagem = %s
            """, (nome_item, self.current_player_id))
            # Aplicar bônus da nova armadura
            cursor.execute("""
                ALTER TABLE skill ADD COLUMN IF NOT EXISTS defesa INTEGER DEFAULT 0;
            """)
            cursor.execute("""
                UPDATE skill SET defesa = defesa + 15 WHERE ID_jogador = %s
            """, (self.current_player_id,))
            self.connection.commit()
            cursor.close()
            print(f"🛡️ Você equipou {nome_item}! Sua defesa aumentou.")
        except Exception as e:
            print(f"❌ Erro ao equipar armadura: {e}")

    def show_navigation_options(self):
        """Menu de navegação visual"""
        scenario = self.get_scenario_info(self.current_scenario_id)
        if not scenario:
            return False
        
        self.clear_screen()
        print("🧙‍♂️ SENHOR DOS ANÉIS - NAVEGAÇÃO 🧙‍♂️")
        print("="*70)
        self.display_status()
        self.display_scenario()
        
        print("\n🧭 **MAPA LOCAL**")
        print("="*40)
        
        # Criar mapa visual simples
        directions = {
            'norte': scenario['norte'], 'sul': scenario['sul'],
            'leste': scenario['leste'], 'oeste': scenario['oeste']
        }
        
        # Norte
        north_symbol = "🔼" if directions['norte'] else "🚫"
        print(f"        {north_symbol}")
        print(f"        N")
        
        # Oeste - Centro - Leste
        west_symbol = "◀️" if directions['oeste'] else "🚫"
        east_symbol = "▶️" if directions['leste'] else "🚫"
        print(f"  {west_symbol} O   🏃 YOU   L {east_symbol}")
        
        # Sul
        south_symbol = "🔽" if directions['sul'] else "🚫"
        print(f"        S")
        print(f"        {south_symbol}")
        
        print("\n📍 **DESTINOS DISPONÍVEIS:**")
        descriptions = self.get_scenario_descriptions()
        
        for direction, scenario_id in directions.items():
            if scenario_id:
                dest_desc = descriptions.get(scenario_id, f"Área {scenario_id}")
                direction_key = direction[0].upper()
                print(f"🗺️ [{direction_key}] {direction.title()}: {dest_desc}")
        
        print("\n🔙 [V] Voltar ao menu principal")
        print("="*40)
        
        return True

    def game_loop(self):
        """Loop principal do jogo"""
        # Iniciar quest inicial apenas uma vez
        self.start_initial_quest()
        
        # Mensagem de boas-vindas épica
        player_stats = self.get_player_stats()
        if player_stats:
            print("🧙‍♂️" + "="*68 + "🧙‍♂️")
            print("    🌟 BEM-VINDO À TERRA MÉDIA, BRAVE ADVENTURER! 🌟")
            print(f"         {player_stats['nome']}, o {player_stats['classe']}")
            print("🧙‍♂️" + "="*68 + "🧙‍♂️")
            self.pause_and_clear("⚡ Pressione Enter para começar sua jornada épica...")
        
        while self.player_alive:
            self.clear_screen()
            print("🧙‍♂️ LORD OF THE RINGS - TERRA MÉDIA 🧙‍♂️")
            print("="*60)
            
            self.display_status()
            self.display_scenario()
            self.check_quests()
            
            print("\n⚔️ **AÇÕES ÉPICAS DISPONÍVEIS:**")
            print("="*40)
            print("1. 🚶 Explorar e mover-se")
            print("2. 👁️ Investigar área")
            print("3. 🎒 Verificar inventário")
            print("4. 📜 Missões ativas")
            print("5. 📊 Status completo")
            print("6. 💾 Salvar progresso")
            print("7. 🚪 Sair da aventura")
            
            choice = input("\n➤ Qual será sua próxima ação, herói? ").strip().lower()
            
            if choice in ["1", "mover", "explorar"]:
                if self.show_navigation_options():
                    while True:
                        move_choice = input("\n➤ Para onde deseja ir? (n/s/l/o/v): ").strip().lower()
                        if move_choice == 'v':
                            break
                        elif move_choice in ['n', 's', 'l', 'o']:
                            direction_map = {'n': 'norte', 's': 'sul', 'l': 'leste', 'o': 'oeste'}
                            if self.move_player(direction_map[move_choice]):
                                time.sleep(2)
                            break
                        else:
                            print("❓ Comando inválido! Use: n, s, l, o, v")
                            
            elif choice in ["2", "investigar", "area"]:
                self.explore_area()
                self.pause_and_clear()
                
            elif choice in ["3", "inventario", "inventário"]:
                self.show_inventory()
                self.pause_and_clear()
                
            elif choice in ["4", "missões", "missoes", "quests"]:
                self.clear_screen()
                print("🧙‍♂️ SENHOR DOS ANÉIS - MISSÕES 🧙‍♂️")
                print("="*60)
                self.display_status()
                self.check_quests()
                self.pause_and_clear()
                
            elif choice in ["5", "status", "stats"]:
                self.show_detailed_stats()
                self.pause_and_clear()
                
            elif choice in ["6", "salvar"]:
                self.clear_screen()
                print("💾 Salvando seu progresso épico...")
                time.sleep(1.5)
                print("✅ Jogo salvo! Sua jornada está segura.")
                time.sleep(1.5)
                
            elif choice in ["7", "sair", "quit"]:
                self.clear_screen()
                print("🌟 Sua jornada na Terra Média foi lendária!")
                print("🧙‍♂️ \"Que a luz de Eärendil brilhe em seu caminho...\"")
                print("\n👋 Até a próxima aventura, nobre herói!")
                break
                
            else:
                print("❓ Comando não reconhecido. Tente novamente.")
                self.pause_and_clear("⏸️ Pressione Enter para continuar...")

    def show_detailed_stats(self):
        """Mostra estatísticas detalhadas do jogador"""
        self.clear_screen()
        print("🧙‍♂️ SENHOR DOS ANÉIS - STATUS COMPLETO 🧙‍♂️")
        print("="*60)
        
        player = self.get_player_stats()
        if player:
            money = self.get_player_money()
            print(f"\n👑 **{player['nome'].upper()}**")
            print(f"🏛️ Classe: {player['classe']}")
            print(f"⭐ Nível: {player['level']}")
            print(f"💫 Habilidade Principal: {player['habilidade']}")
            print(f"🛡️ Resistência: {player['resistencia']}")
            print(f"💰 Dinheiro: {money} moedas")
            
            print(f"\n📊 **ATRIBUTOS DE COMBATE:**")
            print(f"❤️ Vida Máxima: {player['vida']}")
            print(f"💙 Mana Máxima: {player['mana']}")
            print(f"⚔️ Poder de Ataque: {player['ataque']}")
            
            print(f"\n🔮 **AFINIDADES ELEMENTAIS:**")
            print(f"🔥 Fogo: {player['fogo']}")
            print(f"💧 Água: {player['agua']}")
            print(f"🗿 Terra: {player['terra']}")
            print(f"💨 Ar: {player['ar']}")
            
            # Mostrar histórico
            try:
                cursor = self.connection.cursor()
                cursor.execute("""
                    SELECT COUNT(*) as vitorias FROM confronta 
                    WHERE jogador_id = %s AND vencedor = TRUE
                """, (self.current_player_id,))
                
                vitorias = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(*) as derrotas FROM confronta 
                    WHERE jogador_id = %s AND vencedor = FALSE
                """, (self.current_player_id,))
                
                derrotas = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(*) as quests_completadas FROM quest_progresso
                    WHERE id_jogador = %s AND status = 'Completada'
                """, (self.current_player_id,))
                
                quests_completadas = cursor.fetchone()[0]
                
                print(f"\n🏆 **HISTÓRICO DE AVENTURAS:**")
                print(f"✅ Vitórias em Combate: {vitorias}")
                print(f"❌ Derrotas: {derrotas}")
                print(f"📜 Missões Completadas: {quests_completadas}")
                cursor.execute("""
                    SELECT COUNT(*) as criaturas_derrotadas FROM criaturas_derrotadas
                    WHERE id_jogador = %s
                """, (self.current_player_id,))
                
                criaturas_derrotadas = cursor.fetchone()[0]
                print(f"👹 Criaturas Derrotadas: {criaturas_derrotadas}")
                if vitorias + derrotas > 0:
                    win_rate = (vitorias / (vitorias + derrotas)) * 100
                    print(f"📈 Taxa de Vitória: {win_rate:.1f}%")
                
                cursor.close()
                
            except Exception as e:
                print(f"❌ Erro ao carregar histórico: {e}")

    def start_game(self):
        """Inicialização do jogo"""
        if not self.connect_database():
            return
        
        # Configurar sistema de quests
        self.setup_quest_system()
        
        self.clear_screen()
        
        print("🧙‍♂️" + "="*68 + "🧙‍♂️")
        print("              LORD OF THE RINGS")
        print("            TERMINAL MUD GAME")
        print("         🌟 TERRA MÉDIA AWAITS 🌟")
        print("🧙‍♂️" + "="*68 + "🧙‍♂️")
        
        print("\n📜 \"Em um buraco no chão vivia um hobbit...\"")
        print("🌟 \"Mas esta é uma nova história, com um novo herói...\"")
        print("\n🎮 **OPÇÕES DE JOGO:**")
        print("1. 🆕 Forjar um novo herói")
        print("2. 📂 Continuar jornada existente")
        print("3. 🚪 Sair")
        
        choice = input("\n➤ Escolha seu destino: ").strip()
        
        if choice == "1":
            self.create_new_character()
        elif choice == "2":
            self.load_existing_character()
        elif choice == "3":
            print("\n👋 Que os ventos o levem de volta quando estiver pronto!")
            return
        else:
            print("❓ Escolha inválida!")
            self.pause_and_clear()
            self.start_game()

    def create_new_character(self):
        """Processo de criação de personagem"""
        self.clear_screen()
        print("🧙‍♂️ FORJANDO UM NOVO HERÓI 🧙‍♂️")
        print("="*50)
        
        print("📜 \"Nos salões de Mandos, uma nova alma desperta...\"")
        print("🌟 \"Qual será seu nome nesta terra?\"")
        
        name = input("\n📝 Nome do seu herói: ").strip()
        if not name:
            print("❌ Um herói precisa de um nome!")
            self.pause_and_clear()
            return self.create_new_character()
        
        # Buscar classes disponíveis
        available_classes = self.get_available_classes()
        if not available_classes:
            print("❌ Nenhuma classe encontrada no banco de dados!")
            self.pause_and_clear()
            return
        
        self.clear_screen()
        print(f"🧙‍♂️ BEM-VINDO, {name.upper()}! 🧙‍♂️")
        print("="*50)
        print("🎭 \"Escolha sua vocação na Terra Média...\"")
        print("\n⚔️ **CLASSES DISPONÍVEIS:**")
        
        for i, class_info in enumerate(available_classes, 1):
            print(f"\n{i}. {class_info['emoji']} **{class_info['name']}**")
            print(f"   {class_info['description']}")
        
        try:
            class_choice = int(input(f"\n➤ Escolha sua classe (1-{len(available_classes)}): ").strip()) - 1
            if 0 <= class_choice < len(available_classes):
                selected_class = available_classes[class_choice]
                
                if self.create_player_character(name, selected_class['table']):
                    self.pause_and_clear("⚡ Pressione Enter para começar sua lenda...")
                    self.game_loop()
            else:
                print("❌ Classe inválida!")
                self.pause_and_clear()
                self.create_new_character()
        except ValueError:
            print("❌ Por favor, digite um número válido!")
            self.pause_and_clear()
            self.create_new_character()

    def load_existing_character(self):
        """Carregamento de personagem existente"""
        self.clear_screen()
        print("🧙‍♂️ JORNADAS EXISTENTES 🧙‍♂️")
        print("="*40)
        
        # Listar personagens existentes
        existing_players = self.list_existing_players()
        if not existing_players:
            print("📭 Nenhuma jornada anterior encontrada!")
            print("🆕 Talvez seja hora de começar uma nova aventura...")
            self.pause_and_clear()
            return self.start_game()
        
        print("📜 \"Estas almas já caminharam pela Terra Média...\"")
        print("\n🏆 **HERÓIS DISPONÍVEIS:**")
        
        for i, player in enumerate(existing_players, 1):
            print(f"\n{i}. 👤 **{player['nome']}**")
            print(f"   ⚔️ {player['classe']} | ⭐ Nível {player['level']}")
            print(f"   🎯 {player['habilidade']}")
            print(f"   🏆 {player['vitorias']} vitórias")
        
        try:
            player_choice = int(input(f"\n➤ Escolha seu herói (1-{len(existing_players)}): ").strip()) - 1
            if 0 <= player_choice < len(existing_players):
                selected_player = existing_players[player_choice]['nome']
                
                if self.load_existing_player(selected_player):
                    self.pause_and_clear("⚡ Pressione Enter para continuar sua lenda...")
                    self.game_loop()
            else:
                print("❌ Herói inválido!")
                self.pause_and_clear()
                self.load_existing_character()
        except ValueError:
            print("❌ Por favor, digite um número válido!")
            self.pause_and_clear()
            self.load_existing_character()

    def list_existing_players(self) -> List[Dict[str, Any]]:
        """Lista personagens jogadores existentes"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT p.nome, p.level, p.habilidade, 
                       CASE 
                         WHEN EXISTS(SELECT 1 FROM guerreiro g WHERE g.id_personagem = p.ID_personagem) THEN 'Guerreiro'
                         WHEN EXISTS(SELECT 1 FROM mago m WHERE m.id_personagem = p.ID_personagem) THEN 'Mago'
                         WHEN EXISTS(SELECT 1 FROM arqueiro a WHERE a.id_personagem = p.ID_personagem) THEN 'Arqueiro'
                         WHEN EXISTS(SELECT 1 FROM sacerdote s WHERE s.id_personagem = p.ID_personagem) THEN 'Sacerdote'
                         ELSE 'Desconhecida'
                       END as classe,
                       (SELECT COUNT(*) FROM confronta c WHERE c.jogador_id = p.ID_personagem AND c.vencedor = TRUE) as vitorias
                FROM personagem p
                JOIN jogador j ON p.ID_personagem = j.ID_personagem
                ORDER BY p.level DESC, p.nome
            """)
            
            players = []
            for row in cursor.fetchall():
                players.append({
                    'nome': row[0], 'level': row[1], 'habilidade': row[2],
                    'classe': row[3], 'vitorias': row[4]
                })
            
            cursor.close()
            return players
            
        except Exception as e:
            print(f"❌ Erro ao listar personagens: {e}")
            return []

    def load_existing_player(self, player_name: str) -> bool:
        """Carrega um personagem existente"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT p.ID_personagem, j.cenario
                FROM personagem p
                JOIN jogador j ON p.ID_personagem = j.ID_personagem
                WHERE LOWER(p.nome) = LOWER(%s)
                LIMIT 1
            """, (player_name,))
            
            result = cursor.fetchone()
            if result:
                self.current_player_id = result[0]
                self.current_scenario_id = result[1]
                cursor.close()
                return True
            else:
                print(f"❌ Herói '{player_name}' não encontrado!")
                cursor.close()
                return False
                
        except Exception as e:
            print(f"❌ Erro ao carregar herói: {e}")
            return False

    def sell_all_items(self):
        """Vende todos os itens do jogador (exceto moedas) - NOVA FUNÇÃO"""
        try:
            cursor = self.connection.cursor()
            
            # Buscar o inventário do jogador
            cursor.execute("""
                SELECT id_inventario FROM inventario WHERE id_personagem = %s
            """, (self.current_player_id,))
            inv_result = cursor.fetchone()
            if not inv_result:
                print("❌ Inventário não encontrado!")
                cursor.close()
                return False
            inv_id = inv_result[0]

            # Contar itens para venda (exceto moedas)
            cursor.execute("""
                SELECT COUNT(*) FROM item
                WHERE id_inventario = %s AND nome NOT LIKE '%Moeda%'
            """, (inv_id,))
            total_items = cursor.fetchone()[0]
            
            if total_items == 0:
                print("❌ Você não tem itens para vender!")
                cursor.close()
                return False

            # Calcular valor total dos itens
            total_value = 0
            cursor.execute("""
                SELECT nome, COUNT(*) as quantidade
                FROM item
                WHERE id_inventario = %s AND nome NOT LIKE '%Moeda%'
                GROUP BY nome
            """, (inv_id,))
            
            items_to_sell = cursor.fetchall()
            
            # Sistema de preços (mesmo do sell_menu)
            item_prices = {
                "Espada": 8, "Adaga": 5, "Arco": 7, "Cajado": 6, "Bastão": 6, "Machado": 9,
                "Armadura": 10, "Escudo": 4, "Capacete": 3, "Botas": 2,
                "Poção": 4, "Poções": 4,
                "Ferro": 3, "Madeira": 2, "Cristal": 5, "Gema": 6, "Pedra": 1, "Ouro": 8, "Prata": 4,
                "Fragmento": 15, "Anel": 12, "Pergaminho": 3, "Runa": 8, "Palantír": 50,
                "Pão": 1, "Erva": 2, "Pele": 3, "Osso": 2, "Lemba": 2,
                "Élfico": 10, "Sagrado": 12, "Mágico": 15, "Antigo": 8
            }
            
            for nome, quantidade in items_to_sell:
                base_price = 2  # Preço padrão
                for item_type, price in item_prices.items():
                    if item_type.lower() in nome.lower():
                        base_price = price
                        break
                
                # Ajustar preço baseado na raridade
                if "Fragmento do Palantír" in nome:
                    base_price = 50
                elif "Palantír" in nome:
                    base_price = 100
                elif "Fragmento" in nome:
                    base_price = 20
                elif "Anel" in nome and ("Proteção" in nome or "Poder" in nome):
                    base_price = 25
                elif "Élfico" in nome:
                    base_price = 12
                elif "Sagrado" in nome or "Mágico" in nome:
                    base_price = 15
                
                total_value += base_price * quantidade

            # Remover todos os itens (exceto moedas)
            cursor.execute("""
                DELETE FROM item
                WHERE id_inventario = %s AND nome NOT LIKE '%Moeda%'
            """, (inv_id,))
            
            # Adicionar moedas ao inventário
            for _ in range(total_value):
                cursor.execute("""
                    INSERT INTO item (nome, peso, durabilidade, id_inventario)
                    VALUES (%s, %s, %s, %s)
                """, ("Moeda de Ouro", 0.01, 999, inv_id))
            
            self.connection.commit()
            cursor.close()
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na venda em massa: {e}")
            self.connection.rollback()
            return False

    def sell_item_quantity(self, item_id: int, item_name: str, quantity: int, total_price: int):
        """Vende uma quantidade específica de itens - MELHORADA"""
        try:
            cursor = self.connection.cursor()
            
            # Buscar o inventário do jogador
            cursor.execute("""
                SELECT id_inventario FROM inventario WHERE id_personagem = %s
            """, (self.current_player_id,))
            inv_result = cursor.fetchone()
            if not inv_result:
                print("❌ Inventário não encontrado!")
                cursor.close()
                return False
            inv_id = inv_result[0]

            # Verificar se o jogador tem a quantidade suficiente do item
            cursor.execute("""
                SELECT COUNT(*) FROM item
                WHERE id_inventario = %s AND nome = %s
            """, (inv_id, item_name))
            available_quantity = cursor.fetchone()[0]
            
            if available_quantity < quantity:
                print(f"❌ Você não tem {quantity} {item_name} para vender! (Disponível: {available_quantity})")
                cursor.close()
                return False

            # Remover a quantidade especificada de itens pelo nome
            # Usar uma abordagem mais segura com LIMIT
            cursor.execute("""
                DELETE FROM item
                WHERE id_item IN (
                    SELECT id_item FROM item 
                    WHERE id_inventario = %s AND nome = %s 
                    LIMIT %s
                )
            """, (inv_id, item_name, quantity))
            
            # Verificar se a remoção foi bem-sucedida
            if cursor.rowcount != quantity:
                print(f"❌ Erro: Esperava remover {quantity} itens, mas removeu {cursor.rowcount}")
                self.connection.rollback()
                cursor.close()
                return False
            
            # Adicionar moedas ao inventário de forma mais eficiente
            for _ in range(total_price):
                cursor.execute("""
                    INSERT INTO item (nome, peso, durabilidade, id_inventario)
                    VALUES (%s, %s, %s, %s)
                """, ("Moeda de Ouro", 0.01, 999, inv_id))
            
            self.connection.commit()
            cursor.close()
            
            # Verificar se a transação foi bem-sucedida
            new_money = self.get_player_money()
            print(f"💰 Transação concluída! Moedas recebidas: {total_price}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na venda: {e}")
            self.connection.rollback()
            return False

def main():
    """Função principal com tratamento de erros épico"""
    print("🌟 Inicializando a Terra Média...")
    time.sleep(1)
    
    game = LordOfTheRingsMUD()
    try:
        game.start_game()
    except KeyboardInterrupt:
        game.clear_screen()
        print("\n🧙‍♂️ \"Mesmo os menores podem mudar o curso do futuro...\"")
        print("👋 Sua jornada foi interrompida, mas a Terra Média o aguarda!")
        print("✨ Até nossa próxima aventura, nobre herói!")
    except Exception as e:
        game.clear_screen()
        print(f"\n💀 Um poder sombrio causou um erro inesperado:")
        print(f"🔍 {e}")
        print("🧙‍♂️ \"Nem mesmo Gandalf pode prever todos os caminhos...\"")
        print("🔄 Tente reiniciar sua jornada!")
    finally:
        if game.connection:
            game.connection.close()
            print("🔒 Conexão com os registros da Terra Média encerrada.")

if __name__ == "__main__":
    main()