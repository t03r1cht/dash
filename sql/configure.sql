ALTER TABLE dash_board_db.dash_users_verification
  ADD FOREIGN KEY (uid) REFERENCES dash_board_db.dash_users (uid)
  ON DELETE NO ACTION;

ALTER TABLE dash_board_db.dash_forum_subsections
  ADD FOREIGN KEY (section_id) REFERENCES dash_board_db.dash_forum_sections (section_id)
  ON DELETE NO ACTION;

ALTER TABLE dash_board_db.dash_forum_threads
  ADD FOREIGN KEY (subsection_id) REFERENCES dash_board_db.dash_forum_subsections (subsection_id)
  ON DELETE NO ACTION;

ALTER TABLE dash_board_db.dash_forum_threads
  ADD FOREIGN KEY (thread_creator) REFERENCES dash_board_db.dash_users (uid)
  ON DELETE NO ACTION;

GRANT ALL PRIVILEGES ON dash_board_db.* TO 'tech_dash_user'@'localhost';
FLUSH PRIVILEGES;