
-- Indicadores gerais do posto
SELECT COUNT(*) AS total_abastecimentos, SUM(valor_total) AS faturamento_total, MAX(valor_total) AS maior_abastecimento, MIN(valor_total) AS menor_abastecimento
FROM abastecimentos;


-- Faturamento por tipo de combustivel
SELECT combustivel, SUM(valor_total) AS faturamento, COUNT(*) AS quantidade
FROM abastecimentos
GROUP BY combustivel
ORDER BY faturamento DESC;


-- Combustiveis com pelo menos dois abastecimentos
SELECT combustivel, COUNT(*) AS quantidade
FROM abastecimentos
GROUP BY combustivel
HAVING COUNT(*) >= 2;


-- Clientes com gastos acima da media de gastos por cliente
SELECT c.nome, SUM(a.valor_total) AS total_gasto
FROM clientes c
INNER JOIN abastecimentos a ON c.id = a.cliente_id
GROUP BY c.id, c.nome
HAVING SUM(a.valor_total) > (
    SELECT AVG(total_cliente)
    FROM (
        SELECT SUM(valor_total) AS total_cliente
        FROM abastecimentos
        GROUP BY cliente_id
    ) AS media_clientes
);


-- Historico de abastecimentos com identificacao dos clientes
SELECT c.nome, c.cpf, a.combustivel, a.litros, a.preco_litro, a.valor_total, a.data_abastecimento
FROM clientes c
INNER JOIN abastecimentos a ON c.id = a.cliente_id
ORDER BY a.data_abastecimento DESC;
