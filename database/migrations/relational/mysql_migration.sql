CREATE TABLE IF NOT EXISTS Pessoa (
  pk_pessoa VARCHAR(45) NOT NULL,
  primaryName VARCHAR(45) NULL,
  PRIMARY KEY (pk_pessoa));

CREATE TABLE IF NOT EXISTS Nota (
  pk_nota VARCHAR(45) NOT NULL,
  averegeRating DECIMAL(23,4) NULL,
  numVotes BIGINT(23) NULL,
  PRIMARY KEY (pk_nota));

CREATE TABLE IF NOT EXISTS Titulo (
  pk_titulo VARCHAR(45) NOT NULL,
  titleType VARCHAR(45) NULL,
  primaryTitle VARCHAR(45) NULL,
  starYear YEAR(4) NULL,
  runtimeMinutes BIGINT(23) NULL,
  genres VARCHAR(45) NULL,
  Nota_pk_nota VARCHAR(45) NOT NULL,
  PRIMARY KEY (pk_titulo, Nota_pk_nota),
  INDEX fk_Titulo_Nota1_idx (Nota_pk_nota ASC) VISIBLE,
  CONSTRAINT fk_Titulo_Nota1
    FOREIGN KEY (Nota_pk_nota)
    REFERENCES Nota (pk_nota)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE IF NOT EXISTS Papel (
  category VARCHAR(45) NULL,
  characters VARCHAR(45) NULL,
  Pessoa_pk_pessoa VARCHAR(45) NOT NULL,
  Titulo_pk_titulo VARCHAR(45) NOT NULL,
  Titulo_Nota_pk_nota VARCHAR(45) NOT NULL,
  PRIMARY KEY (Pessoa_pk_pessoa, Titulo_pk_titulo, Titulo_Nota_pk_nota),
  INDEX fk_Papel_Titulo1_idx (Titulo_pk_titulo ASC, Titulo_Nota_pk_nota ASC) VISIBLE,
  CONSTRAINT fk_Papel_Pessoa1
    FOREIGN KEY (Pessoa_pk_pessoa)
    REFERENCES Pessoa (pk_pessoa)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Papel_Titulo1
    FOREIGN KEY (Titulo_pk_titulo , Titulo_Nota_pk_nota)
    REFERENCES Titulo (pk_titulo , Nota_pk_nota)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
