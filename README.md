 
![](https://static.wikia.nocookie.net/dublagem/images/7/73/O_Senhor_dos_An%C3%A9is_Logo_PT.png/revision/latest?cb=20240308035242&path-prefix=pt-br)

## 🧙‍♂️ Projeto – Banco de Dados 1

Este projeto foi desenvolvido como parte da disciplina **Sistema Banco de Dados 1** (2025.1) e tem como objetivo aplicar os principais conceitos de modelagem em banco de dados. Inspirado no universo de **O Senhor dos Anéis**, a modelagem inicial possui, relacionamentos e interações que poderiam existir nesse mundo fictício, como personagens, batalhas, itens e cenários.

A proposta da primeira entrega envolve:

- Diagrama Entidade Entidade Relacionamento
- Modelo Entidade Relacionamento
- Modelo Relacional
- Dicionário de Dados

Realizada 02/05/2025

A proposta da segunda entrega:

- Data Definition Language
- Data Manipulation Language
- Data Query Language

Realizada 14/06/2025

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

## Integrantes do Grupo

| Nome               | Matrícula   | GitHub                                     |
|--------------------|-------------|--------------------------------------------|
| [Felipe das Neves Freire](https://github.com/FelipeFreire-gf)     | 202046102  | [@FelipeFreire-gf](https://github.com/FelipeFreire-gf)     |
| [Gabriel Felipe Mesquita Esteves](https://github.com/beltranop)       | 190106956  | [@GabrielMEsteves](https://github.com/GabrielMEsteves)         |
| [Lucas Soares Barros](https://github.com/lucaaassb)       | 202017700  | [@lucaaassb](https://github.com/lucaaassb)   |
| [Fernanda Vaz Duarte dos Santos](https://github.com/Fernandavazgit1)         | 221007715 | [@Fernandavazgit1](https://github.com/Fernandavazgit1)       |
| [Yan Luca Viana de Araújo Fontenele](https://github.com/yan-luca)         | 211031889 | [@yan-luca](https://github.com/yan-luca)       |

## 🔗 Link para o GitHub Pages

Acesse a documentação e demais detalhes do projeto no link abaixo:

➡️ [GitHub Pages – Senhor dos Anéis](https://sbd1.github.io/2025.1-senhor_dos_aneis/)

---

> *"Mesmo a menor das pessoas pode mudar o curso do futuro."* – Galadriel
