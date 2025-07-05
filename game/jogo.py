import psycopg2
import os
from typing import Optional, Dict, Any, List
import time
import platform

class LordOfTheRingsGame:
    def __init__(self):
        self.connection = None
        self.current_player_id = None
        self.current_scenario_id = None
        
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
            # Configurações do banco - ajuste conforme necessário
            self.connection = psycopg2.connect(
                host="db", # Alterado para o nome do serviço no docker-compose
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
    
    def get_available_classes(self) -> List[Dict[str, str]]:
        """Busca as classes disponíveis no banco de dados"""
        try:
            cursor = self.connection.cursor()
            
            # Buscar tabelas de classes que existem no banco
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('guerreiro', 'mago', 'arqueiro', 'sacerdote')
                ORDER BY table_name
            """)
            
            classes = []
            class_descriptions = {
                'arqueiro': {'name': 'Arqueiro', 'emoji': '🏹', 'desc': 'Preciso com ataques à distância'},
                'guerreiro': {'name': 'Guerreiro', 'emoji': '🛡️', 'desc': 'Especialista em combate corpo a corpo'},
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
    
    def get_class_base_stats(self, class_name: str) -> Dict[str, Any]:
        """Busca estatísticas base de uma classe específica no banco"""
        try:
            cursor = self.connection.cursor()
            
            # Buscar um exemplo da classe para obter estatísticas típicas
            cursor.execute(f"""
                SELECT p.vida_maxima, p.mana_maxima, p.habilidade, p.resistencia
                FROM personagem p
                JOIN {class_name} c ON p.id_personagem = c.id_personagem
                LIMIT 1
            """)
            
            result = cursor.fetchone()
            if result:
                return {
                    "vida": result[0],
                    "mana": result[1], 
                    "habilidade": result[2],
                    "resistencia": result[3]
                }
            else:
                # Valores padrão se não encontrar exemplos
                defaults = {
                    "guerreiro": {"vida": 150, "mana": 80, "habilidade": "Combate", "resistencia": "Físico"},
                    "mago": {"vida": 90, "mana": 200, "habilidade": "Feitiçaria", "resistencia": "Fogo"},
                    "arqueiro": {"vida": 110, "mana": 120, "habilidade": "Precisão", "resistencia": "Ar"},
                    "sacerdote": {"vida": 120, "mana": 180, "habilidade": "Cura", "resistencia": "Luz"}
                }
                return defaults.get(class_name, defaults["guerreiro"])
            
        except Exception as e:
            print(f"❌ Erro ao buscar stats da classe: {e}")
            return {"vida": 100, "mana": 100, "habilidade": "Genérica", "resistencia": "Nenhuma"}
        finally:
            cursor.close()
    
    def get_default_scenario(self) -> int:
        """Busca o primeiro cenário disponível no banco"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id_cenario FROM cenario ORDER BY id_cenario LIMIT 1")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 1
        except Exception as e:
            print(f"❌ Erro ao buscar cenário padrão: {e}")
            return 1
    
    def create_player_character(self, name: str, character_class: str) -> bool:
        """Cria um novo personagem jogador"""
        try:
            cursor = self.connection.cursor()
            
            # Obter estatísticas da classe
            stats = self.get_class_base_stats(character_class)
            default_scenario = self.get_default_scenario()
            
            # Inserir personagem
            cursor.execute("""
                INSERT INTO personagem (nome, vida_maxima, mana_maxima, habilidade, dificuldade, level, resistencia, dialogo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING ID_personagem
            """, (name, stats["vida"], stats["mana"], stats["habilidade"], "Normal", 1, stats["resistencia"], f"Olá, sou {name}!"))
            
            player_id = cursor.fetchone()[0]
            
            # Inserir jogador
            cursor.execute("""
                INSERT INTO jogador (ID_personagem, cenario, tipo_equipamento)
                VALUES (%s, %s, %s)
            """, (player_id, default_scenario, "Equipamento Básico"))
            
            # Inserir skills básicas
            cursor.execute("""
                INSERT INTO skill (ID_jogador, atq) VALUES (%s, %s)
            """, (player_id, 50))
            
            # Inserir características elementais
            cursor.execute("""
                INSERT INTO caracteristicas (ID_jogador, fogo, agua, terra, ar)
                VALUES (%s, %s, %s, %s, %s)
            """, (player_id, 25, 25, 25, 25))
            
            # Inserir na tabela da classe específica
            if character_class == "guerreiro":
                cursor.execute("""
                    INSERT INTO guerreiro (id_personagem, atq_Fisico, bloquear_Dano)
                    VALUES (%s, %s, %s)
                """, (player_id, 70, 50))
            elif character_class == "mago":
                cursor.execute("""
                    INSERT INTO mago (id_personagem, atq_Magico, atq_MultiElemento)
                    VALUES (%s, %s, %s)
                """, (player_id, 80, 60))
            elif character_class == "arqueiro":
                cursor.execute("""
                    INSERT INTO arqueiro (id_personagem, atq_Preciso, atq_Rapido)
                    VALUES (%s, %s, %s)
                """, (player_id, 75, 70))
            elif character_class == "sacerdote":
                cursor.execute("""
                    INSERT INTO sacerdote (id_personagem, bencao_Cura, atq_Especial)
                    VALUES (%s, %s, %s)
                """, (player_id, 85, 40))
            
            # Criar inventário inicial
            cursor.execute("""
                INSERT INTO inventario (id_personagem, pods) VALUES (%s, %s)
            """, (player_id, 50))
            
            self.connection.commit()
            self.current_player_id = player_id
            self.current_scenario_id = default_scenario
            
            print(f"🎉 Personagem {name} ({character_class}) criado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar personagem: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
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
                print(f"✅ Personagem {player_name} carregado com sucesso!")
                return True
            else:
                print(f"❌ Personagem '{player_name}' não encontrado!")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao carregar personagem: {e}")
            return False
        finally:
            cursor.close()
    
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
                       END as classe
                FROM personagem p
                JOIN jogador j ON p.ID_personagem = j.ID_personagem
                ORDER BY p.nome
            """)
            
            players = []
            for row in cursor.fetchall():
                players.append({
                    'nome': row[0],
                    'level': row[1], 
                    'habilidade': row[2],
                    'classe': row[3]
                })
            
            cursor.close()
            return players
            
        except Exception as e:
            print(f"❌ Erro ao listar personagens: {e}")
            return []
    
    def get_player_info(self) -> Optional[Dict[str, Any]]:
        """Obtém informações do jogador atual"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT p.nome, p.vida_maxima, p.mana_maxima, p.level, p.habilidade, j.cenario, j.tipo_equipamento,
                       CASE 
                         WHEN EXISTS(SELECT 1 FROM guerreiro g WHERE g.id_personagem = p.ID_personagem) THEN 'Guerreiro'
                         WHEN EXISTS(SELECT 1 FROM mago m WHERE m.id_personagem = p.ID_personagem) THEN 'Mago'
                         WHEN EXISTS(SELECT 1 FROM arqueiro a WHERE a.id_personagem = p.ID_personagem) THEN 'Arqueiro'
                         WHEN EXISTS(SELECT 1 FROM sacerdote s WHERE s.id_personagem = p.ID_personagem) THEN 'Sacerdote'
                         ELSE 'Desconhecida'
                       END as classe
                FROM personagem p
                JOIN jogador j ON p.ID_personagem = j.ID_personagem
                WHERE p.ID_personagem = %s
            """, (self.current_player_id,))
            
            result = cursor.fetchone()
            if result:
                return {
                    "nome": result[0],
                    "vida": result[1],
                    "mana": result[2],
                    "level": result[3],
                    "habilidade": result[4],
                    "cenario": result[5],
                    "equipamento": result[6],
                    "classe": result[7]
                }
            return None
        except Exception as e:
            print(f"❌ Erro ao obter informações do jogador: {e}")
            return None
        finally:
            cursor.close()
    
    def get_scenario_info(self, scenario_id: int) -> Optional[Dict[str, Any]]:
        """Obtém informações do cenário atual"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT id_cenario, sol, chuva, noite, dia, norte_id, leste_id, oeste_id, sul_id
                FROM cenario WHERE id_cenario = %s
            """, (scenario_id,))
            
            result = cursor.fetchone()
            if result:
                return {
                    "id": result[0],
                    "sol": result[1],
                    "chuva": result[2],
                    "noite": result[3],
                    "dia": result[4],
                    "norte": result[5],
                    "leste": result[6],
                    "oeste": result[7],
                    "sul": result[8]
                }
            return None
        except Exception as e:
            print(f"❌ Erro ao obter informações do cenário: {e}")
            return None
        finally:
            cursor.close()
    
    def get_scenario_descriptions(self) -> Dict[int, str]:
        """Busca descrições dos cenários do banco ou usa padrões"""
        return {
            1: "🏞️ Vila do Condado - Um lugar pacífico onde hobbits vivem em harmonia.",
            2: "🌲 Floresta Sombria - Árvores antigas sussurram segredos antigos.",
            3: "⛰️ Montanhas Nevadas - Picos cobertos de neve se estendem ao horizonte.",
            4: "🏰 Ruínas Antigas - Estruturas em ruínas guardam tesouros e perigos."
        }
    
    def get_direction_preview(self, scenario_id: int) -> str:
        """Retorna uma prévia do que há na direção especificada"""
        if scenario_id is None:
            return "🚫 Caminho bloqueado"
        
        descriptions = self.get_scenario_descriptions()
        return descriptions.get(scenario_id, f"🔍 Área desconhecida #{scenario_id}")
    
    def show_navigation_options(self):
        """Mostra as opções de navegação disponíveis"""
        scenario = self.get_scenario_info(self.current_scenario_id)
        if not scenario:
            return False
        
        self.clear_screen()
        print("🧙‍♂️ LORD OF THE RINGS - NAVEGAÇÃO 🧙‍♂️")
        print("="*60)
        self.display_status()
        
        print("\n🧭 **OPÇÕES DE NAVEGAÇÃO**")
        print("="*40)
        
        # Norte
        if scenario['norte']:
            preview = self.get_direction_preview(scenario['norte'])
            print(f"🔼 [N] Norte: {preview}")
        else:
            print(f"🚫 [N] Norte: Caminho bloqueado")
        
        # Sul
        if scenario['sul']:
            preview = self.get_direction_preview(scenario['sul'])
            print(f"🔽 [S] Sul: {preview}")
        else:
            print(f"🚫 [S] Sul: Caminho bloqueado")
        
        # Leste
        if scenario['leste']:
            preview = self.get_direction_preview(scenario['leste'])
            print(f"▶️ [L] Leste: {preview}")
        else:
            print(f"🚫 [L] Leste: Caminho bloqueado")
        
        # Oeste
        if scenario['oeste']:
            preview = self.get_direction_preview(scenario['oeste'])
            print(f"◀️ [O] Oeste: {preview}")
        else:
            print(f"🚫 [O] Oeste: Caminho bloqueado")
        
        print("\n🔙 [V] Voltar ao menu principal")
        print("="*40)
        
        return True
    
    def handle_movement_input(self) -> bool:
        """Gerencia a entrada de movimento do jogador"""
        if not self.show_navigation_options():
            return False
        
        while True:
            choice = input("\n➤ Para onde deseja ir? (n/s/l/o/v): ").strip().lower()
            
            if choice == 'v':
                return False  # Voltar ao menu principal
            elif choice in ['n', 's', 'l', 'o']:
                direction_map = {
                    'n': 'norte',
                    's': 'sul', 
                    'l': 'leste',
                    'o': 'oeste'
                }
                
                direction = direction_map[choice]
                success = self.move_player(direction)
                return success
            else:
                print("❓ Comando inválido! Use: n (norte), s (sul), l (leste), o (oeste), v (voltar)")
                time.sleep(1.5)
    
    def move_player(self, direction: str) -> bool:
        """Move o jogador para uma nova direção"""
        try:
            scenario = self.get_scenario_info(self.current_scenario_id)
            if not scenario:
                return False
            
            direction_map = {
                "norte": scenario["norte"],
                "sul": scenario["sul"],
                "leste": scenario["leste"],
                "oeste": scenario["oeste"]
            }
            
            new_scenario_id = direction_map.get(direction.lower())
            if new_scenario_id is None:
                print("🚫 Não é possível ir nessa direção!")
                time.sleep(1.5)
                return False
            
            # Mostrar movimento
            direction_emoji = {
                "norte": "🔼",
                "sul": "🔽", 
                "leste": "▶️",
                "oeste": "◀️"
            }
            
            print(f"\n{direction_emoji.get(direction, '🚶')} Você se move para o {direction}...")
            time.sleep(1)
            
            # Atualizar posição do jogador no banco
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE jogador SET cenario = %s WHERE ID_personagem = %s
            """, (new_scenario_id, self.current_player_id))
            
            self.connection.commit()
            self.current_scenario_id = new_scenario_id
            
            # Mostrar chegada no novo local
            new_description = self.get_direction_preview(new_scenario_id)
            print(f"📍 Você chegou em: {new_description}")
            time.sleep(1.5)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao mover jogador: {e}")
            self.connection.rollback()
            time.sleep(2)
            return False
        finally:
            cursor.close()
    
    def examine_area(self):
        """Examina a área atual em busca de NPCs, criaturas ou itens"""
        self.clear_screen()
        print("🧙‍♂️ LORD OF THE RINGS - EXPLORAÇÃO 🧙‍♂️")
        print("="*60)
        self.display_status()
        
        try:
            cursor = self.connection.cursor()
            
            print("\n🔍 Você examina cuidadosamente a área ao redor...")
            time.sleep(1)
            
            # Buscar NPCs na área
            cursor.execute("""
                SELECT p.ID_personagem, p.nome, p.dialogo,
                       CASE 
                         WHEN EXISTS(SELECT 1 FROM guia g WHERE g.ID_personagem = p.ID_personagem) THEN 'Guia'
                         WHEN EXISTS(SELECT 1 FROM comerciante c WHERE c.ID_personagem = p.ID_personagem) THEN 'Comerciante'
                         WHEN EXISTS(SELECT 1 FROM npc n WHERE n.ID_personagem = p.ID_personagem) THEN 'NPC'
                         ELSE 'Pessoa'
                       END as tipo
                FROM personagem p
                WHERE p.ID_personagem IN (
                    SELECT ID_personagem FROM guia 
                    UNION 
                    SELECT ID_personagem FROM comerciante 
                    UNION 
                    SELECT ID_personagem FROM npc
                )
                ORDER BY RANDOM()
                LIMIT 3
            """)
            
            npcs = cursor.fetchall()
            
            if npcs:
                print("\n👥 Você encontra algumas pessoas por aqui:")
                for i, npc in enumerate(npcs, 1):
                    print(f"  {i}. {npc[3]} {npc[1]}: \"{npc[2]}\"")
                
                print(f"\n0. 🚶 Voltar")
                
                try:
                    choice = int(input("\n➤ Com quem deseja falar? ").strip())
                    if choice == 0:
                        return
                    elif 1 <= choice <= len(npcs):
                        selected_npc = npcs[choice - 1]
                        self.interact_with_npc(selected_npc[0], selected_npc[1], selected_npc[3])
                    else:
                        print("❓ Opção inválida!")
                        time.sleep(1)
                except ValueError:
                    print("❓ Por favor, digite um número válido!")
                    time.sleep(1)
            else:
                print("👀 Não há nada de especial por aqui no momento.")
                time.sleep(2)
            
            cursor.close()
            
        except Exception as e:
            print(f"❌ Erro ao examinar área: {e}")
            time.sleep(2)
    
    def interact_with_npc(self, npc_id: int, npc_name: str, npc_type: str):
        """Interage com um NPC específico"""
        self.clear_screen()
        print(f"🧙‍♂️ LORD OF THE RINGS - CONVERSANDO COM {npc_name.upper()} 🧙‍♂️")
        print("="*60)
        self.display_status()
        
        try:
            cursor = self.connection.cursor()
            
            print(f"\n💬 Conversando com {npc_name}...")
            time.sleep(1)
            
            if npc_type == "Guia":
                self.interact_with_guide(cursor, npc_id, npc_name)
            elif npc_type == "Comerciante":
                self.interact_with_merchant(cursor, npc_id, npc_name)
            elif npc_type == "NPC":
                self.interact_with_quest_npc(cursor, npc_id, npc_name)
            else:
                # Conversa genérica
                cursor.execute("SELECT dialogo FROM personagem WHERE ID_personagem = %s", (npc_id,))
                dialog = cursor.fetchone()[0]
                print(f"\n{npc_name}: \"{dialog}\"")
                print("\n(Não há mais o que fazer aqui)")
                time.sleep(2)
            
            cursor.close()
            
        except Exception as e:
            print(f"❌ Erro ao interagir com NPC: {e}")
            time.sleep(2)
    
    def interact_with_guide(self, cursor, npc_id: int, npc_name: str):
        """Interação com Guia"""
        try:
            # Buscar informações do guia
            cursor.execute("""
                SELECT g.custo_orientacao, p.dialogo
                FROM guia g
                JOIN personagem p ON g.ID_personagem = p.ID_personagem
                WHERE g.ID_personagem = %s
            """, (npc_id,))
            
            result = cursor.fetchone()
            if result:
                custo = result[0]
                dialogo = result[1]
                
                print(f"\n{npc_name}: \"{dialogo}\"")
                print(f"\n🗺️ {npc_name} oferece orientação por {custo} moedas de ouro.")
                print("\n1. 🧭 Pedir orientação sobre as direções")
                print("2. 🗺️ Perguntar sobre locais importantes")
                print("3. 💰 Perguntar sobre o custo")
                print("4. 🚶 Dispensar o guia")
                
                choice = input("\n➤ O que você quer fazer? ").strip()
                
                if choice == "1":
                    print(f"\n{npc_name}: \"As direções estão bem marcadas aqui. Olhe ao redor e verá as saídas disponíveis.\"")
                    print("📍 Você recebe informações básicas sobre navegação!")
                    
                elif choice == "2":
                    scenario = self.get_scenario_info(self.current_scenario_id)
                    if scenario:
                        print(f"\n{npc_name}: \"Você está em um local interessante. Há caminhos para diferentes regiões aqui.\"")
                        if scenario['norte']: print("   🧭 Ao norte há terras inexploradas...")
                        if scenario['sul']: print("   🧭 Ao sul você encontrará outras aventuras...")
                        if scenario['leste']: print("   🧭 A leste existem novos horizontes...")
                        if scenario['oeste']: print("   🧭 A oeste há mistérios aguardando...")
                    
                elif choice == "3":
                    print(f"\n{npc_name}: \"Meus serviços custam {custo} moedas. Um preço justo pela experiência que tenho!\"")
                    
                elif choice == "4":
                    print(f"\n{npc_name}: \"Muito bem, boa sorte em sua jornada!\"")
                
                time.sleep(3)
            
        except Exception as e:
            print(f"❌ Erro na interação com guia: {e}")
            time.sleep(2)
    
    def interact_with_merchant(self, cursor, npc_id: int, npc_name: str):
        """Interação com Comerciante"""
        try:
            # Buscar informações do comerciante
            cursor.execute("""
                SELECT c.venda_item, c.compra_item, p.dialogo
                FROM comerciante c
                JOIN personagem p ON c.ID_personagem = p.ID_personagem
                WHERE c.ID_personagem = %s
            """, (npc_id,))
            
            result = cursor.fetchone()
            if result:
                venda_item = result[0]
                compra_item = result[1]
                dialogo = result[2]
                
                print(f"\n{npc_name}: \"{dialogo}\"")
                print(f"\n🛒 **LOJA DE {npc_name.upper()}**")
                print(f"💰 Vende: {venda_item}")
                print(f"🔄 Compra: {compra_item}")
                
                print("\n1. 🛍️ Ver itens à venda")
                print("2. 💰 Vender itens")
                print("3. 💬 Conversar")
                print("4. 🚶 Sair da loja")
                
                choice = input("\n➤ O que você quer fazer? ").strip()
                
                if choice == "1":
                    print(f"\n{npc_name}: \"Aqui estão meus melhores itens:\"")
                    print(f"📦 {venda_item}")
                    print("\n💡 Sistema de compra será implementado em breve!")
                    
                elif choice == "2":
                    print(f"\n{npc_name}: \"Estou interessado em: {compra_item}\"")
                    print("💡 Sistema de venda será implementado em breve!")
                    
                elif choice == "3":
                    print(f"\n{npc_name}: \"O comércio vai bem por estas terras. Sempre há aventureiros precisando de equipamentos!\"")
                    
                elif choice == "4":
                    print(f"\n{npc_name}: \"Volte sempre! Sempre tenho novos itens chegando!\"")
                
                time.sleep(3)
            
        except Exception as e:
            print(f"❌ Erro na interação com comerciante: {e}")
            time.sleep(2)
    
    def interact_with_quest_npc(self, cursor, npc_id: int, npc_name: str):
        """Interação com NPC de Quest"""
        try:
            # Buscar informações do NPC
            cursor.execute("""
                SELECT n.quest, n.localizacao, n.hora_aparicao, p.dialogo
                FROM npc n
                JOIN personagem p ON n.ID_personagem = p.ID_personagem
                WHERE n.ID_personagem = %s
            """, (npc_id,))
            
            result = cursor.fetchone()
            if result:
                quest = result[0]
                localizacao = result[1]
                hora_aparicao = result[2]
                dialogo = result[3]
                
                print(f"\n{npc_name}: \"{dialogo}\"")
                
                if quest:
                    print(f"\n📜 **MISSÃO DISPONÍVEL**")
                    print(f"🎯 {quest}")
                    print(f"📍 Local: {localizacao}")
                    if hora_aparicao:
                        print(f"🕐 Disponível às: {hora_aparicao}")
                    
                    print("\n1. ✅ Aceitar missão")
                    print("2. ❓ Perguntar mais detalhes")
                    print("3. ❌ Recusar missão")
                    print("4. 🚶 Ir embora")
                    
                    choice = input("\n➤ O que você decide? ").strip()
                    
                    if choice == "1":
                        print(f"\n{npc_name}: \"Excelente! Estou contando com você!\"")
                        print("📝 Missão adicionada ao seu diário!")
                        print("💡 Sistema de missões será implementado completamente em breve!")
                        
                    elif choice == "2":
                        print(f"\n{npc_name}: \"Esta missão é perigosa, mas a recompensa vale a pena. Prepare-se bem!\"")
                        print("🛡️ Certifique-se de ter equipamentos adequados antes de partir.")
                        
                    elif choice == "3":
                        print(f"\n{npc_name}: \"Compreendo. Talvez outro aventureiro possa ajudar...\"")
                        
                    elif choice == "4":
                        print(f"\n{npc_name}: \"Pense sobre minha proposta. Estarei aqui se mudar de ideia.\"")
                    
                else:
                    print(f"\n{npc_name}: \"Por enquanto não tenho nenhuma tarefa para você.\"")
                
                time.sleep(3)
            
        except Exception as e:
            print(f"❌ Erro na interação com NPC de quest: {e}")
            time.sleep(2)
    
    def show_inventory(self):
        """Mostra o inventário do jogador"""
        self.clear_screen()
        print("🧙‍♂️ LORD OF THE RINGS - INVENTÁRIO 🧙‍♂️")
        print("="*60)
        self.display_status()
        
        try:
            cursor = self.connection.cursor()
            
            # Buscar inventário do jogador
            cursor.execute("""
                SELECT i.pods, COUNT(it.id_item) as num_itens
                FROM inventario i
                LEFT JOIN item it ON i.id_inventario = it.id_inventario
                WHERE i.id_personagem = %s
                GROUP BY i.id_inventario, i.pods
            """, (self.current_player_id,))
            
            result = cursor.fetchone()
            if result:
                capacidade = result[0]
                num_itens = result[1] if result[1] else 0
                
                print(f"\n🎒 **INVENTÁRIO**")
                print(f"📦 Capacidade: {num_itens}/{capacidade} pods utilizados")
                
                if num_itens > 0:
                    # Buscar itens específicos
                    cursor.execute("""
                        SELECT it.nome, it.peso, it.durabilidade
                        FROM item it
                        JOIN inventario inv ON it.id_inventario = inv.id_inventario
                        WHERE inv.id_personagem = %s
                    """, (self.current_player_id,))
                    
                    itens = cursor.fetchall()
                    print("\n📋 Itens:")
                    for item in itens:
                        print(f"  • {item[0]} (Peso: {item[1]}, Durabilidade: {item[2]})")
                else:
                    print("\n📭 Seu inventário está vazio.")
            else:
                print("🎒 Inventário não encontrado.")
            
            cursor.close()
            
        except Exception as e:
            print(f"❌ Erro ao mostrar inventário: {e}")
        
        time.sleep(2)
    
    def display_scenario(self):
        """Exibe a descrição do cenário atual"""
        scenario = self.get_scenario_info(self.current_scenario_id)
        if not scenario:
            return
        
        descriptions = self.get_scenario_descriptions()
        base_description = descriptions.get(scenario['id'], f"Cenário {scenario['id']}")
        
        print("\n" + "="*60)
        print(f"📍 **LOCALIZAÇÃO ATUAL**")
        print(f"{base_description}")
        print(f"🌤️ Clima: {scenario['dia']} com {scenario['sol']}")
        if scenario['chuva'] != 'Sem chuva':
            print(f"🌧️ {scenario['chuva']}")
        print("="*60)
    
    def display_status(self):
        """Exibe o status do jogador"""
        player = self.get_player_info()
        if player:
            print(f"\n👤 {player['nome']} ({player['classe']}) | Nível {player['level']} | ❤️ {player['vida']} | 💙 {player['mana']}")
            print(f"🎯 Habilidade: {player['habilidade']} | ⚔️ {player['equipamento']}")
    
    def game_loop(self):
        """Loop principal do jogo"""
        self.clear_screen()
        
        while True:
            # Exibir cabeçalho do jogo
            print("🧙‍♂️ LORD OF THE RINGS TERMINAL GAME 🧙‍♂️")
            print("="*60)
            
            self.display_status()
            self.display_scenario()
            
            print("\n📋 Ações disponíveis:")
            print("1. 🚶 Mover (norte/sul/leste/oeste)")
            print("2. 👁️ Examinar área")
            print("3. 🎒 Ver inventário")
            print("4. 💾 Salvar jogo")
            print("5. 🚪 Sair do jogo")
            
            choice = input("\n➤ O que você deseja fazer? ").strip().lower()
            
            if choice in ["1", "mover"]:
                moved = self.handle_movement_input()
                if moved:
                    self.clear_screen()
                else:
                    self.pause_and_clear("⏸️ Pressione Enter para continuar...")
                    
            elif choice in ["2", "examinar"]:
                self.examine_area()
                self.pause_and_clear("⏸️ Pressione Enter para voltar ao menu principal...")
                
            elif choice in ["3", "inventário", "inventario"]:
                self.show_inventory()
                self.pause_and_clear("⏸️ Pressione Enter para voltar ao menu principal...")
                
            elif choice in ["4", "salvar"]:
                self.clear_screen()
                print("🧙‍♂️ LORD OF THE RINGS - SALVANDO 🧙‍♂️")
                print("="*60)
                print("💾 Jogo salvo automaticamente!")
                time.sleep(1.5)
                self.clear_screen()
                
            elif choice in ["5", "sair"]:
                self.clear_screen()
                print("👋 Obrigado por jogar! Até a próxima aventura!")
                break
                
            else:
                print("❓ Comando não reconhecido. Tente novamente.")
                self.pause_and_clear("⏸️ Pressione Enter para continuar...")
    
    def start_game(self):
        """Inicia o jogo"""
        if not self.connect_database():
            return
        
        self.clear_screen()
        
        print("🧙‍♂️ LORD OF THE RINGS TERMINAL GAME 🧙‍♂️")
        print("="*60)
        print("🎮 Bem-vindo ao Lord of the Rings!")
        print("\n1. 🆕 Criar novo personagem")
        print("2. 📂 Carregar personagem existente")
        
        choice = input("\n➤ Escolha uma opção: ").strip()
        
        if choice == "1":
            self.clear_screen()
            print("👤 CRIAÇÃO DE PERSONAGEM")
            print("="*30)
            name = input("📝 Nome do seu personagem: ").strip()
            
            # Buscar classes disponíveis do banco
            available_classes = self.get_available_classes()
            if not available_classes:
                print("❌ Nenhuma classe encontrada no banco de dados!")
                self.pause_and_clear()
                return
            
            print("\n⚔️ Escolha sua classe:")
            for i, class_info in enumerate(available_classes, 1):
                print(f"{i}. {class_info['emoji']} {class_info['name']} - {class_info['description']}")
            
            try:
                class_choice = int(input("➤ Escolha (número): ").strip()) - 1
                if 0 <= class_choice < len(available_classes):
                    selected_class = available_classes[class_choice]['table']
                    
                    if self.create_player_character(name, selected_class):
                        print(f"\n🎉 Bem-vindo à Terra Média, {name}!")
                        self.pause_and_clear("⏸️ Pressione Enter para começar sua aventura...")
                        self.game_loop()
                else:
                    print("❌ Opção inválida!")
                    self.pause_and_clear()
            except ValueError:
                print("❌ Por favor, digite um número válido!")
                self.pause_and_clear()
        
        elif choice == "2":
            self.clear_screen()
            # Listar personagens existentes
            existing_players = self.list_existing_players()
            if not existing_players:
                print("❌ Nenhum personagem encontrado! Crie um novo personagem.")
                self.pause_and_clear()
                return
            
            print("📂 PERSONAGENS DISPONÍVEIS")
            print("="*30)
            for i, player in enumerate(existing_players, 1):
                print(f"{i}. {player['nome']} ({player['classe']}) - Nível {player['level']}")
            
            try:
                player_choice = int(input("➤ Escolha um personagem (número): ").strip()) - 1
                if 0 <= player_choice < len(existing_players):
                    selected_player = existing_players[player_choice]['nome']
                    if self.load_existing_player(selected_player):
                        self.pause_and_clear("⏸️ Pressione Enter para continuar sua aventura...")
                        self.game_loop()
                else:
                    print("❌ Opção inválida!")
                    self.pause_and_clear()
            except ValueError:
                print("❌ Por favor, digite um número válido!")
                self.pause_and_clear()
        
        else:
            print("❓ Opção inválida!")
            self.pause_and_clear()

def main():
    """Função principal"""
    game = LordOfTheRingsGame()
    try:
        game.start_game()
    except KeyboardInterrupt:
        game.clear_screen()
        print("\n👋 Jogo interrompido. Até logo!")
    except Exception as e:
        game.clear_screen()
        print(f"\n❌ Erro inesperado: {e}")
    finally:
        if game.connection:
            game.connection.close()

if __name__ == "__main__":
    main()