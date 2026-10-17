
-- Banco de dados: Posto Matos
-- SGBD: PostgreSQL

CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS abastecimentos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    combustivel VARCHAR(30) NOT NULL,
    litros NUMERIC(10, 2) NOT NULL CHECK (litros > 0),
    preco_litro NUMERIC(10, 2) NOT NULL CHECK (preco_litro > 0),
    valor_total NUMERIC(10, 2) NOT NULL CHECK (valor_total > 0),
    data_abastecimento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_abastecimento_cliente
        FOREIGN KEY (cliente_id)
        REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL
);
