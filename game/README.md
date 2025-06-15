# O Senhor dos Anéis - RPG de Texto

Um jogo de RPG baseado no universo de O Senhor dos Anéis, desenvolvido em Python com interface via terminal.

## Requisitos

- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- Banco de dados configurado com as tabelas do arquivo `DDL.sql`

## Instalação

1. Clone o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o banco de dados:

   - Crie um banco de dados chamado `senhor_dos_aneis`
   - Execute o arquivo `DDL.sql` para criar as tabelas
   - Execute o arquivo `DML.sql` para inserir os dados iniciais

4. Configure as credenciais do banco de dados no arquivo `main.py`:

```python
self.conn = psycopg2.connect(
    dbname="senhor_dos_aneis",
    user="seu_usuario",
    password="sua_senha",
    host="localhost",
    port="5432"
)
```

## Executando o Jogo

Para iniciar o jogo, execute:

```bash
python main.py
```

## Funcionalidades

- Criação de personagem com diferentes classes (Guerreiro, Mago, Arqueiro, Sacerdote)
- Sistema de exploração de cenários
- Sistema de inventário
- Sistema de status e características
- Salvamento automático do progresso

## Controles

- Use os números para navegar pelos menus
- Pressione ENTER para confirmar suas escolhas
- Use as setas do teclado para explorar os cenários

## Contribuindo

Sinta-se à vontade para contribuir com o projeto através de pull requests ou reportando issues.
