CREATE TABLE IF NOT EXISTS DIM_Titulo (
    pk_titulo INT PRIMARY KEY,
    titleType VARCHAR(255),
    primaryTitle VARCHAR(255),
    genres VARCHAR(255),
    runtimeMinutes BIGINT(23)
);

CREATE TABLE IF NOT EXISTS DIM_Pessoa (
    pk_pessoa INT PRIMARY KEY,
    primaryName VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS DIM_Tempo (
    pk_tempo INT PRIMARY KEY,
    starYear YEAR(4)
);

CREATE TABLE IF NOT EXISTS DIM_Papel (
    pk_papel INT PRIMARY KEY AUTO_INCREMENT,
    category VARCHAR(255),
    character_name VARCHAR(512)
);

CREATE TABLE IF NOT EXISTS Fato_Avaliacao_Titulo (
    pk_fato INT PRIMARY KEY AUTO_INCREMENT,
    DIM_Titulo_pk_titulo INT,
    DIM_Tempo_pk_tempo INT,
    numVotes BIGINT(23),
    averageRating DECIMAL(4,2),
    FOREIGN KEY (DIM_Titulo_pk_titulo) REFERENCES DIM_Titulo(pk_titulo),
    FOREIGN KEY (DIM_Tempo_pk_tempo) REFERENCES DIM_Tempo(pk_tempo)
);

CREATE TABLE IF NOT EXISTS Fato_Pessoa (
    pk_fato_pessoa INT PRIMARY KEY AUTO_INCREMENT,
    numVotes BIGINT(23),
    averageRating DECIMAL(4,2),
    DIM_Pessoa_pk_pessoa INT NOT NULL,
    FOREIGN KEY (DIM_Pessoa_pk_pessoa) REFERENCES DIM_Pessoa(pk_pessoa)
);
