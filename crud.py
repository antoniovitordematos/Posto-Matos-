# crud.py — Operações CRUD do sistema Posto Matos
# CRUD significa: Create (Criar), Read (Ler), Update (Atualizar), Delete (Deletar).
# Este arquivo contém todas as funções que manipulam os dados de abastecimento.
 
# Importa as estruturas de dados definidas em dados.py
from dados import abastecimentos, cpfs_cadastrados, tipos_combustivel
 
# Importa as funções auxiliares definidas em utils.py
from utils import validar_cpf, formatar_cpf, validar_numero_positivo, iniciais
 
 
def cadastrar_abastecimento():
    """
    CREATE — Cadastra um novo abastecimento no sistema.
    Solicita ao usuário: nome, CPF, tipo de combustível, litros e preço por litro.
    Valida cada campo antes de salvar. Calcula o total automaticamente.
    """
    print("\n--- NOVO ABASTECIMENTO ---")
 
    # Solicita e valida o nome do cliente
    nome = input("Nome do cliente: ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        return
 
    # Solicita e valida o CPF (deve ter 11 dígitos numéricos)
    cpf = input("CPF (somente números): ").strip()
    if not validar_cpf(cpf):
        print("CPF inválido. Digite 11 números.")
        return
 
    # Verifica se o CPF já foi cadastrado anteriormente
    if cpf in cpfs_cadastrados:
        print("Atenção: CPF já possui cadastro. Registrando novo abastecimento.")
 
    # Exibe os tipos de combustível disponíveis para o usuário escolher
    print("\nTipos de combustível disponíveis:")
    for i, tipo in enumerate(tipos_combustivel, 1):
        print(f"  {i}. {tipo}")
 
    # Valida se a opção escolhida é um número dentro do intervalo válido
    opcao = input("Escolha o número do combustível: ").strip()
    if not opcao.isdigit() or not (1 <= int(opcao) <= len(tipos_combustivel)):
        print("Opção inválida.")
        return
 
    combustivel = tipos_combustivel[int(opcao) - 1]  # Obtém o nome do combustível escolhido
 
    # Solicita a quantidade de litros abastecidos
    litros = input("Quantidade de litros: ").strip()
    # BUG CORRIGIDO: o sistema permitia cadastrar litros negativos ou zero,
    # causando valores totais incorretos no abastecimento.
    # CORREÇÃO: adicionada a função validar_numero_positivo() que rejeita
    # qualquer valor que não seja um número maior que zero.
    if not validar_numero_positivo(litros):
        print("Quantidade inválida.")
        return
 
    # Solicita e valida o preço por litro
    preco = input("Preço por litro (R$): ").strip()
    if not validar_numero_positivo(preco):
        print("Preço inválido.")
        return
 
    # Converte os valores para float e calcula o total a pagar
    litros = float(litros)
    preco = float(preco)
    total = litros * preco
 
    # Gera um ID único baseado na quantidade de registros existentes
    novo_id = len(abastecimentos) + 1
 
    # Cria o dicionário com todos os dados do abastecimento
    registro = {
        "id": novo_id,
        "nome": nome,
        "iniciais": iniciais(nome),       # Iniciais geradas pela função auxiliar
        "cpf": cpf,
        "combustivel": combustivel,
        "litros": litros,
        "preco_litro": preco,
        "total": total
    }
 
    # Adiciona o registro na lista de abastecimentos e registra o CPF
    abastecimentos.append(registro)
    cpfs_cadastrados.add(cpf)
 
    print(f"\n Abastecimento registrado! Total: R$ {total:.2f}")
 
 
def listar_abastecimentos():
    """
    READ — Lista todos os abastecimentos cadastrados em formato de tabela.
    Exibe ID, iniciais, nome, CPF formatado, combustível, litros e total.
    Se não houver registros, informa o usuário.
    """
    if not abastecimentos:
        print("\nNenhum abastecimento cadastrado.")
        return
 
    print("\n--- LISTA DE ABASTECIMENTOS ---")
 
    # Cabeçalho da tabela com colunas alinhadas usando formatação f-string
    print(f"{'ID':<5} {'Iniciais':<10} {'Nome':<20} {'CPF':<15} {'Combustível':<20} {'Litros':<8} {'Total':<10}")
    print("-" * 90)
 
    # Percorre todos os registros e exibe cada um em uma linha formatada
    for registro in abastecimentos:
        cpf_fmt = formatar_cpf(registro["cpf"])  # Formata o CPF para exibição
        print(f"{registro['id']:<5} {registro['iniciais']:<10} {registro['nome']:<20} {cpf_fmt:<15} {registro['combustivel']:<20} {registro['litros']:<8.2f} R$ {registro['total']:<10.2f}")
 
 
def buscar_abastecimento():
    """
    READ — Busca um abastecimento específico por ID ou CPF.
    Permite encontrar registros de um cliente sem percorrer a lista manualmente.
    Exibe todos os resultados encontrados para o termo informado.
    """
    print("\n--- BUSCAR ABASTECIMENTO ---")
    termo = input("Digite o ID ou CPF do cliente: ").strip()
 
    # List comprehension — filtra os registros que correspondem ao ID ou CPF digitado
    resultado = [r for r in abastecimentos if str(r["id"]) == termo or r["cpf"] == termo]
 
    if not resultado:
        print("Nenhum registro encontrado.")
        return
 
    # Exibe os registros encontrados em formato de tabela
    print(f"\n{'ID':<5} {'Nome':<20} {'CPF':<15} {'Combustível':<20} {'Litros':<8} {'Total':<10}")
    print("-" * 80)
    for r in resultado:
        cpf_fmt = formatar_cpf(r["cpf"])
        print(f"{r['id']:<5} {r['nome']:<20} {cpf_fmt:<15} {r['combustivel']:<20} {r['litros']:<8.2f} R$ {r['total']:<10.2f}")
 
 
def editar_abastecimento():
    """
    UPDATE — Edita os dados de um abastecimento já existente.
    O usuário informa o ID do registro e pode alterar: nome, combustível, litros e preço.
    Campos deixados em branco mantêm o valor atual. O total é recalculado automaticamente.
    """
    print("\n--- EDITAR ABASTECIMENTO ---")
    id_busca = input("Digite o ID do abastecimento: ").strip()
 
    # Procura o registro com o ID informado
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
 
    # Permite alterar o nome; se deixado em branco, mantém o anterior
    novo_nome = input(f"Nome [{registro['nome']}]: ").strip()
    if novo_nome:
        registro["nome"] = novo_nome
        registro["iniciais"] = iniciais(novo_nome)  # Atualiza as iniciais junto
 
    # Exibe opções de combustível e permite trocar
    print("\nTipos de combustível:")
    for i, tipo in enumerate(tipos_combustivel, 1):
        print(f"  {i}. {tipo}")
    opcao = input(f"Combustível atual: {registro['combustivel']} — novo número (ou Enter): ").strip()
    if opcao.isdigit() and 1 <= int(opcao) <= len(tipos_combustivel):
        registro["combustivel"] = tipos_combustivel[int(opcao) - 1]
 
    # Permite alterar a quantidade de litros
    novo_litros = input(f"Litros [{registro['litros']}]: ").strip()
    if validar_numero_positivo(novo_litros):
        registro["litros"] = float(novo_litros)
 
    # Permite alterar o preço por litro
    novo_preco = input(f"Preço por litro [{registro['preco_litro']}]: ").strip()
    if validar_numero_positivo(novo_preco):
        registro["preco_litro"] = float(novo_preco)
 
    # Recalcula o total com os novos valores
    registro["total"] = registro["litros"] * registro["preco_litro"]
    print(f"\n Registro atualizado! Novo total: R$ {registro['total']:.2f}")
 
 
def deletar_abastecimento():
    """
    DELETE — Remove um abastecimento do sistema pelo ID.
    Antes de deletar, exibe os dados do registro e pede confirmação do usuário.
    Isso evita exclusões acidentais.
    """
    print("\n--- DELETAR ABASTECIMENTO ---")
    id_busca = input("Digite o ID do abastecimento: ").strip()
 
    # Procura o registro com o ID informado
    registro = None
    for r in abastecimentos:
        if str(r["id"]) == id_busca:
            registro = r
            break
 
    if not registro:
        print("Registro não encontrado.")
        return
 
    # Exibe os dados do registro encontrado antes de confirmar a exclusão
    print(f"\nAbastecimento encontrado: {registro['nome']} — {registro['combustivel']} — R$ {registro['total']:.2f}")
    confirmacao = input("Tem certeza que deseja deletar? (s/n): ").strip().lower()
 
    if confirmacao == "s":
        abastecimentos.remove(registro)  # Remove o registro da lista
        print("Registro deletado com sucesso.")
    else:
        print("Operação cancelada.")
 
 
def relatorio_por_combustivel():
    """
    READ — Gera um relatório com o total arrecadado por tipo de combustível.
    Soma os valores de todos os abastecimentos agrupados por tipo.
    Exibe também o total geral arrecadado pelo posto.
    """
    if not abastecimentos:
        print("\nNenhum abastecimento cadastrado.")
        return
 
    print("\n--- RELATÓRIO: TOTAL POR COMBUSTÍVEL ---")
 
    # Dict comprehension — cria um dicionário com cada combustível iniciando em R$ 0,00
    resumo = {tipo: 0.0 for tipo in tipos_combustivel}
 
    # Percorre todos os abastecimentos e acumula o total por tipo de combustível
    for r in abastecimentos:
        resumo[r["combustivel"]] += r["total"]
 
    # Exibe o total arrecadado para cada tipo de combustível
    for tipo, total in resumo.items():
        print(f"  {tipo:<25} R$ {total:.2f}")
 
    # Calcula e exibe o total geral somando todos os combustíveis
    total_geral = sum(resumo.values())
    print(f"\n  {'TOTAL GERAL':<25} R$ {total_geral:.2f}")