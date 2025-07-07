# IMDb Analytics Hub
## 📋 Visão Geral

O IMDb Analytics Hub é um Sistema de Apoio à Decisão (SAD) desenvolvido com base nos dados não comerciais disponibilizados pelo Internet Movie Database (IMDb). Esses dados, atualizados diariamente, oferecem uma ampla gama de informações sobre filmes, séries, artistas, equipes de produção e avaliações de audiência.

---

## 📦 Estrutura do Projeto

```bash
imdb-analytics-hub/
│
├── database/
│ ├── migrations/
│ │ ├── dimensional/
│ │ │ └── mysql_migration.sql ← Script para criar as tabelas
│
├── etl/
│ └── start_etl.py ← Arquivo principal para execução do ETL
│
├── tsv_input_files/ ← Onde os arquivos .tsv devem ser colocados
│
├── .env ← Configurações de ambiente (banco de dados)
└── README.md
```


---

## ✅ Pré-requisitos

- Python 3.10+
- MySQL instalado e rodando
- `pip install -r requirements.txt`
- Criar um arquivo `.env` com as configurações de conexão:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=suasenha
MYSQL_DATABASE=imdb_analytics
MYSQL_PORT=3306
```

## 🚀 Passo a Passo para Execução
1. Execute a migração para criar as tabelas

```bash
  python3 database/migrations/create_migrations.py
```

2. Baixe a base de dados do IMDb
Acesse o site oficial:
👉 https://datasets.imdbws.com/

Baixe os seguintes arquivos:

name.basics.tsv.gz
title.basics.tsv.gz
title.principals.tsv.gz
title.ratings.tsv.gz

3. Extraia os arquivos .tsv
Extraia os arquivos .tsv e coloque-os dentro da pasta:

```bash
tsv_input_files/
├── name.basics.tsv
├── title.basics.tsv
├── title.principals.tsv
├── title.ratings.tsv
```
Importante: Certifique-se de que os arquivos estejam descompactados e com os nomes exatamente iguais aos acima.

4. Execute o ETL
Rode o script principal de ingestão:

```bash
  python etl/start_etl.py
```

Se tudo estiver correto, você verá uma mensagem de sucesso no final.
