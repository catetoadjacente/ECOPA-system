CREATE SCHEMA IF NOT EXISTS `ecopa_system` DEFAULT CHARACTER SET utf8 ;
USE `ecopa_system` ;

-- Tabela motorista
CREATE TABLE IF NOT EXISTS `ecopa_system`.`motorista` (
  `cnh` CHAR(9) NOT NULL,
  `nome` VARCHAR(150) NOT NULL,
  `contato` CHAR(11) NOT NULL,
  `Categoria_cnh` ENUM('B', 'C') NOT NULL,
  PRIMARY KEY (`cnh`),
  UNIQUE INDEX `CNH_UNIQUE` (`cnh` ASC) VISIBLE,
  UNIQUE INDEX `contato_UNIQUE` (`contato` ASC) VISIBLE)
ENGINE = InnoDB;

-- Tabela veiculo
CREATE TABLE IF NOT EXISTS `ecopa_system`.`veiculo` (
  `placa` CHAR(7) NOT NULL,
  `consumo combustivel` DECIMAL(4,2) NULL,
  `capacidade de carga` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`placa`),
  UNIQUE INDEX `placa_UNIQUE` (`placa` ASC) VISIBLE)
ENGINE = InnoDB;

-- Tabela rota
CREATE TABLE IF NOT EXISTS `ecopa_system`.`rota` (
  `id_rota` INT NOT NULL,
  `data` DATE NOT NULL,
  `distancia` DECIMAL(4,2) NOT NULL,
  `tempo_total` TIME NOT NULL,
  `veiculo_placa` CHAR(7) NOT NULL,
  PRIMARY KEY (`id_rota`, `veiculo_placa`),
  UNIQUE INDEX `id_rota_UNIQUE` (`id_rota` ASC) VISIBLE,
  INDEX `fk_rota_veiculo1_idx` (`veiculo_placa` ASC) VISIBLE,
  CONSTRAINT `fk_rota_veiculo1`
    FOREIGN KEY (`veiculo_placa`)
    REFERENCES `ecopa_system`.`veiculo` (`placa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Tabela gerente
CREATE TABLE IF NOT EXISTS `ecopa_system`.`gerente` (
  `cpf` CHAR(11) NOT NULL,
  `nome` VARCHAR(150) NOT NULL,
  `contato` CHAR(11) NOT NULL,
  `Setor` VARCHAR(60) NOT NULL,
  UNIQUE INDEX `CPF_UNIQUE` (`cpf` ASC) VISIBLE,
  UNIQUE INDEX `contato_UNIQUE` (`contato` ASC) VISIBLE,
  UNIQUE INDEX `Setor_UNIQUE` (`Setor` ASC) VISIBLE)
ENGINE = InnoDB;

-- Tabela coleta
CREATE TABLE IF NOT EXISTS `ecopa_system`.`coleta` (
  `id_coleta` INT NOT NULL,
  `quantidade_coletada` DECIMAL(10,2) NOT NULL,
  `horario` DATETIME NOT NULL,
  `observação` TINYTEXT NOT NULL,
  `status` ENUM('pendente', 'concluida', 'cancelada') NOT NULL,
  `gerente_cpf` CHAR(11) NOT NULL,
  PRIMARY KEY (`id_coleta`, `gerente_cpf`),
  UNIQUE INDEX `idcoleta_UNIQUE` (`id_coleta` ASC) VISIBLE,
  INDEX `fk_coleta_gerente1_idx` (`gerente_cpf` ASC) VISIBLE,
  CONSTRAINT `fk_coleta_gerente1`
    FOREIGN KEY (`gerente_cpf`)
    REFERENCES `ecopa_system`.`gerente` (`cpf`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Tabela ponto de coleta
CREATE TABLE IF NOT EXISTS `ecopa_system`.`ponto de coleta` (
  `id_ponto` INT NOT NULL,
  `nome_do_local` VARCHAR(150) NOT NULL,
  `longitutude` DECIMAL(11,8) NOT NULL,
  `quantidade_estimada` DECIMAL(10,2) NOT NULL,
  `prioridade` TINYINT(1) NOT NULL,
  `rota_id_rota` INT NOT NULL,
  `rota_veiculo_placa` CHAR(7) NOT NULL,
  `coleta_id_coleta` INT NOT NULL,
  PRIMARY KEY (`id_ponto`, `rota_id_rota`, `rota_veiculo_placa`, `coleta_id_coleta`),
  UNIQUE INDEX `id_ponto_UNIQUE` (`id_ponto` ASC) VISIBLE,
  UNIQUE INDEX `longitutude_UNIQUE` (`longitutude` ASC) VISIBLE,
  INDEX `fk_ponto de coleta_rota1_idx` (`rota_id_rota` ASC, `rota_veiculo_placa` ASC) VISIBLE,
  INDEX `fk_ponto de coleta_coleta1_idx` (`coleta_id_coleta` ASC) VISIBLE,
  CONSTRAINT `fk_ponto de coleta_rota1`
    FOREIGN KEY (`rota_id_rota` , `rota_veiculo_placa`)
    REFERENCES `ecopa_system`.`rota` (`id_rota` , `veiculo_placa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ponto de coleta_coleta1`
    FOREIGN KEY (`coleta_id_coleta`)
    REFERENCES `ecopa_system`.`coleta` (`id_coleta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Tabela motorista_has_veiculo
CREATE TABLE IF NOT EXISTS `ecopa_system`.`motorista_has_veiculo` (
  `motorista_CNH` CHAR(11) NOT NULL,
  `veiculo_placa` CHAR(7) NOT NULL,
  PRIMARY KEY (`motorista_CNH`, `veiculo_placa`),
  INDEX `fk_motorista_has_veiculo_veiculo1_idx` (`veiculo_placa` ASC) VISIBLE,
  INDEX `fk_motorista_has_veiculo_motorista_idx` (`motorista_CNH` ASC) VISIBLE,
  CONSTRAINT `fk_motorista_has_veiculo_motorista`
    FOREIGN KEY (`motorista_CNH`)
    REFERENCES `ecopa_system`.`motorista` (`cnh`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_motorista_has_veiculo_veiculo1`
    FOREIGN KEY (`veiculo_placa`)
    REFERENCES `ecopa_system`.`veiculo` (`placa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
