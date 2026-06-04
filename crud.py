# crud.py — Operações CRUD do Posto Matos

from dados import abastecimentos, cpfs_cadastrados, tipos_combustivel
from utils import validar_cpf, formatar_cpf, validar_numero_positivo, iniciais


def cadastrar_abastecimento():
    """Cadastra um novo abastecimento no sistema."""
    print("\n--- NOVO ABASTECIMENTO ---")

    nome = input("Nome do cliente: ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        return

    cpf = input("CPF (somente números): ").strip()
    if not validar_cpf(cpf):
        print("CPF inválido. Digite 11 números.")
        return

    if cpf in cpfs_cadastrados:
        print("Atenção: CPF já possui cadastro. Registrando novo abastecimento.")

    print("\nTipos de combustível disponíveis:")
    for i, tipo in enumerate(tipos_combustivel, 1):
        print(f"  {i}. {tipo}")

    opcao = input("Escolha o número do combustível: ").strip()
    if not opcao.isdigit() or not (1 <= int(opcao) <= len(tipos_combustivel)):
        print("Opção inválida.")
        return

    combustivel = tipos_combustivel[int(opcao) - 1]

    litros = input("Quantidade de litros: ").strip()
    if not validar_numero_positivo(litros):
        print("Quantidade inválida.")
        return

    preco = input("Preço por litro (R$): ").strip()
    if not validar_numero_positivo(preco):
        print("Preço inválido.")
        return

    litros = float(litros)
    preco = float(preco)
    total = litros * preco

    novo_id = len(abastecimentos) + 1

    registro = {
        "id": novo_id,
        "nome": nome,
        "iniciais": iniciais(nome),
        "cpf": cpf,
        "combustivel": combustivel,
        "litros": litros,
        "preco_litro": preco,
        "total": total
    }

    abastecimentos.append(registro)
    cpfs_cadastrados.add(cpf)

    print(f"\n Abastecimento registrado! Total: R$ {total:.2f}")


def listar_abastecimentos():
    """Lista todos os abastecimentos cadastrados em formato de tabela."""
    if not abastecimentos:
        print("\nNenhum abastecimento cadastrado.")
        return

    print("\n--- LISTA DE ABASTECIMENTOS ---")
    print(f"{'ID':<5} {'Iniciais':<10} {'Nome':<20} {'CPF':<15} {'Combustível':<20} {'Litros':<8} {'Total':<10}")
    print("-" * 90)

    for registro in abastecimentos:
        cpf_fmt = formatar_cpf(registro["cpf"])
        print(f"{registro['id']:<5} {registro['iniciais']:<10} {registro['nome']:<20} {cpf_fmt:<15} {registro['combustivel']:<20} {registro['litros']:<8.2f} R$ {registro['total']:<10.2f}")


def buscar_abastecimento():
    """Busca um abastecimento por ID ou CPF."""
    print("\n--- BUSCAR ABASTECIMENTO ---")
    termo = input("Digite o ID ou CPF do cliente: ").strip()

    # List comprehension — filtra registros pelo ID ou CPF
    resultado = [r for r in abastecimentos if str(r["id"]) == termo or r["cpf"] == termo]

    if not resultado:
        print("Nenhum registro encontrado.")
        return

    print(f"\n{'ID':<5} {'Nome':<20} {'CPF':<15} {'Combustível':<20} {'Litros':<8} {'Total':<10}")
    print("-" * 80)
    for r in resultado:
        cpf_fmt = formatar_cpf(r["cpf"])
        print(f"{r['id']:<5} {r['nome']:<20} {cpf_fmt:<15} {r['combustivel']:<20} {r['litros']:<8.2f} R$ {r['total']:<10.2f}")


def editar_abastecimento():
    """Edita os dados de um abastecimento existente."""
    print("\n--- EDITAR ABASTECIMENTO ---")
    id_busca = input("Digite o ID do abastecimento: ").strip()

    registro = None
    for r in abastecimentos:
        if str(r["id"]) == id_busca:
            registro = r
            break

    if not registro:
        print("Registro não encontrado.")
        return

    print(f"\nEditando abastecimento de: {registro['nome']}")
    print("Deixe em branco para manter o valor atual.\n")

    novo_nome = input(f"Nome [{registro['nome']}]: ").strip()
    if novo_nome:
        registro["nome"] = novo_nome
        registro["iniciais"] = iniciais(novo_nome)

    print("\nTipos de combustível:")
    for i, tipo in enumerate(tipos_combustivel, 1):
        print(f"  {i}. {tipo}")
    opcao = input(f"Combustível atual: {registro['combustivel']} — novo número (ou Enter): ").strip()
    if opcao.isdigit() and 1 <= int(opcao) <= len(tipos_combustivel):
        registro["combustivel"] = tipos_combustivel[int(opcao) - 1]

    novo_litros = input(f"Litros [{registro['litros']}]: ").strip()
    if validar_numero_positivo(novo_litros):
        registro["litros"] = float(novo_litros)

    novo_preco = input(f"Preço por litro [{registro['preco_litro']}]: ").strip()
    if validar_numero_positivo(novo_preco):
        registro["preco_litro"] = float(novo_preco)

    registro["total"] = registro["litros"] * registro["preco_litro"]
    print(f"\n Registro atualizado! Novo total: R$ {registro['total']:.2f}")


def deletar_abastecimento():
    """Remove um abastecimento por ID com confirmação do usuário."""
    print("\n--- DELETAR ABASTECIMENTO ---")
    id_busca = input("Digite o ID do abastecimento: ").strip()

    registro = None
    for r in abastecimentos:
        if str(r["id"]) == id_busca:
            registro = r
            break

    if not registro:
        print("Registro não encontrado.")
        return

    print(f"\nAbastecimento encontrado: {registro['nome']} — {registro['combustivel']} — R$ {registro['total']:.2f}")
    confirmacao = input("Tem certeza que deseja deletar? (s/n): ").strip().lower()

    if confirmacao == "s":
        abastecimentos.remove(registro)
        print("0 Registro deletado com sucesso.")
    else:
        print("Operação cancelada.")


def relatorio_por_combustivel():
    """Gera relatório com total arrecadado por tipo de combustível."""
    if not abastecimentos:
        print("\nNenhum abastecimento cadastrado.")
        return

    print("\n--- RELATÓRIO: TOTAL POR COMBUSTÍVEL ---")

    # Dict comprehension — cria resumo com total por combustível
    resumo = {tipo: 0.0 for tipo in tipos_combustivel}

    for r in abastecimentos:
        resumo[r["combustivel"]] += r["total"]

    for tipo, total in resumo.items():
        print(f"  {tipo:<25} R$ {total:.2f}")

    total_geral = sum(resumo.values())
    print(f"\n  {'TOTAL GERAL':<25} R$ {total_geral:.2f}")