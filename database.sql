SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema ecopa
-- -----------------------------------------------------

CREATE SCHEMA IF NOT EXISTS `ecopa` DEFAULT CHARACTER SET utf8mb3 ;
USE `ecopa` ;

-- -----------------------------------------------------
-- Table `ecopa`.`gerente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecopa`.`gerente` (
  `cpf` VARCHAR(11) NOT NULL,
  `nome` VARCHAR(90) NOT NULL,
  `Celular` CHAR(15) NOT NULL,
  `email` VARCHAR(90) NULL DEFAULT NULL,
  `senha` VARCHAR(120) NULL DEFAULT NULL,
  PRIMARY KEY (`cpf`),
  UNIQUE INDEX `idGerente_UNIQUE` (`cpf` ASC) VISIBLE,
  UNIQUE INDEX `contato_UNIQUE` (`Celular` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
