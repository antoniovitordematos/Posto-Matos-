
from conexao import conectar
from dados import tipos_combustivel
from utils import validar_cpf, formatar_cpf, validar_numero_positivo, iniciais


def converter_numero(valor):
    """Converte um número digitado com ponto ou vírgula decimal."""
    return float(valor.strip().replace(",", "."))


def cadastrar_abastecimento():
    """Cadastra um cliente e registra seu abastecimento no PostgreSQL."""
    print("\n--- NOVO ABASTECIMENTO ---")

    nome = input("Nome do cliente: ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        return

    cpf = input("CPF (somente números): ").strip()
    if not validar_cpf(cpf):
        print("CPF inválido. Digite 11 números.")
        return

    print("\nTipos de combustível disponíveis:")
    for i, tipo in enumerate(tipos_combustivel, 1):
        print(f"  {i}. {tipo}")

    opcao = input("Escolha o número do combustível: ").strip()
    if not opcao.isdigit() or not (1 <= int(opcao) <= len(tipos_combustivel)):
        print("Opção inválida.")
        return

    combustivel = tipos_combustivel[int(opcao) - 1]

    litros_txt = input("Quantidade de litros: ").strip()
    preco_txt = input("Preço por litro (R$): ").strip()

    if not validar_numero_positivo(litros_txt):
        print("Quantidade de litros inválida.")
        return

    if not validar_numero_positivo(preco_txt):
        print("Preço por litro inválido.")
        return

    try:
        litros = converter_numero(litros_txt)
        preco = converter_numero(preco_txt)
        total = round(litros * preco, 2)

        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO clientes (nome, cpf)
                    VALUES (%s, %s)
                    ON CONFLICT (cpf) DO NOTHING
                    """,
                    (nome, cpf)
                )

                cursor.execute(
                    "SELECT id FROM clientes WHERE cpf = %s",
                    (cpf,)
                )
                cliente_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO abastecimentos
                    (cliente_id, combustivel, litros, preco_litro, valor_total)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (cliente_id, combustivel, litros, preco, total)
                )

        print(f"\nAbastecimento registrado! Total: R$ {total:.2f}")

    except Exception as erro:
        print(f"Erro ao cadastrar abastecimento: {erro}")


def listar_abastecimentos():
    """Lista os abastecimentos registrados no banco de dados."""
    try:
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT a.id, c.nome, c.cpf, a.combustivel,
                           a.litros, a.preco_litro, a.valor_total
                    FROM abastecimentos a
                    JOIN clientes c ON c.id = a.cliente_id
                    ORDER BY a.id
                    """
                )
                registros = cursor.fetchall()

        if not registros:
            print("\nNenhum abastecimento cadastrado.")
            return

        print("\n--- LISTA DE ABASTECIMENTOS ---")
        print(
            f"{'ID':<5} {'Iniciais':<10} {'Nome':<20} "
            f"{'CPF':<15} {'Combustível':<22} "
            f"{'Litros':<10} {'Total':<10}"
        )
        print("-" * 100)

        for r in registros:
            cpf_fmt = formatar_cpf(r[2])
            print(
                f"{r[0]:<5} {iniciais(r[1]):<10} {r[1]:<20} "
                f"{cpf_fmt:<15} {r[3]:<22} "
                f"{float(r[4]):<10.2f} R$ {float(r[6]):<10.2f}"
            )

    except Exception as erro:
        print(f"Erro ao listar abastecimentos: {erro}")


def buscar_abastecimento():
    """Busca abastecimentos pelo ID ou CPF do cliente."""
    termo = input("\nDigite o ID do abastecimento ou CPF: ").strip()

    if not termo:
        print("Digite um ID ou CPF.")
        return

    try:
        with conectar() as conn:
            with conn.cursor() as cursor:
                if termo.isdigit() and len(termo) != 11:
                    cursor.execute(
                        """
                        SELECT a.id, c.nome, c.cpf, a.combustivel,
                               a.litros, a.valor_total
                        FROM abastecimentos a
                        JOIN clientes c ON c.id = a.cliente_id
                        WHERE a.id = %s
                        ORDER BY a.id
                        """,
                        (int(termo),)
                    )
                else:
                    cursor.execute(
                        """
                        SELECT a.id, c.nome, c.cpf, a.combustivel,
                               a.litros, a.valor_total
                        FROM abastecimentos a
                        JOIN clientes c ON c.id = a.cliente_id
                        WHERE c.cpf = %s
                        ORDER BY a.id
                        """,
                        (termo,)
                    )

                registros = cursor.fetchall()

        if not registros:
            print("Nenhum registro encontrado.")
            return

        print("\n--- RESULTADO DA BUSCA ---")
        for r in registros:
            print(f"ID: {r[0]}")
            print(f"Cliente: {r[1]}")
            print(f"CPF: {formatar_cpf(r[2])}")
            print(f"Combustível: {r[3]}")
            print(f"Litros: {float(r[4]):.2f}")
            print(f"Total: R$ {float(r[5]):.2f}")
            print("-" * 35)

    except Exception as erro:
        print(f"Erro ao buscar abastecimento: {erro}")


