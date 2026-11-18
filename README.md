
# Posto Matos — Sistema de Gerenciamento de Abastecimentos

## 1. Sobre o projeto

O Posto Matos é um sistema desenvolvido em Python, integrado ao banco de dados PostgreSQL, para gerenciar clientes e abastecimentos de um posto de combustíveis.

O sistema possui duas formas de utilização: pelo terminal e por uma interface gráfica desenvolvida com Tkinter.

Além das operações de cadastro, consulta, edição e exclusão, o projeto conta com um Dashboard que apresenta indicadores e gráficos gerados a partir de consultas SQL ao banco de dados.

## 2. Funcionalidades

- Login com usuário e senha.
- Cadastro de clientes e abastecimentos.
- Consulta e listagem de abastecimentos.
- Pesquisa por ID do abastecimento, CPF ou nome do cliente.
- Edição de registros cadastrados.
- Exclusão de abastecimentos.
- Cálculo automático do valor total do abastecimento.
- Numeração sequencial dos registros na interface gráfica.
- Relatório de faturamento por tipo de combustível no terminal.
- Dashboard com indicadores de desempenho.
- Gráficos de faturamento e quantidade de abastecimentos.
- Atualização dos dados do Dashboard.
- Integração com o banco de dados PostgreSQL.

## 3. Dashboard

O Dashboard foi desenvolvido com Tkinter e Matplotlib, utilizando consultas SQL para apresentar os dados cadastrados no PostgreSQL.

### 3.1. Indicadores (KPIs)

O Dashboard apresenta quatro indicadores:

1. Total de abastecimentos: quantidade de abastecimentos registrados.
2. Faturamento total: soma dos valores dos abastecimentos.
3. Maior abastecimento: maior valor individual registrado.
4. Menor abastecimento: menor valor individual registrado.

Os indicadores utilizam as funções SQL COUNT(), SUM(), MAX() e MIN().

### 3.2. Gráficos

O Dashboard apresenta dois tipos de gráficos:

- Gráfico de barras: demonstra o faturamento por tipo de combustível.
- Gráfico de pizza: demonstra a distribuição da quantidade de abastecimentos por combustível.

Os gráficos utilizam os dados retornados por consultas SQL com GROUP BY.

### 3.3. Atualização dos dados

O Dashboard possui um botão de atualização.

Ao clicar em "Atualizar Dashboard", o sistema realiza novas consultas ao PostgreSQL e atualiza os indicadores e gráficos conforme os registros existentes no banco de dados.

## 4. Tecnologias utilizadas

- Python
- Tkinter
- Matplotlib
- PostgreSQL
- Psycopg
- python-dotenv
- Git e GitHub
- Visual Studio Code

## 5. Estrutura dos arquivos

- `main.py` — sistema executado pelo terminal.
- `interface.py` — interface gráfica para gerenciamento de abastecimentos.
- `dashboard.py` — Dashboard com indicadores e gráficos.
- `auth.py` — autenticação de usuários.
- `conexao.py` — conexão com o banco PostgreSQL.
- `crud.py` — operações de cadastro, consulta, edição e exclusão.
- `dados.py` — dados e opções utilizados pelo sistema.
- `utils.py` — funções auxiliares.
- `banco.sql` — comandos SQL de estrutura e preparação do banco.
- `consultas_dashboard.sql` — consultas SQL utilizadas para análise dos dados.
- `teste_conexao.py` — arquivo para testar a conexão com o banco.
- `README.md` — documentação do projeto.
- `.gitignore` — arquivos ignorados pelo Git.
- `.env` — configurações locais de conexão, não publicado no GitHub.

## 6. Banco de dados

O sistema utiliza o PostgreSQL, com o banco de dados denominado `posto_matos`.

As principais tabelas são:

### 6.1. Clientes

Armazena os dados dos clientes cadastrados.

Campos principais:
- id
- nome
- cpf

### 6.2. Abastecimentos

Armazena os abastecimentos realizados pelos clientes.

