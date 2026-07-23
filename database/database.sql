-- =============================================================
-- ECOPA System - Schema Remodelado
-- =============================================================
CREATE SCHEMA IF NOT EXISTS ecopa_system DEFAULT CHARACTER SET utf8mb3;
USE ecopa_system;

-- -----------------------------------------------------
-- Table: gerente
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS gerente (
  cpf VARCHAR(11) NOT NULL,
  nome VARCHAR(90) NOT NULL,
  celular CHAR(15) NOT NULL,
  email VARCHAR(90) NOT NULL,
  senha VARCHAR(120) NOT NULL,
  setor VARCHAR(45) NOT NULL,
  PRIMARY KEY (cpf),
  UNIQUE INDEX celular_UNIQUE (celular ASC) VISIBLE,
  UNIQUE INDEX email_UNIQUE (email ASC) VISIBLE)
ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Table: ponto_de_coleta
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS ponto_de_coleta (
  id_ponto INT NOT NULL AUTO_INCREMENT,
  endereco VARCHAR(45) NOT NULL,
  email VARCHAR(255) NULL,
  estabelecimento VARCHAR(100) NOT NULL,
  telefone VARCHAR(45) NOT NULL,
  proprietario VARCHAR(90) NOT NULL,
  PRIMARY KEY (id_ponto))
ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Table: coleta
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS coleta (
  id_coleta INT NOT NULL AUTO_INCREMENT,
  data DATETIME NOT NULL,
  quantidade DECIMAL(10,2) NOT NULL,
  observacao TEXT NULL,
  status ENUM('Pendente', 'Realizada') NOT NULL DEFAULT 'Pendente',
  gerente_cpf VARCHAR(11) NOT NULL,
  ponto_de_coleta_id_ponto INT NOT NULL,
  PRIMARY KEY (id_coleta),
  INDEX fk_coleta_gerente1_idx (gerente_cpf ASC) VISIBLE,
  INDEX fk_coleta_ponto_de_coleta1_idx (ponto_de_coleta_id_ponto ASC) VISIBLE,
  CONSTRAINT fk_coleta_gerente1
    FOREIGN KEY (gerente_cpf)
    REFERENCES gerente (cpf)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_coleta_ponto_de_coleta1
    FOREIGN KEY (ponto_de_coleta_id_ponto)
    REFERENCES ponto_de_coleta (id_ponto)
    ON DELETE NO ACTION ON UPDATE NO ACTION)
ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Table: horario_ponto
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS horario_ponto (
  idhorario INT NOT NULL AUTO_INCREMENT,
  dia_semana TINYINT NOT NULL COMMENT '1=DOM, 2=SEG, 3=TER, 4=QUA, 5=QUI, 6=SEX, 7=SAB',
  abertura TIME NOT NULL,
  fechamento TIME NOT NULL,
  ativo TINYINT(1) NOT NULL DEFAULT '1',
  ponto_de_coleta_id_ponto INT NOT NULL,
  PRIMARY KEY (idhorario),
  INDEX fk_horario_ponto_ponto_de_coleta_idx (ponto_de_coleta_id_ponto ASC) VISIBLE,
  CONSTRAINT fk_horario_ponto_ponto_de_coleta
    FOREIGN KEY (ponto_de_coleta_id_ponto)
    REFERENCES ponto_de_coleta (id_ponto)
    ON DELETE CASCADE ON UPDATE NO ACTION)
ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Table: lote (estoque gerado a partir de coletas realizadas)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS lote (
  id_lote INT NOT NULL AUTO_INCREMENT,
  id_coleta INT NOT NULL,
  quantidade_coletada DECIMAL(10,2) NOT NULL,
  quantidade_restante DECIMAL(10,2) NOT NULL,
  status ENUM('Disponivel', 'Parcialmente Consumido', 'Esgotado') NOT NULL DEFAULT 'Disponivel',
  data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_lote),
  INDEX fk_lote_coleta_idx (id_coleta ASC) VISIBLE,
  CONSTRAINT fk_lote_coleta
    FOREIGN KEY (id_coleta)
    REFERENCES coleta (id_coleta)
    ON DELETE NO ACTION ON UPDATE NO ACTION)
ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Table: destinacao (entidade independente - centros de destino)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS destinacao (
  id_destinacao INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(100) NOT NULL,
  tipo ENUM('Reciclagem', 'Biomassa', 'Compostagem', 'Aterro', 'Outro') NOT NULL,
  endereco VARCHAR(150) NOT NULL,
  telefone VARCHAR(45) NULL,
  email VARCHAR(100) NULL,
  cnpj VARCHAR(20) NULL,
  PRIMARY KEY (id_destinacao),
  UNIQUE INDEX cnpj_UNIQUE (cnpj ASC) VISIBLE)
ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Table: pedido (remessa de material para um destino)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS pedido (
  id_pedido INT NOT NULL AUTO_INCREMENT,
  id_destinacao INT NOT NULL,
  quantidade_solicitada DECIMAL(10,2) NOT NULL,
  data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status ENUM('Aberto', 'Atendido Parcialmente', 'Atendido', 'Cancelado') NOT NULL DEFAULT 'Aberto',
  observacao TEXT NULL,
  PRIMARY KEY (id_pedido),
  INDEX fk_pedido_destinacao_idx (id_destinacao ASC) VISIBLE,
  CONSTRAINT fk_pedido_destinacao
    FOREIGN KEY (id_destinacao)
    REFERENCES destinacao (id_destinacao)
    ON DELETE NO ACTION ON UPDATE NO ACTION)
ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Table: pedido_lote (N:N - quais lotes foram consumidos por cada pedido)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS pedido_lote (
  id_pedido_lote INT NOT NULL AUTO_INCREMENT,
  id_pedido INT NOT NULL,
  id_lote INT NOT NULL,
  quantidade_consumida DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id_pedido_lote),
  INDEX fk_pedido_lote_pedido_idx (id_pedido ASC) VISIBLE,
  INDEX fk_pedido_lote_lote_idx (id_lote ASC) VISIBLE,
  CONSTRAINT fk_pedido_lote_pedido
    FOREIGN KEY (id_pedido)
    REFERENCES pedido (id_pedido)
    ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT fk_pedido_lote_lote
    FOREIGN KEY (id_lote)
    REFERENCES lote (id_lote)
    ON DELETE NO ACTION ON UPDATE NO ACTION)
ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb3;

-- =============================================================
-- Indices para performance (consultas com filtro de data/status)
-- =============================================================
CREATE INDEX idx_coleta_data ON coleta(data);
CREATE INDEX idx_coleta_status ON coleta(status);
CREATE INDEX idx_pedido_data ON pedido(data);
CREATE INDEX idx_pedido_status ON pedido(status);
