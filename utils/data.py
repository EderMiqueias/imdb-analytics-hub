import ast


def limpar_dados_nulos(dados):
    dados_limpos = []
    for row in dados:
        try:
            assert row[0] is not None  # pk
            assert isinstance(row[0], int)
            dados_limpos.append(row)
        except Exception:
            continue
    return dados_limpos


def dividir_array(array: list, n: int):
    """
    :param array: Qualquer lista
    :param n: número maximo de valores em cada parte
    """
    return [array[i:i + n] for i in range(0, len(array), n)]


def string_para_lista(s):
    try:
        return ast.literal_eval(s)
    except (ValueError, SyntaxError):
        return []
