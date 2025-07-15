import pandas as pd
from pathlib import Path


def extrair_primeiras_linhas(caminho_arquivo_csv, linhas=1000000):
    caminho_arquivo_csv = Path(caminho_arquivo_csv)

    if not caminho_arquivo_csv.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo_csv}")

    df = pd.read_csv(caminho_arquivo_csv, sep='\t', nrows=linhas)

    caminho_saida = 'tsv_input_files/' + f"{caminho_arquivo_csv.stem}.tsv"
    df.to_csv(caminho_saida, index=False, sep='\t')

    return caminho_saida


# Gera um novo arquivo com as 10.000 primeiras linhas de "title.basics.tsv"
extrair_primeiras_linhas("tsv_input_files/originals/title.basics.tsv")
extrair_primeiras_linhas("tsv_input_files/originals/name.basics.tsv")
extrair_primeiras_linhas("tsv_input_files/originals/title.principals.tsv")
extrair_primeiras_linhas("tsv_input_files/originals/title.ratings.tsv")