def editar_abastecimento():
    """Permite editar os dados de um abastecimento existente."""
    id_txt = input("\nDigite o ID do abastecimento: ").strip()

    if not id_txt.isdigit():
        print("ID inválido.")
        return

    try:
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT a.id, a.cliente_id, c.nome, a.combustivel,
                           a.litros, a.preco_litro, c.cpf
                    FROM abastecimentos a
                    JOIN clientes c ON c.id = a.cliente_id
                    WHERE a.id = %s
                    """,
                    (int(id_txt),)
                )
                registro = cursor.fetchone()

                if not registro:
                    print("Registro não encontrado.")
                    return

                abastecimento_id, cliente_id, nome, combustivel, litros, preco, cpf = registro

                print(f"\nEditando abastecimento de: {nome}")
                novo_nome = input(f"Nome [{nome}]: ").strip()
                if not novo_nome:
                    novo_nome = nome

                print("\nTipos de combustível:")
                for i, tipo in enumerate(tipos_combustivel, 1):
                    print(f"  {i}. {tipo}")

                opcao = input(
                    f"Combustível atual: {combustivel} — novo número (Enter mantém): "
                ).strip()

                if opcao.isdigit() and 1 <= int(opcao) <= len(tipos_combustivel):
                    combustivel = tipos_combustivel[int(opcao) - 1]

                litros_txt = input(f"Litros [{litros}]: ").strip()
                preco_txt = input(f"Preço por litro [{preco}]: ").strip()

                if litros_txt:
                    if not validar_numero_positivo(litros_txt):
                        print("Quantidade de litros inválida.")
                        return
                    litros = converter_numero(litros_txt)

                if preco_txt:
                    if not validar_numero_positivo(preco_txt):
                        print("Preço inválido.")
                        return
                    preco = converter_numero(preco_txt)

                total = round(float(litros) * float(preco), 2)

                cursor.execute(
                    "UPDATE clientes SET nome = %s WHERE id = %s",
                    (novo_nome, cliente_id)
                )

                cursor.execute(
                    """
                    UPDATE abastecimentos
                    SET combustivel = %s, litros = %s,
                        preco_litro = %s, valor_total = %s
                    WHERE id = %s
                    """,
                    (combustivel, litros, preco, total, abastecimento_id)
                )

        print(f"Registro atualizado! Novo total: R$ {total:.2f}")

    except Exception as erro:
        print(f"Erro ao editar abastecimento: {erro}")


def deletar_abastecimento():
    """Exclui um abastecimento após confirmação."""
    id_txt = input("\nDigite o ID do abastecimento: ").strip()

    if not id_txt.isdigit():
        print("ID inválido.")
        return

    try:
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT a.id, c.nome, a.combustivel, a.valor_total
                    FROM abastecimentos a
                    JOIN clientes c ON c.id = a.cliente_id
                    WHERE a.id = %s
                    """,
                    (int(id_txt),)
                )
                registro = cursor.fetchone()

                if not registro:
                    print("Registro não encontrado.")
                    return

                print(
                    f"\nAbastecimento: {registro[1]} — {registro[2]} "
                    f"— R$ {float(registro[3]):.2f}"
                )
                confirmacao = input(
                    "Tem certeza que deseja deletar? (s/n): "
                ).strip().lower()

                if confirmacao == "s":
                    cursor.execute(
                        "DELETE FROM abastecimentos WHERE id = %s",
                        (int(id_txt),)
                    )
                    print("Registro deletado com sucesso.")
                else:
                    print("Operação cancelada.")

    except Exception as erro:
        print(f"Erro ao deletar abastecimento: {erro}")


def relatorio_por_combustivel():
    """Exibe o total arrecadado por tipo de combustível."""
    try:
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT combustivel, SUM(valor_total), COUNT(*)
                    FROM abastecimentos
                    GROUP BY combustivel
                    ORDER BY combustivel
                    """
                )
                registros = cursor.fetchall()

        print("\n--- RELATÓRIO POR COMBUSTÍVEL ---")

        if not registros:
            print("Nenhum abastecimento cadastrado.")
            return

        total_geral = 0.0

        for combustivel, total, quantidade in registros:
            total = float(total)
            total_geral += total
            print(
                f"{combustivel:<25} "
                f"Abastecimentos: {quantidade:<5} "
                f"Total: R$ {total:.2f}"
            )

        print(f"\nTOTAL GERAL: R$ {total_geral:.2f}")

    except Exception as erro:
        print(f"Erro ao gerar relatório: {erro}")
