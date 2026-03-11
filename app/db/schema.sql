CREATE DATABASE IF NOT EXISTS Industrias_Wayne
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE Industrias_Wayne;

CREATE TABLE IF NOT EXISTS usuarios (
id INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(80),
email VARCHAR(80),
senha VARCHAR(255),
tipo_perfil ENUM ('funcionario', 'gerente', 'admin_seguranca'),
ativo BOOLEAN
);

CREATE TABLE IF NOT EXISTS recursos(
id INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(80),
categoria ENUM('equipamento', 'veiculo', 'dispositivo'),
descricao VARCHAR(255),
status ENUM('ativo', 'em_manutencao', 'desativado', 'outro'),
localizacao VARCHAR(80),
observacoes_adicionais VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS movimentacoes_recursos(
id INT PRIMARY KEY AUTO_INCREMENT,
recurso_id INT,
FOREIGN KEY (recurso_id) REFERENCES recursos(id),
usuario_id INT,
FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
tipo_movimentacao ENUM ('cadastrado', 'atualizado', 'desativado'),
data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logs_acessos(
id INT PRIMARY KEY AUTO_INCREMENT,
usuario_id INT,
FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
tipo_acao ENUM ('login_sucesso', 'login_falha', 'acesso_negado', 'logout'), 
data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
detalhes VARCHAR(255)
);