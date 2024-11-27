DROP SCHEMA IF EXISTS prato_certo;

CREATE SCHEMA prato_certo;

USE prato_certo;

CREATE TABLE usuarios (
	matricula VARCHAR(12) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    senha CHAR(64) NOT NULL,
    administrador BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE itens_cardapio (
	nome VARCHAR(255) PRIMARY KEY
);

CREATE TABLE itens_cardapios_dias (
	dia DATE NOT NULL,
    tipo ENUM('cafe', 'almoco', 'lanche', 'janta') NOT NULL,
    item VARCHAR(255) NOT NULL,
    FOREIGN KEY (item) REFERENCES itens_cardapio (nome)
);

CREATE TABLE reservas (
	dia DATE NOT NULL,
    tipo ENUM('cafe', 'almoco', 'lanche', 'janta') NOT NULL,
    usuario VARCHAR(12) NOT NULL,
    FOREIGN KEY (usuario) REFERENCES usuarios (matricula)
);

CREATE TABLE costumes (
	usuario VARCHAR(12) NOT NULL,
    tipo ENUM('cafe', 'almoco', 'lanche', 'janta') NOT NULL,
    FOREIGN KEY (usuario) REFERENCES usuarios (matricula)
);
