import psycopg2
import os
from time import sleep
from colorama import init, Fore, Style

# Inicializa o colorama para cores no terminal
init()

class JogoSenhorDosAneis:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.jogador_atual = None
        self.conectar_banco()

    def conectar_banco(self):
        try:
            self.conn = psycopg2.connect(
                dbname="senhor_dos_aneis",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432"
            )
            self.cursor = self.conn.cursor()
            print(f"{Fore.GREEN}Conexão com o banco de dados estabelecida com sucesso!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro ao conectar ao banco de dados: {e}{Style.RESET_ALL}")
            exit(1)

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_titulo(self):
        self.limpar_tela()
        print(f"{Fore.YELLOW}{'='*50}")
        print(f"{Fore.YELLOW}O SENHOR DOS ANÉIS - RPG DE TEXTO")
        print(f"{Fore.YELLOW}{'='*50}{Style.RESET_ALL}\n")

    def menu_principal(self):
        while True:
            self.mostrar_titulo()
            print(f"{Fore.CYAN}1. Novo Jogo")
            print("2. Carregar Jogo")
            print("3. Sair{Style.RESET_ALL}")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.criar_personagem()
            elif opcao == "2":
                self.carregar_jogo()
            elif opcao == "3":
                print(f"\n{Fore.YELLOW}Obrigado por jogar!{Style.RESET_ALL}")
                break
            else:
                print(f"\n{Fore.RED}Opção inválida!{Style.RESET_ALL}")
                sleep(1)

    def criar_personagem(self):
        self.mostrar_titulo()
        print(f"{Fore.CYAN}Criação de Personagem{Style.RESET_ALL}\n")
        
        nome = input("Digite o nome do seu personagem: ")
        
        print("\nEscolha sua classe:")
        print("1. Guerreiro")
        print("2. Mago")
        print("3. Arqueiro")
        print("4. Sacerdote")
        
        classe = input("\nEscolha uma classe (1-4): ")
        
        # Inserir personagem no banco
        try:
            self.cursor.execute("""
                INSERT INTO personagem (nome, vida_maxima, mana_maxima, habilidade, dificuldade, level, resistencia)
                VALUES (%s, 100, 100, 'Iniciante', 'Normal', 1, 'Nenhuma')
                RETURNING ID_personagem
            """, (nome,))
            
            id_personagem = self.cursor.fetchone()[0]
            
            # Inserir na tabela jogador
            self.cursor.execute("""
                INSERT INTO jogador (ID_personagem, cenario, tipo_equipamento)
                VALUES (%s, 1, 'Básico')
            """, (id_personagem,))
            
            # Inserir na tabela específica da classe
            if classe == "1":
                self.cursor.execute("""
                    INSERT INTO guerreiro (id_personagem, atq_Fisico, bloquear_Dano)
                    VALUES (%s, 10, 5)
                """, (id_personagem,))
            elif classe == "2":
                self.cursor.execute("""
                    INSERT INTO mago (id_personagem, atq_Magico, atq_MultiElemento)
                    VALUES (%s, 15, 5)
                """, (id_personagem,))
            elif classe == "3":
                self.cursor.execute("""
                    INSERT INTO arqueiro (id_personagem, atq_Preciso, atq_Rapido)
                    VALUES (%s, 12, 8)
                """, (id_personagem,))
            elif classe == "4":
                self.cursor.execute("""
                    INSERT INTO sacerdote (id_personagem, bencao_Cura, atq_Especial)
                    VALUES (%s, 15, 5)
                """, (id_personagem,))
            
            self.conn.commit()
            print(f"\n{Fore.GREEN}Personagem criado com sucesso!{Style.RESET_ALL}")
            sleep(2)
            self.jogar(id_personagem)
            
        except Exception as e:
            self.conn.rollback()
            print(f"\n{Fore.RED}Erro ao criar personagem: {e}{Style.RESET_ALL}")
            sleep(2)

    def carregar_jogo(self):
        self.mostrar_titulo()
        print(f"{Fore.CYAN}Carregar Jogo{Style.RESET_ALL}\n")
        
        try:
            self.cursor.execute("""
                SELECT p.ID_personagem, p.nome, p.level
                FROM personagem p
                JOIN jogador j ON p.ID_personagem = j.ID_personagem
                ORDER BY p.nome
            """)
            
            personagens = self.cursor.fetchall()
            
            if not personagens:
                print(f"{Fore.YELLOW}Nenhum personagem encontrado!{Style.RESET_ALL}")
                sleep(2)
                return
            
            print("Personagens disponíveis:")
            for i, (id_personagem, nome, level) in enumerate(personagens, 1):
                print(f"{i}. {nome} (Nível {level})")
            
            escolha = input("\nEscolha um personagem (número) ou 0 para voltar: ")
            
            if escolha == "0":
                return
            
            try:
                escolha = int(escolha)
                if 1 <= escolha <= len(personagens):
                    id_personagem = personagens[escolha-1][0]
                    self.jogar(id_personagem)
                else:
                    print(f"\n{Fore.RED}Opção inválida!{Style.RESET_ALL}")
                    sleep(1)
            except ValueError:
                print(f"\n{Fore.RED}Opção inválida!{Style.RESET_ALL}")
                sleep(1)
                
        except Exception as e:
            print(f"\n{Fore.RED}Erro ao carregar personagens: {e}{Style.RESET_ALL}")
            sleep(2)

    def jogar(self, id_personagem):
        self.jogador_atual = id_personagem
        while True:
            self.mostrar_titulo()
            self.mostrar_status()
            
            print(f"\n{Fore.CYAN}1. Explorar")
            print("2. Inventário")
            print("3. Status")
            print("4. Salvar e Sair{Style.RESET_ALL}")
            
            opcao = input("\nEscolha uma ação: ")
            
            if opcao == "1":
                self.explorar()
            elif opcao == "2":
                self.mostrar_inventario()
            elif opcao == "3":
                self.mostrar_status_detalhado()
            elif opcao == "4":
                print(f"\n{Fore.YELLOW}Jogo salvo!{Style.RESET_ALL}")
                sleep(1)
                break
            else:
                print(f"\n{Fore.RED}Opção inválida!{Style.RESET_ALL}")
                sleep(1)

    def mostrar_status(self):
        try:
            self.cursor.execute("""
                SELECT p.nome, p.level, p.vida_maxima, p.mana_maxima
                FROM personagem p
                WHERE p.ID_personagem = %s
            """, (self.jogador_atual,))
            
            nome, level, vida, mana = self.cursor.fetchone()
            
            print(f"{Fore.GREEN}Nome: {nome}")
            print(f"Nível: {level}")
            print(f"Vida: {vida}")
            print(f"Mana: {mana}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}Erro ao carregar status: {e}{Style.RESET_ALL}")

    def mostrar_status_detalhado(self):
        self.mostrar_titulo()
        self.mostrar_status()
        
        try:
            # Buscar características
            self.cursor.execute("""
                SELECT fogo, agua, terra, ar
                FROM caracteristicas
                WHERE ID_jogador = %s
            """, (self.jogador_atual,))
            
            caracteristicas = self.cursor.fetchone()
            if caracteristicas:
                fogo, agua, terra, ar = caracteristicas
                print(f"\n{Fore.YELLOW}Características:")
                print(f"Fogo: {fogo}")
                print(f"Água: {agua}")
                print(f"Terra: {terra}")
                print(f"Ar: {ar}{Style.RESET_ALL}")
            
            input("\nPressione ENTER para continuar...")
            
        except Exception as e:
            print(f"{Fore.RED}Erro ao carregar características: {e}{Style.RESET_ALL}")
            sleep(2)

    def mostrar_inventario(self):
        self.mostrar_titulo()
        print(f"{Fore.CYAN}Inventário{Style.RESET_ALL}\n")
        
        try:
            self.cursor.execute("""
                SELECT i.nome, i.peso, i.durabilidade,
                       a.dano, ar.defesa
                FROM inventario inv
                JOIN item i ON i.id_inventario = inv.id_inventario
                LEFT JOIN arma a ON i.id_item = a.id_item
                LEFT JOIN armadura ar ON i.id_item = ar.id_item
                WHERE inv.id_personagem = %s
            """, (self.jogador_atual,))
            
            itens = self.cursor.fetchall()
            
            if not itens:
                print(f"{Fore.YELLOW}Seu inventário está vazio!{Style.RESET_ALL}")
            else:
                for item in itens:
                    nome, peso, durabilidade, dano, defesa = item
                    print(f"{Fore.GREEN}Nome: {nome}")
                    print(f"Peso: {peso}")
                    print(f"Durabilidade: {durabilidade}")
                    if dano:
                        print(f"Dano: {dano}")
                    if defesa:
                        print(f"Defesa: {defesa}")
                    print(f"{Style.RESET_ALL}")
            
            input("\nPressione ENTER para continuar...")
            
        except Exception as e:
            print(f"{Fore.RED}Erro ao carregar inventário: {e}{Style.RESET_ALL}")
            sleep(2)

    def explorar(self):
        self.mostrar_titulo()
        print(f"{Fore.CYAN}Explorando...{Style.RESET_ALL}\n")
        
        try:
            # Buscar cenário atual
            self.cursor.execute("""
                SELECT c.id_cenario, c.sol, c.chuva, c.noite, c.dia,
                       c.norte_id, c.leste_id, c.oeste_id, c.sul_id
                FROM jogador j
                JOIN cenario c ON j.cenario = c.id_cenario
                WHERE j.ID_personagem = %s
            """, (self.jogador_atual,))
            
            cenario = self.cursor.fetchone()
            if not cenario:
                print(f"{Fore.RED}Erro ao carregar cenário!{Style.RESET_ALL}")
                return
            
            id_cenario, sol, chuva, noite, dia, norte, leste, oeste, sul = cenario
            
            print(f"{Fore.YELLOW}Cenário Atual:")
            print(f"Clima: {sol}")
            print(f"Período: {dia}{Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}Direções disponíveis:")
            if norte: print("1. Norte")
            if leste: print("2. Leste")
            if oeste: print("3. Oeste")
            if sul: print("4. Sul")
            print("5. Voltar{Style.RESET_ALL}")
            
            direcao = input("\nEscolha uma direção: ")
            
            if direcao == "5":
                return
            
            novo_cenario = None
            if direcao == "1" and norte:
                novo_cenario = norte
            elif direcao == "2" and leste:
                novo_cenario = leste
            elif direcao == "3" and oeste:
                novo_cenario = oeste
            elif direcao == "4" and sul:
                novo_cenario = sul
            
            if novo_cenario:
                self.cursor.execute("""
                    UPDATE jogador
                    SET cenario = %s
                    WHERE ID_personagem = %s
                """, (novo_cenario, self.jogador_atual))
                self.conn.commit()
                print(f"\n{Fore.GREEN}Movendo para o novo cenário...{Style.RESET_ALL}")
                sleep(1)
            else:
                print(f"\n{Fore.RED}Direção inválida!{Style.RESET_ALL}")
                sleep(1)
            
        except Exception as e:
            print(f"{Fore.RED}Erro ao explorar: {e}{Style.RESET_ALL}")
            sleep(2)

if __name__ == "__main__":
    jogo = JogoSenhorDosAneis()
    jogo.menu_principal() 