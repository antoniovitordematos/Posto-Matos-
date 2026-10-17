# Posto Matos — Sistema de Controle de Abastecimentos

## 1. Descrição do projeto

O Posto Matos é um sistema desenvolvido em Python para gerenciar abastecimentos de um posto de combustíveis. O sistema permite cadastrar, listar, buscar, editar e excluir abastecimentos, além de gerar relatórios por tipo de combustível.

A aplicação possui autenticação de usuários e utiliza um banco de dados PostgreSQL para armazenar as informações.

## 2. Tecnologias utilizadas

- Python
- PostgreSQL 18
- Psycopg
- python-dotenv
- pgAdmin 4
- Visual Studio Code

## 3. Funcionalidades

- Cadastro e autenticação de usuários.
- Cadastro de abastecimentos.
- Listagem dos abastecimentos registrados.
- Busca por identificador do abastecimento ou CPF do cliente.
- Edição de abastecimentos.
- Exclusão de abastecimentos.
- Relatórios por tipo de combustível.
- Cálculo do valor total do abastecimento.
- Relacionamento entre clientes e abastecimentos por chave estrangeira.
- Armazenamento das senhas dos usuários em formato de hash.

## 4. Estrutura do projeto

- `main.py`: menu principal e controle do sistema.
- `auth.py`: cadastro inicial e autenticação de usuários.
- `conexao.py`: conexão com o banco de dados PostgreSQL.
- `crud.py`: funções de cadastro, consulta, edição, exclusão e relatórios.
- `dados.py`: dados auxiliares, incluindo os tipos de combustível.
- `utils.py`: funções auxiliares.
- `teste_conexao.py`: teste da conexão com o banco de dados.
- `banco.sql`: comandos SQL para criação das tabelas.
- `README.md`: documentação do projeto.
- `.gitignore`: define arquivos que não devem ser enviados ao GitHub.
- `.env`: armazena localmente a senha do banco de dados e não deve ser publicado.

## 5. Banco de dados

Nome do banco de dados: `posto_matos`

O sistema utiliza as seguintes tabelas:

- **clientes:** armazena os dados dos clientes, como nome e CPF.
- **abastecimentos:** armazena os dados dos abastecimentos, incluindo combustível, quantidade de litros, preço por litro, valor total e data.
- **usuarios:** armazena os dados necessários para autenticação dos usuários.

A tabela `abastecimentos` possui a coluna `cliente_id`, que funciona como chave estrangeira relacionada à chave primária `id` da tabela `clientes`.

Esse relacionamento permite associar cada abastecimento ao respectivo cliente.

## 6. Instalação

Para executar o projeto, é necessário ter o Python e o PostgreSQL instalados no computador.

Abra o terminal na pasta do projeto e instale as bibliotecas utilizadas:

```bash
python -m pip install "psycopg[binary]" python-dotenv
```

## 7. Configuração do banco de dados

Crie o banco de dados `posto_matos` no PostgreSQL.

Em seguida, utilize o arquivo `banco.sql` para criar as tabelas necessárias, caso ainda não existam.

Na pasta principal do projeto, crie um arquivo chamado `.env` e adicione:

```text
DB_PASSWORD=sua_senha_do_postgresql
```

Substitua `sua_senha_do_postgresql` pela senha configurada no seu PostgreSQL.

O arquivo `conexao.py` utiliza essa variável para estabelecer a conexão com o banco de dados.

**Importante:** o arquivo `.env` contém informações confidenciais e não deve ser enviado ao GitHub. O arquivo `.gitignore` está configurado para ignorá-lo.

## 8. Execução do sistema

Depois de configurar o banco de dados e instalar as dependências, execute o seguinte comando no terminal:

```bash
python main.py
```

O sistema apresentará uma tela de login. Após a autenticação, será exibido o menu principal com as opções de cadastro, consulta, edição, exclusão e relatório de abastecimentos.

## 9. Credenciais para teste

As credenciais abaixo foram testadas e permitem acessar o sistema neste ambiente:

- **Usuário:** `play`
- **Senha:** `12345678`

Essas credenciais são destinadas à demonstração e à avaliação das funcionalidades do projeto.

Para utilizar o projeto em outro banco de dados, será necessário garantir que esse usuário esteja cadastrado ou criar um novo usuário pelo mecanismo de autenticação disponível no sistema.

## 10. Testes realizados

Durante os testes, foram verificadas as seguintes funcionalidades:

- Conexão com o PostgreSQL.
- Login com usuário e senha válidos.
- Recusa de acesso com credenciais incorretas.
- Cadastro de abastecimentos.
- Busca de abastecimentos.
- Edição de registros.
- Relatórios por tipo de combustível.
- Exclusão de abastecimentos.

## 11. Repositório

O código-fonte do projeto será disponibilizado no GitHub.

**Link do repositório:** adicionar o endereço do repositório após a publicação.