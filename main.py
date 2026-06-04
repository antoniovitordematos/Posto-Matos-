# main.py — 

from crud import (
    cadastrar_abastecimento,
    listar_abastecimentos,
    buscar_abastecimento,
    editar_abastecimento,
    deletar_abastecimento,
    relatorio_por_combustivel
)


def exibir_menu():
    """Exibe o menu principal do sistema."""
    print("\n" + "=" * 40)
    print("       POSTO MATOS — SISTEMA CRUD")
    print("=" * 40)
    print("  1. Cadastrar abastecimento")
    print("  2. Listar abastecimentos")
    print("  3. Buscar abastecimento")
    print("  4. Editar abastecimento")
    print("  5. Deletar abastecimento")
    print("  6. Relatório por combustível")
    print("  0. Sair")
    print("=" * 40)


def main():
    """Função principal — loop do menu."""
    print("\nBem-vindo ao sistema do Posto Matos!")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_abastecimento()
        elif opcao == "2":
            listar_abastecimentos()
        elif opcao == "3":
            buscar_abastecimento()
        elif opcao == "4":
            editar_abastecimento()
        elif opcao == "5":
            deletar_abastecimento()
        elif opcao == "6":
            relatorio_por_combustivel()
        elif opcao == "0":
            print("\nSaindo do sistema. Até logo!")
            break
        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()