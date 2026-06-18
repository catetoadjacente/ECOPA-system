-- Schema ecopa_system
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ecopa_system` DEFAULT CHARACTER SET utf8 ;
USE `ecopa_system` ;

-- -----------------------------------------------------
-- Table `ecopa_system`.`Gerente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecopa_system`.`Gerente` (
  `idcpf` VARCHAR(11) NOT NULL,
  `nome` VARCHAR(90) NOT NULL,
  `Celular` CHAR(15) NOT NULL,
  `email` VARCHAR(90) NOT NULL,
  `senha` VARCHAR(120) NOT NULL,
  `setor` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idcpf`),
  UNIQUE INDEX `idGerente_UNIQUE` (`idcpf` ASC) VISIBLE,
  UNIQUE INDEX `Nome_UNIQUE` (`nome` ASC) VISIBLE,
  UNIQUE INDEX `contato_UNIQUE` (`Celular` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `senha_UNIQUE` (`senha` ASC) VISIBLE,
  UNIQUE INDEX `setor_UNIQUE` (`setor` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ecopa_system`.`coleta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecopa_system`.`coleta` (
  `id_coteta` INT NOT NULL,
  `dat` DATETIME NOT NULL,
  `quantidade` DECIMAL(10,2) NOT NULL,
  `observacao` TEXT(150) NOT NULL,
  PRIMARY KEY (`id_coteta`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ecopa_system`.`deatinacoes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecopa_system`.`deatinacoes` (
  `iddeatinacoes` INT NOT NULL,
  `cnpj` VARCHAR(20) NOT NULL,
  `cliente` VARCHAR(45) NOT NULL,
  `data` DATETIME NULL,
  PRIMARY KEY (`iddeatinacoes`),
  UNIQUE INDEX `iddeatinacoes_UNIQUE` (`iddeatinacoes` ASC) VISIBLE,
  UNIQUE INDEX `cnpj_UNIQUE` (`cnpj` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ecopa_system`.`ponto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecopa_system`.`ponto` (
  `idponto` INT NOT NULL,
  `endereco` VARCHAR(45) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `estabelecimento` VARCHAR(100) NOT NULL,
  `telefone` VARCHAR(45) NOT NULL,
  `propretario` VARCHAR(90) NOT NULL,
  PRIMARY KEY (`idponto`),
  UNIQUE INDEX `idponto_UNIQUE` (`idponto` ASC) VISIBLE,
  UNIQUE INDEX `endereco_UNIQUE` (`endereco` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `estabelecimento_UNIQUE` (`estabelecimento` ASC) VISIBLE,
  UNIQUE INDEX `telefone_UNIQUE` (`telefone` ASC) VISIBLE,
  UNIQUE INDEX `propretario_UNIQUE` (`propretario` ASC) VISIBLE)
ENGINE = InnoDB;

