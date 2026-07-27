-- ============================================================
-- SISTEMA DE ALMOXARIFADO - BANCO DE DADOS (VERSAO ATUAL)
-- Execute este arquivo inteiro no MySQL Workbench antes de rodar o sistema.
-- ============================================================

DROP DATABASE IF EXISTS almoxarifado;
CREATE DATABASE almoxarifado;
USE almoxarifado;

-- ------------------------------------------------------------
-- Tabela: produtos
-- ------------------------------------------------------------
CREATE TABLE produtos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  unidade_medida VARCHAR(20) NOT NULL,
  quantidade_estoque INT NOT NULL DEFAULT 0,
  valor_unitario DECIMAL(10,2) NOT NULL,
  limite_minimo INT NOT NULL DEFAULT 0,
  limite_maximo INT NOT NULL DEFAULT 100,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Tabela: movimentacoes
-- Registra as entradas e saidas de produtos do almoxarifado.
-- ------------------------------------------------------------
CREATE TABLE movimentacoes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  produto_id INT NOT NULL,
  tipo ENUM('ENTRADA', 'SAIDA') NOT NULL,
  quantidade INT NOT NULL,
  data_movimentacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_movimentacao_produto
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- ------------------------------------------------------------
-- Carga inicial de dados
-- ------------------------------------------------------------
INSERT INTO produtos
  (nome, unidade_medida, quantidade_estoque, valor_unitario, limite_minimo, limite_maximo)
VALUES
  ('Detergente Neutro 5L',     'GALAO',  40,  18.90, 10, 100),
  ('Agua Sanitaria 2L',        'FRASCO', 25,   7.50,  5, 100),
  ('Desinfetante Floral 5L',   'GALAO',  12,  22.40, 10, 100),
  ('Papel Toalha Interfolha',  'PACOTE', 60,  14.75, 15, 100),
  ('Saco de Lixo 100L',        'ROLO',    8,  29.90, 10, 100),
  ('Alcool 70% 1L',            'FRASCO', 33,  11.20, 10, 100);

INSERT INTO movimentacoes (produto_id, tipo, quantidade, data_movimentacao) VALUES
  (1, 'ENTRADA', 50, '2026-06-02 08:15:00'),
  (1, 'SAIDA',   10, '2026-06-05 14:30:00'),
  (2, 'ENTRADA', 30, '2026-06-03 09:00:00'),
  (2, 'SAIDA',    5, '2026-06-10 16:45:00'),
  (3, 'ENTRADA', 20, '2026-06-04 10:20:00'),
  (3, 'SAIDA',    8, '2026-06-12 11:05:00'),
  (4, 'ENTRADA', 60, '2026-06-06 08:40:00'),
  (5, 'ENTRADA', 15, '2026-06-07 13:10:00'),
  (5, 'SAIDA',    7, '2026-06-15 15:50:00'),
  (6, 'ENTRADA', 40, '2026-06-08 07:55:00'),
  (6, 'SAIDA',    7, '2026-06-18 17:20:00');

-- ------------------------------------------------------------
-- Conferencia
-- ------------------------------------------------------------
SELECT * FROM produtos;
SELECT * FROM movimentacoes;