Campos principais:
- id
- cliente_id
- combustivel
- litros
- preco_litro
- valor_total
- data_abastecimento

### 6.3. Usuários

Armazena as informações utilizadas na autenticação do sistema.

Campos principais:
- id
- nome
- usuario
- senha_hash

As tabelas clientes e abastecimentos possuem relacionamento por chave estrangeira.

## 7. Consultas SQL

O projeto utiliza consultas SQL para realizar operações de gerenciamento e gerar informações para o Dashboard.

O arquivo `consultas_dashboard.sql` contém consultas que demonstram o uso dos seguintes recursos:

- COUNT(): contagem de registros.
- SUM(): soma de valores.
- MIN(): identificação do menor valor.
- MAX(): identificação do maior valor.
- GROUP BY: agrupamento dos abastecimentos por combustível.
- HAVING: aplicação de condições sobre os grupos.
- SUBQUERY: utilização de consultas internas para análise de dados.
- JOIN: relacionamento entre as tabelas clientes e abastecimentos.

Essas consultas permitem obter informações sobre faturamento, quantidade de abastecimentos e gastos dos clientes.

## 8. Configuração do banco de dados

O banco utilizado pelo sistema é `posto_matos`.

A conexão está configurada para utilizar:

- Host: localhost
- Porta: 5432
- Banco: posto_matos
- Usuário PostgreSQL: postgres

No arquivo `.env`, localizado na pasta do projeto, configure:

```env
DB_PASSWORD=sua_senha_do_postgresql
```

Substitua `sua_senha_do_postgresql` pela senha utilizada no seu ambiente.

O arquivo `.env` contém uma informação sensível e não deve ser publicado no GitHub.

Certifique-se de que o PostgreSQL esteja em execução e de que as tabelas tenham sido criadas conforme o arquivo `banco.sql`.

## 9. Instruções para execução

### 9.1. Instalação das dependências

Com o Python instalado, abra o terminal do VS Code na pasta do projeto e execute:

```bash
python -m pip install "psycopg[binary]" python-dotenv matplotlib
```

### 9.2. Preparação do banco de dados

Inicie o PostgreSQL e verifique se o banco `posto_matos` está criado.

Caso necessário, utilize os comandos disponíveis no arquivo `banco.sql` para preparar as tabelas.

Configure o arquivo `.env` conforme explicado anteriormente.

### 9.3. Execução da interface gráfica

Para iniciar a interface gráfica, execute:

```bash
python interface.py
```

A tela de login será exibida.

Após a autenticação, o usuário poderá cadastrar, consultar, editar, pesquisar e excluir abastecimentos.

Para visualizar os indicadores e gráficos, clique no botão "Dashboard".

### 9.4. Execução pelo terminal

Para executar a versão textual do sistema, utilize:

```bash
python main.py
```

Após a autenticação, o menu principal será exibido, permitindo realizar as operações CRUD e consultar o relatório por combustível.

### 9.5. Acesso ao Dashboard

Na interface gráfica:

1. Realize o login.
2. Acesse a tela principal do Posto Matos.
3. Clique no botão "Dashboard".
4. Visualize os quatro indicadores e os dois gráficos.
5. Clique em "Atualizar Dashboard" para consultar os dados mais recentes do banco.

## 10. Usuário e senha para teste

O sistema exige autenticação com usuário e senha cadastrados no PostgreSQL.

Para realizar os testes, utilize uma conta previamente cadastrada na tabela `usuarios`.

Por segurança, não publique senhas reais ou credenciais de acesso ao banco de dados no repositório público.

## 11. Objetivo do projeto

O objetivo do Posto Matos é aplicar os conhecimentos de programação e banco de dados no desenvolvimento de um sistema funcional de gerenciamento de abastecimentos.

O projeto demonstra a integração entre Python e PostgreSQL, a utilização de operações CRUD, o relacionamento entre tabelas e a criação de consultas SQL para análise de informações.

O Dashboard complementa o sistema, permitindo visualizar indicadores e gráficos que auxiliam no acompanhamento dos abastecimentos e do faturamento do posto.
