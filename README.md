# Posto Matos — Sistema de Controle de Abastecimentos

## 1. Descrição do sistema

O Posto Matos é um sistema desenvolvido em Python para gerenciar os abastecimentos de um posto de combustível. Ele permite cadastrar, consultar, editar e excluir registros, além de gerar relatórios por tipo de combustível. O sistema também possui cadastro e login de usuários.

## 2. Tecnologias utilizadas

- Python
- PostgreSQL 18
- Psycopg
- python-dotenv
- SQL
- Visual Studio Code (VS Code)

## 3. Funcionalidades

- Cadastro e login de usuários.
- Cadastro de abastecimentos.
- Listagem dos abastecimentos registrados.
- Busca de abastecimentos por identificador.
- Edição e exclusão de registros.
- Relatórios por tipo de combustível.
- Consulta de abastecimentos relacionados aos clientes.

## 4. Estrutura do banco de dados

O sistema utiliza o banco de dados `posto_matos`, composto por três tabelas principais:

- **clientes:** armazena o identificador, o nome e o CPF dos clientes.
- **abastecimentos:** armazena o cliente relacionado, o tipo de combustível, a quantidade de litros, o preço por litro, o valor total e a data do abastecimento.
- **usuarios:** armazena os dados necessários para a autenticação dos usuários.

A tabela `abastecimentos` possui a chave estrangeira `cliente_id`, que referencia a chave primária `id` da tabela `clientes`. Essa relação permite identificar o cliente de cada abastecimento.

## 5. Configuração do banco de dados

1. Instale o PostgreSQL e abra o pgAdmin 4.
2. Crie um banco de dados chamado `posto_matos`.
3. Execute o arquivo `banco.sql` para criar as tabelas necessárias.
4. Crie um arquivo `.env` na pasta do projeto com a seguinte configuração:

```env
DB_PASSWORD=sua_senha_do_postgresql
```

Substitua `sua_senha_do_postgresql` pela senha utilizada na sua instalação do PostgreSQL.

O arquivo `.env` não deve ser enviado ao GitHub, pois contém informações confidenciais.

## 6. Instalação e execução

Abra o terminal na pasta do projeto e instale as dependências:

```bash
python -m pip install "psycopg[binary]" python-dotenv
```

Para iniciar o sistema, execute:

```bash
python main.py
```

Na primeira utilização, siga as instruções apresentadas para cadastrar um usuário, caso ainda não exista um usuário cadastrado no banco de dados.

## 7. Organização dos arquivos

- `main.py`: inicia o sistema e apresenta o menu principal.
- `conexao.py`: realiza a conexão com o PostgreSQL.
- `auth.py`: gerencia o cadastro e o login dos usuários.
- `crud.py`: contém as operações de cadastro, consulta, edição, exclusão e os relatórios.
- `dados.py`: reúne funções relacionadas aos dados do sistema.
- `utils.py`: contém funções auxiliares.
- `banco.sql`: contém os comandos SQL para criação das tabelas.
- `teste_conexao.py`: verifica a conexão com o banco de dados.
- `.gitignore`: define os arquivos que não devem ser enviados ao GitHub.
- `.env`: armazena localmente a senha de acesso ao banco de dados.
- `README.md`: apresenta as informações e instruções do projeto.

## 8. Usuário e senha para teste

- **Usuário:** `play`
- **Senha:** `12345678`

Essas credenciais foram utilizadas nos testes do sistema no banco de dados local. Em outra instalação, é necessário cadastrar o usuário correspondente no banco de dados.

## 9. Repositório no GitHub

[Posto Matos — GitHub](https://github.com/antoniovitordematos/Posto-Matos-)