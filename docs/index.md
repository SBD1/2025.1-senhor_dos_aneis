# Lord of The Rings Terminal Game

<div align="center">
  <img src="assets/imgL.png" alt="Capa" width="50%">
  <p><b>Figura 1:</b> Capa oficial do Jogo</p>
</div>

O **Lord of The Rings Terminal Game** é inspirado no universo de Senhor dos Aneis criado por J. R. R. Tolkien. Nosso objetivo é recriar a essência da série de filmes, com foco em mecânicas de exploração, gerenciamento e combate.

---

## Sobre o Projeto

Em **Lord of The Rings Terminal Game**, você assume o papel de um aventureiro, um hobbit que vive em paz na sua vila, porém, avido para viver novas aventuras e explorar a magnitude do mundo. Nosso projeto adapta essa experiência para o terminal, com funcionalidades como:

- **Exploração de masmorras**: Navegue pelas masmorras, enfrentando desafios e coletando itens valiosos.
- **Combate contra monstros**: Enfrente uma variedade de inimigos com diferentes habilidades e comportamentos.
- **Sistema de armas e armaduras**: Equipe-se com armas e armaduras que podem possuir diferentes efeitos.
- **Efeitos e habilidades especiais**: Utilize habilidades e efeitos únicos para derrotar inimigos e superar obstáculos.
- **Gerenciamento de inventário**: Organize os itens coletados durante as explorações e decida o que vender ou guardar.
- **Progressão do personagem**: Melhore as habilidades e desbloqueie novos equipamentos e funcionalidades.

A aplicação é desenvolvida em **Python**, com a lógica de dados estruturada em **PostgreSQL**, utilizando SQL puro para modelagem, triggers, views e controle de acesso.

---

# Contribuidores:

<div align="center">
  <table>
    <tr>
      <td align="center"><a href="https://github.com/FelipeFreire-gf"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/62055315?v=4" width="100px;" alt=""/><br /><sub><b>Felipe das Neves</b></sub></a><br />202046102</td>
      <td align="center"><a href="https://github.com/GabrielMEsteves"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/98546978?v=4" width="100px;" alt=""/><br /><sub><b>Gabriel Felipe</b></sub></a><br />190106956</td>
      <td align="center"><a href="https://github.com/lucaaassb"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u//82137254?v=4" width="100px;" alt=""/><br /><sub><b>Lucas Soares</b></sub></a><br />202017700</td>
      <td align="center"><a href="https://github.com/Fernandavazgit1"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/144569110?v=4" width="100px;" alt=""/><br /><sub><b>Fernanda Vaz</b></sub></a><br />221007715</td>
      <td align="center"><a href="https://github.com/yan-luca"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/108501120?v=4" width="100px;" alt=""/><br /><sub><b>Yan Luca</b></sub></a><br />211031889</td>
    </tr>
  </table>
</div>

## Estrutura do Projeto

O projeto está organizado em três ambientes principais:

- **`game/cli`**: Código da interface em terminal (Python), responsável pela interação do usuário com o sistema.
- **`game/sql`**: Lógica do banco de dados (PostgreSQL), incluindo tabelas, seeds, views, triggers e controles de acesso.
- **`apps/docs`**: Documentação do projeto, criada com MkDocs, explicando o funcionamento, decisões de arquitetura, DER/MER e instruções de uso.

Essa estrutura modular facilita o desenvolvimento e a manutenção do projeto.

---

## Como Executar

### Requisitos

- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- Banco de dados configurado com as tabelas do arquivo `DDL.sql`

### Instalação

1. Clone o repositório

Obs.: Pode ser interessante você suber ir máquina virtual para manter a integridade do SO;
Caso queira aqui está o passo a passo para a virtualização usando o python no ambiente windows:

```bash
python -m venv venv
```

Inicializar a máquina virtual:

```bash
venv/Scripts/activate
```

Após:

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

### Executando o Jogo

Para iniciar o jogo, execute:

```bash
python main.py
```

### Funcionalidades

- Criação de personagem com diferentes classes (Guerreiro, Mago, Arqueiro, Sacerdote)
- Sistema de exploração de cenários
- Sistema de inventário
- Sistema de status e características
- Salvamento automático do progresso

### Controles

- Use os números para navegar pelos menus
- Pressione ENTER para confirmar suas escolhas
- Use as setas do teclado para explorar os cenários

---

## Tabela de Versionamento

| Versão | Data       | Descrição                                     | Autor(es)                                                             | Revisor(es)                                                          |
|--------|------------|-----------------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------|
|1.0  | 02/04/2025     | Criação da página 'Home', contendo informações sobre o projeto | [Felipe das Neves](https://github.com/FelipeFreire-gf)  |Todos os Integrantes|
|1.1  | 15/06/2025     | Desenvolvimento do tópico de execução do jogo | [Lucas Soares](https://github.com/lucaaassb)  | [Felipe das Neves](https://github.com/FelipeFreire-gf) |
