DROP DATABASE IF EXISTS dash_board_db;

CREATE DATABASE dash_board_db;

CREATE TABLE dash_board_db.dash_users (
  uid           INT          NOT NULL AUTO_INCREMENT,
  username      VARCHAR(100) NOT NULL UNIQUE,
  email         VARCHAR(250) NOT NULL UNIQUE,
  password      VARCHAR(150) NOT NULL,
  creation_date DATETIME     NOT NULL,
  role_id       INT          NOT NULL,
  profile_data  VARCHAR(5000),
  PRIMARY KEY (uid)
)
  ENGINE = INNODB;

CREATE TABLE dash_board_db.dash_users_verification (
  uid               INT     NOT NULL,
  verified          BOOLEAN NOT NULL,
  token             VARCHAR(50),
  verification_date DATETIME
)
  ENGINE = INNODB;

CREATE TABLE dash_board_db.dash_roles (
  role_id      INT NOT NULL AUTO_INCREMENT,
  name         VARCHAR(100),
  config_board BOOLEAN,
  PRIMARY KEY (role_id)
)
  ENGINE = INNODB;

CREATE TABLE dash_board_db.dash_forum_sections (
  section_id            INT NOT NULL AUTO_INCREMENT,
  section_name          VARCHAR(150),
  section_creation_date DATETIME,
  PRIMARY KEY (section_id)
)
  ENGINE = INNODB;

CREATE TABLE dash_board_db.dash_forum_subsections (
  subsection_id            INT NOT NULL AUTO_INCREMENT,
  section_id               INT,
  subsection_name          VARCHAR(150),
  subsection_desc          VARCHAR(250),
  subsection_creation_date DATETIME,
  PRIMARY KEY (subsection_id)
)
  ENGINE = INNODB;

CREATE TABLE dash_board_db.dash_forum_threads (
  thread_id            INT NOT NULL AUTO_INCREMENT,
  subsection_id        INT,
  thread_title         VARCHAR(250),
  thread_creator       INT,
  thread_views         INT,
  thread_replies       INT,
  thread_status        VARCHAR(50),
  thread_creation_date DATETIME,
  PRIMARY KEY (thread_id)
)
  ENGINE = INNODB;


DROP USER IF EXISTS 'tech_dash_user'@'localhost', 'tech_dash_user'@'%';
FLUSH PRIVILEGES;
CREATE USER 'tech_dash_user'@'localhost'
  IDENTIFIED BY 'dash_mysql_db';