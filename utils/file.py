def ler_arquivo(caminho_arquivo: str, encoding: str = 'utf-8') -> str:
    try:
        with open(caminho_arquivo, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
    except Exception as e:
        raise Exception(f"Erro ao ler {caminho_arquivo}: {str(e)}")
