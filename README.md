# Posto Matos — Sistema de Gerenciamento de Abastecimentos

## 1. Sobre o projeto

O Posto Matos é um sistema desenvolvido em Python com banco de dados PostgreSQL para gerenciar clientes e abastecimentos de um posto de combustíveis.

O sistema possui duas formas de utilização: pelo terminal e por uma interface gráfica desenvolvida com Tkinter.

## 2. Funcionalidades

- Login com usuário e senha.
- Cadastro de clientes e abastecimentos.
- Consulta e listagem de abastecimentos.
- Pesquisa por ID do abastecimento, CPF ou nome do cliente.
- Edição de registros cadastrados.
- Exclusão de abastecimentos.
- Cálculo automático do valor total do abastecimento.
- Integração com banco de dados PostgreSQL.

## 3. Tecnologias utilizadas

- Python
- Tkinter
- PostgreSQL
- Psycopg
- python-dotenv
- Git e GitHub

## 4. Arquivos do projeto

- `main.py` — sistema executado pelo terminal.
- `interface.py` — interface gráfica para gerenciamento de abastecimentos.
- `auth.py` — autenticação de usuários.
- `conexao.py` — conexão com o banco de dados.
- `crud.py` — operações de cadastro, consulta, edição e exclusão.
- `dados.py` — dados e opções utilizados pelo sistema.
- `utils.py` — funções auxiliares.
- `banco.sql` — comandos SQL para criação e preparação do banco de dados.
- `.gitignore` — arquivos ignorados pelo Git.

## 5. Configuração do banco de dados

O sistema utiliza o PostgreSQL e o banco de dados `posto_matos`.

No arquivo `.env`, localizado na pasta do projeto, configure a senha do usuário PostgreSQL:

```env
DB_PASSWORD=sua_senha_do_postgresql
```

Substitua `sua_senha_do_postgresql` pela senha configurada no seu ambiente.

Certifique-se de que o PostgreSQL esteja em execução e de que o banco de dados e as tabelas tenham sido criados conforme os comandos disponíveis em `banco.sql`.

O arquivo `.env` deve permanecer no computador e não deve ser enviado ao GitHub.

## 6. Instruções para execução

### 6.1. Instalação das dependências

Com o Python instalado, abra o terminal do VS Code na pasta do projeto e execute:

```bash
pip install "psycopg[binary]" python-dotenv
```

### 6.2. Preparação do banco de dados

Inicie o PostgreSQL e verifique se o banco `posto_matos` e suas tabelas estão criados.

Configure o arquivo `.env` conforme explicado na seção anterior. Caso o banco ainda não esteja preparado, utilize os comandos de `banco.sql`.

### 6.3. Execução da interface gráfica

Para iniciar a interface gráfica, execute:

```bash
python interface.py
```

A tela de login será exibida. Informe o usuário e a senha cadastrados no banco de dados.

Após a autenticação, será possível acessar as funções de cadastro, consulta, edição e exclusão de abastecimentos.

### 6.4. Execução pelo terminal

Para executar a versão textual do sistema, utilize:

```bash
python main.py
```

Após a autenticação, o menu principal será exibido no terminal, permitindo utilizar as funcionalidades disponíveis.

## 7. Usuário e senha para teste

Utilize as credenciais abaixo para acessar o sistema:

- **Usuário:** `play`
- **Senha:** `12345678`


