CREATE TABLE IF NOT EXISTS DIM_Titulo (
    pk_titulo INT PRIMARY KEY,
    titleType VARCHAR(45),
    primaryTitle VARCHAR(45),
    genres VARCHAR(45),
    runtimeMinutes BIGINT(23)
);

CREATE TABLE IF NOT EXISTS DIM_Pessoa (
    pk_pessoa INT PRIMARY KEY,
    primaryName VARCHAR(45)
);

CREATE TABLE IF NOT EXISTS DIM_Tempo (
    pk_tempo INT PRIMARY KEY,
    starYear YEAR(4)
);

CREATE TABLE IF NOT EXISTS DIM_Papel (
    pk_papel INT PRIMARY KEY,
    category VARCHAR(45),
    characters VARCHAR(45)
);

CREATE TABLE IF NOT EXISTS Fato_Avaliacao_Titulo (
    pk_fato INT PRIMARY KEY,
    DIM_Titulo_pk_titulo INT,
    DIM_Tempo_pk_tempo INT,
    DIM_Pessoa_pk_pessoa INT,
    DIM_Papel_pk_papel INT,
    numVotes BIGINT(23),
    averageRating DECIMAL(4,2),
    FOREIGN KEY (DIM_Titulo_pk_titulo) REFERENCES DIM_Titulo(pk_titulo),
    FOREIGN KEY (DIM_Tempo_pk_tempo) REFERENCES DIM_Tempo(pk_tempo),
    FOREIGN KEY (DIM_Pessoa_pk_pessoa) REFERENCES DIM_Pessoa(pk_pessoa),
    FOREIGN KEY (DIM_Papel_pk_papel) REFERENCES DIM_Papel(pk_papel)
);
