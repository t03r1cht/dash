DROP DATABASE IF EXISTS dash_board_db;

CREATE DATABASE dash_board_db;

CREATE TABLE dash_board_db.dash_users(
  uid INT NOT NULL AUTO_INCREMENT,
  username varchar(100) NOT NULL UNIQUE,
  email varchar(250) NOT NULL UNIQUE,
  password varchar(150) NOT NULL,
  creation_date DATETIME NOT NULL,
  role_id INT NOT NULL,
  profile_data varchar(5000),
  PRIMARY KEY (uid)
) ENGINE=INNODB;

CREATE TABLE dash_board_db.dash_users_verification(
  uid INT NOT NULL,
  verified BOOLEAN NOT NULL,
  token VARCHAR(50),
  verification_date DATETIME
) ENGINE=INNODB;

CREATE TABLE dash_board_db.dash_roles(
  role_id INT NOT NULL AUTO_INCREMENT,
  name varchar(100),
  config_board BOOLEAN,
  PRIMARY KEY (role_id)
) ENGINE=INNODB;


DROP USER IF EXISTS 'tech_dash_user'@'localhost', 'tech_dash_user'@'%';
FLUSH PRIVILEGES;
CREATE USER 'tech_dash_user'@'localhost' IDENTIFIED BY 'dash_mysql_db';