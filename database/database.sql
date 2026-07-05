CREATE SCHEMA IF NOT EXISTS `ecopa_system` DEFAULT CHARACTER SET utf8mb3 ;
USE `ecopa_system` ;

-- -----------------------------------------------------
-- Table `ecopa_system`.`gerente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecopa_system`.`gerente` (
  `cpf` VARCHAR(11) NOT NULL,
  `nome` VARCHAR(90) NOT NULL,
  `celular` CHAR(15) NOT NULL,
  `email` VARCHAR(90) NOT NULL,
  `senha` VARCHAR(120) NOT NULL,
  `setor` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`cpf`),
  UNIQUE INDEX `celular_UNIQUE` (`celular` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `ecopa_system`.`ponto_de_coleta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecopa_system`.`ponto_de_coleta` (
  `id_ponto` INT NOT NULL AUTO_INCREMENT,
  `endereco` VARCHAR(45) NOT NULL,
  `email` VARCHAR(255) NULL,
  `estabelecimento` VARCHAR(100) NOT NULL,
  `telefone` VARCHAR(45) NOT NULL,
  `proprietario` VARCHAR(90) NOT NULL,
  PRIMARY KEY (`id_ponto`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `ecopa_system`.`coleta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecopa_system`.`coleta` (
  `id_coleta` INT NOT NULL AUTO_INCREMENT,
  `data` DATETIME NOT NULL,
  `quantidade` DECIMAL(10,2) NOT NULL,
  `observacao` TEXT NULL,
  `gerente_cpf` VARCHAR(11) NOT NULL,
  `ponto_de_coleta_id_ponto` INT NOT NULL,
  PRIMARY KEY (`id_coleta`),
  INDEX `fk_coleta_gerente1_idx` (`gerente_cpf` ASC) VISIBLE,
  INDEX `fk_coleta_ponto_de_coleta1_idx` (`ponto_de_coleta_id_ponto` ASC) VISIBLE,
  CONSTRAINT `fk_coleta_gerente1`
    FOREIGN KEY (`gerente_cpf`)
    REFERENCES `ecopa_system`.`gerente` (`cpf`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_coleta_ponto_de_coleta1`
    FOREIGN KEY (`ponto_de_coleta_id_ponto`)
    REFERENCES `ecopa_system`.`ponto_de_coleta` (`id_ponto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `ecopa_system`.`destinacoes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecopa_system`.`destinacoes` (
  `id_destinacoes` INT NOT NULL AUTO_INCREMENT,
  `cnpj` VARCHAR(20) NOT NULL,
  `cliente` VARCHAR(45) NOT NULL,
  `data` DATETIME NOT NULL,
  `coleta_id_coleta` INT NOT NULL,
  PRIMARY KEY (`id_destinacoes`),
  UNIQUE INDEX `cnpj_UNIQUE` (`cnpj` ASC) VISIBLE,
  INDEX `fk_destinacoes_coleta1_idx` (`coleta_id_coleta` ASC) VISIBLE,
  CONSTRAINT `fk_destinacoes_coleta1`
    FOREIGN KEY (`coleta_id_coleta`)
    REFERENCES `ecopa_system`.`coleta` (`id_coleta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `ecopa_system`.`horario_ponto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecopa_system`.`horario_ponto` (
  `idhorario` INT NOT NULL AUTO_INCREMENT,
  `dia_semana` TINYINT NOT NULL COMMENT '1=DOM, 2=SEG, 3=TER, 4=QUA, 5=QUI, 6=SEX, 7=SAB',
  `abertura` TIME NOT NULL,
  `fechamento` TIME NOT NULL,
  `ativo` TINYINT(1) NOT NULL DEFAULT '1',
  `ponto_de_coleta_id_ponto` INT NOT NULL,
  PRIMARY KEY (`idhorario`),
  INDEX `fk_horario_ponto_ponto_de_coleta_idx` (`ponto_de_coleta_id_ponto` ASC) VISIBLE,
  CONSTRAINT `fk_horario_ponto_ponto_de_coleta`
    FOREIGN KEY (`ponto_de_coleta_id_ponto`)
    REFERENCES `ecopa_system`.`ponto_de_coleta` (`id_ponto`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;



