# utils.py — Funções auxiliares do Posto Matos

def validar_cpf(cpf):
    """Verifica se o CPF tem 11 dígitos numéricos."""
    return cpf.isdigit() and len(cpf) == 11


def formatar_cpf(cpf):
    """Formata CPF: 12345678901 → 123.456.789-01"""
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def validar_numero_positivo(valor):
    """Verifica se o valor é um número maior que zero."""
    try:
        return float(valor) > 0
    except ValueError:
        return False


def gerador_registros(lista):
    """Gerador que percorre os registros um a um."""
    for registro in lista:
        yield registro


def iniciais(nome):
    """Retorna as iniciais do nome. Ex: João Silva → J.S."""
    partes = nome.strip().split()
    return ".".join(p[0].upper() for p in partes) + "."