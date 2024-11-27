DROP SCHEMA IF EXISTS prato_certo;

CREATE SCHEMA prato_certo;

USE prato_certo;

CREATE TABLE usuarios (
	matricula VARCHAR(12) PRIMARY KEY,
    senha CHAR(64) NOT NULL,
    administrador BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE itens_cardapios (
	id INT PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(255) NOT NULL,
    imagem MEDIUMBLOB NOT NULL
);

CREATE TABLE itens_cardapios_dias (
	dia DATE NOT NULL,
    tipo ENUM('cafe', 'almoco', 'lanche', 'janta') NOT NULL,
    item INT NOT NULL,
    FOREIGN KEY (item) REFERENCES itens_cardapios (id)
);

CREATE TABLE reservas (
	dia DATE NOT NULL,
    tipo ENUM('cafe', 'almoco', 'lanche', 'janta') NOT NULL,
    usuario VARCHAR(12) NOT NULL,
    FOREIGN KEY (usuario) REFERENCES usuarios (matricula)
);