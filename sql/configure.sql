ALTER TABLE dash_board_db.dash_users_verification
  ADD FOREIGN KEY (uid) REFERENCES dash_board_db.dash_users (uid)
  ON DELETE NO ACTION;

GRANT ALL PRIVILEGES ON dash_board_db.* TO 'tech_dash_user'@'localhost';
FLUSH PRIVILEGES;